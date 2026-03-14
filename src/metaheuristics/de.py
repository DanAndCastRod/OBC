"""
Evolucion Diferencial (DE) para el problema de coproductos.

Estrategias: DE/rand/1/bin y DE/best/1/bin adaptadas a variables mixtas
(y binario, q entero) mediante discretizacion.

Referencia: Storn & Price 1997.

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 2.4
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from src.metaheuristics.base import BaseMetaheuristic
from src.metaheuristics.encoding import random_solution, repair_lot_sizing
from src.model.parameters import ProblemInstance
from src.model.solution import Solution

DEFAULT_CONFIG = {
    "pop_size": 50,
    "max_generations": 200,
    "F": 0.8,  # factor de escala
    "CR": 0.9,  # tasa de cruce
    "strategy": "rand/1/bin",  # 'rand/1/bin' o 'best/1/bin'
    "stagnation_limit": 50,
}


class DifferentialEvolution(BaseMetaheuristic):
    """Evolucion Diferencial con variables mixtas.

    Pseudocodigo:
    ```
    P = inicializar_poblacion_continua(pop_size)
    fitness = evaluar(discretizar(P))
    PARA gen = 1 ... max_generations:
        PARA i = 0 ... pop_size-1:
            // Mutacion DE
            SI strategy == 'rand/1/bin':
                r1,r2,r3 = aleatorios != i
                mutante = P[r1] + F * (P[r2] - P[r3])
            SI strategy == 'best/1/bin':
                r1,r2 = aleatorios != i
                mutante = P[best] + F * (P[r1] - P[r2])

            // Cruce binomial
            trial = copia(P[i])
            PARA j = 0 ... dim-1:
                SI random < CR O j == j_rand:
                    trial[j] = mutante[j]

            // Discretizar y evaluar
            y_t, q_t = discretizar(trial)
            fit_t = fitness(y_t, q_t)

            // Seleccion greedy
            SI fit_t >= fitness[i]:
                P[i] = trial
                fitness[i] = fit_t

        SI estancamiento(stagnation_limit):
            BREAK
    RETORNAR mejor(P)
    ```
    """

    def __init__(self, config: Optional[dict] = None):
        merged = {**DEFAULT_CONFIG, **(config or {})}
        super().__init__(merged)

    def solve(self, instance: ProblemInstance, **kwargs) -> Solution:
        """Ejecutar DE completo."""
        self.reset()

        pop_size = self.config["pop_size"]
        max_gen = self.config["max_generations"]
        F = self.config["F"]
        CR = self.config["CR"]
        strategy = self.config["strategy"]
        stag_limit = self.config["stagnation_limit"]

        q_min = instance.capacity_min
        q_max = instance.capacity_max
        n_t = instance.n_periods
        dim = 2 * n_t  # first n_t: y (continuous), next n_t: q (continuous)

        # --- Inicializar poblacion en espacio continuo ---
        population = np.zeros((pop_size, dim))
        fitness = np.zeros(pop_size)

        for i in range(pop_size):
            y, q = random_solution(instance)
            population[i] = self._encode(y, q, q_min, q_max)
            fitness[i] = self.evaluate_fitness(y, q, instance)

        # Mejor global
        best_idx = int(np.argmax(fitness))
        _, sol = self.evaluate_and_get_solution(
            *self._decode(population[best_idx], n_t, q_min, q_max), instance
        )
        self.update_best(fitness[best_idx], sol, instance)
        div0 = self._population_diversity(population, n_t)
        self.log_iteration(0, self.best_fitness, fitness[best_idx], diversity=div0)

        stagnation = 0

        # --- Loop generacional ---
        for gen in range(1, max_gen + 1):
            improved_any = False

            for i in range(pop_size):
                # Mutacion
                mutant = self._mutate_de(population, fitness, i, best_idx, F, strategy)

                # Cruce binomial
                trial = self._crossover_de(population[i], mutant, CR, dim)

                # Clampar al rango valido
                trial = np.clip(trial, 0.0, 1.0)

                # Discretizar y evaluar
                y_t, q_t = self._decode(trial, n_t, q_min, q_max)
                fit_t = self.evaluate_fitness(y_t, q_t, instance)

                # Seleccion greedy
                if fit_t >= fitness[i]:
                    population[i] = trial
                    fitness[i] = fit_t
                    improved_any = True

                    if fit_t > self.best_fitness:
                        _, sol = self.evaluate_and_get_solution(y_t, q_t, instance)
                        self.update_best(fit_t, sol, instance)
                        best_idx = i

            if improved_any:
                stagnation = 0
            else:
                stagnation += 1

            diversity = self._population_diversity(population, n_t)
            self.log_iteration(
                gen,
                self.best_fitness,
                float(np.max(fitness)),
                diversity=diversity,
            )

            if stagnation >= stag_limit:
                break

        return self.best_solution

    # ============================================================
    # Operadores DE
    # ============================================================

    @staticmethod
    def _mutate_de(
        population: np.ndarray,
        fitness: np.ndarray,
        target_idx: int,
        best_idx: int,
        F: float,
        strategy: str,
    ) -> np.ndarray:
        """Mutacion DE: generar vector mutante."""
        pop_size = len(population)
        candidates = [j for j in range(pop_size) if j != target_idx]

        if strategy == "best/1/bin":
            # mutant = best + F * (r1 - r2)
            r1, r2 = np.random.choice(candidates, size=2, replace=False)
            mutant = population[best_idx] + F * (population[r1] - population[r2])
        else:
            # rand/1/bin (default)
            r1, r2, r3 = np.random.choice(candidates, size=3, replace=False)
            mutant = population[r1] + F * (population[r2] - population[r3])

        return mutant

    @staticmethod
    def _crossover_de(
        target: np.ndarray, mutant: np.ndarray, CR: float, dim: int
    ) -> np.ndarray:
        """Cruce binomial DE."""
        trial = target.copy()
        j_rand = np.random.randint(dim)

        for j in range(dim):
            if np.random.random() < CR or j == j_rand:
                trial[j] = mutant[j]

        return trial

    # ============================================================
    # Codificacion/Decodificacion continua
    # ============================================================

    @staticmethod
    def _encode(y: np.ndarray, q: np.ndarray, q_min: int, q_max: int) -> np.ndarray:
        """Codificar (y, q) -> vector continuo [0, 1].

        y_t -> [0, 1]: 0.0 = off, 1.0 = on
        q_t -> [0, 1]: normalizado en [q_min, q_max]
        """
        n_t = len(y)
        vec = np.zeros(2 * n_t)

        for t in range(n_t):
            vec[t] = 1.0 if y[t] else 0.0
            if y[t] and q_max > q_min:
                vec[n_t + t] = (q[t] - q_min) / (q_max - q_min)
            else:
                vec[n_t + t] = 0.0

        return vec

    @staticmethod
    def _decode(
        vec: np.ndarray, n_t: int, q_min: int, q_max: int
    ) -> tuple[np.ndarray, np.ndarray]:
        """Decodificar vector continuo -> (y, q) discreto.

        y_t = 1 si vec[t] > 0.5
        q_t = round(vec[n_t+t] * (q_max - q_min) + q_min) si y_t=1
        """
        y = np.array([vec[t] > 0.5 for t in range(n_t)], dtype=bool)
        q = np.zeros(n_t, dtype=np.int64)

        for t in range(n_t):
            if y[t]:
                q_raw = vec[n_t + t] * (q_max - q_min) + q_min
                q[t] = int(np.clip(round(q_raw), q_min, q_max))

        y, q = repair_lot_sizing(y, q, q_min, q_max)
        return y, q

    @staticmethod
    def _population_diversity(population: np.ndarray, n_t: int) -> float:
        """Estimar diversidad sobre representacion continua [0,1]."""
        if population.size == 0:
            return float("nan")

        y_part = population[:, :n_t]
        q_part = population[:, n_t:]

        y_div = float(np.mean(np.std(y_part, axis=0)))
        q_div = float(np.mean(np.std(q_part, axis=0)))

        return 0.5 * (y_div + q_div)
