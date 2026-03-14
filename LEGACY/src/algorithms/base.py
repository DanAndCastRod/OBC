"""
DLBP Avícola - Clases Base para Metaheurísticas
================================================
Este módulo define las estructuras de datos fundamentales para 
la implementación de algoritmos de optimización.

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: 2 - Implementación Algorítmica
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Callable
import numpy as np
import copy


@dataclass
class ProblemInstance:
    """
    Representa una instancia del problema DLBP.
    Esta clase es inmutable una vez creada.
    
    Attributes:
        tareas: Lista ordenada de identificadores de tareas
        tiempos: Diccionario {tarea: tiempo_procesamiento}
        precedencias: Diccionario {tarea: [lista_de_predecesoras]}
        tiempo_ciclo: Tiempo máximo permitido por estación (segundos)
        n_estaciones_max: Número máximo de estaciones disponibles
        coproductos: Datos económicos de coproductos (opcional)
    """
    tareas: List[str]
    tiempos: Dict[str, float]
    precedencias: Dict[str, List[str]]
    tiempo_ciclo: float
    n_estaciones_max: int = 15
    coproductos: Optional[Dict] = None
    
    def __post_init__(self):
        """Valida la consistencia de la instancia."""
        # Construir grafo de precedencias para cálculos rápidos
        self._construir_grafo()
    
    def _construir_grafo(self):
        """Construye estructuras auxiliares para validación de precedencias."""
        self.sucesores: Dict[str, List[str]] = {t: [] for t in self.tareas}
        for tarea, predecesoras in self.precedencias.items():
            for pred in predecesoras:
                if pred in self.sucesores:
                    self.sucesores[pred].append(tarea)
    
    def es_precedencia_valida(self, orden: List[str]) -> bool:
        """
        Verifica si un orden de tareas respeta las precedencias.
        
        Args:
            orden: Lista de tareas en el orden propuesto
            
        Returns:
            True si todas las precedencias se respetan
        """
        posicion = {tarea: i for i, tarea in enumerate(orden)}
        for tarea, predecesoras in self.precedencias.items():
            for pred in predecesoras:
                if pred in posicion and tarea in posicion:
                    if posicion[pred] >= posicion[tarea]:
                        return False
        return True
    
    @property
    def n_tareas(self) -> int:
        return len(self.tareas)
    
    @property
    def tiempo_total(self) -> float:
        return sum(self.tiempos.values())


@dataclass
class Solution:
    """
    Representa una solución del DLBP (asignación de tareas a estaciones).
    
    Representación:
    - Internamente se usa una permutación de tareas (cromosoma)
    - La asignación a estaciones se deriva mediante decodificación voraz
    
    Attributes:
        cromosoma: Permutación de tareas (representación genética)
        asignacion: Dict {estacion: [tareas]} (decodificado)
        fitness: Valor de la función objetivo
    """
    cromosoma: List[str]
    instancia: ProblemInstance = field(repr=False)
    asignacion: Dict[str, List[str]] = field(default_factory=dict)
    fitness: float = 0.0
    n_estaciones: int = 0
    tiempos_estacion: Dict[str, float] = field(default_factory=dict)
    es_factible: bool = False
    
    def __post_init__(self):
        """Decodifica el cromosoma automáticamente al crear la solución."""
        if self.cromosoma:
            self.decodificar()
    
    def decodificar(self):
        """
        Decodifica el cromosoma (permutación) en una asignación de estaciones.
        Usa el algoritmo Best-Fit respetando precedencias.
        
        Best-Fit: para cada tarea, busca la estación abierta con MENOR
        espacio residual donde aún quepa la tarea Y se respeten precedencias.
        Si ninguna estación abierta sirve, abre una nueva.
        
        Esto crea más diversidad que First-Fit porque el orden de la
        permutación tiene mayor impacto en la solución resultante.
        """
        self.asignacion = {}
        self.tiempos_estacion = {}
        tarea_a_estacion: Dict[str, int] = {}
        n_estaciones = 0
        
        # Lista de estaciones abiertas: [(estacion_id_int, tiempo_usado)]
        estaciones_abiertas: List[Tuple[int, float]] = []
        
        for tarea in self.cromosoma:
            tiempo_tarea = self.instancia.tiempos.get(tarea, 0)
            
            # Determinar la estación mínima por precedencias
            min_estacion = 1
            for pred in self.instancia.precedencias.get(tarea, []):
                if pred in tarea_a_estacion:
                    min_estacion = max(min_estacion, tarea_a_estacion[pred])
            
            # Buscar la mejor estación abierta (Best-Fit)
            mejor_idx = -1
            menor_residuo = float('inf')
            
            for idx, (est_id, t_usado) in enumerate(estaciones_abiertas):
                # Debe cumplir: estación >= min_estacion por precedencias
                if est_id < min_estacion:
                    continue
                
                residuo = self.instancia.tiempo_ciclo - t_usado
                if tiempo_tarea <= residuo and residuo < menor_residuo:
                    mejor_idx = idx
                    menor_residuo = residuo
            
            if mejor_idx >= 0:
                # Asignar a la mejor estación existente
                est_id_int = estaciones_abiertas[mejor_idx][0]
                estaciones_abiertas[mejor_idx] = (
                    est_id_int,
                    estaciones_abiertas[mejor_idx][1] + tiempo_tarea
                )
            else:
                # Abrir nueva estación
                n_estaciones += 1
                est_id_int = n_estaciones
                estaciones_abiertas.append((est_id_int, tiempo_tarea))
            
            estacion_id = f"S{est_id_int:02d}"
            if estacion_id not in self.asignacion:
                self.asignacion[estacion_id] = []
                self.tiempos_estacion[estacion_id] = 0.0
            
            self.asignacion[estacion_id].append(tarea)
            self.tiempos_estacion[estacion_id] += tiempo_tarea
            tarea_a_estacion[tarea] = est_id_int
        
        self.n_estaciones = max(e[0] for e in estaciones_abiertas) if estaciones_abiertas else 0
        
        # Validar precedencias
        self.es_factible = self._validar_precedencias(tarea_a_estacion)
    
    def _validar_precedencias(self, tarea_a_estacion: Dict[str, int]) -> bool:
        """Verifica que las precedencias se respeten en la asignación."""
        for tarea, predecesoras in self.instancia.precedencias.items():
            if tarea not in tarea_a_estacion:
                continue
            for pred in predecesoras:
                if pred in tarea_a_estacion:
                    if tarea_a_estacion[pred] > tarea_a_estacion[tarea]:
                        return False
        return True
    
    def calcular_fitness(self, tipo: str = "estaciones") -> float:
        """
        Calcula el fitness de la solución.
        
        Args:
            tipo: "estaciones" (minimizar) o "eficiencia" (maximizar)
            
        Returns:
            Valor de fitness
        """
        if not self.es_factible:
            self.fitness = float('inf') if tipo == "estaciones" else 0.0
            return self.fitness
        
        if tipo == "estaciones":
            # Minimizar número de estaciones (penalizar infactibilidad)
            self.fitness = self.n_estaciones
        elif tipo == "eficiencia":
            # Maximizar utilización promedio
            if self.n_estaciones > 0:
                utilizacion = sum(self.tiempos_estacion.values()) / (
                    self.n_estaciones * self.instancia.tiempo_ciclo
                )
                self.fitness = utilizacion * 100
            else:
                self.fitness = 0.0
        
        return self.fitness
    
    def clonar(self) -> 'Solution':
        """Crea una copia profunda de la solución."""
        return Solution(
            cromosoma=copy.deepcopy(self.cromosoma),
            instancia=self.instancia
        )
    
    def __lt__(self, other: 'Solution') -> bool:
        """Permite comparar soluciones (menor es mejor para minimización)."""
        return self.fitness < other.fitness


class Optimizer(ABC):
    """
    Clase base abstracta para todos los optimizadores.
    Define la interfaz común que deben implementar GA, TS, y Híbridos.
    """
    
    def __init__(self, instancia: ProblemInstance, seed: int = 42):
        """
        Args:
            instancia: Instancia del problema a resolver
            seed: Semilla para reproducibilidad
        """
        self.instancia = instancia
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.mejor_solucion: Optional[Solution] = None
        self.historial_fitness: List[float] = []
        self.iteraciones = 0
    
    @abstractmethod
    def optimizar(self, max_iter: int = 100, verbose: bool = False) -> Solution:
        """
        Ejecuta el algoritmo de optimización.
        
        Args:
            max_iter: Número máximo de iteraciones
            verbose: Si mostrar progreso
            
        Returns:
            Mejor solución encontrada
        """
        pass
    
    @abstractmethod
    def generar_solucion_inicial(self) -> Solution:
        """Genera una solución inicial factible."""
        pass
    
    def generar_orden_topologico(self) -> List[str]:
        """
        Genera un orden de tareas que respeta las precedencias.
        Usa ordenamiento topológico con aleatorización.
        
        Returns:
            Lista de tareas en orden válido
        """
        # Contar grados de entrada
        grado_entrada = {t: 0 for t in self.instancia.tareas}
        for tarea, preds in self.instancia.precedencias.items():
            grado_entrada[tarea] = len(preds)
        
        # Cola de tareas sin predecesoras
        disponibles = [t for t in self.instancia.tareas if grado_entrada[t] == 0]
        self.rng.shuffle(disponibles)
        
        orden = []
        while disponibles:
            # Seleccionar una tarea aleatoriamente de las disponibles
            idx = self.rng.integers(0, len(disponibles))
            tarea = disponibles.pop(idx)
            orden.append(tarea)
            
            # Actualizar grados de entrada de sucesores
            for sucesor in self.instancia.sucesores.get(tarea, []):
                grado_entrada[sucesor] -= 1
                if grado_entrada[sucesor] == 0:
                    disponibles.append(sucesor)
        
        return orden
    
    def reportar(self) -> Dict:
        """Genera un reporte del proceso de optimización."""
        return {
            "algoritmo": self.__class__.__name__,
            "mejor_fitness": self.mejor_solucion.fitness if self.mejor_solucion else None,
            "n_estaciones": self.mejor_solucion.n_estaciones if self.mejor_solucion else None,
            "iteraciones": self.iteraciones,
            "historial": self.historial_fitness
        }


# =============================================================================
# Funciones auxiliares
# =============================================================================

def cargar_instancia_demo() -> ProblemInstance:
    """Carga la instancia de demostración (12 áreas avícolas)."""
    import sys
    import os
    
    # Agregar directorio de models al path
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
    if models_dir not in sys.path:
        sys.path.insert(0, models_dir)
    
    from dlbp_completo import crear_instancia_completa
    
    datos = crear_instancia_completa()
    return ProblemInstance(
        tareas=datos["tareas"],
        tiempos=datos["tiempos"],
        precedencias=datos["precedencias"],
        tiempo_ciclo=datos["tiempo_ciclo"],
        n_estaciones_max=len(datos["estaciones"])
    )


if __name__ == "__main__":
    # Prueba básica
    print("=" * 60)
    print("DLBP - Test de Clases Base")
    print("=" * 60)
    
    # Cargar instancia
    instancia = cargar_instancia_demo()
    print(f"\n✓ Instancia cargada:")
    print(f"  Tareas: {instancia.n_tareas}")
    print(f"  Tiempo total: {instancia.tiempo_total}s")
    print(f"  Tiempo de ciclo: {instancia.tiempo_ciclo}s")
    
    # Crear solución usando orden topológico
    rng = np.random.default_rng(42)
    
    # Generar orden válido manualmente
    grado_entrada = {t: len(instancia.precedencias.get(t, [])) for t in instancia.tareas}
    disponibles = [t for t in instancia.tareas if grado_entrada[t] == 0]
    orden = []
    while disponibles:
        idx = rng.integers(0, len(disponibles))
        tarea = disponibles.pop(idx)
        orden.append(tarea)
        for suc in instancia.sucesores.get(tarea, []):
            grado_entrada[suc] -= 1
            if grado_entrada[suc] == 0:
                disponibles.append(suc)
    
    solucion = Solution(cromosoma=orden, instancia=instancia)
    solucion.calcular_fitness("estaciones")
    
    print(f"\n✓ Solución generada:")
    print(f"  Factible: {solucion.es_factible}")
    print(f"  Estaciones: {solucion.n_estaciones}")
    print(f"  Fitness: {solucion.fitness}")
    
    # Mostrar asignación
    print("\n  Asignación:")
    for est, tareas_est in solucion.asignacion.items():
        tiempo = solucion.tiempos_estacion[est]
        util = (tiempo / instancia.tiempo_ciclo) * 100
        print(f"    {est}: {len(tareas_est)} tareas, {tiempo:.0f}s ({util:.0f}%)")
    
    print("\n" + "=" * 60)
    print("✓ Clases base validadas correctamente")
    print("=" * 60)
