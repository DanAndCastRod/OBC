"""
Tests Unitarios para Módulos de Experimentos
=============================================
Valida los módulos en src/experiments/

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: Mejoras - Ampliación de Tests
"""

import sys
import os
import unittest
import json
import tempfile

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'experiments'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'algorithms'))

from base import ProblemInstance
from generar_instancias import (
    InstanceSpec,
    generar_precedencias_aleatorias,
    generar_tiempos_aleatorios,
    generar_instancia,
    generar_conjunto_instancias,
    exportar_instancia
)
import numpy as np


class TestInstanceSpec(unittest.TestCase):
    """Tests para la clase InstanceSpec."""
    
    def test_crear_spec_valido(self):
        """Verifica creación de especificación válida."""
        spec = InstanceSpec(
            nombre="test_instance",
            n_tareas=10,
            n_areas=2,
            tiempo_ciclo=30,
            tiempo_min=5,
            tiempo_max=15,
            densidad_precedencias=0.3
        )
        self.assertEqual(spec.nombre, "test_instance")
        self.assertEqual(spec.n_tareas, 10)
    
    def test_spec_atributos_completos(self):
        """Verifica que todos los atributos están presentes."""
        spec = InstanceSpec(
            nombre="test",
            n_tareas=20,
            n_areas=4,
            tiempo_ciclo=40,
            tiempo_min=3,
            tiempo_max=15,
            densidad_precedencias=0.25
        )
        self.assertTrue(hasattr(spec, 'nombre'))
        self.assertTrue(hasattr(spec, 'n_tareas'))
        self.assertTrue(hasattr(spec, 'n_areas'))
        self.assertTrue(hasattr(spec, 'tiempo_ciclo'))
        self.assertTrue(hasattr(spec, 'tiempo_min'))
        self.assertTrue(hasattr(spec, 'tiempo_max'))
        self.assertTrue(hasattr(spec, 'densidad_precedencias'))


class TestGeneradorPrecedencias(unittest.TestCase):
    """Tests para la función generar_precedencias_aleatorias."""
    
    def test_genera_dict_para_todas_tareas(self):
        """Verifica que genera precedencias para todas las tareas."""
        rng = np.random.default_rng(42)
        precs = generar_precedencias_aleatorias(
            n_tareas=10,
            n_areas=2,
            densidad=0.3,
            rng=rng
        )
        
        self.assertEqual(len(precs), 10)
        for i in range(10):
            self.assertIn(f"T{i:03d}", precs)
    
    def test_primera_tarea_sin_predecesoras(self):
        """Verifica que la primera tarea no tiene predecesoras."""
        rng = np.random.default_rng(42)
        precs = generar_precedencias_aleatorias(
            n_tareas=10,
            n_areas=2,
            densidad=0.0,  # Sin densidad adicional
            rng=rng
        )
        
        self.assertEqual(len(precs["T000"]), 0)
    
    def test_grafo_sin_ciclos(self):
        """Verifica que el grafo de precedencias no tiene ciclos."""
        rng = np.random.default_rng(42)
        precs = generar_precedencias_aleatorias(
            n_tareas=20,
            n_areas=4,
            densidad=0.5,
            rng=rng
        )
        
        # Verificar mediante ordenamiento topológico
        tareas = [f"T{i:03d}" for i in range(20)]
        grado = {t: len(precs.get(t, [])) for t in tareas}
        disponibles = [t for t in tareas if grado[t] == 0]
        orden = []
        
        while disponibles:
            t = disponibles.pop(0)
            orden.append(t)
            for sucesor in tareas:
                if t in precs.get(sucesor, []):
                    grado[sucesor] -= 1
                    if grado[sucesor] == 0:
                        disponibles.append(sucesor)
        
        # Si no hay ciclos, orden == n_tareas
        self.assertEqual(len(orden), 20, "Grafo tiene ciclos")


class TestGeneradorTiempos(unittest.TestCase):
    """Tests para la función generar_tiempos_aleatorios."""
    
    def test_genera_tiempos_para_todas_tareas(self):
        """Verifica que genera tiempos para todas las tareas."""
        tareas = ["T1", "T2", "T3", "T4", "T5"]
        rng = np.random.default_rng(42)
        
        tiempos = generar_tiempos_aleatorios(
            tareas=tareas,
            tiempo_min=5,
            tiempo_max=20,
            rng=rng
        )
        
        self.assertEqual(len(tiempos), 5)
        for t in tareas:
            self.assertIn(t, tiempos)
    
    def test_tiempos_en_rango(self):
        """Verifica que los tiempos están dentro del rango especificado."""
        tareas = [f"T{i}" for i in range(100)]
        rng = np.random.default_rng(42)
        
        tiempos = generar_tiempos_aleatorios(
            tareas=tareas,
            tiempo_min=5,
            tiempo_max=20,
            rng=rng
        )
        
        for t, tiempo in tiempos.items():
            self.assertGreaterEqual(tiempo, 5, f"{t} tiene tiempo < min")
            self.assertLessEqual(tiempo, 20, f"{t} tiene tiempo > max")


class TestGenerarInstancia(unittest.TestCase):
    """Tests para la función generar_instancia."""
    
    def test_genera_instancia_valida(self):
        """Verifica que genera una instancia ProblemInstance válida."""
        spec = InstanceSpec(
            nombre="test_pequena",
            n_tareas=10,
            n_areas=2,
            tiempo_ciclo=30,
            tiempo_min=5,
            tiempo_max=15,
            densidad_precedencias=0.2
        )
        
        instancia = generar_instancia(spec, semilla=42)
        
        self.assertIsInstance(instancia, ProblemInstance)
        self.assertEqual(instancia.n_tareas, 10)
        self.assertEqual(instancia.tiempo_ciclo, 30)
    
    def test_instancia_reproducible(self):
        """Verifica que la misma semilla produce la misma instancia."""
        spec = InstanceSpec(
            nombre="test",
            n_tareas=15,
            n_areas=3,
            tiempo_ciclo=35,
            tiempo_min=5,
            tiempo_max=18,
            densidad_precedencias=0.25
        )
        
        inst1 = generar_instancia(spec, semilla=123)
        inst2 = generar_instancia(spec, semilla=123)
        
        self.assertEqual(inst1.tiempos, inst2.tiempos)
        self.assertEqual(inst1.precedencias, inst2.precedencias)
    
    def test_diferentes_semillas_diferentes_instancias(self):
        """Verifica que diferentes semillas producen diferentes instancias."""
        spec = InstanceSpec(
            nombre="test",
            n_tareas=20,
            n_areas=4,
            tiempo_ciclo=40,
            tiempo_min=3,
            tiempo_max=15,
            densidad_precedencias=0.3
        )
        
        inst1 = generar_instancia(spec, semilla=100)
        inst2 = generar_instancia(spec, semilla=200)
        
        # Probablemente diferentes tiempos
        self.assertNotEqual(inst1.tiempos, inst2.tiempos)


class TestGenerarConjuntoInstancias(unittest.TestCase):
    """Tests para la función generar_conjunto_instancias."""
    
    def test_genera_cuatro_instancias(self):
        """Verifica que genera el conjunto completo de 4 instancias."""
        instancias = generar_conjunto_instancias()
        
        self.assertEqual(len(instancias), 4)
        self.assertIn("pequeña_20t", instancias)
        self.assertIn("mediana_40t", instancias)
        self.assertIn("grande_70t", instancias)
        self.assertIn("muy_grande_100t", instancias)
    
    def test_tamanos_correctos(self):
        """Verifica que cada instancia tiene el tamaño correcto."""
        instancias = generar_conjunto_instancias()
        
        self.assertEqual(instancias["pequeña_20t"].n_tareas, 20)
        self.assertEqual(instancias["mediana_40t"].n_tareas, 40)
        self.assertEqual(instancias["grande_70t"].n_tareas, 70)
        self.assertEqual(instancias["muy_grande_100t"].n_tareas, 100)


class TestExportarInstancia(unittest.TestCase):
    """Tests para la función exportar_instancia."""
    
    def test_exportar_json_valido(self):
        """Verifica que exporta un archivo JSON válido."""
        spec = InstanceSpec(
            nombre="test_export",
            n_tareas=5,
            n_areas=1,
            tiempo_ciclo=25,
            tiempo_min=5,
            tiempo_max=10,
            densidad_precedencias=0.1
        )
        instancia = generar_instancia(spec, semilla=42)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            path = exportar_instancia(instancia, "test_export", tmpdir)
            
            self.assertTrue(os.path.exists(path))
            
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.assertEqual(data["nombre"], "test_export")
            self.assertEqual(data["n_tareas"], 5)
    
    def test_json_contiene_campos_requeridos(self):
        """Verifica que el JSON tiene todos los campos necesarios."""
        spec = InstanceSpec(
            nombre="complete_test",
            n_tareas=8,
            n_areas=2,
            tiempo_ciclo=30,
            tiempo_min=5,
            tiempo_max=12,
            densidad_precedencias=0.2
        )
        instancia = generar_instancia(spec, semilla=42)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            path = exportar_instancia(instancia, "complete_test", tmpdir)
            
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            campos_requeridos = ["nombre", "n_tareas", "tiempo_ciclo", 
                                 "tiempo_total", "tareas", "tiempos", "precedencias"]
            for campo in campos_requeridos:
                self.assertIn(campo, data, f"Falta campo: {campo}")


if __name__ == "__main__":
    print("=" * 60)
    print("DLBP Avícola - Tests de Experimentos (experiments/)")
    print("=" * 60)
    unittest.main(verbosity=2)
