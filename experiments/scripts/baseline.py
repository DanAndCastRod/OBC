"""
Heuristicas baseline para comparacion experimental (Fase 4).

Dos estrategias simples de referencia:
1. Proporcional: q_t = ceil(max_f(d_bar_ft / alpha_f))
   Produce lo justo para cubrir el producto mas demandado en promedio.
2. Max capacidad: q_t = Q_max siempre (produccion maxima todos los dias).

Se selecciona la mejor (mayor Z) como baseline para H1.

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 4.1
"""

from __future__ import annotations

import math
import time
from typing import TYPE_CHECKING, Literal

import numpy as np

if TYPE_CHECKING:
    from src.model.parameters import ProblemInstance

from src.model import decoder, objective
from src.model.solution import Solution


def _compute_proportional_q(instance: ProblemInstance) -> np.ndarray:
    """Calcular q_t proporcional: producir para el producto mas demandado.

    q_t = ceil(max_f(d_bar_ft / alpha_f))

    donde d_bar_ft es la demanda promedio del producto f en periodo t
    y alpha_f es el yield del producto f (fraccion de carcasa).

    Returns:
        Vector q[T] con cantidades proporcionales.
    """
    T = instance.n_periods
    q = np.zeros(T, dtype=np.int64)

    # alpha efectivo por forma de corte: fraccion de carcasa que produce f
    # composition[f, a] * alpha[a] da las partes anatomicas por forma de corte
    # El yield de f depende de la pieza principal usada
    # Simplificamos: alpha_f = sum_a(composition[f,a] * alpha[a]) / weight
    # = masa de la forma f por carcasa / peso_carcasa
    alpha_f = np.zeros(instance.n_cut_forms, dtype=np.float64)
    for f in range(instance.n_cut_forms):
        required_parts = np.where(instance.composition[f] > 0)[0]
        if required_parts.size > 0:
            # Cada forma usa la pieza mas restrictiva
            alpha_f[f] = float(np.min(instance.alpha[required_parts]))
        else:
            alpha_f[f] = 1.0  # fallback

    # Demanda promedio por escenario: d_bar[f, t] = E_w[d[f,t,w]]
    d_bar = np.einsum("ftw,w->ft", instance.demand, instance.scenario_probs)

    for t in range(T):
        # q_t = ceil(max_f(d_bar_ft / alpha_f))
        # alpha_f da cuantas "unidades de forma f se obtienen por carcasa"
        # d_bar_ft / alpha_f = carcasas necesarias para cubrir forma f
        ratios = np.zeros(instance.n_cut_forms, dtype=np.float64)
        for f in range(instance.n_cut_forms):
            if alpha_f[f] > 1e-9:
                # Ajustar por peso de carcasa:
                # produccion_f = alpha_f * weight * q_t
                # Para cubrir d_bar_ft: q_t >= d_bar_ft / (alpha_f * weight)
                ratios[f] = d_bar[f, t] / (alpha_f[f] * instance.weight)

        q_t = math.ceil(float(np.max(ratios))) if np.max(ratios) > 0 else 0

        # Respetar limites de capacidad
        q[t] = max(instance.capacity_min, min(q_t, instance.capacity_max))

    return q


def _compute_max_capacity_q(instance: ProblemInstance) -> np.ndarray:
    """Calcular q_t = Q_max siempre (produccion maxima).

    Returns:
        Vector q[T] con Q_max en todos los periodos.
    """
    return np.full(instance.n_periods, instance.capacity_max, dtype=np.int64)


def solve_baseline(
    instance: ProblemInstance,
    strategy: Literal["proportional", "max_capacity", "best"] = "best",
) -> Solution:
    """Resolver instancia con heuristica baseline.

    Args:
        instance: Instancia del problema.
        strategy: Estrategia a usar:
            - 'proportional': produccion proporcional a demanda
            - 'max_capacity': produccion maxima siempre
            - 'best': evalua ambas y retorna la mejor

    Returns:
        Solution con la mejor heuristica baseline.
    """
    strategies = {}

    if strategy in ("proportional", "best"):
        strategies["baseline-proportional"] = _solve_single(
            instance, _compute_proportional_q, "baseline-proportional"
        )

    if strategy in ("max_capacity", "best"):
        strategies["baseline-max"] = _solve_single(
            instance, _compute_max_capacity_q, "baseline-max"
        )

    if strategy == "best":
        # Seleccionar la mejor Z
        best_name = max(strategies, key=lambda k: strategies[k].objective_value)
        return strategies[best_name]

    # Solo una estrategia solicitada
    return next(iter(strategies.values()))


def _solve_single(
    instance: ProblemInstance,
    q_func,
    algorithm_name: str,
) -> Solution:
    """Ejecutar una estrategia baseline individual.

    Args:
        instance: Instancia del problema.
        q_func: Funcion que calcula q[T].
        algorithm_name: Nombre del algoritmo para metadata.

    Returns:
        Solution evaluada y validada.
    """
    t0 = time.time()

    # Calcular cantidades
    q = q_func(instance)

    # Setup: y_t = 1 si q_t > 0
    y = (q > 0).astype(bool)

    # Decodificar segunda etapa (ventas, inventario, insatisfaccion)
    sol = decoder.decode(y, q, instance)

    # Evaluar funcion objetivo
    bd = objective.evaluate_vectorized(sol, instance)

    # Verificar factibilidad
    sol.check_feasibility(instance)

    elapsed = time.time() - t0

    # Metadata
    sol.algorithm = algorithm_name
    sol.elapsed_seconds = elapsed
    sol.n_evaluations = 1

    return sol
