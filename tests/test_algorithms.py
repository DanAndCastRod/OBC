"""
Tests Unitarios para el Framework de Metaheurísticas DLBP
=========================================================
Valida las clases base y los algoritmos implementados en src/algorithms/

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: 2 - Implementación Algorítmica
"""

import sys
import os
import unittest

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'algorithms'))

from base import ProblemInstance, Solution, Optimizer
from genetic_algorithm import GeneticAlgorithm, GAConfig
from tabu_search import TabuSearch, TSConfig
from hybrid import HybridAlgorithm, HybridConfig


def crear_instancia_test():
    """Crea una instancia de prueba de 11 tareas (sin dependencia de pulp)."""
    return ProblemInstance(
        tareas=[
            "T01_Colgado", "T02_Evisceracion", "T03_SepararCabezaPatas",
            "T04_Chiller", "T05_Seleccion", "T06_AreaDespresado",
            "T07_CortarPernil", "T08_Contramuslo", "T09_Muslo",
            "T10_DeshuesarMuslo", "T11_FiletearMuslo"
        ],
        tiempos={
            "T01_Colgado": 5, "T02_Evisceracion": 20, "T03_SepararCabezaPatas": 12,
            "T04_Chiller": 8, "T05_Seleccion": 6, "T06_AreaDespresado": 4,
            "T07_CortarPernil": 15, "T08_Contramuslo": 10, "T09_Muslo": 10,
            "T10_DeshuesarMuslo": 18, "T11_FiletearMuslo": 12
        },
        precedencias={
            "T01_Colgado": [], "T02_Evisceracion": ["T01_Colgado"],
            "T03_SepararCabezaPatas": ["T02_Evisceracion"],
            "T04_Chiller": ["T03_SepararCabezaPatas"],
            "T05_Seleccion": ["T04_Chiller"],
            "T06_AreaDespresado": ["T05_Seleccion"],
            "T07_CortarPernil": ["T06_AreaDespresado"],
            "T08_Contramuslo": ["T07_CortarPernil"],
            "T09_Muslo": ["T07_CortarPernil"],
            "T10_DeshuesarMuslo": ["T09_Muslo"],
            "T11_FiletearMuslo": ["T10_DeshuesarMuslo"]
        },
        tiempo_ciclo=40
    )


class TestProblemInstance(unittest.TestCase):
    """Tests para la clase ProblemInstance."""
    
    def setUp(self):
        """Crea una instancia pequeña para tests."""
        self.instancia = ProblemInstance(
            tareas=["T1", "T2", "T3", "T4"],
            tiempos={"T1": 10, "T2": 15, "T3": 20, "T4": 10},
            precedencias={"T1": [], "T2": ["T1"], "T3": ["T1"], "T4": ["T2", "T3"]},
            tiempo_ciclo=30
        )
    
    def test_n_tareas(self):
        """Verifica el conteo de tareas."""
        self.assertEqual(self.instancia.n_tareas, 4)
    
    def test_tiempo_total(self):
        """Verifica el cálculo del tiempo total."""
        self.assertEqual(self.instancia.tiempo_total, 55)
    
    def test_precedencia_valida(self):
        """Verifica validación de precedencias correctas."""
        orden_valido = ["T1", "T2", "T3", "T4"]
        self.assertTrue(self.instancia.es_precedencia_valida(orden_valido))
    
    def test_precedencia_invalida(self):
        """Verifica detección de precedencias violadas."""
        orden_invalido = ["T4", "T2", "T3", "T1"]  # T4 antes de T1
        self.assertFalse(self.instancia.es_precedencia_valida(orden_invalido))


class TestSolution(unittest.TestCase):
    """Tests para la clase Solution."""
    
    def setUp(self):
        """Crea instancia y solución de prueba."""
        self.instancia = ProblemInstance(
            tareas=["T1", "T2", "T3", "T4"],
            tiempos={"T1": 10, "T2": 15, "T3": 20, "T4": 10},
            precedencias={"T1": [], "T2": ["T1"], "T3": ["T1"], "T4": ["T2", "T3"]},
            tiempo_ciclo=30
        )
        self.cromosoma = ["T1", "T2", "T3", "T4"]
    
    def test_decodificacion(self):
        """Verifica que la decodificación asigna tareas a estaciones."""
        sol = Solution(cromosoma=self.cromosoma, instancia=self.instancia)
        self.assertGreater(sol.n_estaciones, 0)
        self.assertTrue(len(sol.asignacion) > 0)
    
    def test_factibilidad(self):
        """Verifica que soluciones válidas se marcan como factibles."""
        sol = Solution(cromosoma=self.cromosoma, instancia=self.instancia)
        self.assertTrue(sol.es_factible)
    
    def test_fitness_estaciones(self):
        """Verifica cálculo de fitness por estaciones."""
        sol = Solution(cromosoma=self.cromosoma, instancia=self.instancia)
        fitness = sol.calcular_fitness(tipo="estaciones")
        self.assertEqual(fitness, sol.n_estaciones)
    
    def test_clonacion(self):
        """Verifica que la clonación crea una copia independiente."""
        sol_original = Solution(cromosoma=self.cromosoma, instancia=self.instancia)
        sol_clon = sol_original.clonar()
        sol_clon.cromosoma[0] = "MODIFICADO"
        self.assertNotEqual(sol_original.cromosoma[0], sol_clon.cromosoma[0])


class TestGeneticAlgorithm(unittest.TestCase):
    """Tests para el Algoritmo Genético."""
    
    def setUp(self):
        """Carga instancia completa para GA."""
        self.instancia = crear_instancia_test()
    
    def test_inicializacion(self):
        """Verifica que GA se inicializa correctamente."""
        ga = GeneticAlgorithm(self.instancia)
        self.assertIsNotNone(ga.instancia)
        self.assertIsNotNone(ga.config)
    
    def test_solucion_inicial(self):
        """Verifica generación de solución inicial factible."""
        ga = GeneticAlgorithm(self.instancia)
        sol = ga.generar_solucion_inicial()
        self.assertTrue(sol.es_factible)
    
    def test_optimizacion_basica(self):
        """Verifica que GA ejecuta sin errores."""
        config = GAConfig(max_generaciones=10, poblacion_size=10)
        ga = GeneticAlgorithm(self.instancia, config=config, seed=42)
        resultado = ga.optimizar(max_iter=10, verbose=False)
        self.assertIsNotNone(resultado)
        self.assertTrue(resultado.es_factible)


class TestTabuSearch(unittest.TestCase):
    """Tests para Búsqueda Tabú."""
    
    def setUp(self):
        """Carga instancia completa para TS."""
        self.instancia = crear_instancia_test()
    
    def test_inicializacion(self):
        """Verifica que TS se inicializa correctamente."""
        ts = TabuSearch(self.instancia)
        self.assertIsNotNone(ts.instancia)
        self.assertIsNotNone(ts.config)
    
    def test_solucion_inicial(self):
        """Verifica generación de solución inicial factible."""
        ts = TabuSearch(self.instancia)
        sol = ts.generar_solucion_inicial()
        self.assertTrue(sol.es_factible)
    
    def test_optimizacion_basica(self):
        """Verifica que TS ejecuta sin errores."""
        config = TSConfig(max_iteraciones=20)
        ts = TabuSearch(self.instancia, config=config, seed=42)
        resultado = ts.optimizar(max_iter=20, verbose=False)
        self.assertIsNotNone(resultado)
        self.assertTrue(resultado.es_factible)


class TestHybridAlgorithm(unittest.TestCase):
    """Tests para Algoritmo Híbrido."""
    
    def setUp(self):
        """Carga instancia completa para Híbrido."""
        self.instancia = crear_instancia_test()
    
    def test_inicializacion(self):
        """Verifica que Híbrido se inicializa correctamente."""
        hybrid = HybridAlgorithm(self.instancia)
        self.assertIsNotNone(hybrid.instancia)
    
    def test_optimizacion_basica(self):
        """Verifica que Híbrido ejecuta sin errores."""
        config = HybridConfig(generaciones_ga=10, poblacion_size=10, aplicar_ts_cada=5)
        hybrid = HybridAlgorithm(self.instancia, config=config, seed=42)
        resultado = hybrid.optimizar(max_iter=10, verbose=False)
        self.assertIsNotNone(resultado)
        self.assertTrue(resultado.es_factible)


class TestIntegracion(unittest.TestCase):
    """Tests de integración entre componentes."""
    
    def setUp(self):
        """Carga instancia demo."""
        self.instancia = crear_instancia_test()
    
    def test_comparacion_algoritmos(self):
        """Verifica que todos los algoritmos producen soluciones comparables."""
        # Ejecutar cada algoritmo con pocas iteraciones
        ga = GeneticAlgorithm(self.instancia, seed=42)
        ts = TabuSearch(self.instancia, seed=42)
        hybrid = HybridAlgorithm(self.instancia, seed=42)
        
        sol_ga = ga.optimizar(max_iter=10, verbose=False)
        sol_ts = ts.optimizar(max_iter=20, verbose=False)
        sol_hybrid = hybrid.optimizar(max_iter=10, verbose=False)
        
        # Todas deben ser factibles
        self.assertTrue(sol_ga.es_factible)
        self.assertTrue(sol_ts.es_factible)
        self.assertTrue(sol_hybrid.es_factible)
        
        # El número de estaciones debe ser razonable (entre 3 y 15 para 11 tareas)
        for sol in [sol_ga, sol_ts, sol_hybrid]:
            self.assertGreaterEqual(sol.n_estaciones, 3)
            self.assertLessEqual(sol.n_estaciones, 15)


class TestEdgeCases(unittest.TestCase):
    """Tests para casos límite y condiciones extremas."""
    
    def test_instancia_una_tarea(self):
        """Verifica comportamiento con una sola tarea."""
        instancia = ProblemInstance(
            tareas=["T1"],
            tiempos={"T1": 10},
            precedencias={"T1": []},
            tiempo_ciclo=30
        )
        
        ga = GeneticAlgorithm(instancia, seed=42)
        sol = ga.generar_solucion_inicial()
        
        self.assertEqual(sol.n_estaciones, 1)
        self.assertTrue(sol.es_factible)
    
    def test_instancia_sin_precedencias(self):
        """Verifica instancia donde ninguna tarea tiene predecesoras."""
        instancia = ProblemInstance(
            tareas=["T1", "T2", "T3", "T4"],
            tiempos={"T1": 10, "T2": 10, "T3": 10, "T4": 10},
            precedencias={"T1": [], "T2": [], "T3": [], "T4": []},
            tiempo_ciclo=30
        )
        
        ga = GeneticAlgorithm(instancia, seed=42)
        sol = ga.generar_solucion_inicial()
        
        self.assertTrue(sol.es_factible)
        self.assertGreater(sol.n_estaciones, 0)
    
    def test_tiempos_iguales(self):
        """Verifica instancia donde todas las tareas tienen el mismo tiempo."""
        instancia = ProblemInstance(
            tareas=["T1", "T2", "T3", "T4", "T5"],
            tiempos={"T1": 10, "T2": 10, "T3": 10, "T4": 10, "T5": 10},
            precedencias={
                "T1": [], "T2": ["T1"], "T3": ["T2"], 
                "T4": ["T3"], "T5": ["T4"]
            },
            tiempo_ciclo=25
        )
        
        ga = GeneticAlgorithm(instancia, seed=42)
        resultado = ga.generar_solucion_inicial()
        
        self.assertTrue(resultado.es_factible)
        # Con tiempo_ciclo=25 y tareas de 10s, caben 2 por estación
        self.assertLessEqual(resultado.n_estaciones, 3)
    
    def test_tiempo_ciclo_muy_grande(self):
        """Verifica instancia donde tiempo de ciclo permite todo en 1 estación."""
        instancia = ProblemInstance(
            tareas=["T1", "T2", "T3"],
            tiempos={"T1": 10, "T2": 10, "T3": 10},
            precedencias={"T1": [], "T2": ["T1"], "T3": ["T2"]},
            tiempo_ciclo=100  # Muy grande
        )
        
        ga = GeneticAlgorithm(instancia, seed=42)
        resultado = ga.generar_solucion_inicial()
        
        self.assertTrue(resultado.es_factible)
        self.assertEqual(resultado.n_estaciones, 1)
    
    def test_tiempo_ciclo_muy_pequeno(self):
        """Verifica instancia donde cada tarea ocupa una estación."""
        instancia = ProblemInstance(
            tareas=["T1", "T2", "T3"],
            tiempos={"T1": 10, "T2": 15, "T3": 20},
            precedencias={"T1": [], "T2": ["T1"], "T3": ["T2"]},
            tiempo_ciclo=20  # Solo cabe una tarea por estación
        )
        
        ga = GeneticAlgorithm(instancia, seed=42)
        resultado = ga.generar_solucion_inicial()
        
        self.assertTrue(resultado.es_factible)
        self.assertEqual(resultado.n_estaciones, 3)  # Una por tarea


if __name__ == "__main__":
    print("=" * 60)
    print("DLBP Avícola - Tests Unitarios Fase 2")
    print("=" * 60)
    
    # Ejecutar con verbosidad
    unittest.main(verbosity=2)
