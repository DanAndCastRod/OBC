"""
Tests para las extensiones de Fase 5: NSGA-II y Paralelización
"""

import pytest
import sys
import os

# Agregar path del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from algorithms.base import ProblemInstance, Solution, cargar_instancia_demo
from algorithms.nsga2 import NSGA2, NSGA2Config, MultiObjectiveSolution
from algorithms.parallel import (
    ParallelEvaluator, 
    ParallelExperimentRunner, 
    ParallelNeighborhoodGenerator
)


# =============================================================================
# Tests NSGA-II
# =============================================================================

class TestNSGA2Config:
    """Tests para la configuración de NSGA-II."""
    
    def test_config_default(self):
        """Verifica valores por defecto de configuración."""
        config = NSGA2Config()
        assert config.poblacion_size == 100
        assert config.max_generaciones == 100
        assert config.prob_cruce == 0.9
        assert config.prob_mutacion == 0.1
        assert 'estaciones' in config.objetivos
        assert 'desbalance' in config.objetivos
    
    def test_config_custom(self):
        """Verifica configuración personalizada."""
        config = NSGA2Config(poblacion_size=50, max_generaciones=30)
        assert config.poblacion_size == 50
        assert config.max_generaciones == 30


class TestMultiObjectiveSolution:
    """Tests para soluciones multi-objetivo."""
    
    @pytest.fixture
    def instancia(self):
        return cargar_instancia_demo()
    
    @pytest.fixture
    def solucion(self, instancia):
        orden = list(instancia.tareas)
        return Solution(instancia=instancia, cromosoma=orden)
    
    def test_crear_mo_solution(self, solucion):
        """Verifica creación de solución multi-objetivo."""
        mo_sol = MultiObjectiveSolution(solucion=solucion)
        
        assert 'estaciones' in mo_sol.objetivos
        assert 'desbalance' in mo_sol.objetivos
        assert 'eficiencia' in mo_sol.objetivos
        assert mo_sol.rank == 0
        assert mo_sol.crowding_distance == 0.0
    
    def test_objetivos_son_numericos(self, solucion):
        """Verifica que los objetivos son valores numéricos válidos."""
        mo_sol = MultiObjectiveSolution(solucion=solucion)
        
        assert isinstance(mo_sol.objetivos['estaciones'], (int, float))
        assert isinstance(mo_sol.objetivos['desbalance'], float)
        assert isinstance(mo_sol.objetivos['eficiencia'], float)
        assert mo_sol.objetivos['estaciones'] >= 1
        assert mo_sol.objetivos['desbalance'] >= 0
    
    def test_dominancia(self, instancia):
        """Verifica lógica de dominancia de Pareto."""
        orden1 = list(instancia.tareas)
        orden2 = list(reversed(instancia.tareas))
        
        sol1 = Solution(instancia=instancia, cromosoma=orden1)
        sol2 = Solution(instancia=instancia, cromosoma=orden2)
        
        mo_sol1 = MultiObjectiveSolution(solucion=sol1)
        mo_sol2 = MultiObjectiveSolution(solucion=sol2)
        
        # Una de las dos debería dominar o ninguna
        dominancia1 = mo_sol1.domina(mo_sol2)
        dominancia2 = mo_sol2.domina(mo_sol1)
        
        # No pueden dominarse mutuamente
        assert not (dominancia1 and dominancia2)


class TestNSGA2Algorithm:
    """Tests para el algoritmo NSGA-II."""
    
    @pytest.fixture
    def instancia(self):
        return cargar_instancia_demo()
    
    def test_inicializacion(self, instancia):
        """Verifica inicialización del NSGA-II."""
        config = NSGA2Config(poblacion_size=20, max_generaciones=5)
        nsga2 = NSGA2(instancia, config, seed=42)
        
        assert nsga2.config.poblacion_size == 20
        assert len(nsga2.poblacion) == 0  # Aún no inicializada
    
    def test_inicializar_poblacion(self, instancia):
        """Verifica creación de población inicial."""
        config = NSGA2Config(poblacion_size=10)
        nsga2 = NSGA2(instancia, config, seed=42)
        nsga2.inicializar_poblacion()
        
        assert len(nsga2.poblacion) == 10
        assert all(isinstance(s, MultiObjectiveSolution) for s in nsga2.poblacion)
    
    def test_non_dominated_sort(self, instancia):
        """Verifica clasificación por dominancia."""
        config = NSGA2Config(poblacion_size=20)
        nsga2 = NSGA2(instancia, config, seed=42)
        nsga2.inicializar_poblacion()
        
        frentes = nsga2.non_dominated_sort(nsga2.poblacion)
        
        assert len(frentes) >= 1
        assert len(frentes[0]) >= 1  # Al menos una solución no dominada
    
    def test_optimizar_rapido(self, instancia):
        """Verifica ejecución rápida del algoritmo."""
        config = NSGA2Config(poblacion_size=10, max_generaciones=5)
        nsga2 = NSGA2(instancia, config, seed=42)
        
        frente = nsga2.optimizar(verbose=False)
        
        assert len(frente) >= 1
        assert all(isinstance(s, MultiObjectiveSolution) for s in frente)
    
    def test_mejor_compromiso(self, instancia):
        """Verifica obtención de mejor compromiso."""
        config = NSGA2Config(poblacion_size=10, max_generaciones=5)
        nsga2 = NSGA2(instancia, config, seed=42)
        nsga2.optimizar(verbose=False)
        
        mejor = nsga2.obtener_mejor_compromiso()
        
        assert mejor is not None
        assert isinstance(mejor, MultiObjectiveSolution)
        assert mejor.objetivos['estaciones'] >= 1


# =============================================================================
# Tests Paralelización
# =============================================================================

class TestParallelEvaluator:
    """Tests para el evaluador paralelo."""
    
    @pytest.fixture
    def instancia(self):
        return cargar_instancia_demo()
    
    @pytest.fixture
    def poblacion(self, instancia):
        import random
        random.seed(42)
        poblacion = []
        for _ in range(20):
            orden = list(instancia.tareas)
            random.shuffle(orden)
            sol = Solution(instancia=instancia, cromosoma=orden)
            poblacion.append(sol)
        return poblacion
    
    def test_crear_evaluator(self):
        """Verifica creación del evaluador."""
        evaluator = ParallelEvaluator(n_workers=2)
        assert evaluator.n_workers == 2
        assert not evaluator.use_threads
    
    def test_evaluar_poblacion(self, poblacion):
        """Verifica evaluación de población."""
        evaluator = ParallelEvaluator(n_workers=2, use_threads=True)
        fitnesses = evaluator.evaluar_poblacion(poblacion)
        
        assert len(fitnesses) == len(poblacion)
        assert all(isinstance(f, (int, float)) for f in fitnesses)
    
    def test_resultado_consistente(self, poblacion):
        """Verifica que resultados paralelos son consistentes con secuenciales."""
        evaluator = ParallelEvaluator(n_workers=2, use_threads=True)
        
        # Paralelo
        fitnesses_par = evaluator.evaluar_poblacion(poblacion)
        
        # Secuencial
        fitnesses_seq = [sol.calcular_fitness() for sol in poblacion]
        
        assert fitnesses_par == fitnesses_seq


class TestParallelNeighborhoodGenerator:
    """Tests para el generador de vecindarios paralelo."""
    
    @pytest.fixture
    def instancia(self):
        return cargar_instancia_demo()
    
    @pytest.fixture
    def solucion(self, instancia):
        orden = list(instancia.tareas)
        return Solution(instancia=instancia, cromosoma=orden)
    
    def test_crear_generator(self):
        """Verifica creación del generador."""
        gen = ParallelNeighborhoodGenerator(n_workers=2)
        assert gen.n_workers == 2
    
    def test_generar_vecindario(self, solucion):
        """Verifica generación de vecindario."""
        gen = ParallelNeighborhoodGenerator(n_workers=2)
        vecinos = gen.generar_vecindario(solucion, tamano=10, tipo_movimiento="swap")
        
        assert len(vecinos) == 10
        assert all(isinstance(v[0], Solution) for v in vecinos)
        assert all(isinstance(v[1], tuple) for v in vecinos)


# =============================================================================
# Test de integración
# =============================================================================

class TestIntegracionExtensiones:
    """Tests de integración para las extensiones."""
    
    def test_import_extensiones(self):
        """Verifica que las extensiones se pueden importar correctamente."""
        from algorithms import NSGA2, ParallelEvaluator
        
        assert NSGA2 is not None
        assert ParallelEvaluator is not None
    
    def test_nsga2_con_evaluacion_paralela(self):
        """Test conceptual: NSGA-II podría usar evaluación paralela."""
        instancia = cargar_instancia_demo()
        config = NSGA2Config(poblacion_size=10, max_generaciones=3)
        nsga2 = NSGA2(instancia, config, seed=42)
        
        # Inicializar y evaluar
        nsga2.inicializar_poblacion()
        
        # Las soluciones multi-objetivo ya tienen objetivos calculados
        assert all(s.objetivos for s in nsga2.poblacion)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
