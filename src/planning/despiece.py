"""
Decisión de despiece de un solo periodo con perfiles de pollo.

Responde a la pregunta operativa: *dado un lote de pollo (con un peso y unas
proporciones anatómicas) y un mix comercial (qué cortes se pueden vender, a qué
precio y cuánto se demanda), ¿cómo despiezar la carcasa para maximizar la
utilidad?* — teniendo en cuenta que algunos cortes compiten por la misma pieza
anatómica (p. ej. vender el pernil entero O deshuesarlo en muslo + contramuslo,
no ambos del mismo animal).

Modelo (una sola línea, un periodo, demanda conocida):

    max  Σ_f  precio_f · venta_f
    s.a. Σ_f  comp_{f,a} · prod_f  ≤  masa_a      ∀ parte a   (disponibilidad)
         venta_f ≤ prod_f                          ∀ forma f   (no vender lo no producido)
         venta_f ≤ demanda_f                       ∀ forma f   (no exceder el pedido)
         Σ_{f∈g} activo_f ≤ 1                       ∀ grupo g   (exclusividad de corte)
         prod_f ≤ M · activo_f                      ∀ f∈g
         prod_f, venta_f ≥ 0 ;  activo_f ∈ {0,1}

donde `masa_a` es la masa (kg) de la pieza anatómica `a` disponible en el lote,
resultado de mezclar los perfiles de pollo del lote:

    masa_a = Σ_perfil  n_perfil · peso_perfil · alpha_perfil[a]

`comp_{f,a}` es la cantidad de la pieza `a` (kg) que consume 1 kg del corte `f`.
Con la convención binaria del catálogo de la tesis, producir X kg de un corte
consume X kg de cada pieza que lo compone; el módulo también admite coeficientes
fraccionarios si se dispone de rendimientos reales de planta.

Este modelo es el análogo determinista de un periodo del MILP multi-periodo de
la tesis (`src/model/`), y se resuelve de forma exacta porque su tamaño es
pequeño.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Sequence

import numpy as np
import pulp


# ================================================================
# Perfiles de pollo
# ================================================================


@dataclass(frozen=True)
class BirdProfile:
    """Perfil de un tipo de pollo.

    Attributes:
        name: Etiqueta ("liviano", "estándar", "pesado", ...).
        weight_kg: Peso medio de la carcasa (kg).
        parts: Nombres de las piezas anatómicas.
        alpha: Proporción de cada pieza sobre el peso de la carcasa (suma ~1).
    """

    name: str
    weight_kg: float
    parts: tuple[str, ...]
    alpha: tuple[float, ...]

    def __post_init__(self) -> None:
        if len(self.parts) != len(self.alpha):
            raise ValueError("parts y alpha deben tener la misma longitud")
        s = float(sum(self.alpha))
        if abs(s - 1.0) > 1e-6:
            raise ValueError(f"alpha del perfil '{self.name}' debe sumar 1.0 (suma={s:.4f})")
        if self.weight_kg <= 0:
            raise ValueError("weight_kg debe ser positivo")

    def part_mass_per_carcass(self) -> np.ndarray:
        """Masa (kg) de cada pieza por carcasa: peso · alpha."""
        return self.weight_kg * np.asarray(self.alpha, dtype=np.float64)


# Piezas anatómicas canónicas (Ross 308 / Cobb 500, 6 piezas).
# Fuente base: src/instances/calibration.py (USDA/FAO, Solano-Blanco 2022).
_PARTS = ("pechuga", "muslo", "contramuslo", "ala", "menudencias", "otros")

# Proporciones por perfil. El perfil "estándar" usa las proporciones
# canónicas de la calibración; liviano y pesado desplazan el rendimiento en la
# dirección reportada por las guías de manejo (un ave más pesada rinde
# proporcionalmente más pechuga y menos armazón/menudencia). Son un punto de
# partida CALIBRABLE: reemplácelos con los rendimientos reales de su planta.
PERFILES_ESTANDAR: dict[str, BirdProfile] = {
    "liviano": BirdProfile(
        name="liviano",
        weight_kg=2.0,
        parts=_PARTS,
        alpha=(0.28, 0.18, 0.14, 0.09, 0.06, 0.25),
    ),
    "estándar": BirdProfile(
        name="estándar",
        weight_kg=2.5,
        parts=_PARTS,
        alpha=(0.30, 0.18, 0.14, 0.08, 0.05, 0.25),
    ),
    "pesado": BirdProfile(
        name="pesado",
        weight_kg=3.0,
        parts=_PARTS,
        alpha=(0.32, 0.18, 0.13, 0.08, 0.05, 0.24),
    ),
}


@dataclass
class FlockMix:
    """Mezcla de perfiles que compone el lote a procesar.

    Attributes:
        counts: Número de carcasas por perfil, en el mismo orden que `profiles`.
        profiles: Perfiles de pollo del lote (deben compartir las mismas piezas).
    """

    profiles: Sequence[BirdProfile]
    counts: Sequence[float]

    def __post_init__(self) -> None:
        if len(self.profiles) != len(self.counts):
            raise ValueError("profiles y counts deben tener la misma longitud")
        if not self.profiles:
            raise ValueError("la mezcla debe tener al menos un perfil")
        parts0 = self.profiles[0].parts
        if any(p.parts != parts0 for p in self.profiles):
            raise ValueError("todos los perfiles deben compartir las mismas piezas anatómicas")
        if any(c < 0 for c in self.counts):
            raise ValueError("los conteos no pueden ser negativos")

    @property
    def parts(self) -> tuple[str, ...]:
        return self.profiles[0].parts

    @property
    def total_carcasses(self) -> float:
        return float(sum(self.counts))

    def part_pool(self) -> np.ndarray:
        """Masa total (kg) disponible por pieza anatómica, mezclando perfiles."""
        pool = np.zeros(len(self.parts), dtype=np.float64)
        for prof, n in zip(self.profiles, self.counts):
            pool += float(n) * prof.part_mass_per_carcass()
        return pool

    @classmethod
    def single(cls, profile: BirdProfile, carcasses: float) -> "FlockMix":
        """Lote de un solo perfil."""
        return cls(profiles=[profile], counts=[carcasses])

    @classmethod
    def from_fractions(
        cls,
        total_carcasses: float,
        fractions: dict[str, float],
        catalog: Optional[dict[str, BirdProfile]] = None,
    ) -> "FlockMix":
        """Construye la mezcla a partir de fracciones por nombre de perfil.

        Args:
            total_carcasses: Total de carcasas del lote.
            fractions: Fracción de cada perfil (deben sumar ~1), por nombre.
            catalog: Catálogo de perfiles; por defecto `PERFILES_ESTANDAR`.
        """
        catalog = catalog or PERFILES_ESTANDAR
        s = float(sum(fractions.values()))
        if abs(s - 1.0) > 1e-6:
            raise ValueError(f"las fracciones deben sumar 1.0 (suma={s:.4f})")
        profiles, counts = [], []
        for name, frac in fractions.items():
            if name not in catalog:
                raise KeyError(f"perfil desconocido: '{name}' (disponibles: {list(catalog)})")
            profiles.append(catalog[name])
            counts.append(total_carcasses * frac)
        return cls(profiles=profiles, counts=counts)


# ================================================================
# Mix comercial (catálogo de cortes)
# ================================================================


@dataclass
class CommercialItem:
    """Un corte comercial vendible.

    Attributes:
        name: Nombre del corte.
        composition: kg de cada pieza anatómica que consume 1 kg del corte,
            en el orden de las piezas del lote. Con la convención de la tesis es
            binaria (1 si el corte usa esa pieza).
        price_per_kg: Precio de venta (COP/kg).
        demand_kg: Demanda / pedido máximo (kg). None = sin tope.
        exclusivity_group: Etiqueta de grupo; los cortes con la misma etiqueta
            compiten por la misma pieza y solo uno puede activarse por lote.
    """

    name: str
    composition: tuple[float, ...]
    price_per_kg: float
    demand_kg: Optional[float] = None
    exclusivity_group: Optional[str] = None


def catalogo_despiece_default() -> list[CommercialItem]:
    """Catálogo comercial de referencia (6 piezas, precios FENAVI 2024).

    El pernil completo y los cortes individuales (muslo, contramuslo) comparten
    las mismas piezas anatómicas, por lo que compiten por la misma masa. Esa
    competencia la resuelve automáticamente la restricción de disponibilidad
    (`part_pool`): no hace falta forzar exclusividad. Con estos precios, el
    óptimo tiende a deshuesar (muslo + contramuslo rinden 9000+8500 > 11000 del
    pernil entero) salvo que la demanda de pernil lo justifique.

    Si por una razón comercial se desea ofrecer *o* el pernil *o* los cortes
    individuales (no ambos), basta con asignarles el mismo `exclusivity_group`.
    Orden de piezas: pechuga, muslo, contramuslo, ala, menudencias, otros.
    """
    return [
        CommercialItem("Pechuga",           (1, 0, 0, 0, 0, 0), 14000.0),
        CommercialItem("Pernil completo",   (0, 1, 1, 0, 0, 0), 11000.0),
        CommercialItem("Muslo",             (0, 1, 0, 0, 0, 0),  9000.0),
        CommercialItem("Contramuslo",       (0, 0, 1, 0, 0, 0),  8500.0),
        CommercialItem("Ala",               (0, 0, 0, 1, 0, 0),  6000.0),
        CommercialItem("Menudencias",       (0, 0, 0, 0, 1, 0),  4000.0),
        CommercialItem("Subproducto",       (0, 0, 0, 0, 0, 1),  1500.0),
    ]


# ================================================================
# Resultado
# ================================================================


@dataclass
class DespiecePlan:
    """Resultado de la optimización de despiece."""

    status: str
    profit: float
    produced_kg: dict[str, float]
    sold_kg: dict[str, float]
    unmet_kg: dict[str, float]
    part_pool_kg: dict[str, float]
    part_used_kg: dict[str, float]
    part_utilization: dict[str, float] = field(default_factory=dict)

    def resumen(self) -> str:
        """Texto legible con el plan, ventas por corte y uso de cada pieza."""
        lines = [
            f"Estado: {self.status}",
            f"Utilidad esperada: {self.profit:,.0f} COP",
            "",
            f"{'Corte':<20}{'Producir(kg)':>14}{'Vender(kg)':>13}{'Sin cubrir(kg)':>16}",
            "-" * 63,
        ]
        for name in self.produced_kg:
            lines.append(
                f"{name:<20}{self.produced_kg[name]:>14,.0f}"
                f"{self.sold_kg[name]:>13,.0f}{self.unmet_kg[name]:>16,.0f}"
            )
        lines += ["", f"{'Pieza':<16}{'Disponible(kg)':>16}{'Usada(kg)':>13}{'Uso(%)':>9}", "-" * 54]
        for part in self.part_pool_kg:
            lines.append(
                f"{part:<16}{self.part_pool_kg[part]:>16,.0f}"
                f"{self.part_used_kg[part]:>13,.0f}{100 * self.part_utilization[part]:>8.1f}%"
            )
        return "\n".join(lines)


# ================================================================
# Optimizador
# ================================================================


def optimizar_despiece(
    flock: FlockMix,
    items: Sequence[CommercialItem],
    solver: str = "cbc",
    verbose: bool = False,
) -> DespiecePlan:
    """Calcula el plan de despiece óptimo (exacto) para un lote y un mix.

    Args:
        flock: Mezcla de perfiles de pollo del lote.
        items: Catálogo de cortes comerciales (mix comercial).
        solver: 'cbc' (por defecto), 'highs' o 'gurobi'.
        verbose: Muestra el log del solver.

    Returns:
        DespiecePlan con producción, ventas, demanda insatisfecha y uso de
        cada pieza anatómica.
    """
    n_parts = len(flock.parts)
    for it in items:
        if len(it.composition) != n_parts:
            raise ValueError(
                f"'{it.name}': composition tiene {len(it.composition)} piezas, "
                f"se esperaban {n_parts}"
            )

    pool = flock.part_pool()
    big_m = float(pool.sum()) + 1.0  # cota superior segura para producción

    model = pulp.LpProblem("despiece", pulp.LpMaximize)

    prod = {it.name: pulp.LpVariable(f"prod_{i}", lowBound=0) for i, it in enumerate(items)}
    sell = {it.name: pulp.LpVariable(f"sell_{i}", lowBound=0) for i, it in enumerate(items)}

    # Activación binaria solo para cortes en grupos de exclusividad
    groups: dict[str, list[CommercialItem]] = {}
    for it in items:
        if it.exclusivity_group:
            groups.setdefault(it.exclusivity_group, []).append(it)
    active = {
        it.name: pulp.LpVariable(f"act_{i}", cat="Binary")
        for i, it in enumerate(items)
        if it.exclusivity_group
    }

    # Objetivo: maximizar ingresos por ventas
    model += pulp.lpSum(it.price_per_kg * sell[it.name] for it in items)

    # Disponibilidad anatómica por pieza
    for a, part in enumerate(flock.parts):
        model += (
            pulp.lpSum(it.composition[a] * prod[it.name] for it in items) <= pool[a],
            f"pool_{part}",
        )

    # Ventas acotadas por producción y por demanda
    for it in items:
        model += (sell[it.name] <= prod[it.name], f"sell_le_prod_{it.name}")
        if it.demand_kg is not None:
            model += (sell[it.name] <= it.demand_kg, f"sell_le_demand_{it.name}")

    # Exclusividad: a lo sumo un corte activo por grupo
    for gname, gitems in groups.items():
        model += (pulp.lpSum(active[it.name] for it in gitems) <= 1, f"excl_{gname}")
        for it in gitems:
            model += (prod[it.name] <= big_m * active[it.name], f"link_{it.name}")

    if solver.lower() == "highs":
        pulp_solver = pulp.HiGHS_CMD(msg=int(verbose))
    elif solver.lower() == "gurobi":
        pulp_solver = pulp.GUROBI_CMD(msg=int(verbose))
    else:
        pulp_solver = pulp.PULP_CBC_CMD(msg=int(verbose))

    model.solve(pulp_solver)
    status = pulp.LpStatus.get(model.status, "Unknown")

    produced = {it.name: float(prod[it.name].value() or 0.0) for it in items}
    sold = {it.name: float(sell[it.name].value() or 0.0) for it in items}
    unmet = {
        it.name: (max(0.0, it.demand_kg - sold[it.name]) if it.demand_kg is not None else 0.0)
        for it in items
    }

    part_used = np.zeros(n_parts, dtype=np.float64)
    for it in items:
        part_used += np.asarray(it.composition, dtype=np.float64) * produced[it.name]

    pool_d = {part: float(pool[a]) for a, part in enumerate(flock.parts)}
    used_d = {part: float(part_used[a]) for a, part in enumerate(flock.parts)}
    util_d = {
        part: (used_d[part] / pool_d[part] if pool_d[part] > 1e-9 else 0.0)
        for part in pool_d
    }
    profit = float(pulp.value(model.objective) or 0.0)

    return DespiecePlan(
        status=status,
        profit=profit,
        produced_kg=produced,
        sold_kg=sold,
        unmet_kg=unmet,
        part_pool_kg=pool_d,
        part_used_kg=used_d,
        part_utilization=util_d,
    )
