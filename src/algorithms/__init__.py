# Módulo de algoritmos para DLBP Avícola
# Extensiones de Fase 5 incluidas

from .base import ProblemInstance, Solution, Optimizer, cargar_instancia_demo
from .genetic_algorithm import GeneticAlgorithm, GAConfig
from .tabu_search import TabuSearch
from .hybrid import HybridAlgorithm, HybridConfig

# Extensiones Fase 5
from .nsga2 import NSGA2, NSGA2Config, MultiObjectiveSolution
from .parallel import (
    ParallelEvaluator, 
    ParallelExperimentRunner, 
    ParallelNeighborhoodGenerator
)

__all__ = [
    # Base
    'ProblemInstance',
    'Solution', 
    'Optimizer',
    'cargar_instancia_demo',
    # Algoritmos principales
    'GeneticAlgorithm',
    'GAConfig',
    'TabuSearch',
    'HybridAlgorithm',
    'HybridConfig',
    # Extensiones Fase 5
    'NSGA2',
    'NSGA2Config',
    'MultiObjectiveSolution',
    'ParallelEvaluator',
    'ParallelExperimentRunner',
    'ParallelNeighborhoodGenerator',
]
