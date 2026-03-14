"""
Evaluador de la funcion objetivo (Eq. 1 del anteproyecto).

Max Z = sum_w pi_w [ sum_t ( sum_f r_f * v_ftw
                             - c_prod * q_t
                             - F * y_t
                             - sum_f c_inv_f * I_ftw
                             - sum_f c_pen_f * u_ftw ) ]

Adaptado para 3 capas (DD-03): f = formas de corte, no piezas anatomicas.

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 1.3
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from src.model.parameters import ProblemInstance
    from src.model.solution import Solution

from src.model.solution import SolutionBreakdown


def evaluate(solution: Solution, instance: ProblemInstance) -> SolutionBreakdown:
    """Calcular la funcion objetivo Z y su desglose por componente.

    Implementa Eq. 1 del anteproyecto, adaptada a formas de corte.

    Args:
        solution: Solucion con variables de primera y segunda etapa.
        instance: Instancia del problema.

    Returns:
        SolutionBreakdown con cada componente y el total.

    Raises:
        ValueError: Si las variables de segunda etapa no estan calculadas.
    """
    if solution.v is None or solution.I is None or solution.u is None:
        raise ValueError(
            "Variables de segunda etapa (v, I, u) no calculadas. "
            "Ejecute decoder.decode() primero."
        )

    pi = instance.scenario_probs  # [W]
    T = instance.n_periods
    F = instance.n_cut_forms

    # --- Ingresos por ventas ---
    # sum_w pi_w * sum_t sum_f r_f * v_ftw
    revenue = 0.0
    for w in range(instance.n_scenarios):
        for t in range(T):
            for f in range(F):
                revenue += pi[w] * instance.prices[f] * solution.v[f, t, w]

    # --- Costo de produccion ---
    # sum_w pi_w * sum_t c_prod * q_t  (q_t no depende de w)
    # = sum_t c_prod * q_t  (porque sum(pi_w) = 1)
    prod_cost = float(instance.cost_prod * solution.q.sum())

    # --- Costo de setup ---
    # sum_t F * y_t
    setup_cost = float(instance.cost_setup * solution.y.sum())

    # --- Costo de inventario ---
    # sum_w pi_w * sum_t sum_f c_inv_f * I_ftw
    inv_cost = 0.0
    for w in range(instance.n_scenarios):
        for t in range(T):
            for f in range(F):
                inv_cost += pi[w] * instance.cost_inv[f] * solution.I[f, t, w]

    # --- Penalizacion por insatisfaccion ---
    # sum_w pi_w * sum_t sum_f c_pen_f * u_ftw
    pen_cost = 0.0
    for w in range(instance.n_scenarios):
        for t in range(T):
            for f in range(F):
                pen_cost += pi[w] * instance.cost_pen[f] * solution.u[f, t, w]

    breakdown = SolutionBreakdown(
        revenue=revenue,
        prod_cost=prod_cost,
        setup_cost=setup_cost,
        inv_cost=inv_cost,
        pen_cost=pen_cost,
    )

    solution.objective_value = breakdown.total
    solution.breakdown = breakdown

    return breakdown


def evaluate_vectorized(
    solution: Solution, instance: ProblemInstance
) -> SolutionBreakdown:
    """Version vectorizada (mas rapida) del evaluador.

    Equivalente a evaluate() pero usa operaciones NumPy.
    """
    if solution.v is None or solution.I is None or solution.u is None:
        raise ValueError("Variables de segunda etapa (v, I, u) no calculadas.")

    pi = instance.scenario_probs  # [W]

    # Revenue: sum_w pi_w * sum_t sum_f r_f * v_ftw
    # prices[F] broadcast con v[F, T, W]
    revenue = float(np.einsum("w,f,ftw->", pi, instance.prices, solution.v))

    # Prod cost: c_prod * sum(q_t)
    prod_cost = float(instance.cost_prod * solution.q.sum())

    # Setup cost: F * sum(y_t)
    setup_cost = float(instance.cost_setup * solution.y.sum())

    # Inv cost: sum_w pi_w * sum_t sum_f c_inv_f * I_ftw
    inv_cost = float(np.einsum("w,f,ftw->", pi, instance.cost_inv, solution.I))

    # Pen cost: sum_w pi_w * sum_t sum_f c_pen_f * u_ftw
    pen_cost = float(np.einsum("w,f,ftw->", pi, instance.cost_pen, solution.u))

    breakdown = SolutionBreakdown(
        revenue=revenue,
        prod_cost=prod_cost,
        setup_cost=setup_cost,
        inv_cost=inv_cost,
        pen_cost=pen_cost,
    )

    solution.objective_value = breakdown.total
    solution.breakdown = breakdown

    return breakdown
