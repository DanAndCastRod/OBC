"""
Algoritmo Genetico (GA) para el problema de coproductos.

Operadores adaptados a variables mixtas:
- y (binario): cruce de dos puntos + bit-flip
- q (entero): cruce de dos puntos + mutacion gaussiana acotada

Referencia: Akbari-Aghghaleh 2025.

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 2.2
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from src.metaheuristics.base import BaseMetaheuristic
from src.metaheuristics.encoding import (
    crossover_two_point,
    mutate,
    random_solution,
)
from src.model.parameters import ProblemInstance
from src.model.solution import Solution

# Defaults
DEFAULT_CONFIG = {
    "pop_size": 50,
    "n_generations": 200,
    "crossover_rate": 0.8,
    "mutation_rate": 0.1,
    "selection_size": 3,
    "elitism_count": 2,
    "stagnation_limit": 50,
}


class GeneticAlgorithm(BaseMetaheuristic):
    """Algoritmo Genetico con variables mixtas.

    Pseudocodigo:
    ```
    P = inicializar_poblacion(pop_size)
    evaluar(P)
    PARA gen = 1 ... n_generations:
        elite = top_k(P, elitism_count)
        P_new = elite
        MIENTRAS |P_new| < pop_size:
            p1, p2 = seleccion_torneo(P, k=selection_size)
            SI random < crossover_rate:
                c1, c2 = crossover(p1, p2)
            SINO:
                c1, c2 = p1, p2
            c1 = mutar(c1, mutation_rate)
            c2 = mutar(c2, mutation_rate)
            P_new.agregar(c1, c2)
        P = P_new[:pop_size]
        evaluar(P)
        SI estancamiento(stagnation_limit):
            BREAK
    RETORNAR mejor(P)
    ```
    """

    def __init__(self, config: Optional[dict] = None):
        merged = {**DEFAULT_CONFIG, **(config or {})}
        super().__init__(merged)

    def solve(self, instance: ProblemInstance, **kwargs) -> Solution:
        """Ejecutar GA completo.

        Args:
            instance: Instancia del problema.

        Returns:
            Mejor solucion encontrada.
        """
        self.reset()

        pop_size = self.config["pop_size"]
        n_gen = self.config["n_generations"]
        cx_rate = self.config["crossover_rate"]
        mut_rate = self.config["mutation_rate"]
        sel_size = self.config["selection_size"]
        elite_n = self.config["elitism_count"]
        stag_limit = self.config["stagnation_limit"]

        q_min = instance.capacity_min
        q_max = instance.capacity_max

        # --- Inicializar poblacion ---
        population = self._initialize_population(pop_size, instance)
        fitness = self._evaluate_population(population, instance)

        # Registrar mejor
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
            # Elitismo: conservar top-k
            elite_indices = np.argsort(fitness)[-elite_n:]
            new_pop = [population[i] for i in elite_indices]

            # Generar hijos hasta llenar poblacion
            while len(new_pop) < pop_size:
                # Seleccion por torneo
                p1 = self._tournament_select(population, fitness, sel_size)
                p2 = self._tournament_select(population, fitness, sel_size)

                # Cruce
                if np.random.random() < cx_rate:
                    y_c1, q_c1, y_c2, q_c2 = crossover_two_point(
                        p1[0], p1[1], p2[0], p2[1], q_min, q_max
                    )
                    c1 = (y_c1, q_c1)
                    c2 = (y_c2, q_c2)
                else:
                    c1 = (p1[0].copy(), p1[1].copy())
                    c2 = (p2[0].copy(), p2[1].copy())

                # Mutacion
                y_m1, q_m1 = mutate(
                    c1[0], c1[1], q_min, q_max, p_toggle=mut_rate, delta=0.15
                )
                y_m2, q_m2 = mutate(
                    c2[0], c2[1], q_min, q_max, p_toggle=mut_rate, delta=0.15
                )

                new_pop.append((y_m1, q_m1))
                new_pop.append((y_m2, q_m2))

            population = new_pop[:pop_size]
            fitness = self._evaluate_population(population, instance)

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

            # Criterio de parada por estancamiento
            if stagnation >= stag_limit:
                break

        return self.best_solution

    # ============================================================
    # Metodos internos
    # ============================================================

    def _initialize_population(
        self, pop_size: int, instance: ProblemInstance
    ) -> list[tuple[np.ndarray, np.ndarray]]:
        """Generar poblacion inicial aleatoria."""
        return [random_solution(instance) for _ in range(pop_size)]

    def _evaluate_population(
        self,
        population: list[tuple[np.ndarray, np.ndarray]],
        instance: ProblemInstance,
    ) -> np.ndarray:
        """Evaluar fitness de toda la poblacion."""
        fitness = np.array(
            [self.evaluate_fitness(y, q, instance) for y, q in population]
        )
        return fitness

    def _tournament_select(
        self,
        population: list[tuple[np.ndarray, np.ndarray]],
        fitness: np.ndarray,
        k: int,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Seleccion por torneo de tamanio k."""
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
