"""
ProblemInstance: Estructura de datos para una instancia del problema de
optimizacion de coproductos avicolas.

Coherente con DD-03 (3 capas: piezas anatomicas, formas de corte, SKUs)
y DD-02 (granularidad en dias).

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 1.2
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import numpy as np
import yaml


@dataclass
class ExclusivityGroup:
    """Grupo de formas de corte mutuamente excluyentes.

    Ejemplo: Pernil completo (f3) vs Muslo individual (f5) + Contramuslo (f6)
    comparten la pieza anatomica 'muslo', por lo que son excluyentes.
    """

    name: str
    cut_form_indices: list[int]  # indices de formas que compiten
    shared_part_index: int  # indice de la pieza anatomica compartida

    def __repr__(self) -> str:
        return f"ExclusivityGroup({self.name}, forms={self.cut_form_indices})"


@dataclass
class ProblemInstance:
    """Instancia completa del problema de optimizacion de coproductos.

    Estructura de 3 capas (DD-03):
    - Capa 1: Piezas anatomicas (alpha, n_parts) — biologia, fijas
    - Capa 2: Formas de corte (composition, n_cut_forms) — var. de decision
    - Capa 3: SKUs (~350) — se agregan a Capa 2 (preprocesamiento)

    La demanda y precios se expresan a nivel de forma de corte (Capa 2).
    """

    # --- Metadata ---
    name: str = ""
    profile: str = ""
    seed: Optional[int] = None

    # --- Capa 1: Piezas Anatomicas ---
    n_parts: int = 0
    part_names: list[str] = field(default_factory=list)
    alpha: np.ndarray = field(default_factory=lambda: np.array([]))

    # --- Capa 2: Formas de Corte ---
    n_cut_forms: int = 0
    cut_form_names: list[str] = field(default_factory=list)
    composition: np.ndarray = field(default_factory=lambda: np.array([]))
    exclusivity_groups: list[ExclusivityGroup] = field(default_factory=list)
    cut_config: Optional[np.ndarray] = None  # None = variable, array = fija

    # --- Periodos (dias) ---
    n_periods: int = 0

    # --- Parametros economicos ---
    weight: float = 2.3  # kg/carcasa
    prices: np.ndarray = field(default_factory=lambda: np.array([]))
    cost_prod: float = 0.0  # COP/carcasa
    cost_setup: float = 0.0  # COP/dia
    cost_inv: np.ndarray = field(default_factory=lambda: np.array([]))
    cost_pen: np.ndarray = field(default_factory=lambda: np.array([]))

    # --- Capacidad ---
    capacity_max: int = 0  # carcasas/dia
    capacity_min: int = 0  # lote minimo

    # --- Perecibilidad (dias) ---
    shelf_life: np.ndarray = field(default_factory=lambda: np.array([]))

    # --- Escenarios estocasticos ---
    n_scenarios: int = 0
    scenario_probs: np.ndarray = field(default_factory=lambda: np.array([]))
    demand: np.ndarray = field(default_factory=lambda: np.array([]))

    def validate(self) -> list[str]:
        """Verificar consistencia de la instancia.

        Returns:
            Lista de errores encontrados. Vacia si es valida.
        """
        errors = []

        # --- Capa 1: Piezas anatomicas ---
        if len(self.alpha) != self.n_parts:
            errors.append(
                f"alpha tiene {len(self.alpha)} elementos, esperado {self.n_parts}"
            )
        if len(self.alpha) > 0 and not np.isclose(self.alpha.sum(), 1.0):
            errors.append(f"sum(alpha) = {self.alpha.sum():.6f}, esperado 1.0")
        if len(self.part_names) != self.n_parts:
            errors.append(
                f"part_names tiene {len(self.part_names)} elementos, esperado {self.n_parts}"
            )

        # --- Capa 2: Formas de corte ---
        if self.composition.ndim == 2:
            rows, cols = self.composition.shape
            if rows != self.n_cut_forms:
                errors.append(
                    f"composition tiene {rows} filas, esperado {self.n_cut_forms}"
                )
            if cols != self.n_parts:
                errors.append(
                    f"composition tiene {cols} columnas, esperado {self.n_parts}"
                )
            if np.any(self.composition < 0):
                errors.append("composition no puede tener valores negativos")
        elif self.n_cut_forms > 0:
            errors.append("composition debe ser un array 2D")

        if len(self.cut_form_names) != self.n_cut_forms:
            errors.append(
                f"cut_form_names tiene {len(self.cut_form_names)} elementos, "
                f"esperado {self.n_cut_forms}"
            )
        if self.cut_config is not None:
            if len(self.cut_config) != self.n_cut_forms:
                errors.append(
                    f"cut_config tiene {len(self.cut_config)} elementos, "
                    f"esperado {self.n_cut_forms}"
                )
            if np.any((self.cut_config != 0) & (self.cut_config != 1)):
                errors.append("cut_config debe contener solo valores 0/1")

        # Validar exclusividad: indices dentro de rango
        for group in self.exclusivity_groups:
            for idx in group.cut_form_indices:
                if idx < 0 or idx >= self.n_cut_forms:
                    errors.append(
                        f"ExclusivityGroup '{group.name}': indice {idx} fuera "
                        f"de rango [0, {self.n_cut_forms})"
                    )
            if group.shared_part_index < 0 or group.shared_part_index >= self.n_parts:
                errors.append(
                    f"ExclusivityGroup '{group.name}': shared_part_index "
                    f"{group.shared_part_index} fuera de rango [0, {self.n_parts})"
                )
            if self.cut_config is not None:
                valid_indices = [
                    idx for idx in group.cut_form_indices if 0 <= idx < self.n_cut_forms
                ]
                active_in_group = sum(
                    int(self.cut_config[idx]) for idx in valid_indices
                )
                if active_in_group > 1:
                    errors.append(
                        f"ExclusivityGroup '{group.name}': cut_config activa "
                        f"{active_in_group} formas excluyentes"
                    )

        # --- Parametros economicos ---
        if len(self.prices) != self.n_cut_forms:
            errors.append(
                f"prices tiene {len(self.prices)} elementos, esperado {self.n_cut_forms}"
            )
        if len(self.cost_inv) != self.n_cut_forms:
            errors.append(
                f"cost_inv tiene {len(self.cost_inv)} elementos, esperado {self.n_cut_forms}"
            )
        if len(self.cost_pen) != self.n_cut_forms:
            errors.append(
                f"cost_pen tiene {len(self.cost_pen)} elementos, esperado {self.n_cut_forms}"
            )
        if self.capacity_min > self.capacity_max:
            errors.append(
                f"capacity_min ({self.capacity_min}) > capacity_max ({self.capacity_max})"
            )

        # --- Perecibilidad ---
        if len(self.shelf_life) != self.n_cut_forms:
            errors.append(
                f"shelf_life tiene {len(self.shelf_life)} elementos, "
                f"esperado {self.n_cut_forms}"
            )

        # --- Escenarios ---
        if len(self.scenario_probs) > 0:
            if len(self.scenario_probs) != self.n_scenarios:
                errors.append(
                    f"scenario_probs tiene {len(self.scenario_probs)} elementos, "
                    f"esperado {self.n_scenarios}"
                )
            if not np.isclose(self.scenario_probs.sum(), 1.0):
                errors.append(
                    f"sum(scenario_probs) = {self.scenario_probs.sum():.6f}, esperado 1.0"
                )

        # --- Demanda ---
        expected_shape = (self.n_cut_forms, self.n_periods, self.n_scenarios)
        if self.demand.ndim == 3:
            if self.demand.shape != expected_shape:
                errors.append(
                    f"demand shape {self.demand.shape}, esperado {expected_shape}"
                )
        elif self.n_cut_forms > 0:
            errors.append(f"demand debe ser un array 3D, tiene {self.demand.ndim}D")

        return errors

    @classmethod
    def from_yaml(cls, path: str | Path) -> ProblemInstance:
        """Cargar instancia desde archivo YAML.

        Args:
            path: Ruta al archivo YAML.

        Returns:
            ProblemInstance cargada y validada.

        Raises:
            ValueError: Si la instancia no es valida.
            FileNotFoundError: Si el archivo no existe.
        """
        path = Path(path)
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        meta = data.get("metadata", {})
        prob = data.get("problem", {})

        # Construir exclusivity groups
        groups = []
        for g in prob.get("exclusivity_groups", []):
            groups.append(
                ExclusivityGroup(
                    name=g.get("name", "unnamed"),
                    cut_form_indices=g["products"],
                    shared_part_index=g["shared_part"],
                )
            )

        # Scenario probs: null -> equiprobable
        n_scenarios = prob["n_scenarios"]
        scenario_probs_raw = prob.get("scenario_probs")
        if scenario_probs_raw is None:
            scenario_probs = np.ones(n_scenarios) / n_scenarios
        else:
            scenario_probs = np.array(scenario_probs_raw, dtype=np.float64)

        # Cut config: null -> variable (None)
        cut_config_raw = prob.get("cut_config")
        cut_config = (
            np.array(cut_config_raw, dtype=np.int32)
            if cut_config_raw is not None
            else None
        )

        instance = cls(
            # Metadata
            name=meta.get("name", path.stem),
            profile=meta.get("profile", ""),
            seed=meta.get("seed"),
            # Capa 1
            n_parts=prob["n_parts"],
            part_names=prob.get("part_names", []),
            alpha=np.array(prob["alpha"], dtype=np.float64),
            # Capa 2
            n_cut_forms=prob["n_products"],
            cut_form_names=prob.get("product_names", []),
            composition=np.array(prob["composition"], dtype=np.int32),
            exclusivity_groups=groups,
            cut_config=cut_config,
            # Periodos
            n_periods=prob["n_periods"],
            # Economicos
            weight=prob.get("weight", 2.3),
            prices=np.array(prob["prices"], dtype=np.float64),
            cost_prod=prob["cost_prod"],
            cost_setup=prob["cost_setup"],
            cost_inv=np.array(prob["cost_inv"], dtype=np.float64),
            cost_pen=np.array(prob["cost_pen"], dtype=np.float64),
            # Capacidad
            capacity_max=prob["capacity_max"],
            capacity_min=prob["capacity_min"],
            # Perecibilidad
            shelf_life=np.array(prob["shelf_life"], dtype=np.int32),
            # Escenarios
            n_scenarios=n_scenarios,
            scenario_probs=scenario_probs,
            demand=np.array(prob["demand"], dtype=np.float64),
        )

        errors = instance.validate()
        if errors:
            raise ValueError(
                f"Instancia invalida ({path.name}):\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

        return instance

    def to_yaml(self, path: str | Path) -> None:
        """Exportar instancia a archivo YAML.

        Args:
            path: Ruta de destino.
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "metadata": {
                "name": self.name,
                "profile": self.profile,
                "seed": self.seed,
            },
            "problem": {
                "n_parts": self.n_parts,
                "part_names": self.part_names,
                "alpha": self.alpha.tolist(),
                "n_products": self.n_cut_forms,
                "product_names": self.cut_form_names,
                "composition": self.composition.tolist(),
                "exclusivity_groups": [
                    {
                        "name": g.name,
                        "products": g.cut_form_indices,
                        "shared_part": g.shared_part_index,
                    }
                    for g in self.exclusivity_groups
                ],
                "cut_config": (
                    self.cut_config.tolist() if self.cut_config is not None else None
                ),
                "n_periods": self.n_periods,
                "weight": self.weight,
                "prices": self.prices.tolist(),
                "cost_prod": self.cost_prod,
                "cost_setup": self.cost_setup,
                "cost_inv": self.cost_inv.tolist(),
                "cost_pen": self.cost_pen.tolist(),
                "capacity_max": self.capacity_max,
                "capacity_min": self.capacity_min,
                "shelf_life": self.shelf_life.tolist(),
                "n_scenarios": self.n_scenarios,
                "scenario_probs": (
                    self.scenario_probs.tolist()
                    if not np.allclose(
                        self.scenario_probs,
                        np.ones(self.n_scenarios) / self.n_scenarios,
                    )
                    else None
                ),
                "demand": self.demand.tolist(),
            },
        }

        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    def summary(self) -> str:
        """Resumen legible de la instancia."""
        lines = [
            f"ProblemInstance: {self.name}",
            f"  Perfil: {self.profile}",
            f"  Piezas anatomicas: {self.n_parts} ({', '.join(self.part_names)})",
            f"  Formas de corte: {self.n_cut_forms} ({', '.join(self.cut_form_names)})",
            f"  Periodos: {self.n_periods} dias",
            f"  Escenarios: {self.n_scenarios}",
            f"  Capacidad: [{self.capacity_min}, {self.capacity_max}] carcasas/dia",
            f"  Peso carcasa: {self.weight} kg",
            f"  Config. corte: {'fija' if self.cut_config is not None else 'variable'}",
            f"  Exclusividad: {len(self.exclusivity_groups)} grupo(s)",
        ]
        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            f"ProblemInstance(name='{self.name}', parts={self.n_parts}, "
            f"forms={self.n_cut_forms}, T={self.n_periods}, "
            f"omega={self.n_scenarios})"
        )
