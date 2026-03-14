"""
Codificacion compartida para metaheuristicas.

Funciones para generar, reparar y perturbar soluciones
del problema de coproductos (vectores y, q).

Coherente con DD-07: cromosoma de 2 vectores.

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 2.1
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from src.model.parameters import ProblemInstance


def generate_random_binary(n_t: int, p_active: float = 0.7) -> np.ndarray:
    """Generar vector setup aleatorio.

    Args:
        n_t: Numero de periodos.
        p_active: Probabilidad de activar cada periodo.

    Returns:
        Vector binario [T].
    """
    return np.random.random(n_t) < p_active


def generate_random_integer(
    n_t: int, q_min: int, q_max: int, y: np.ndarray
) -> np.ndarray:
    """Generar vector cantidad aleatorio, coherente con setup.

    q_t = 0 si y_t = 0, else q_t ~ Uniform[q_min, q_max]

    Args:
        n_t: Numero de periodos.
        q_min: Lote minimo.
        q_max: Capacidad maxima.
        y: Vector setup binario.

    Returns:
        Vector entero [T].
    """
    q = np.zeros(n_t, dtype=np.int64)
    for t in range(n_t):
        if y[t]:
            q[t] = np.random.randint(q_min, q_max + 1)
    return q


def random_solution(instance: ProblemInstance) -> tuple[np.ndarray, np.ndarray]:
    """Generar solucion aleatoria factible.

    Args:
        instance: Instancia del problema.

    Returns:
        Tupla (y, q) factible.
    """
    y = generate_random_binary(instance.n_periods)
    q = generate_random_integer(
        instance.n_periods, instance.capacity_min, instance.capacity_max, y
    )
    return y, q


def repair_lot_sizing(
    y: np.ndarray,
    q: np.ndarray,
    q_min: int,
    q_max: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Reparar solucion para garantizar factibilidad.

    Reglas:
    - Si y_t = 0: q_t = 0
    - Si y_t = 1 y q_t < q_min: q_t = q_min
    - Si y_t = 1 y q_t > q_max: q_t = q_max
    - Si q_t > 0 y y_t = 0: activar y_t = 1

    Args:
        y: Vector setup (bool).
        q: Vector cantidad (int).
        q_min: Lote minimo.
        q_max: Capacidad maxima.

    Returns:
        Tupla (y, q) reparada.
    """
    y = np.array(y, dtype=bool).copy()
    q = np.array(q, dtype=np.int64).copy()

    for t in range(len(y)):
        if q[t] > 0 and not y[t]:
            y[t] = True  # activar si hay produccion

        if not y[t]:
            q[t] = 0
        else:
            q[t] = max(q_min, min(q[t], q_max))

    return y, q


def neighborhood_toggle(y: np.ndarray, k: int = 1) -> np.ndarray:
    """Perturbar vector setup toggling k bits aleatorios.

    Args:
        y: Vector setup original.
        k: Numero de bits a cambiar.

    Returns:
        Vector setup perturbado (copia).
    """
    y_new = y.copy()
    indices = np.random.choice(len(y), size=min(k, len(y)), replace=False)
    y_new[indices] = ~y_new[indices]
    return y_new


def neighborhood_quantity(
    q: np.ndarray,
    y: np.ndarray,
    q_min: int,
    q_max: int,
    delta: float = 0.2,
) -> np.ndarray:
    """Perturbar vector cantidad con ruido gaussiano.

    Solo perturba periodos con y_t = 1.
    delta controla la magnitud: q_new = q + N(0, delta * q_max).

    Args:
        q: Vector cantidad original.
        y: Vector setup.
        q_min: Lote minimo.
        q_max: Capacidad maxima.
        delta: Escala de perturbacion (fraccion de q_max).

    Returns:
        Vector cantidad perturbado y reparado (copia).
    """
    q_new = q.copy().astype(np.float64)
    noise = np.random.normal(0, delta * q_max, size=len(q))

    for t in range(len(q)):
        if y[t]:
            q_new[t] = max(q_min, min(q_new[t] + noise[t], q_max))
        else:
            q_new[t] = 0

    return q_new.astype(np.int64)


# ============================================================
# Operadores geneticos (para GA y DE)
# ============================================================


def crossover_uniform(
    y1: np.ndarray,
    q1: np.ndarray,
    y2: np.ndarray,
    q2: np.ndarray,
    q_min: int,
    q_max: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Cruce uniforme: para cada t, elegir gen de p1 o p2.

    Returns:
        (y_child1, q_child1, y_child2, q_child2)
    """
    mask = np.random.random(len(y1)) < 0.5

    y_c1 = np.where(mask, y1, y2)
    q_c1 = np.where(mask, q1, q2)
    y_c2 = np.where(mask, y2, y1)
    q_c2 = np.where(mask, q2, q1)

    y_c1, q_c1 = repair_lot_sizing(y_c1, q_c1, q_min, q_max)
    y_c2, q_c2 = repair_lot_sizing(y_c2, q_c2, q_min, q_max)

    return y_c1, q_c1, y_c2, q_c2


def crossover_two_point(
    y1: np.ndarray,
    q1: np.ndarray,
    y2: np.ndarray,
    q2: np.ndarray,
    q_min: int,
    q_max: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Cruce de dos puntos.

    Returns:
        (y_child1, q_child1, y_child2, q_child2)
    """
    n = len(y1)
    if n < 3:
        return crossover_uniform(y1, q1, y2, q2, q_min, q_max)

    pts = sorted(np.random.choice(n, size=2, replace=False))
    p1, p2 = pts[0], pts[1]

    y_c1 = np.concatenate([y1[:p1], y2[p1:p2], y1[p2:]])
    q_c1 = np.concatenate([q1[:p1], q2[p1:p2], q1[p2:]])
    y_c2 = np.concatenate([y2[:p1], y1[p1:p2], y2[p2:]])
    q_c2 = np.concatenate([q2[:p1], q1[p1:p2], q2[p2:]])

    y_c1, q_c1 = repair_lot_sizing(y_c1, q_c1, q_min, q_max)
    y_c2, q_c2 = repair_lot_sizing(y_c2, q_c2, q_min, q_max)

    return y_c1, q_c1, y_c2, q_c2


def mutate(
    y: np.ndarray,
    q: np.ndarray,
    q_min: int,
    q_max: int,
    p_toggle: float = 0.1,
    p_quantity: float | None = None,
    delta: float = 0.15,
) -> tuple[np.ndarray, np.ndarray]:
    """Mutacion combinada: toggle de setup + perturbacion de cantidad.

    Args:
        y, q: Individuo original.
        q_min, q_max: Limites de lote.
        p_toggle: Probabilidad de toggle por bit (setup).
        p_quantity: Probabilidad de perturbar cantidad por periodo activo.
            Si es None, usa el mismo valor de `p_toggle`.
        delta: Escala de perturbacion de cantidad.

    Returns:
        (y_mutated, q_mutated)
    """
    if p_quantity is None:
        p_quantity = p_toggle

    if not (0.0 <= p_toggle <= 1.0):
        raise ValueError(f"p_toggle fuera de rango [0,1]: {p_toggle}")
    if not (0.0 <= p_quantity <= 1.0):
        raise ValueError(f"p_quantity fuera de rango [0,1]: {p_quantity}")

    y_new = y.copy()
    q_new = q.copy().astype(np.float64)

    for t in range(len(y)):
        # Toggle setup con probabilidad p_toggle
        if np.random.random() < p_toggle:
            y_new[t] = not y_new[t]

        # Perturbar cantidad solo con probabilidad p_quantity
        if y_new[t]:
            if np.random.random() < p_quantity:
                noise = np.random.normal(0, delta * q_max)
                q_new[t] = q_new[t] + noise
            q_new[t] = max(q_min, min(q_new[t], q_max))
        else:
            q_new[t] = 0

    y_new, q_new = repair_lot_sizing(
        y_new.astype(bool), q_new.astype(np.int64), q_min, q_max
    )
    return y_new, q_new
