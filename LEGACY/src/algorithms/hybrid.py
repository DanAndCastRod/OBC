"""
DLBP Avícola - Algoritmo Híbrido (Memetic Algorithm)
=====================================================
Combina Algoritmo Genético (exploración global) con 
Búsqueda Tabú (intensificación local).

Basado en:
- Hu et al. (2023): Hyper-heuristic for stochastic DLBP
- Tian et al. (2023): Hybrid evolutionary algorithm for DLBP

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: 2 - Implementación Algorítmica
"""

import numpy as np
from typing import List, Optional
from dataclasses import dataclass
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base import ProblemInstance, Solution, Optimizer, cargar_instancia_demo
from genetic_algorithm import GeneticAlgorithm, GAConfig
from tabu_search import TabuSearch, TSConfig


@dataclass
class HybridConfig:
    """Configuración del Algoritmo Híbrido."""
    # Parámetros GA
    poblacion_size: int = 40
    generaciones_ga: int = 50
    prob_cruce: float = 0.85
    prob_mutacion: float = 0.1
    elitismo: int = 2
    
    # Parámetros TS (intensificación local)
    iter_ts_por_individuo: int = 20
    aplicar_ts_cada: int = 10  # Aplicar TS cada N generaciones
    top_n_para_ts: int = 5  # Aplicar TS a los N mejores
    
    tipo_fitness: str = "estaciones"


class HybridAlgorithm(Optimizer):
    """
    Algoritmo Memético: GA + Tabu Search.
    
    Estrategia:
    1. Usar GA para exploración global del espacio de soluciones
    2. Periódicamente, aplicar TS a los mejores individuos para refinamiento local
    3. Los individuos mejorados vuelven a la población
    """
    
    def __init__(self, instancia: ProblemInstance, config: HybridConfig = None, seed: int = 42):
        super().__init__(instancia, seed)
        self.config = config or HybridConfig()
        
        # Configurar GA interno
        self.ga_config = GAConfig(
            poblacion_size=self.config.poblacion_size,
            max_generaciones=self.config.aplicar_ts_cada,
            prob_cruce=self.config.prob_cruce,
            prob_mutacion=self.config.prob_mutacion,
            elitismo=self.config.elitismo,
            tipo_fitness=self.config.tipo_fitness
        )
        
        # Configurar TS interno
        self.ts_config = TSConfig(
            max_iteraciones=self.config.iter_ts_por_individuo,
            tamano_lista_tabu=10,
            tamano_vecindario=15,
            tipo_movimiento="swap",
            tipo_fitness=self.config.tipo_fitness
        )
        
        self.ga: Optional[GeneticAlgorithm] = None
    
    def generar_solucion_inicial(self) -> Solution:
        """Genera una solución inicial."""
        orden = self.generar_orden_topologico()
        sol = Solution(cromosoma=orden, instancia=self.instancia)
        sol.calcular_fitness(self.config.tipo_fitness)
        return sol
    
    def aplicar_busqueda_local(self, solucion: Solution) -> Solution:
        """Aplica Tabu Search como búsqueda local."""
        ts = TabuSearch(self.instancia, self.ts_config, seed=self.rng.integers(0, 10000))
        ts.solucion_actual = solucion.clonar()
        ts.mejor_solucion = solucion.clonar()
        
        # Ejecutar TS sin verbose
        return ts.optimizar(max_iter=self.config.iter_ts_por_individuo, verbose=False)
    
    def optimizar(self, max_iter: int = None, verbose: bool = True) -> Solution:
        """
        Ejecuta el algoritmo híbrido.
        
        Args:
            max_iter: Número de generaciones totales
            verbose: Mostrar progreso
            
        Returns:
            Mejor solución encontrada
        """
        if max_iter is None:
            max_iter = self.config.generaciones_ga
        
        if verbose:
            print(f"\n🔄 Iniciando Algoritmo Híbrido (GA + TS)...")
            print(f"   Población: {self.config.poblacion_size}")
            print(f"   Generaciones GA: {max_iter}")
            print(f"   TS cada: {self.config.aplicar_ts_cada} gen")
            print(f"   TS iter: {self.config.iter_ts_por_individuo}")
        
        # Inicializar GA
        self.ga = GeneticAlgorithm(self.instancia, self.ga_config, seed=self.seed)
        self.ga.inicializar_poblacion()
        self.mejor_solucion = self.ga.poblacion[0].clonar()
        
        gen_actual = 0
        while gen_actual < max_iter:
            # Ejecutar N generaciones de GA
            gen_bloque = min(self.config.aplicar_ts_cada, max_iter - gen_actual)
            
            for _ in range(gen_bloque):
                self.ga.poblacion = self.ga.evolucionar_generacion()
                self.ga._ordenar_poblacion()
                
                if self.ga.poblacion[0].fitness < self.mejor_solucion.fitness:
                    self.mejor_solucion = self.ga.poblacion[0].clonar()
                
                self.historial_fitness.append(self.mejor_solucion.fitness)
                gen_actual += 1
            
            # Aplicar TS a los mejores individuos
            if gen_actual < max_iter:
                if verbose:
                    print(f"   Gen {gen_actual}: Aplicando TS a top {self.config.top_n_para_ts}...")
                
                for i in range(min(self.config.top_n_para_ts, len(self.ga.poblacion))):
                    mejorado = self.aplicar_busqueda_local(self.ga.poblacion[i])
                    if mejorado.fitness <= self.ga.poblacion[i].fitness:
                        self.ga.poblacion[i] = mejorado
                        if mejorado.fitness < self.mejor_solucion.fitness:
                            self.mejor_solucion = mejorado.clonar()
                
                self.ga._ordenar_poblacion()
        
        self.iteraciones = gen_actual
        
        if verbose:
            print(f"\n✅ Híbrido finalizado: {self.mejor_solucion.n_estaciones} estaciones")
        
        return self.mejor_solucion


def main():
    """Función principal de demostración."""
    print("=" * 70)
    print("DLBP AVÍCOLA - ALGORITMO HÍBRIDO (MEMETIC)")
    print("Basado en Hu et al. (2023) y Tian et al. (2023)")
    print("=" * 70)
    
    # Cargar instancia
    instancia = cargar_instancia_demo()
    print(f"\n📋 Instancia: {instancia.n_tareas} tareas, ciclo = {instancia.tiempo_ciclo}s")
    
    # Configurar Híbrido
    config = HybridConfig(
        poblacion_size=40,
        generaciones_ga=100,
        aplicar_ts_cada=20,
        iter_ts_por_individuo=30,
        top_n_para_ts=5
    )
    
    # Ejecutar
    hibrido = HybridAlgorithm(instancia, config, seed=42)
    mejor = hibrido.optimizar(verbose=True)
    
    # Resultados
    print("\n" + "=" * 70)
    print("📊 RESULTADOS")
    print("=" * 70)
    print(f"   Estaciones utilizadas: {mejor.n_estaciones}")
    print(f"   Solución factible: {mejor.es_factible}")
    print(f"   Generaciones: {hibrido.iteraciones}")
    
    print("\n🏭 Asignación:")
    for est, tareas in mejor.asignacion.items():
        tiempo = mejor.tiempos_estacion[est]
        util = (tiempo / instancia.tiempo_ciclo) * 100
        print(f"   {est}: {len(tareas)} tareas, {tiempo:.0f}s ({util:.0f}%)")
    
    print("\n" + "=" * 70)
    print("✅ Algoritmo Híbrido validado")
    print("=" * 70)


if __name__ == "__main__":
    main()
