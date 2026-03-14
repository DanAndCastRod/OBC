"""
Datos de calibracion para instancias del problema de coproductos.

Fuentes principales:
- Solano-Blanco et al. (2022): costos y capacidades avicolas, Santa Marta
- FENAVI (2024): precios al productor, Colombia
- Tahraoui et al. (2025): estructura multi-producto
- FAO/USDA: proporciones anatomicas estandar de pollo Ross 308

Cada constante incluye referencia a la fuente y pagina/tabla.
Ver docs/calibration_sources.md para la tabla completa de trazabilidad.

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 3.2
"""

from __future__ import annotations

from copy import deepcopy
from typing import Optional

import numpy as np

from src.model.parameters import ProblemInstance

# ================================================================
# Proporciones anatomicas (% peso carcasa)
# ================================================================

ANATOMICAL_PROPORTIONS: dict[str, float] = {
    # Fuente: USDA/FAO poultry carcass yield (Ross 308 broiler 2.3-2.5 kg)
    # Ref: Solano-Blanco 2022 Tabla 2; Cobb Broiler Management Guide 2024
    "pechuga": 0.30,  # 28-32%  → 0.30
    "muslo": 0.18,  # 16-20%  → 0.18
    "contramuslo": 0.14,  # 12-16%  → 0.14
    "ala": 0.08,  # 7-9%    → 0.08
    "menudencias": 0.05,  # 4-6%    → 0.05 (higado, corazon, molleja)
    "otros": 0.25,  # 22-28%  → 0.25 (espalda, cuello, grasa, piel)
}
# Validacion: sum = 1.0
assert abs(sum(ANATOMICAL_PROPORTIONS.values()) - 1.0) < 1e-10


# ================================================================
# Precios al productor (COP/kg)
# ================================================================

PRICE_RANGES_COP: dict[str, dict[str, float]] = {
    # Fuente: FENAVI Boletin Estadistico 2024, precios mayorista Canal Bogota
    # Ref: https://fenavi.org/estadisticas/
    "pechuga": {
        "min": 12_000,
        "max": 15_000,
        "default": 14_000,
        "fuente": "FENAVI 2024 — Canal mayorista Bogota",
    },
    "pernil_completo": {
        "min": 9_500,
        "max": 12_000,
        "default": 11_000,
        "fuente": "FENAVI 2024 — Precio pernil/pierna",
    },
    "muslo": {
        "min": 8_000,
        "max": 10_000,
        "default": 9_000,
        "fuente": "FENAVI 2024 — Muslo individual",
    },
    "contramuslo": {
        "min": 7_500,
        "max": 9_500,
        "default": 8_500,
        "fuente": "FENAVI 2024 — Contramuslo individual",
    },
    "ala": {
        "min": 5_000,
        "max": 7_500,
        "default": 6_000,
        "fuente": "FENAVI 2024 — Ala entera",
    },
    "menudencias": {
        "min": 3_000,
        "max": 5_000,
        "default": 4_000,
        "fuente": "FENAVI 2024 — Menudencias empacadas",
    },
    "subproducto_fresco": {
        "min": 1_000,
        "max": 2_500,
        "default": 1_500,
        "fuente": "Estimacion — Subproducto para rendering",
    },
    "harina_avicola": {
        "min": 1_800,
        "max": 3_000,
        "default": 2_200,
        "fuente": "Estimacion — Harina para alimentacion animal",
    },
    "filete_pechuga": {
        "min": 14_000,
        "max": 18_000,
        "default": 16_000,
        "fuente": "FENAVI 2024 — Filete premium deshuesado",
    },
    "medio_pollo": {
        "min": 10_000,
        "max": 13_000,
        "default": 12_000,
        "fuente": "FENAVI 2024 — Medio pollo empacado",
    },
}


# ================================================================
# Costos operativos de referencia
# ================================================================

COST_REFERENCE: dict[str, dict[str, float]] = {
    # Fuente: Solano-Blanco 2022 Seccion 4.2 (planta Santa Marta)
    "cost_prod": {
        "min": 1_500,
        "max": 2_500,
        "default": 2_000,
        "unit": "COP/carcasa",
        "fuente": "Solano-Blanco 2022 — Costo procesamiento por ave",
    },
    "cost_setup": {
        "min": 500_000,
        "max": 1_500_000,
        "default": 500_000,
        "unit": "COP/periodo",
        "fuente": "Solano-Blanco 2022 — Costo arranque linea de produccion",
    },
    "cost_inv": {
        "min": 100,
        "max": 500,
        "default": 300,
        "unit": "COP/kg/periodo",
        "fuente": "Solano-Blanco 2022 — Costo refrigeracion/almacenamiento",
        "note": "Varia por producto: fresco alto, congelado bajo",
    },
    "cost_pen": {
        "min": 2_000,
        "max": 6_000,
        "default": 4_000,
        "unit": "COP/kg insatisfecho",
        "fuente": "Estimacion — Penalizacion por demanda no servida",
        "note": "Tipicamente 30-50% del precio de venta del producto",
    },
}


# ================================================================
# Capacidades de planta
# ================================================================

CAPACITY_REFERENCE: dict[str, dict[str, int]] = {
    # Fuente: Solano-Blanco 2022 Seccion 3.1 (planta mediana Santa Marta)
    "standard": {
        "Q_min": 500,  # lote minimo viable (por eficiencia)
        "Q_max": 5_000,  # capacidad maxima linea estandar
        "fuente": "Solano-Blanco 2022 — Planta mediana Santa Marta",
    },
    "large": {
        "Q_min": 1_000,
        "Q_max": 10_000,
        "fuente": "Estimacion — Planta grande (tipo PPC/Bucanero)",
    },
    "industrial": {
        "Q_min": 2_000,
        "Q_max": 20_000,
        "fuente": "Estimacion — Planta industrial integrada",
    },
}


# ================================================================
# Vida util (dias)
# ================================================================

SHELF_LIFE: dict[str, dict[str, int]] = {
    # Fuente: Norma NTC 3644-2 (Colombia), Codex Alimentarius CAC/RCP 44-1995
    "refrigerado": {
        "min": 4,
        "max": 7,
        "default": 5,
        "fuente": "NTC 3644-2 — Pollo fresco refrigerado (0-4°C)",
    },
    "menudencias": {
        "min": 2,
        "max": 4,
        "default": 3,
        "fuente": "NTC 3644-2 — Menudencias frescas (mayor degradacion)",
    },
    "congelado": {
        "min": 30,
        "max": 365,
        "default": 30,
        "fuente": "NTC 3644-2 — Pollo congelado (-18°C)",
    },
    "harina": {
        "min": 90,
        "max": 365,
        "default": 180,
        "fuente": "Codex CAC/RCP 44 — Subproductos deshidratados",
    },
}


# ================================================================
# Peso carcasa
# ================================================================

WEIGHT_REFERENCE: dict[str, float] = {
    # Fuente: Cobb 500 / Ross 308 performance objectives 2024
    "min": 2.0,  # kg, pollo joven
    "max": 3.0,  # kg, pollo pesado
    "default": 2.5,  # kg, estandar industrial colombiano
    "fuente": "Cobb/Ross performance guide 2024",
}


# ================================================================
# Correlacion entre coproductos
# ================================================================


def get_default_correlation(n_products: int) -> np.ndarray:
    """Matriz de correlacion por defecto entre coproductos.

    Justificacion: los coproductos de una misma carcasa tienen alta
    correlacion positiva (cuando hay mas pollos, hay mas de todo).
    La pechuga y subproductos tienen menor correlacion porque la
    pechuga tiene demanda mas estable (producto premium).

    Args:
        n_products: Numero de formas de corte.

    Returns:
        Matriz de correlacion [n, n] definida positiva.
    """
    # Correlacion base alta para coproductos de misma ave
    rho = 0.6
    corr = np.full((n_products, n_products), rho)
    np.fill_diagonal(corr, 1.0)

    # Pechuga (idx 0) menos correlacionada con subproductos
    if n_products > 3:
        corr[0, -1] = 0.3
        corr[-1, 0] = 0.3
        corr[0, -2] = 0.35 if n_products > 4 else 0.3
        corr[-2, 0] = 0.35 if n_products > 4 else 0.3

    return corr


# ================================================================
# Calibrar instancia existente
# ================================================================


def calibrate_instance(
    instance: ProblemInstance,
    source: str = "solano_blanco",
    weight: Optional[float] = None,
    cost_prod: Optional[float] = None,
    cost_setup: Optional[float] = None,
) -> ProblemInstance:
    """Recalibrar parametros economicos de una instancia existente.

    Aplica valores de referencia de la literatura sin cambiar la estructura
    (formas de corte, demanda, escenarios).

    Args:
        instance: Instancia a calibrar.
        source: Fuente de calibracion ('solano_blanco' o 'fenavi').
        weight: Override peso carcasa.
        cost_prod: Override costo produccion.
        cost_setup: Override costo setup.

    Returns:
        Copia calibrada de la instancia (no modifica la original).

    Raises:
        ValueError: Si la fuente no es valida.
    """
    valid_sources = ("solano_blanco", "fenavi")
    if source not in valid_sources:
        raise ValueError(f"source '{source}' no valido. Opciones: {valid_sources}")

    # Clonar para no mutar la original
    inst = deepcopy(instance)

    # --- Peso ---
    inst.weight = weight or WEIGHT_REFERENCE["default"]

    # --- Costos operativos ---
    inst.cost_prod = cost_prod or COST_REFERENCE["cost_prod"]["default"]
    inst.cost_setup = cost_setup or COST_REFERENCE["cost_setup"]["default"]

    # --- Capacidad (segun perfil) ---
    if inst.profile in ("large", "industrial"):
        cap_key = inst.profile
    else:
        cap_key = "standard"
    cap = CAPACITY_REFERENCE.get(cap_key, CAPACITY_REFERENCE["standard"])
    inst.capacity_min = cap["Q_min"]
    inst.capacity_max = cap["Q_max"]

    # --- Validar resultado ---
    errors = inst.validate()
    if errors:
        raise ValueError(
            "Instancia calibrada invalida:\n" + "\n".join(f"  - {e}" for e in errors)
        )

    return inst


def validate_calibration_data() -> list[str]:
    """Verificar coherencia interna de los datos de calibracion.

    Returns:
        Lista de errores. Vacia si todo es coherente.
    """
    errors = []

    # Alpha sum = 1
    alpha_sum = sum(ANATOMICAL_PROPORTIONS.values())
    if abs(alpha_sum - 1.0) > 1e-10:
        errors.append(f"ANATOMICAL_PROPORTIONS sum = {alpha_sum}, esperado 1.0")

    # Costos < Precios (sanity)
    cost_inv_max = COST_REFERENCE["cost_inv"]["max"]
    for name, pr in PRICE_RANGES_COP.items():
        if cost_inv_max >= pr["min"]:
            errors.append(
                f"cost_inv max ({cost_inv_max}) >= price min de {name} ({pr['min']})"
            )

    # Q_min < Q_max
    for cap_name, cap in CAPACITY_REFERENCE.items():
        if cap["Q_min"] >= cap["Q_max"]:
            errors.append(
                f"CAPACITY {cap_name}: Q_min ({cap['Q_min']}) >= Q_max ({cap['Q_max']})"
            )

    # Shelf life > 0
    for cat, sl in SHELF_LIFE.items():
        if sl["default"] <= 0:
            errors.append(f"SHELF_LIFE {cat}: default <= 0")

    # Weight > 0
    if WEIGHT_REFERENCE["default"] <= 0:
        errors.append("WEIGHT default <= 0")

    return errors
