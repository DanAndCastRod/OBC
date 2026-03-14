"""
Recocido Simulado (Simulated Annealing) para el problema de coproductos.

Esquema de enfriamiento geometrico con reheating opcional.
Perturbaciones mixtas sobre (y, q): toggle setup, perturbacion cantidad, o ambas.

Referencia: Kirkpatrick 1983, criterio de Metropolis.

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 2.3
"""

from __future__ import annotations

import math
from typing import Optional

import numpy as np

from src.metaheuristics.base import BaseMetaheuristic
from src.metaheuristics.encoding import (
    neighborhood_quantity,
    neighborhood_toggle,
    random_solution,
    repair_lot_sizing,
)
from src.model.parameters import ProblemInstance
from src.model.solution import Solution

DEFAULT_CONFIG = {
    "T_initial": None,  # None = auto-estimate
    "T_final": 1.0,
    "cooling_rate": 0.95,
    "max_iterations": 500,
    "n_neighbors": 1,
    "p_toggle": 0.3,  # prob: only toggle setup
    "p_quantity": 0.4,  # prob: only perturb quantity
    # p_both = 1 - p_toggle - p_quantity = 0.3
    "delta": 0.15,  # perturbation scale for quantity
    "reheat_factor": 1.5,  # T *= reheat_factor when stagnating
    "reheat_threshold": 50,  # iterations without improvement to trigger reheat
}


class SimulatedAnnealing(BaseMetaheuristic):
    """Recocido Simulado con enfriamiento geometrico y reheating.

    Pseudocodigo:
    ```
    s = solucion_aleatoria()
    T = T_initial (o auto-estimado)
    MIENTRAS T > T_final:
        PARA i = 1 ... max_iterations:
            s' = generar_vecino(s)
            delta = fitness(s') - fitness(s)
            SI delta > 0 O random < exp(delta / T):
                s = s'
            SI s' mejor que best:
                best = s'
                stagnation = 0
            SINO:
                stagnation += 1
            SI stagnation >= reheat_threshold:
                T *= reheat_factor
                stagnation = 0
        T *= cooling_rate
    RETORNAR best
    ```
    """

    def __init__(self, config: Optional[dict] = None):
        merged = {**DEFAULT_CONFIG, **(config or {})}
        super().__init__(merged)

    def solve(self, instance: ProblemInstance, **kwargs) -> Solution:
        """Ejecutar SA completo."""
        self.reset()

        T = self.config["T_initial"]
        T_final = self.config["T_final"]
        cooling = self.config["cooling_rate"]
        max_iter = self.config["max_iterations"]
        reheat_factor = self.config["reheat_factor"]
        reheat_threshold = self.config["reheat_threshold"]

        q_min = instance.capacity_min
        q_max = instance.capacity_max

        # Solucion inicial
        y_curr, q_curr = random_solution(instance)
        fit_curr = self.evaluate_fitness(y_curr, q_curr, instance)

        # Guardar mejor
        fit_best, sol_best = self.evaluate_and_get_solution(y_curr, q_curr, instance)
        self.update_best(fit_best, sol_best, instance)

        # Auto-estimar temperatura inicial
        if T is None:
            T = self._estimate_initial_temperature(instance)

        iteration = 0
        stagnation = 0

        # Loop de enfriamiento
        while T > T_final:
            for _ in range(max_iter):
                # Generar vecino
                y_new, q_new = self._generate_neighbor(y_curr, q_curr, q_min, q_max)
                fit_new = self.evaluate_fitness(y_new, q_new, instance)

                # Criterio de Metropolis
                delta = fit_new - fit_curr
                if self._accept(delta, T):
                    y_curr = y_new
                    q_curr = q_new
                    fit_curr = fit_new

                # Actualizar mejor
                if fit_new > self.best_fitness:
                    _, sol = self.evaluate_and_get_solution(y_new, q_new, instance)
                    self.update_best(fit_new, sol, instance)
                    stagnation = 0
                else:
                    stagnation += 1

                iteration += 1
                self.log_iteration(iteration, self.best_fitness, fit_curr)

                # Reheating si estancado
                if stagnation >= reheat_threshold:
                    T *= reheat_factor
                    stagnation = 0

            # Enfriamiento
            T *= cooling

        return self.best_solution

    def _generate_neighbor(
        self,
        y: np.ndarray,
        q: np.ndarray,
        q_min: int,
        q_max: int,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Generar vecino con perturbacion mixta."""
        p_toggle = self.config["p_toggle"]
        p_quantity = self.config["p_quantity"]
        delta = self.config["delta"]

        r = np.random.random()

        if r < p_toggle:
            # Solo toggle setup
            y_new = neighborhood_toggle(y, k=1)
            q_new = q.copy()
        elif r < p_toggle + p_quantity:
            # Solo perturbacion cantidad
            y_new = y.copy()
            q_new = neighborhood_quantity(q, y, q_min, q_max, delta)
        else:
            # Ambas
            y_new = neighborhood_toggle(y, k=1)
            q_new = neighborhood_quantity(q, y_new, q_min, q_max, delta)

        y_new, q_new = repair_lot_sizing(y_new, q_new, q_min, q_max)
        return y_new, q_new

    @staticmethod
    def _accept(delta: float, temperature: float) -> bool:
        """Criterio de Metropolis: aceptar si mejora o con probabilidad."""
        if delta > 0:
            return True
        if temperature <= 0:
            return False
        prob = math.exp(delta / temperature)
        return np.random.random() < prob

    def _estimate_initial_temperature(
        self, instance: ProblemInstance, n_samples: int = 20
    ) -> float:
        """Estimar T0 tal que ~80% de las soluciones se acepten inicialmente.

        Genera n_samples pares de soluciones aleatorias y calcula
        el delta promedio. T0 = -delta_avg / ln(0.8).
        """
        deltas = []
        for _ in range(n_samples):
            y1, q1 = random_solution(instance)
            y2, q2 = random_solution(instance)
            f1 = self.evaluate_fitness(y1, q1, instance)
            f2 = self.evaluate_fitness(y2, q2, instance)
            deltas.append(abs(f1 - f2))

        delta_avg = np.mean(deltas) if deltas else 1e6
        if delta_avg < 1:
            delta_avg = 1e6
        T0 = -delta_avg / math.log(0.8)
        return T0
