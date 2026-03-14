"""
Tests Unitarios para Módulos de Modelos DLBP
=============================================
Valida los módulos en src/models/

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: Mejoras - Ampliación de Tests
"""

import sys
import os
import unittest

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'algorithms'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'models'))

from base import ProblemInstance, Solution


def crear_instancia_pequena():
    """Crea una instancia pequeña para tests rápidos."""
    return ProblemInstance(
        tareas=["T1", "T2", "T3", "T4", "T5"],
        tiempos={"T1": 10, "T2": 15, "T3": 20, "T4": 10, "T5": 8},
        precedencias={
            "T1": [],
            "T2": ["T1"],
            "T3": ["T1"],
            "T4": ["T2", "T3"],
            "T5": ["T4"]
        },
        tiempo_ciclo=30
    )


class TestDLBPCompleto(unittest.TestCase):
    """Tests para el módulo dlbp_completo.py"""
    
    def test_importar_crear_instancia(self):
        """Verifica que la función crear_instancia_completa existe."""
        try:
            from dlbp_completo import crear_instancia_completa
            self.assertTrue(callable(crear_instancia_completa))
        except ImportError:
            self.skipTest("pulp no instalado - saltando test MILP")
    
    def test_crear_instancia_completa_estructura(self):
        """Verifica estructura de la instancia completa."""
        try:
            from dlbp_completo import crear_instancia_completa
            datos = crear_instancia_completa()
            
            # Debe tener las claves requeridas
            self.assertIn("tareas", datos)
            self.assertIn("tiempos", datos)
            self.assertIn("precedencias", datos)
            self.assertIn("tiempo_ciclo", datos)
            
            # Debe tener al menos 10 tareas (modelo avícola)
            self.assertGreaterEqual(len(datos["tareas"]), 10)
            
        except ImportError:
            self.skipTest("pulp no instalado - saltando test MILP")
    
    def test_tiempos_positivos(self):
        """Verifica que todos los tiempos sean positivos."""
        try:
            from dlbp_completo import crear_instancia_completa
            datos = crear_instancia_completa()
            
            for tarea, tiempo in datos["tiempos"].items():
                self.assertGreater(tiempo, 0, f"Tiempo de {tarea} debe ser positivo")
                
        except ImportError:
            self.skipTest("pulp no instalado - saltando test MILP")


class TestMILPValidation(unittest.TestCase):
    """Tests para el módulo milp_validation.py"""
    
    def test_importar_modulo(self):
        """Verifica que el módulo puede importarse."""
        try:
            import milp_validation
            self.assertTrue(hasattr(milp_validation, '__file__'))
        except ImportError:
            self.skipTest("pulp no instalado - saltando test MILP")


class TestDLBPProfit(unittest.TestCase):
    """Tests para el módulo dlbp_profit.py (modelo con beneficio)."""
    
    def test_importar_modulo(self):
        """Verifica que el módulo puede importarse."""
        try:
            import dlbp_profit
            self.assertTrue(hasattr(dlbp_profit, '__file__'))
        except ImportError:
            self.skipTest("pulp no instalado - saltando test")


class TestStochasticDLBP(unittest.TestCase):
    """Tests para el módulo stochastic_dlbp.py"""
    
    def test_importar_modulo(self):
        """Verifica que el módulo puede importarse."""
        try:
            import stochastic_dlbp
            self.assertTrue(hasattr(stochastic_dlbp, '__file__'))
        except ImportError:
            self.skipTest("Dependencias no instaladas")


class TestProblemInstanceValidation(unittest.TestCase):
    """Tests de validación de instancias del problema."""
    
    def test_instancia_sin_tareas_vacias(self):
        """Verifica que la instancia tiene tareas."""
        inst = crear_instancia_pequena()
        self.assertGreater(inst.n_tareas, 0)
    
    def test_tiempo_total_correcto(self):
        """Verifica cálculo del tiempo total."""
        inst = crear_instancia_pequena()
        expected = 10 + 15 + 20 + 10 + 8  # 63
        self.assertEqual(inst.tiempo_total, expected)
    
    def test_precedencias_sin_ciclos(self):
        """Verifica que las precedencias no forman ciclos."""
        inst = crear_instancia_pequena()
        
        # Simular ordenamiento topológico
        grado = {t: len(inst.precedencias.get(t, [])) for t in inst.tareas}
        disponibles = [t for t in inst.tareas if grado[t] == 0]
        orden = []
        
        while disponibles:
            t = disponibles.pop(0)
            orden.append(t)
            for sucesor in inst.sucesores.get(t, []):
                grado[sucesor] -= 1
                if grado[sucesor] == 0:
                    disponibles.append(sucesor)
        
        # Si no hay ciclos, orden debe tener todas las tareas
        self.assertEqual(len(orden), inst.n_tareas)
    
    def test_estaciones_minimas_teoricas(self):
        """Verifica cálculo de estaciones mínimas teóricas."""
        inst = crear_instancia_pequena()
        min_teorico = inst.tiempo_total / inst.tiempo_ciclo
        
        # Mínimo teórico = ceil(63/30) = 3
        import math
        self.assertEqual(math.ceil(min_teorico), 3)


class TestSolutionValidation(unittest.TestCase):
    """Tests adicionales para validación de soluciones."""
    
    def setUp(self):
        self.instancia = crear_instancia_pequena()
    
    def test_solucion_respeta_precedencias(self):
        """Verifica que todas las precedencias se respetan."""
        cromosoma = ["T1", "T2", "T3", "T4", "T5"]
        sol = Solution(cromosoma=cromosoma, instancia=self.instancia)
        self.assertTrue(sol.es_factible)
    
    def test_solucion_viola_precedencias(self):
        """Verifica detección de violación de precedencias."""
        # T5 debe ir después de T4, pero aquí va primero
        cromosoma = ["T5", "T4", "T3", "T2", "T1"]
        sol = Solution(cromosoma=cromosoma, instancia=self.instancia)
        # Debería detectar que no es factible
        self.assertFalse(sol.es_factible)
    
    def test_tiempos_estacion_no_exceden_ciclo(self):
        """Verifica que ninguna estación excede el tiempo de ciclo."""
        cromosoma = ["T1", "T2", "T3", "T4", "T5"]
        sol = Solution(cromosoma=cromosoma, instancia=self.instancia)
        
        for est, tiempo in sol.tiempos_estacion.items():
            self.assertLessEqual(tiempo, self.instancia.tiempo_ciclo,
                                f"Estación {est} excede tiempo de ciclo")
    
    def test_eficiencia_en_rango_valido(self):
        """Verifica que la eficiencia está entre 0% y 100%."""
        cromosoma = ["T1", "T2", "T3", "T4", "T5"]
        sol = Solution(cromosoma=cromosoma, instancia=self.instancia)
        sol.calcular_fitness(tipo="eficiencia")
        
        self.assertGreaterEqual(sol.fitness, 0)
        self.assertLessEqual(sol.fitness, 100)


if __name__ == "__main__":
    print("=" * 60)
    print("DLBP Avícola - Tests de Módulos (models/)")
    print("=" * 60)
    unittest.main(verbosity=2)
