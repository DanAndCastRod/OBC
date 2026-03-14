"""
DLBP Avícola - Módulo de Paralelización
========================================
Implementa evaluación paralela de poblaciones para acelerar
la ejecución de metaheurísticas.

Autor: Daniel Castañeda
Fecha: Enero 2026
Extensión: Fase 5 - Paralelización

Características:
- Evaluación paralela de fitness usando multiprocessing
- Ejecución paralela de réplicas de experimentos
- Generación paralela de vecindarios para Tabu Search
"""

from multiprocessing import Pool, cpu_count
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from functools import partial
from typing import List, Callable, Any, Dict, Tuple
import time
import os
import sys

# Importar clases base usando import relativo si es paquete
try:
    from .base import ProblemInstance, Solution
except ImportError:
    # Fallback para ejecución como script
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from base import ProblemInstance, Solution


class ParallelEvaluator:
    """
    Evaluador paralelo para poblaciones de soluciones.
    
    Uso:
        evaluator = ParallelEvaluator(n_workers=4)
        fitnesses = evaluator.evaluar_poblacion(poblacion, instancia)
    """
    
    def __init__(self, n_workers: int = None, use_threads: bool = False):
        """
        Args:
            n_workers: Número de workers (por defecto: CPU cores - 1)
            use_threads: Usar ThreadPool en lugar de ProcessPool
                        (útil cuando hay mucho I/O o en Windows)
        """
        self.n_workers = n_workers or max(1, cpu_count() - 1)
        self.use_threads = use_threads
        self._executor_class = ThreadPoolExecutor if use_threads else ProcessPoolExecutor
    
    def evaluar_poblacion(
        self, 
        poblacion: List[Solution], 
        tipo_fitness: str = "estaciones"
    ) -> List[float]:
        """
        Evalúa una población en paralelo.
        
        Args:
            poblacion: Lista de soluciones a evaluar
            tipo_fitness: Tipo de fitness a calcular
            
        Returns:
            Lista de valores de fitness
        """
        if len(poblacion) < self.n_workers * 2:
            # Para poblaciones pequeñas, secuencial es más rápido
            return [sol.calcular_fitness(tipo_fitness) for sol in poblacion]
        
        with self._executor_class(max_workers=self.n_workers) as executor:
            futures = [
                executor.submit(self._evaluar_solucion, sol, tipo_fitness)
                for sol in poblacion
            ]
            return [f.result() for f in futures]
    
    @staticmethod
    def _evaluar_solucion(solucion: Solution, tipo_fitness: str) -> float:
        """Evalúa una sola solución (para uso paralelo)."""
        return solucion.calcular_fitness(tipo_fitness)


class ParallelExperimentRunner:
    """
    Ejecutor paralelo de réplicas de experimentos.
    
    Uso:
        runner = ParallelExperimentRunner()
        resultados = runner.ejecutar_replicas(
            funcion_experimento,
            n_replicas=10,
            **kwargs
        )
    """
    
    def __init__(self, n_workers: int = None):
        """
        Args:
            n_workers: Número de workers (por defecto: CPU cores)
        """
        self.n_workers = n_workers or cpu_count()
    
    def ejecutar_replicas(
        self,
        funcion: Callable,
        n_replicas: int,
        seeds: List[int] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Ejecuta múltiples réplicas de un experimento en paralelo.
        
        Args:
            funcion: Función que ejecuta una réplica
                    Debe aceptar 'seed' como argumento
            n_replicas: Número de réplicas
            seeds: Lista de semillas (genera automáticamente si None)
            **kwargs: Argumentos adicionales para la función
            
        Returns:
            Lista de resultados de cada réplica
        """
        if seeds is None:
            seeds = list(range(42, 42 + n_replicas))
        
        resultados = []
        with ProcessPoolExecutor(max_workers=self.n_workers) as executor:
            futures = {
                executor.submit(funcion, seed=seed, **kwargs): i
                for i, seed in enumerate(seeds)
            }
            
            for future in as_completed(futures):
                idx = futures[future]
                try:
                    resultado = future.result()
                    resultado['replica_id'] = idx
                    resultados.append(resultado)
                except Exception as e:
                    resultados.append({
                        'replica_id': idx,
                        'error': str(e),
                        'exito': False
                    })
        
        # Ordenar por ID de réplica
        resultados.sort(key=lambda x: x['replica_id'])
        return resultados


class ParallelNeighborhoodGenerator:
    """
    Generador paralelo de vecindarios para Tabu Search.
    
    Uso:
        generator = ParallelNeighborhoodGenerator()
        vecinos = generator.generar_vecindario(
            solucion_actual,
            instancia,
            tamano=50
        )
    """
    
    def __init__(self, n_workers: int = None):
        self.n_workers = n_workers or max(1, cpu_count() - 1)
    
    def generar_vecindario(
        self,
        solucion: Solution,
        tamano: int,
        tipo_movimiento: str = "swap"
    ) -> List[Tuple[Solution, Tuple[int, int]]]:
        """
        Genera un vecindario en paralelo.
        
        Args:
            solucion: Solución actual
            tamano: Número de vecinos a generar
            tipo_movimiento: Tipo de movimiento ("swap", "insert", "2-opt")
            
        Returns:
            Lista de tuplas (vecino, movimiento)
        """
        import random
        import copy
        
        movimientos = self._generar_movimientos(
            len(solucion.cromosoma), tamano, tipo_movimiento
        )
        
        # Para vecindarios pequeños, secuencial es suficiente
        if tamano < 20:
            return [
                self._aplicar_movimiento(solucion, mov, tipo_movimiento)
                for mov in movimientos
            ]
        
        # Paralelizar
        with ThreadPoolExecutor(max_workers=self.n_workers) as executor:
            futures = [
                executor.submit(
                    self._aplicar_movimiento, solucion, mov, tipo_movimiento
                )
                for mov in movimientos
            ]
            return [f.result() for f in futures]
    
    def _generar_movimientos(
        self, n: int, tamano: int, tipo: str
    ) -> List[Tuple[int, int]]:
        """Genera lista de movimientos posibles."""
        import random
        movimientos = set()
        
        while len(movimientos) < tamano:
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
            if i != j:
                if tipo == "swap":
                    movimientos.add((min(i, j), max(i, j)))
                else:
                    movimientos.add((i, j))
        
        return list(movimientos)
    
    def _aplicar_movimiento(
        self, solucion: Solution, movimiento: Tuple[int, int], tipo: str
    ) -> Tuple[Solution, Tuple[int, int]]:
        """Aplica un movimiento y crea nueva solución."""
        import copy
        
        nuevo_cromosoma = copy.copy(solucion.cromosoma)
        i, j = movimiento
        
        if tipo == "swap":
            nuevo_cromosoma[i], nuevo_cromosoma[j] = nuevo_cromosoma[j], nuevo_cromosoma[i]
        elif tipo == "insert":
            tarea = nuevo_cromosoma.pop(i)
            nuevo_cromosoma.insert(j, tarea)
        elif tipo == "2-opt":
            nuevo_cromosoma[i:j+1] = reversed(nuevo_cromosoma[i:j+1])
        
        nueva_solucion = Solution(
            instancia=solucion.instancia,
            cromosoma=nuevo_cromosoma
        )
        
        return nueva_solucion, movimiento


def benchmark_paralelo(n_soluciones: int = 100, n_workers_list: List[int] = None):
    """
    Ejecuta benchmark de rendimiento paralelo vs secuencial.
    
    Args:
        n_soluciones: Tamaño de la población a evaluar
        n_workers_list: Lista de configuraciones de workers a probar
    """
    from base import cargar_instancia_demo
    import random
    
    print("=" * 60)
    print("BENCHMARK: Evaluación Paralela vs Secuencial")
    print("=" * 60)
    
    # Cargar instancia
    instancia = cargar_instancia_demo()
    print(f"Instancia: {instancia.n_tareas} tareas")
    print(f"Población: {n_soluciones} soluciones")
    print(f"CPUs disponibles: {cpu_count()}")
    print()
    
    # Generar población de prueba
    random.seed(42)
    poblacion = []
    for _ in range(n_soluciones):
        cromosoma = list(instancia.tareas)
        random.shuffle(cromosoma)
        sol = Solution(instancia=instancia, cromosoma=cromosoma)
        poblacion.append(sol)
    
    if n_workers_list is None:
        n_workers_list = [1, 2, 4, cpu_count()]
    
    resultados = []
    
    # Secuencial
    print("Evaluación secuencial...")
    start = time.time()
    _ = [sol.calcular_fitness() for sol in poblacion]
    tiempo_seq = time.time() - start
    print(f"  Tiempo: {tiempo_seq:.4f}s")
    resultados.append(('Secuencial', 1, tiempo_seq, 1.0))
    
    # Paralelo con diferentes configuraciones
    for n_workers in n_workers_list:
        if n_workers == 1:
            continue
        
        print(f"\nEvaluación paralela ({n_workers} workers)...")
        evaluator = ParallelEvaluator(n_workers=n_workers, use_threads=True)
        
        start = time.time()
        _ = evaluator.evaluar_poblacion(poblacion)
        tiempo_par = time.time() - start
        
        speedup = tiempo_seq / tiempo_par
        print(f"  Tiempo: {tiempo_par:.4f}s")
        print(f"  Speedup: {speedup:.2f}x")
        
        resultados.append((f'Paralelo ({n_workers}w)', n_workers, tiempo_par, speedup))
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"{'Método':<20} {'Workers':<10} {'Tiempo (s)':<12} {'Speedup':<10}")
    print("-" * 52)
    for nombre, workers, tiempo, speedup in resultados:
        print(f"{nombre:<20} {workers:<10} {tiempo:<12.4f} {speedup:<10.2f}x")
    
    return resultados


# =============================================================================
# Demostración
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("DLBP Avícola - Módulo de Paralelización")
    print("=" * 60 + "\n")
    
    # Ejecutar benchmark
    benchmark_paralelo(n_soluciones=50)
