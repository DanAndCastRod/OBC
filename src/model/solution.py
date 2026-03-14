"""
Solution: Estructura de datos para una solucion del problema de
optimizacion de coproductos avicolas.

Coherente con DD-07 (cromosoma de 2 vectores + decoder greedy).

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 1.2
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

import numpy as np

if TYPE_CHECKING:
    from src.model.parameters import ProblemInstance


@dataclass
class SolutionBreakdown:
    """Desglose de la funcion objetivo por componente."""

    revenue: float = 0.0  # Ingresos por ventas
    prod_cost: float = 0.0  # Costo de produccion
    setup_cost: float = 0.0  # Costo de setup
    inv_cost: float = 0.0  # Costo de inventario
    pen_cost: float = 0.0  # Penalizacion por insatisfaccion

    @property
    def total(self) -> float:
        """Z = revenue - prod_cost - setup_cost - inv_cost - pen_cost"""
        return (
            self.revenue
            - self.prod_cost
            - self.setup_cost
            - self.inv_cost
            - self.pen_cost
        )

    def __repr__(self) -> str:
        return (
            f"Breakdown(Z={self.total:,.0f}, rev={self.revenue:,.0f}, "
            f"prod={self.prod_cost:,.0f}, setup={self.setup_cost:,.0f}, "
            f"inv={self.inv_cost:,.0f}, pen={self.pen_cost:,.0f})"
        )


@dataclass
class Solution:
    """Solucion del problema de optimizacion de coproductos.

    Primera etapa (variables de decision directas):
    - y[t]: setup binario por periodo
    - q[t]: cantidad de carcasas por periodo

    Segunda etapa (calculadas por el decoder greedy, por escenario):
    - v[f, t, w]: ventas por forma de corte, periodo, escenario
    - I[f, t, w]: inventario
    - u[f, t, w]: demanda insatisfecha
    """

    # --- Primera etapa ---
    y: np.ndarray = field(default_factory=lambda: np.array([]))  # bool [T]
    q: np.ndarray = field(default_factory=lambda: np.array([]))  # int  [T]

    # --- Segunda etapa (por escenario) ---
    p: Optional[np.ndarray] = (
        None  # float [F, T] produccion por forma (1ra etapa extendida)
    )
    v: Optional[np.ndarray] = None  # float [F, T, W]  ventas
    I: Optional[np.ndarray] = None  # float [F, T, W]  inventario
    u: Optional[np.ndarray] = None  # float [F, T, W]  insatisfaccion
    z: Optional[np.ndarray] = None  # bool  [F, T] activacion de forma de corte

    # --- Valor objetivo ---
    objective_value: float = 0.0
    breakdown: SolutionBreakdown = field(default_factory=SolutionBreakdown)
    is_feasible: bool = False

    # --- Metadata ---
    algorithm: str = ""
    elapsed_seconds: float = 0.0
    n_evaluations: int = 0

    def check_feasibility(self, instance: ProblemInstance) -> list[str]:
        """Verificar factibilidad de la solucion contra una instancia.

        Args:
            instance: Instancia del problema.

        Returns:
            Lista de violaciones. Vacia si es factible.
        """
        violations = []

        # Setup-cantidad: si y[t]=0 entonces q[t] debe ser 0
        for t in range(len(self.y)):
            if not self.y[t] and self.q[t] > 0:
                violations.append(f"t={t}: y[t]=0 pero q[t]={self.q[t]} > 0")

        # Lote minimo: si y[t]=1, q[t] >= Q_min
        for t in range(len(self.y)):
            if self.y[t] and 0 < self.q[t] < instance.capacity_min:
                violations.append(
                    f"t={t}: q[t]={self.q[t]} < Q_min={instance.capacity_min}"
                )

        # Capacidad maxima
        for t in range(len(self.q)):
            if self.q[t] > instance.capacity_max:
                violations.append(
                    f"t={t}: q[t]={self.q[t]} > Q_max={instance.capacity_max}"
                )

        # No negativos en segunda etapa
        if self.p is not None and np.any(self.p < -1e-9):
            violations.append("Produccion por forma negativa detectada")
        if self.v is not None and np.any(self.v < -1e-9):
            violations.append("Ventas negativas detectadas")
        if self.I is not None and np.any(self.I < -1e-9):
            violations.append("Inventario negativo detectado")
        if self.u is not None and np.any(self.u < -1e-9):
            violations.append("Insatisfaccion negativa detectada")

        self.is_feasible = len(violations) == 0
        return violations

    @property
    def n_periods(self) -> int:
        """Numero de periodos en la solucion."""
        return len(self.y)

    @property
    def total_production(self) -> int:
        """Total de carcasas producidas."""
        return int(self.q.sum())

    @property
    def n_setups(self) -> int:
        """Numero de periodos con setup activo."""
        return int(self.y.sum())

    def summary(self) -> str:
        """Resumen legible de la solucion."""
        lines = [
            f"Solution ({self.algorithm})",
            f"  Z = {self.objective_value:,.0f} COP",
            f"  Factible: {self.is_feasible}",
            f"  Periodos: {self.n_periods}",
            f"  Setups: {self.n_setups} / {self.n_periods}",
            f"  Produccion total: {self.total_production:,} carcasas",
            f"  Tiempo: {self.elapsed_seconds:.2f}s",
        ]
        if self.breakdown.revenue > 0:
            lines.append(f"  {self.breakdown}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            f"Solution(alg='{self.algorithm}', Z={self.objective_value:,.0f}, "
            f"feasible={self.is_feasible}, T={self.n_periods})"
        )
