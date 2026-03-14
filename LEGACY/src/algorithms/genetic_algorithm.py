"""
DLBP Avícola - Algoritmo Genético (GA)
======================================
Implementación de un Algoritmo Genético para el problema DLBP.

Basado en:
- Wang et al. (2021): Genetic simulated annealing for parallel DLBP
- McGovern & Gupta (2007): Balancing method and genetic algorithm for DLBP

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: 2 - Implementación Algorítmica
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import copy
import sys
import os

# Agregar el directorio padre al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base import ProblemInstance, Solution, Optimizer, cargar_instancia_demo


@dataclass
class GAConfig:
    """Configuración del Algoritmo Genético."""
    poblacion_size: int = 50
    max_generaciones: int = 100
    prob_cruce: float = 0.8
    prob_mutacion: float = 0.15
    tamano_torneo: int = 3
    elitismo: int = 2  # Número de mejores individuos que pasan directo
    tipo_cruce: str = "OX"  # OX (Order Crossover) o PMX
    tipo_mutacion: str = "swap"  # swap o insert
    tipo_fitness: str = "estaciones"


class GeneticAlgorithm(Optimizer):
    """
    Algoritmo Genético para el problema DLBP.
    
    Características:
    - Representación: Permutación de tareas (respetando precedencias)
    - Selección: Torneo
    - Cruce: Order Crossover (OX) o PMX
    - Mutación: Swap o Insert
    - Elitismo: Los mejores N individuos pasan a la siguiente generación
    """
    
    def __init__(self, instancia: ProblemInstance, config: GAConfig = None, seed: int = 42):
        super().__init__(instancia, seed)
        self.config = config or GAConfig()
        self.poblacion: List[Solution] = []
        self.generacion_actual = 0
        self.stats: Dict[str, List] = {
            "mejor_fitness": [],
            "fitness_promedio": [],
            "peor_fitness": []
        }
    
    def generar_solucion_inicial(self) -> Solution:
        """Genera una solución usando orden topológico aleatorizado."""
        orden = self.generar_orden_topologico()
        solucion = Solution(cromosoma=orden, instancia=self.instancia)
        solucion.calcular_fitness(self.config.tipo_fitness)
        return solucion
    
    def inicializar_poblacion(self):
        """Crea la población inicial."""
        self.poblacion = []
        for _ in range(self.config.poblacion_size):
            sol = self.generar_solucion_inicial()
            self.poblacion.append(sol)
        self._ordenar_poblacion()
    
    def _ordenar_poblacion(self):
        """Ordena la población por fitness (menor es mejor)."""
        self.poblacion.sort(key=lambda s: s.fitness)
    
    def seleccion_torneo(self) -> Solution:
        """Selecciona un individuo mediante torneo."""
        indices = self.rng.choice(
            len(self.poblacion), 
            size=self.config.tamano_torneo, 
            replace=False
        )
        candidatos = [self.poblacion[i] for i in indices]
        return min(candidatos, key=lambda s: s.fitness)
    
    def cruce_ox(self, padre1: Solution, padre2: Solution) -> Tuple[Solution, Solution]:
        """
        Order Crossover (OX).
        Mantiene un segmento del padre1 y completa con orden del padre2.
        """
        size = len(padre1.cromosoma)
        # Seleccionar puntos de corte
        pt1, pt2 = sorted(self.rng.choice(size, 2, replace=False))
        
        def crear_hijo(p1: List[str], p2: List[str]) -> List[str]:
            hijo = [None] * size
            # Copiar segmento del padre1
            hijo[pt1:pt2] = p1[pt1:pt2]
            heredados = set(hijo[pt1:pt2])
            # Completar con padre2 respetando orden
            pos = pt2
            for gen in p2:
                if gen not in heredados:
                    if pos >= size:
                        pos = 0
                    while hijo[pos] is not None:
                        pos = (pos + 1) % size
                    hijo[pos] = gen
            return hijo
        
        hijo1_crom = crear_hijo(padre1.cromosoma, padre2.cromosoma)
        hijo2_crom = crear_hijo(padre2.cromosoma, padre1.cromosoma)
        
        # Reparar hijos si violan precedencias
        hijo1_crom = self._reparar_precedencias(hijo1_crom)
        hijo2_crom = self._reparar_precedencias(hijo2_crom)
        
        hijo1 = Solution(cromosoma=hijo1_crom, instancia=self.instancia)
        hijo2 = Solution(cromosoma=hijo2_crom, instancia=self.instancia)
        
        hijo1.calcular_fitness(self.config.tipo_fitness)
        hijo2.calcular_fitness(self.config.tipo_fitness)
        
        return hijo1, hijo2
    
    def _reparar_precedencias(self, cromosoma: List[str]) -> List[str]:
        """Repara un cromosoma para que respete las precedencias."""
        posicion = {tarea: i for i, tarea in enumerate(cromosoma)}
        reparado = cromosoma.copy()
        
        # Intentar reparar intercambiando tareas que violen precedencias
        for _ in range(100):  # Máximo 100 intentos
            valido = True
            for tarea, preds in self.instancia.precedencias.items():
                if tarea not in posicion:
                    continue
                for pred in preds:
                    if pred in posicion and posicion[pred] >= posicion[tarea]:
                        # Intercambiar posiciones
                        idx_tarea = posicion[tarea]
                        idx_pred = posicion[pred]
                        reparado[idx_tarea], reparado[idx_pred] = reparado[idx_pred], reparado[idx_tarea]
                        posicion[tarea] = idx_pred
                        posicion[pred] = idx_tarea
                        valido = False
                        break
                if not valido:
                    break
            if valido:
                break
        
        return reparado
    
    def mutacion_swap(self, solucion: Solution) -> Solution:
        """Mutación por intercambio de dos posiciones."""
        nuevo_crom = solucion.cromosoma.copy()
        size = len(nuevo_crom)
        i, j = self.rng.choice(size, 2, replace=False)
        nuevo_crom[i], nuevo_crom[j] = nuevo_crom[j], nuevo_crom[i]
        
        # Reparar si es necesario
        nuevo_crom = self._reparar_precedencias(nuevo_crom)
        
        nueva_sol = Solution(cromosoma=nuevo_crom, instancia=self.instancia)
        nueva_sol.calcular_fitness(self.config.tipo_fitness)
        return nueva_sol
    
    def mutacion_insert(self, solucion: Solution) -> Solution:
        """Mutación por inserción (mover un gen a otra posición)."""
        nuevo_crom = solucion.cromosoma.copy()
        size = len(nuevo_crom)
        origen, destino = self.rng.choice(size, 2, replace=False)
        
        gen = nuevo_crom.pop(origen)
        nuevo_crom.insert(destino, gen)
        
        # Reparar si es necesario
        nuevo_crom = self._reparar_precedencias(nuevo_crom)
        
        nueva_sol = Solution(cromosoma=nuevo_crom, instancia=self.instancia)
        nueva_sol.calcular_fitness(self.config.tipo_fitness)
        return nueva_sol
    
    def evolucionar_generacion(self) -> List[Solution]:
        """Ejecuta una generación del GA."""
        nueva_poblacion = []
        
        # Elitismo: pasar los mejores directamente
        for i in range(self.config.elitismo):
            nueva_poblacion.append(self.poblacion[i].clonar())
        
        # Generar el resto mediante selección, cruce y mutación
        while len(nueva_poblacion) < self.config.poblacion_size:
            # Selección
            padre1 = self.seleccion_torneo()
            padre2 = self.seleccion_torneo()
            
            # Cruce
            if self.rng.random() < self.config.prob_cruce:
                hijo1, hijo2 = self.cruce_ox(padre1, padre2)
            else:
                hijo1 = padre1.clonar()
                hijo2 = padre2.clonar()
            
            # Mutación
            if self.rng.random() < self.config.prob_mutacion:
                if self.config.tipo_mutacion == "swap":
                    hijo1 = self.mutacion_swap(hijo1)
                else:
                    hijo1 = self.mutacion_insert(hijo1)
            
            if self.rng.random() < self.config.prob_mutacion:
                if self.config.tipo_mutacion == "swap":
                    hijo2 = self.mutacion_swap(hijo2)
                else:
                    hijo2 = self.mutacion_insert(hijo2)
            
            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < self.config.poblacion_size:
                nueva_poblacion.append(hijo2)
        
        return nueva_poblacion
    
    def optimizar(self, max_iter: int = None, verbose: bool = True) -> Solution:
        """
        Ejecuta el algoritmo genético completo.
        
        Args:
            max_iter: Número de generaciones (usa config si None)
            verbose: Mostrar progreso
            
        Returns:
            Mejor solución encontrada
        """
        if max_iter is None:
            max_iter = self.config.max_generaciones
        
        if verbose:
            print(f"\n🧬 Iniciando Algoritmo Genético...")
            print(f"   Población: {self.config.poblacion_size}")
            print(f"   Generaciones: {max_iter}")
            print(f"   Cruce: {self.config.prob_cruce:.0%} ({self.config.tipo_cruce})")
            print(f"   Mutación: {self.config.prob_mutacion:.0%} ({self.config.tipo_mutacion})")
        
        # Inicializar población
        self.inicializar_poblacion()
        self.mejor_solucion = self.poblacion[0].clonar()
        
        for gen in range(max_iter):
            self.generacion_actual = gen
            
            # Evolucionar
            self.poblacion = self.evolucionar_generacion()
            self._ordenar_poblacion()
            
            # Actualizar mejor solución
            if self.poblacion[0].fitness < self.mejor_solucion.fitness:
                self.mejor_solucion = self.poblacion[0].clonar()
            
            # Estadísticas
            fitnesses = [s.fitness for s in self.poblacion if s.es_factible]
            if fitnesses:
                self.stats["mejor_fitness"].append(min(fitnesses))
                self.stats["fitness_promedio"].append(np.mean(fitnesses))
                self.stats["peor_fitness"].append(max(fitnesses))
            
            self.historial_fitness.append(self.mejor_solucion.fitness)
            
            # Mostrar progreso
            if verbose and (gen + 1) % 10 == 0:
                print(f"   Gen {gen+1:3d}: Mejor = {self.mejor_solucion.fitness:.0f} estaciones")
        
        self.iteraciones = max_iter
        
        if verbose:
            print(f"\n✅ GA finalizado: {self.mejor_solucion.n_estaciones} estaciones")
        
        return self.mejor_solucion


def main():
    """Función principal de demostración."""
    print("=" * 70)
    print("DLBP AVÍCOLA - ALGORITMO GENÉTICO")
    print("Basado en Wang et al. (2021) y McGovern & Gupta (2007)")
    print("=" * 70)
    
    # Cargar instancia
    instancia = cargar_instancia_demo()
    print(f"\n📋 Instancia: {instancia.n_tareas} tareas, ciclo = {instancia.tiempo_ciclo}s")
    
    # Configurar GA
    config = GAConfig(
        poblacion_size=50,
        max_generaciones=100,
        prob_cruce=0.85,
        prob_mutacion=0.15,
        elitismo=2
    )
    
    # Ejecutar GA
    ga = GeneticAlgorithm(instancia, config, seed=42)
    mejor = ga.optimizar(verbose=True)
    
    # Resultados
    print("\n" + "=" * 70)
    print("📊 RESULTADOS")
    print("=" * 70)
    print(f"   Estaciones utilizadas: {mejor.n_estaciones}")
    print(f"   Solución factible: {mejor.es_factible}")
    print(f"   Generaciones: {ga.iteraciones}")
    
    print("\n🏭 Asignación:")
    for est, tareas in mejor.asignacion.items():
        tiempo = mejor.tiempos_estacion[est]
        util = (tiempo / instancia.tiempo_ciclo) * 100
        print(f"   {est}: {len(tareas)} tareas, {tiempo:.0f}s ({util:.0f}%)")
    
    print("\n" + "=" * 70)
    print("✅ Algoritmo Genético validado")
    print("=" * 70)


if __name__ == "__main__":
    main()
