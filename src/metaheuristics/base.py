"""
Clase base abstracta para metaheuristicas.

Define interfaz comun (solve, evaluate_fitness) y tracking de progreso.
Todas las metaheuristicas (GA, SA, DE, GA-SA) heredan de esta clase.

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 2.1
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import numpy as np

from src.metaheuristics.encoding import random_solution, repair_lot_sizing
from src.model import decoder, objective
from src.model.parameters import ProblemInstance
from src.model.solution import Solution


@dataclass
class IterationLog:
    """Registro de una iteracion."""

    iteration: int
    best_fitness: float
    current_fitness: float
    elapsed_seconds: float
    n_evaluations: int
    diversity: float | None = None


class BaseMetaheuristic(ABC):
    """Clase base abstracta para metaheuristicas.

    Atributos:
        config: Diccionario de hiperparametros.
        history: Historial de iteraciones.
        best_solution: Mejor solucion encontrada.
        best_fitness: Mejor fitness encontrado.
        n_evaluations: Contador de evaluaciones de fitness.
    """

    def __init__(self, config: Optional[dict] = None):
        self.config: dict = config or {}
        self.history: list[IterationLog] = []
        self.best_solution: Optional[Solution] = None
        self.best_fitness: float = -np.inf
        self.n_evaluations: int = 0
        self._start_time: float = 0.0

    @abstractmethod
    def solve(self, instance: ProblemInstance, **kwargs) -> Solution:
        """Resolver instancia con la metaheuristica.

        Args:
            instance: Instancia del problema.
            **kwargs: Parametros adicionales.

        Returns:
            Mejor solucion encontrada.
        """
        ...

    def evaluate_fitness(
        self,
        y: np.ndarray,
        q: np.ndarray,
        instance: ProblemInstance,
    ) -> float:
        """Evaluar fitness de una solucion (y, q).

        Pipeline: repair -> decode -> evaluate -> Z

        Args:
            y: Vector setup.
            q: Vector cantidad.
            instance: Instancia del problema.

        Returns:
            Valor de Z (fitness).
        """
        # Reparar si es necesario
        y, q = repair_lot_sizing(y, q, instance.capacity_min, instance.capacity_max)

        # Decodificar segunda etapa
        sol = decoder.decode(y, q, instance)

        # Evaluar funcion objetivo
        bd = objective.evaluate_vectorized(sol, instance)

        self.n_evaluations += 1
        return bd.total

    def evaluate_and_get_solution(
        self,
        y: np.ndarray,
        q: np.ndarray,
        instance: ProblemInstance,
    ) -> tuple[float, Solution]:
        """Evaluar fitness y retornar solucion completa.

        Returns:
            (fitness, Solution)
        """
        y, q = repair_lot_sizing(y, q, instance.capacity_min, instance.capacity_max)
        sol = decoder.decode(y, q, instance)
        bd = objective.evaluate_vectorized(sol, instance)
        self.n_evaluations += 1
        return bd.total, sol

    def generate_random(
        self, instance: ProblemInstance
    ) -> tuple[np.ndarray, np.ndarray]:
        """Generar solucion aleatoria factible.

        Returns:
            (y, q) factible.
        """
        return random_solution(instance)

    def update_best(
        self, fitness: float, sol: Solution, instance: ProblemInstance
    ) -> bool:
        """Actualizar mejor solucion si fitness mejora.

        Returns:
            True si se actualizo.
        """
        if fitness > self.best_fitness:
            self.best_fitness = fitness
            self.best_solution = sol
            return True
        return False

    def log_iteration(
        self,
        iteration: int,
        best_fitness: float,
        current_fitness: float,
        n_evaluations: Optional[int] = None,
        diversity: Optional[float] = None,
    ) -> None:
        """Registrar progreso de la iteracion actual."""
        elapsed = time.time() - self._start_time
        self.history.append(
            IterationLog(
                iteration=iteration,
                best_fitness=best_fitness,
                current_fitness=current_fitness,
                elapsed_seconds=elapsed,
                n_evaluations=(
                    self.n_evaluations if n_evaluations is None else n_evaluations
                ),
                diversity=diversity,
            )
        )

    def reset(self) -> None:
        """Resetear estado para nueva ejecucion."""
        self.history = []
        self.best_solution = None
        self.best_fitness = -np.inf
        self.n_evaluations = 0
        self._start_time = time.time()

    @property
    def name(self) -> str:
        """Nombre de la metaheuristica."""
        return self.__class__.__name__

    def convergence_data(self) -> tuple[list[int], list[float]]:
        """Datos para grafico de convergencia.

        Returns:
            (iteraciones, mejores_fitness)
        """
        iters = [log.iteration for log in self.history]
        best = [log.best_fitness for log in self.history]
        return iters, best

    def summary(self) -> str:
        """Resumen de la ejecucion."""
        elapsed = self.history[-1].elapsed_seconds if self.history else 0
        return (
            f"{self.name} Summary:\n"
            f"  Best Z: {self.best_fitness:,.0f}\n"
            f"  Evaluations: {self.n_evaluations:,}\n"
            f"  Iterations: {len(self.history)}\n"
            f"  Time: {elapsed:.2f}s\n"
            f"  Config: {self.config}"
        )
