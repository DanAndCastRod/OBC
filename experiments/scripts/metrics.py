"""
Metricas de respuesta para el diseno experimental (Fase 4).

Centraliza el calculo de todas las metricas definidas en el plan:
- Z (funcion objetivo)
- Gap de optimalidad vs CBC
- Nivel de servicio
- Inventario promedio
- Inventario de baja rotacion

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 4.1
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from src.model.parameters import ProblemInstance
    from src.model.solution import Solution


@dataclass
class ExperimentMetrics:
    """Conjunto completo de metricas para una ejecucion experimental."""

    z_value: float  # Funcion objetivo total
    gap_percent: float  # Gap vs CBC (%) — NaN si no hay ref
    service_level: float  # Nivel de servicio (%)
    avg_inventory: float  # Inventario promedio (unidades)
    low_rotation_inventory: float  # Inventario baja rotacion (unidades)
    elapsed_seconds: float  # Tiempo computacional (seg)
    n_evaluations: int  # Numero de evaluaciones de fitness
    is_feasible: bool  # Factibilidad

    def to_dict(self) -> dict:
        """Convertir a diccionario para CSV/JSON."""
        return {
            "z_value": self.z_value,
            "gap_percent": self.gap_percent,
            "service_level": self.service_level,
            "avg_inventory": self.avg_inventory,
            "low_rotation_inventory": self.low_rotation_inventory,
            "elapsed_seconds": self.elapsed_seconds,
            "n_evaluations": self.n_evaluations,
            "is_feasible": self.is_feasible,
        }

    def __repr__(self) -> str:
        return (
            f"Metrics(Z={self.z_value:,.0f}, gap={self.gap_percent:.2f}%, "
            f"service={self.service_level:.1f}%, "
            f"inv={self.avg_inventory:,.1f}, "
            f"low_rot={self.low_rotation_inventory:,.1f}, "
            f"t={self.elapsed_seconds:.2f}s, "
            f"feasible={self.is_feasible})"
        )


def compute_objective(solution: Solution, instance: ProblemInstance) -> float:
    """Calcular Z (funcion objetivo) usando el evaluador vectorizado.

    Si la solucion ya tiene objective_value calculado, lo retorna directamente.

    Args:
        solution: Solucion completa (con v, I, u calculados).
        instance: Instancia del problema.

    Returns:
        Valor de Z.
    """
    from src.model import objective

    if solution.objective_value != 0.0:
        return solution.objective_value

    bd = objective.evaluate_vectorized(solution, instance)
    return bd.total


def compute_gap(z_algo: float, z_reference: float) -> float:
    """Calcular gap de optimalidad porcentual.

    Gap = (Z_ref - Z_algo) / |Z_ref| * 100

    Args:
        z_algo: Valor Z del algoritmo a evaluar.
        z_reference: Valor Z de referencia (CBC optimo).

    Returns:
        Gap en porcentaje. NaN si referencia es 0 o NaN.
    """
    if np.isnan(z_reference) or abs(z_reference) < 1e-9:
        return float("nan")
    return (z_reference - z_algo) / abs(z_reference) * 100.0


def compute_service_level(solution: Solution, instance: ProblemInstance) -> float:
    """Calcular nivel de servicio porcentual.

    Nivel de servicio = (sum v_ftw / sum d_ftw) * 100

    Args:
        solution: Solucion con ventas (v) calculadas.
        instance: Instancia con demanda.

    Returns:
        Nivel de servicio en porcentaje.
    """
    if solution.v is None:
        return 0.0

    total_sales = float(np.sum(solution.v))
    total_demand = float(np.sum(instance.demand))

    if total_demand < 1e-9:
        return 100.0

    return (total_sales / total_demand) * 100.0


def compute_avg_inventory(solution: Solution, instance: ProblemInstance) -> float:
    """Calcular inventario promedio.

    I_avg = (1 / |T| * |Omega|) * sum_{t,w} sum_f I_ftw

    Args:
        solution: Solucion con inventario (I) calculado.
        instance: Instancia del problema.

    Returns:
        Inventario promedio por periodo-escenario.
    """
    if solution.I is None:
        return 0.0

    total_inv = float(np.sum(solution.I))
    n_tw = instance.n_periods * instance.n_scenarios

    if n_tw == 0:
        return 0.0

    return total_inv / n_tw


def compute_low_rotation_inventory(
    solution: Solution,
    instance: ProblemInstance,
    threshold: float = 0.5,
) -> float:
    """Calcular inventario de productos de baja rotacion.

    Un producto f es de baja rotacion si su ratio de ventas promedio
    sobre demanda promedio es menor que el umbral:
        v_bar_f / d_bar_f < threshold

    Args:
        solution: Solucion con ventas (v) e inventario (I).
        instance: Instancia con demanda.
        threshold: Umbral de rotacion (default 0.5).

    Returns:
        Inventario total de productos de baja rotacion.
    """
    if solution.v is None or solution.I is None:
        return 0.0

    n_forms = instance.n_cut_forms
    low_rot_inv = 0.0

    for f in range(n_forms):
        avg_sales = float(np.mean(solution.v[f, :, :]))
        avg_demand = float(np.mean(instance.demand[f, :, :]))

        if avg_demand < 1e-9:
            continue

        rotation_ratio = avg_sales / avg_demand
        if rotation_ratio < threshold:
            low_rot_inv += float(np.sum(solution.I[f, :, :]))

    return low_rot_inv


def compute_all_metrics(
    solution: Solution,
    instance: ProblemInstance,
    z_reference: float = float("nan"),
    elapsed_seconds: float = 0.0,
    n_evaluations: int = 0,
) -> ExperimentMetrics:
    """Calcular todas las metricas de una ejecucion experimental.

    Args:
        solution: Solucion completa.
        instance: Instancia del problema.
        z_reference: Valor Z de referencia para gap (NaN si no hay).
        elapsed_seconds: Tiempo computacional externo.
        n_evaluations: Numero de evaluaciones de fitness.

    Returns:
        ExperimentMetrics con todas las metricas.
    """
    from src.model import constraints

    z = compute_objective(solution, instance)
    gap = compute_gap(z, z_reference)
    service = compute_service_level(solution, instance)
    avg_inv = compute_avg_inventory(solution, instance)
    low_rot = compute_low_rotation_inventory(solution, instance)
    feasible = constraints.all_satisfied(solution, instance)

    return ExperimentMetrics(
        z_value=z,
        gap_percent=gap,
        service_level=service,
        avg_inventory=avg_inv,
        low_rotation_inventory=low_rot,
        elapsed_seconds=elapsed_seconds,
        n_evaluations=n_evaluations,
        is_feasible=feasible,
    )
