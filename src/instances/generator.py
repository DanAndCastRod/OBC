"""
Generador parametrizable de instancias para el problema de coproductos.

Perfiles predefinidos calibrados contra la industria avicola colombiana:
- Toy: 3 formas, 4 periodos, 5 escenarios (debug)
- Small: 6 formas, 12 periodos, 20 escenarios (validacion con solver)
- Medium: 6 formas, 12 periodos, 50 escenarios (calibracion)
- Large: 8 formas, 24 periodos, 100 escenarios (comparacion MH)
- Industrial: 10 formas, 52 periodos, 500 escenarios (scalability)

Referencia de parametros:
- Proporciones anatomicas: literatura avicola estandar
- Precios: FENAVI 2024, Solano-Blanco 2022
- Costos: Solano-Blanco 2022
- Demanda: LogNormal con estacionalidad sinusoidal

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 3.1
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.instances.distributions import generate_scenarios
from src.model.parameters import ExclusivityGroup, ProblemInstance

# ================================================================
# Catalogo de productos avicolas
# ================================================================


@dataclass
class ProductCatalog:
    """Catalogo de formas de corte avicolas estandar.

    Define las piezas anatomicas, formas de corte, composicion,
    y exclusividades para cada perfil de tamano.
    """

    @staticmethod
    def toy() -> dict:
        """3 formas simples sin exclusividad."""
        return {
            "n_parts": 3,
            "part_names": ["Pechuga", "Muslo", "Otros"],
            "alpha": np.array([0.35, 0.25, 0.40]),
            "n_cut_forms": 3,
            "cut_form_names": ["Pechuga", "Muslo", "Subproducto"],
            "composition": np.array(
                [
                    [1, 0, 0],
                    [0, 1, 0],
                    [0, 0, 1],
                ],
                dtype=np.int32,
            ),
            "exclusivity_groups": [],
            "cut_config": np.array([1, 1, 1], dtype=np.int32),
            # Economicos
            "prices": np.array([14000, 9000, 1500], dtype=np.float64),
            "cost_inv": np.array([300, 250, 100], dtype=np.float64),
            "cost_pen": np.array([5000, 3500, 500], dtype=np.float64),
            "shelf_life": np.array([5, 5, 30], dtype=np.int32),
            # Demanda base y CV
            "base_demands": np.array([4000, 2500, 1200], dtype=np.float64),
            "cvs": np.array([0.10, 0.20, 0.35]),
        }

    @staticmethod
    def small() -> dict:
        """6 formas con exclusividad muslo/pernil."""
        return {
            "n_parts": 5,
            "part_names": ["Pechuga", "Muslo", "Contramuslo", "Ala", "Otros"],
            "alpha": np.array([0.30, 0.18, 0.14, 0.08, 0.30]),
            "n_cut_forms": 6,
            "cut_form_names": [
                "Pechuga",
                "Pernil completo",
                "Muslo solo",
                "Contramuslo solo",
                "Ala",
                "Subproducto",
            ],
            "composition": np.array(
                [
                    [1, 0, 0, 0, 0],  # Pechuga = a0
                    [0, 1, 1, 0, 0],  # Pernil  = a1 + a2
                    [0, 1, 0, 0, 0],  # Muslo   = a1
                    [0, 0, 1, 0, 0],  # Contra  = a2
                    [0, 0, 0, 1, 0],  # Ala     = a3
                    [0, 0, 0, 0, 1],  # Subprod = a4
                ],
                dtype=np.int32,
            ),
            "exclusivity_groups": [
                ExclusivityGroup(
                    name="Pernil vs Individual",
                    cut_form_indices=[1, 2],  # Pernil vs Muslo solo
                    shared_part_index=1,  # Comparten muslo
                ),
            ],
            # Pernil activo, muslo inactivo (exclusividad)
            "cut_config": np.array([1, 1, 0, 0, 1, 1], dtype=np.int32),
            "prices": np.array(
                [14000, 11000, 9000, 8500, 6000, 1500], dtype=np.float64
            ),
            "cost_inv": np.array([300, 280, 250, 250, 200, 100], dtype=np.float64),
            "cost_pen": np.array([5000, 4000, 3500, 3500, 2500, 500], dtype=np.float64),
            "shelf_life": np.array([5, 5, 5, 5, 5, 30], dtype=np.int32),
            "base_demands": np.array(
                [4500, 3000, 1500, 1200, 2000, 1000], dtype=np.float64
            ),
            "cvs": np.array([0.10, 0.20, 0.25, 0.25, 0.30, 0.40]),
        }

    @staticmethod
    def medium() -> dict:
        """6 formas (misma estructura que small, mas escenarios)."""
        cat = ProductCatalog.small()
        return cat

    @staticmethod
    def large() -> dict:
        """8 formas: agrega subproductos procesados."""
        return {
            "n_parts": 6,
            "part_names": [
                "Pechuga",
                "Muslo",
                "Contramuslo",
                "Ala",
                "Menudencias",
                "Otros",
            ],
            "alpha": np.array([0.30, 0.15, 0.12, 0.08, 0.05, 0.30]),
            "n_cut_forms": 8,
            "cut_form_names": [
                "Pechuga",
                "Pernil completo",
                "Muslo solo",
                "Contramuslo solo",
                "Ala",
                "Menudencias",
                "Subproducto fresco",
                "Harina avicola",
            ],
            "composition": np.array(
                [
                    [1, 0, 0, 0, 0, 0],  # Pechuga
                    [0, 1, 1, 0, 0, 0],  # Pernil
                    [0, 1, 0, 0, 0, 0],  # Muslo solo
                    [0, 0, 1, 0, 0, 0],  # Contramuslo solo
                    [0, 0, 0, 1, 0, 0],  # Ala
                    [0, 0, 0, 0, 1, 0],  # Menudencias
                    [0, 0, 0, 0, 0, 1],  # Subproducto fresco
                    [0, 0, 0, 0, 1, 1],  # Harina (menud + otros)
                ],
                dtype=np.int32,
            ),
            "exclusivity_groups": [
                ExclusivityGroup(
                    name="Pernil vs Individual",
                    cut_form_indices=[1, 2],
                    shared_part_index=1,
                ),
                ExclusivityGroup(
                    name="Menudencias vs Harina",
                    cut_form_indices=[5, 7],
                    shared_part_index=4,
                ),
            ],
            "cut_config": np.array([1, 1, 0, 0, 1, 1, 1, 0], dtype=np.int32),
            "prices": np.array(
                [
                    14000,
                    11000,
                    9000,
                    8500,
                    6000,
                    4000,
                    1500,
                    2200,
                ],
                dtype=np.float64,
            ),
            "cost_inv": np.array(
                [
                    300,
                    280,
                    250,
                    250,
                    200,
                    180,
                    100,
                    80,
                ],
                dtype=np.float64,
            ),
            "cost_pen": np.array(
                [
                    5000,
                    4000,
                    3500,
                    3500,
                    2500,
                    2000,
                    500,
                    400,
                ],
                dtype=np.float64,
            ),
            "shelf_life": np.array([5, 5, 5, 5, 5, 3, 30, 180], dtype=np.int32),
            "base_demands": np.array(
                [
                    5000,
                    3500,
                    1800,
                    1500,
                    2500,
                    800,
                    1200,
                    600,
                ],
                dtype=np.float64,
            ),
            "cvs": np.array(
                [
                    0.10,
                    0.18,
                    0.25,
                    0.25,
                    0.30,
                    0.35,
                    0.40,
                    0.30,
                ]
            ),
        }

    @staticmethod
    def industrial() -> dict:
        """10 formas: incluye presentaciones premium y cortes especiales."""
        return {
            "n_parts": 6,
            "part_names": [
                "Pechuga",
                "Muslo",
                "Contramuslo",
                "Ala",
                "Menudencias",
                "Otros",
            ],
            "alpha": np.array([0.30, 0.15, 0.12, 0.08, 0.05, 0.30]),
            "n_cut_forms": 10,
            "cut_form_names": [
                "Pechuga entera",
                "Filete pechuga",
                "Pernil completo",
                "Muslo solo",
                "Contramuslo solo",
                "Ala entera",
                "Menudencias",
                "Subproducto fresco",
                "Harina avicola",
                "Medio pollo",
            ],
            "composition": np.array(
                [
                    [1, 0, 0, 0, 0, 0],  # Pechuga entera
                    [1, 0, 0, 0, 0, 0],  # Filete pechuga (mismo corte, premium)
                    [0, 1, 1, 0, 0, 0],  # Pernil
                    [0, 1, 0, 0, 0, 0],  # Muslo solo
                    [0, 0, 1, 0, 0, 0],  # Contramuslo solo
                    [0, 0, 0, 1, 0, 0],  # Ala entera
                    [0, 0, 0, 0, 1, 0],  # Menudencias
                    [0, 0, 0, 0, 0, 1],  # Subproducto fresco
                    [0, 0, 0, 0, 1, 1],  # Harina avicola
                    [1, 1, 1, 1, 0, 0],  # Medio pollo
                ],
                dtype=np.int32,
            ),
            "exclusivity_groups": [
                ExclusivityGroup(
                    name="Pechuga entera vs Filete",
                    cut_form_indices=[0, 1],
                    shared_part_index=0,
                ),
                ExclusivityGroup(
                    name="Pernil vs Individual",
                    cut_form_indices=[2, 3],
                    shared_part_index=1,
                ),
                ExclusivityGroup(
                    name="Menudencias vs Harina",
                    cut_form_indices=[6, 8],
                    shared_part_index=4,
                ),
            ],
            "cut_config": np.array([1, 0, 1, 0, 0, 1, 1, 1, 0, 0], dtype=np.int32),
            "prices": np.array(
                [
                    14000,
                    16000,
                    11000,
                    9000,
                    8500,
                    6000,
                    4000,
                    1500,
                    2200,
                    12000,
                ],
                dtype=np.float64,
            ),
            "cost_inv": np.array(
                [
                    300,
                    350,
                    280,
                    250,
                    250,
                    200,
                    180,
                    100,
                    80,
                    320,
                ],
                dtype=np.float64,
            ),
            "cost_pen": np.array(
                [
                    5000,
                    6000,
                    4000,
                    3500,
                    3500,
                    2500,
                    2000,
                    500,
                    400,
                    4500,
                ],
                dtype=np.float64,
            ),
            "shelf_life": np.array([5, 3, 5, 5, 5, 5, 3, 30, 180, 3], dtype=np.int32),
            "base_demands": np.array(
                [
                    5000,
                    2000,
                    3500,
                    1800,
                    1500,
                    2500,
                    800,
                    1200,
                    600,
                    1000,
                ],
                dtype=np.float64,
            ),
            "cvs": np.array(
                [
                    0.10,
                    0.15,
                    0.18,
                    0.25,
                    0.25,
                    0.30,
                    0.35,
                    0.40,
                    0.30,
                    0.20,
                ]
            ),
        }


# ================================================================
# Perfiles de tamano
# ================================================================

SIZE_PROFILES = {
    "toy": {"n_periods": 4, "n_scenarios": 5, "catalog_fn": ProductCatalog.toy},
    "small": {"n_periods": 12, "n_scenarios": 20, "catalog_fn": ProductCatalog.small},
    "medium": {"n_periods": 12, "n_scenarios": 50, "catalog_fn": ProductCatalog.medium},
    "large": {"n_periods": 24, "n_scenarios": 100, "catalog_fn": ProductCatalog.large},
    "industrial": {
        "n_periods": 52,
        "n_scenarios": 500,
        "catalog_fn": ProductCatalog.industrial,
    },
}

# Perfiles de demanda: controlan estacionalidad
DEMAND_PROFILES = {
    "stable": {"amplitude": 0.0, "period": 52, "phase_shift": 0.0},
    "seasonal": {"amplitude": 0.20, "period": 52, "phase_shift": -np.pi / 2},
    "volatile": {"amplitude": 0.35, "period": 26, "phase_shift": 0.0},
}


# ================================================================
# InstanceGenerator
# ================================================================


class InstanceGenerator:
    """Generador parametrizable de instancias del problema de coproductos.

    Uso basico:
        gen = InstanceGenerator()
        inst = gen.generate(size_profile="small", seed=42)

    Uso avanzado:
        inst = gen.generate(
            size_profile="medium",
            demand_profile="seasonal",
            n_periods=24,       # override
            n_scenarios=100,    # override
            seed=123,
        )
    """

    # Parametros economicos fijos (Solano-Blanco 2022, FENAVI 2024)
    DEFAULT_WEIGHT = 2.5  # kg/carcasa promedio
    DEFAULT_COST_PROD = 2000.0  # COP/carcasa
    DEFAULT_COST_SETUP = 500_000.0  # COP/periodo
    DEFAULT_CAPACITY_MAX = 5000  # carcasas/periodo
    DEFAULT_CAPACITY_MIN = 500  # lote minimo

    def generate(
        self,
        size_profile: str = "small",
        demand_profile: str = "stable",
        n_periods: int | None = None,
        n_scenarios: int | None = None,
        seed: int = 42,
        weight: float | None = None,
        cost_prod: float | None = None,
        cost_setup: float | None = None,
        capacity_max: int | None = None,
        capacity_min: int | None = None,
        distribution: str = "lognormal",
    ) -> ProblemInstance:
        """Generar una instancia completa del problema.

        Args:
            size_profile: 'toy', 'small', 'medium', 'large', 'industrial'.
            demand_profile: 'stable', 'seasonal', 'volatile'.
            n_periods: Override del horizonte (default del perfil).
            n_scenarios: Override de escenarios (default del perfil).
            seed: Semilla aleatoria para reproducibilidad.
            weight: Override peso carcasa (kg).
            cost_prod: Override costo produccion (COP/carcasa).
            cost_setup: Override costo setup (COP/periodo).
            capacity_max: Override capacidad maxima.
            capacity_min: Override capacidad minima.
            distribution: 'lognormal' (default) o 'normal'.

        Returns:
            ProblemInstance valida y reproducible.

        Raises:
            ValueError: Si el perfil no existe o la instancia es invalida.
        """
        # --- Validar perfil ---
        if size_profile not in SIZE_PROFILES:
            raise ValueError(
                f"size_profile '{size_profile}' no valido. "
                f"Opciones: {list(SIZE_PROFILES.keys())}"
            )
        if demand_profile not in DEMAND_PROFILES:
            raise ValueError(
                f"demand_profile '{demand_profile}' no valido. "
                f"Opciones: {list(DEMAND_PROFILES.keys())}"
            )

        # --- Cargar perfil ---
        sp = SIZE_PROFILES[size_profile]
        catalog = sp["catalog_fn"]()
        dp = DEMAND_PROFILES[demand_profile]

        n_t = n_periods if n_periods is not None else sp["n_periods"]
        n_w = n_scenarios if n_scenarios is not None else sp["n_scenarios"]

        # --- Generar demanda ---
        demand = generate_scenarios(
            n_products=catalog["n_cut_forms"],
            n_periods=n_t,
            n_scenarios=n_w,
            base_demands=catalog["base_demands"],
            cvs=catalog["cvs"],
            distribution=distribution,
            seasonality=dp if dp["amplitude"] > 0 else None,
            seed=seed,
        )

        # --- Scenario probs (equiprobable) ---
        scenario_probs = np.ones(n_w) / n_w

        # --- Capacidad escalada para large/industrial ---
        cap_max = capacity_max or self.DEFAULT_CAPACITY_MAX
        cap_min = capacity_min or self.DEFAULT_CAPACITY_MIN

        if size_profile in ("large", "industrial"):
            cap_max = capacity_max or 10_000
            cap_min = capacity_min or 1000

        # --- Construir instancia ---
        instance = ProblemInstance(
            name=f"{size_profile}_seed{seed}",
            profile=size_profile,
            seed=seed,
            # Capa 1
            n_parts=catalog["n_parts"],
            part_names=catalog["part_names"],
            alpha=catalog["alpha"],
            # Capa 2
            n_cut_forms=catalog["n_cut_forms"],
            cut_form_names=catalog["cut_form_names"],
            composition=catalog["composition"],
            exclusivity_groups=catalog["exclusivity_groups"],
            cut_config=catalog["cut_config"],
            # Periodos
            n_periods=n_t,
            # Economicos
            weight=weight or self.DEFAULT_WEIGHT,
            prices=catalog["prices"],
            cost_prod=cost_prod or self.DEFAULT_COST_PROD,
            cost_setup=cost_setup or self.DEFAULT_COST_SETUP,
            cost_inv=catalog["cost_inv"],
            cost_pen=catalog["cost_pen"],
            # Capacidad
            capacity_max=cap_max,
            capacity_min=cap_min,
            # Perecibilidad
            shelf_life=catalog["shelf_life"],
            # Escenarios
            n_scenarios=n_w,
            scenario_probs=scenario_probs,
            demand=demand,
        )

        # --- Validar ---
        errors = instance.validate()
        if errors:
            raise ValueError(
                f"Instancia generada invalida ({instance.name}):\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

        return instance

    def generate_set(
        self,
        size_profile: str = "small",
        demand_profile: str = "stable",
        n_seeds: int = 3,
        base_seed: int = 100,
        **kwargs,
    ) -> list[ProblemInstance]:
        """Generar un conjunto de instancias con diferentes seeds.

        Args:
            size_profile: Perfil de tamano.
            demand_profile: Perfil de demanda.
            n_seeds: Cuantas instancias generar.
            base_seed: Seed inicial (se incrementa).
            **kwargs: Argumentos adicionales para generate().

        Returns:
            Lista de ProblemInstance.
        """
        return [
            self.generate(
                size_profile=size_profile,
                demand_profile=demand_profile,
                seed=base_seed + i,
                **kwargs,
            )
            for i in range(n_seeds)
        ]

    @staticmethod
    def available_profiles() -> dict:
        """Retornar perfiles disponibles con sus parametros."""
        result = {}
        for name, sp in SIZE_PROFILES.items():
            cat = sp["catalog_fn"]()
            result[name] = {
                "n_cut_forms": cat["n_cut_forms"],
                "n_periods": sp["n_periods"],
                "n_scenarios": sp["n_scenarios"],
                "n_exclusivity_groups": len(cat["exclusivity_groups"]),
            }
        return result
