"""Modelo de optimizacion de coproductos avicolas."""

from src.model import constraints, decoder, objective
from src.model.parameters import ExclusivityGroup, ProblemInstance
from src.model.solution import Solution, SolutionBreakdown

__all__ = [
    "ProblemInstance",
    "ExclusivityGroup",
    "Solution",
    "SolutionBreakdown",
    "constraints",
    "decoder",
    "objective",
]
