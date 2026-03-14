"""
Hibrido GA-SA (Algoritmo Memetico) para el problema de coproductos.

Combina la exploracion global del GA con la explotacion local del SA.
Cada N generaciones, aplica SA como busqueda local a los top-k individuos.

Referencia: Akbari-Aghghaleh 2025.

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 2.5
"""

from __future__ import annotations

import math
from typing import Optional

import numpy as np

from src.metaheuristics.base import BaseMetaheuristic
from src.metaheuristics.encoding import (
    crossover_two_point,
    mutate,
    neighborhood_quantity,
    neighborhood_toggle,
    random_solution,
    repair_lot_sizing,
)
from src.model.parameters import ProblemInstance
from src.model.solution import Solution

DEFAULT_CONFIG = {
    # GA params
    "pop_size": 50,
    "n_generations": 200,
    "crossover_rate": 0.8,
    "mutation_rate": 0.1,
    "selection_size": 3,
    "elitism_count": 2,
    "stagnation_limit": 50,
    # SA local search params
    "local_search_freq": 10,  # cada cuantas generaciones aplicar SA
    "local_search_top_k": 5,  # a cuantos top individuos aplicar SA
    "local_search_iters": 30,  # iteraciones de SA por individuo
    "local_search_T": 5000.0,  # temperatura inicial del SA local
    "local_search_cooling": 0.9,  # cooling rate del SA local
}


class HybridGASA(BaseMetaheuristic):
    """Algoritmo Memetico GA + SA.

    Pseudocodigo:
    ```
    P = inicializar_poblacion(pop_size)
    evaluar(P)
    PARA gen = 1 ... n_generations:
        // --- Fase GA ---
        elite = top_k(P, elitism_count)
        P_new = elite
        MIENTRAS |P_new| < pop_size:
            p1, p2 = torneo(P)
            c1, c2 = crossover(p1, p2)
            c1, c2 = mutar(c1), mutar(c2)
            P_new.agregar(c1, c2)
        P = P_new[:pop_size]
        evaluar(P)

        // --- Fase SA (cada local_search_freq generaciones) ---
        SI gen % local_search_freq == 0:
            top_indices = argsort(fitness)[-top_k:]
            PARA i EN top_indices:
                P[i] = busqueda_local_SA(P[i], local_search_iters)
                fitness[i] = evaluar(P[i])

        SI estancamiento(stagnation_limit):
            BREAK
    RETORNAR mejor(P)
    ```
    """

    def __init__(self, config: Optional[dict] = None):
        merged = {**DEFAULT_CONFIG, **(config or {})}
        super().__init__(merged)

    def solve(self, instance: ProblemInstance, **kwargs) -> Solution:
        """Ejecutar GA-SA completo."""
        self.reset()

        pop_size = self.config["pop_size"]
        n_gen = self.config["n_generations"]
        cx_rate = self.config["crossover_rate"]
        mut_rate = self.config["mutation_rate"]
        sel_size = self.config["selection_size"]
        elite_n = self.config["elitism_count"]
        stag_limit = self.config["stagnation_limit"]
        ls_freq = self.config["local_search_freq"]
        ls_top_k = self.config["local_search_top_k"]

        q_min = instance.capacity_min
        q_max = instance.capacity_max

        # --- Inicializar poblacion ---
        population = [random_solution(instance) for _ in range(pop_size)]
        fitness = np.array(
            [self.evaluate_fitness(y, q, instance) for y, q in population]
        )

        # Mejor global
        best_idx = int(np.argmax(fitness))
        best_fit, best_sol = self.evaluate_and_get_solution(
            population[best_idx][0], population[best_idx][1], instance
        )
        self.update_best(best_fit, best_sol, instance)
        div0 = self._population_diversity(population, q_min, q_max)
        self.log_iteration(0, self.best_fitness, best_fit, diversity=div0)

        stagnation = 0

        # --- Loop generacional ---
        for gen in range(1, n_gen + 1):
            # === Fase GA ===
            elite_indices = np.argsort(fitness)[-elite_n:]
            new_pop = [population[i] for i in elite_indices]

            while len(new_pop) < pop_size:
                p1 = self._tournament(population, fitness, sel_size)
                p2 = self._tournament(population, fitness, sel_size)

                if np.random.random() < cx_rate:
                    y_c1, q_c1, y_c2, q_c2 = crossover_two_point(
                        p1[0], p1[1], p2[0], p2[1], q_min, q_max
                    )
                    c1, c2 = (y_c1, q_c1), (y_c2, q_c2)
                else:
                    c1 = (p1[0].copy(), p1[1].copy())
                    c2 = (p2[0].copy(), p2[1].copy())

                y_m1, q_m1 = mutate(c1[0], c1[1], q_min, q_max, p_toggle=mut_rate)
                y_m2, q_m2 = mutate(c2[0], c2[1], q_min, q_max, p_toggle=mut_rate)

                new_pop.append((y_m1, q_m1))
                new_pop.append((y_m2, q_m2))

            population = new_pop[:pop_size]
            fitness = np.array(
                [self.evaluate_fitness(y, q, instance) for y, q in population]
            )

            # === Fase SA (busqueda local periodica) ===
            if gen % ls_freq == 0:
                top_indices = np.argsort(fitness)[-ls_top_k:]
                for i in top_indices:
                    y_imp, q_imp, fit_imp = self._local_search(
                        population[i][0], population[i][1], instance
                    )
                    if fit_imp > fitness[i]:
                        population[i] = (y_imp, q_imp)
                        fitness[i] = fit_imp

            # Actualizar mejor
            gen_best_idx = int(np.argmax(fitness))
            gen_best_fit = fitness[gen_best_idx]

            if gen_best_fit > self.best_fitness:
                _, sol = self.evaluate_and_get_solution(
                    population[gen_best_idx][0],
                    population[gen_best_idx][1],
                    instance,
                )
                self.update_best(gen_best_fit, sol, instance)
                stagnation = 0
            else:
                stagnation += 1

            diversity = self._population_diversity(population, q_min, q_max)
            self.log_iteration(
                gen,
                self.best_fitness,
                gen_best_fit,
                diversity=diversity,
            )

            if stagnation >= stag_limit:
                break

        return self.best_solution

    # ============================================================
    # Busqueda local SA
    # ============================================================

    def _local_search(
        self,
        y: np.ndarray,
        q: np.ndarray,
        instance: ProblemInstance,
    ) -> tuple[np.ndarray, np.ndarray, float]:
        """SA corto como busqueda local sobre un individuo.

        Returns:
            (y_best, q_best, fitness_best)
        """
        ls_iters = self.config["local_search_iters"]
        T = self.config["local_search_T"]
        cooling = self.config["local_search_cooling"]
        q_min = instance.capacity_min
        q_max = instance.capacity_max

        y_curr, q_curr = y.copy(), q.copy()
        fit_curr = self.evaluate_fitness(y_curr, q_curr, instance)
        y_best, q_best, fit_best = y_curr.copy(), q_curr.copy(), fit_curr

        for _ in range(ls_iters):
            # Perturbar
            r = np.random.random()
            if r < 0.3:
                y_new = neighborhood_toggle(y_curr, k=1)
                q_new = q_curr.copy()
            elif r < 0.7:
                y_new = y_curr.copy()
                q_new = neighborhood_quantity(q_curr, y_curr, q_min, q_max, 0.1)
            else:
                y_new = neighborhood_toggle(y_curr, k=1)
                q_new = neighborhood_quantity(q_curr, y_new, q_min, q_max, 0.1)

            y_new, q_new = repair_lot_sizing(y_new, q_new, q_min, q_max)
            fit_new = self.evaluate_fitness(y_new, q_new, instance)

            # Metropolis
            delta = fit_new - fit_curr
            if delta > 0 or (
                T > 0 and np.random.random() < math.exp(delta / max(T, 1e-10))
            ):
                y_curr, q_curr, fit_curr = y_new, q_new, fit_new

                if fit_new > fit_best:
                    y_best, q_best, fit_best = y_new.copy(), q_new.copy(), fit_new

            T *= cooling

        return y_best, q_best, fit_best

    @staticmethod
    def _tournament(population, fitness, k):
        indices = np.random.choice(len(population), size=k, replace=False)
        best = indices[np.argmax(fitness[indices])]
        return population[best]

    @staticmethod
    def _population_diversity(
        population: list[tuple[np.ndarray, np.ndarray]],
        q_min: int,
        q_max: int,
    ) -> float:
        """Estimar diversidad poblacional combinando y y q normalizado."""
        if not population:
            return float("nan")

        y_mat = np.array([ind[0].astype(float) for ind in population], dtype=float)
        q_mat = np.array([ind[1].astype(float) for ind in population], dtype=float)

        p = np.mean(y_mat, axis=0)
        y_div = float(np.mean(2.0 * p * (1.0 - p)))

        if q_max > q_min:
            q_norm = (q_mat - q_min) / (q_max - q_min)
            q_div = float(np.mean(np.std(q_norm, axis=0)))
        else:
            q_div = 0.0

        return 0.5 * (y_div + q_div)
