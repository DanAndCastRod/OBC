"""
DLBP Avícola - Búsqueda Tabú (Tabu Search)
==========================================
Implementación de Búsqueda Tabú para el problema DLBP.

Basado en:
- Suwannarongsri et al. (2007): Hybrid Tabu Search for ALB
- Glover & Laguna (1997): Tabu Search fundamentals

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: 2 - Implementación Algorítmica
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field
from collections import deque
import copy
import sys
import os

# Agregar el directorio padre al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base import ProblemInstance, Solution, Optimizer, cargar_instancia_demo


@dataclass
class TSConfig:
    """Configuración de Tabu Search."""
    max_iteraciones: int = 200
    tamano_lista_tabu: int = 20
    tamano_vecindario: int = 30
    tipo_movimiento: str = "swap"  # swap, insert, o mixto
    criterio_aspiracion: bool = True
    intensificacion_cada: int = 50  # Reiniciar desde mejor cada N iter sin mejora
    tipo_fitness: str = "estaciones"


class TabuSearch(Optimizer):
    """
    Búsqueda Tabú para el problema DLBP.
    
    Características:
    - Vecindario: Movimientos Swap e Insert
    - Lista Tabú: Memoria de corto plazo
    - Criterio de Aspiración: Permite movimientos tabú si mejoran el mejor global
    - Intensificación: Reinicia desde mejor solución si hay estancamiento
    """
    
    def __init__(self, instancia: ProblemInstance, config: TSConfig = None, seed: int = 42):
        super().__init__(instancia, seed)
        self.config = config or TSConfig()
        self.lista_tabu: deque = deque(maxlen=self.config.tamano_lista_tabu)
        self.solucion_actual: Optional[Solution] = None
        self.iter_sin_mejora = 0
    
    def generar_solucion_inicial(self) -> Solution:
        """Genera una solución inicial usando orden topológico aleatorizado."""
        orden = self.generar_orden_topologico()
        solucion = Solution(cromosoma=orden, instancia=self.instancia)
        solucion.calcular_fitness(self.config.tipo_fitness)
        return solucion
    
    def generar_vecino_swap(self, solucion: Solution) -> Tuple[Solution, Tuple]:
        """
        Genera un vecino intercambiando dos posiciones.
        
        Returns:
            (nueva_solucion, movimiento) donde movimiento = (i, j) posiciones intercambiadas
        """
        nuevo_crom = solucion.cromosoma.copy()
        size = len(nuevo_crom)
        
        # Seleccionar dos posiciones aleatorias
        i, j = self.rng.choice(size, 2, replace=False)
        nuevo_crom[i], nuevo_crom[j] = nuevo_crom[j], nuevo_crom[i]
        
        # Reparar precedencias si es necesario
        nuevo_crom = self._reparar_precedencias(nuevo_crom)
        
        nueva_sol = Solution(cromosoma=nuevo_crom, instancia=self.instancia)
        nueva_sol.calcular_fitness(self.config.tipo_fitness)
        
        # El movimiento se identifica por las tareas intercambiadas
        movimiento = (solucion.cromosoma[i], solucion.cromosoma[j])
        return nueva_sol, movimiento
    
    def generar_vecino_insert(self, solucion: Solution) -> Tuple[Solution, Tuple]:
        """
        Genera un vecino moviendo una tarea a otra posición.
        
        Returns:
            (nueva_solucion, movimiento) donde movimiento = (tarea, origen, destino)
        """
        nuevo_crom = solucion.cromosoma.copy()
        size = len(nuevo_crom)
        
        origen = self.rng.integers(0, size)
        destino = self.rng.integers(0, size)
        while destino == origen:
            destino = self.rng.integers(0, size)
        
        tarea = nuevo_crom.pop(origen)
        nuevo_crom.insert(destino, tarea)
        
        # Reparar precedencias
        nuevo_crom = self._reparar_precedencias(nuevo_crom)
        
        nueva_sol = Solution(cromosoma=nuevo_crom, instancia=self.instancia)
        nueva_sol.calcular_fitness(self.config.tipo_fitness)
        
        movimiento = (tarea, origen, destino)
        return nueva_sol, movimiento
    
    def _reparar_precedencias(self, cromosoma: List[str]) -> List[str]:
        """Repara un cromosoma para que respete las precedencias."""
        posicion = {tarea: i for i, tarea in enumerate(cromosoma)}
        reparado = cromosoma.copy()
        
        for _ in range(100):
            valido = True
            for tarea, preds in self.instancia.precedencias.items():
                if tarea not in posicion:
                    continue
                for pred in preds:
                    if pred in posicion and posicion[pred] >= posicion[tarea]:
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
    
    def generar_vecindario(self, solucion: Solution) -> List[Tuple[Solution, Tuple]]:
        """Genera el vecindario de una solución."""
        vecindario = []
        
        for _ in range(self.config.tamano_vecindario):
            if self.config.tipo_movimiento == "swap":
                vecino, mov = self.generar_vecino_swap(solucion)
            elif self.config.tipo_movimiento == "insert":
                vecino, mov = self.generar_vecino_insert(solucion)
            else:  # mixto
                if self.rng.random() < 0.5:
                    vecino, mov = self.generar_vecino_swap(solucion)
                else:
                    vecino, mov = self.generar_vecino_insert(solucion)
            
            vecindario.append((vecino, mov))
        
        return vecindario
    
    def es_tabu(self, movimiento: Tuple) -> bool:
        """Verifica si un movimiento está en la lista tabú."""
        # Para swap (a, b), también es tabú (b, a)
        if len(movimiento) == 2:
            return movimiento in self.lista_tabu or (movimiento[1], movimiento[0]) in self.lista_tabu
        return movimiento in self.lista_tabu
    
    def optimizar(self, max_iter: int = None, verbose: bool = True) -> Solution:
        """
        Ejecuta la búsqueda tabú.
        
        Args:
            max_iter: Número máximo de iteraciones
            verbose: Mostrar progreso
            
        Returns:
            Mejor solución encontrada
        """
        if max_iter is None:
            max_iter = self.config.max_iteraciones
        
        if verbose:
            print(f"\n🔍 Iniciando Búsqueda Tabú...")
            print(f"   Iteraciones: {max_iter}")
            print(f"   Lista Tabú: {self.config.tamano_lista_tabu}")
            print(f"   Vecindario: {self.config.tamano_vecindario}")
            print(f"   Movimiento: {self.config.tipo_movimiento}")
        
        # Inicialización
        self.solucion_actual = self.generar_solucion_inicial()
        self.mejor_solucion = self.solucion_actual.clonar()
        self.iter_sin_mejora = 0
        
        for it in range(max_iter):
            self.iteraciones = it + 1
            
            # Generar vecindario
            vecindario = self.generar_vecindario(self.solucion_actual)
            
            # Filtrar soluciones no factibles
            vecindario = [(v, m) for v, m in vecindario if v.es_factible]
            
            if not vecindario:
                # Si no hay vecinos factibles, reiniciar
                self.solucion_actual = self.generar_solucion_inicial()
                continue
            
            # Ordenar por fitness
            vecindario.sort(key=lambda x: x[0].fitness)
            
            # Seleccionar mejor vecino no tabú (o que cumpla aspiración)
            mejor_vecino = None
            mejor_mov = None
            
            for vecino, mov in vecindario:
                if not self.es_tabu(mov):
                    mejor_vecino = vecino
                    mejor_mov = mov
                    break
                elif self.config.criterio_aspiracion:
                    # Criterio de aspiración: permitir si mejora el mejor global
                    if vecino.fitness < self.mejor_solucion.fitness:
                        mejor_vecino = vecino
                        mejor_mov = mov
                        break
            
            # Si todos son tabú, tomar el mejor de todos
            if mejor_vecino is None:
                mejor_vecino, mejor_mov = vecindario[0]
            
            # Actualizar solución actual
            self.solucion_actual = mejor_vecino
            self.lista_tabu.append(mejor_mov)
            
            # Actualizar mejor global
            if self.solucion_actual.fitness < self.mejor_solucion.fitness:
                self.mejor_solucion = self.solucion_actual.clonar()
                self.iter_sin_mejora = 0
            else:
                self.iter_sin_mejora += 1
            
            self.historial_fitness.append(self.mejor_solucion.fitness)
            
            # Intensificación: reiniciar desde mejor si hay estancamiento
            if self.iter_sin_mejora >= self.config.intensificacion_cada:
                self.solucion_actual = self.mejor_solucion.clonar()
                self.lista_tabu.clear()
                self.iter_sin_mejora = 0
            
            # Mostrar progreso
            if verbose and (it + 1) % 20 == 0:
                print(f"   Iter {it+1:3d}: Actual = {self.solucion_actual.fitness:.0f}, Mejor = {self.mejor_solucion.fitness:.0f}")
        
        if verbose:
            print(f"\n✅ TS finalizado: {self.mejor_solucion.n_estaciones} estaciones")
        
        return self.mejor_solucion


def main():
    """Función principal de demostración."""
    print("=" * 70)
    print("DLBP AVÍCOLA - BÚSQUEDA TABÚ (TABU SEARCH)")
    print("Basado en Suwannarongsri et al. (2007)")
    print("=" * 70)
    
    # Cargar instancia
    instancia = cargar_instancia_demo()
    print(f"\n📋 Instancia: {instancia.n_tareas} tareas, ciclo = {instancia.tiempo_ciclo}s")
    
    # Configurar TS
    config = TSConfig(
        max_iteraciones=200,
        tamano_lista_tabu=20,
        tamano_vecindario=30,
        tipo_movimiento="mixto",
        criterio_aspiracion=True
    )
    
    # Ejecutar TS
    ts = TabuSearch(instancia, config, seed=42)
    mejor = ts.optimizar(verbose=True)
    
    # Resultados
    print("\n" + "=" * 70)
    print("📊 RESULTADOS")
    print("=" * 70)
    print(f"   Estaciones utilizadas: {mejor.n_estaciones}")
    print(f"   Solución factible: {mejor.es_factible}")
    print(f"   Iteraciones: {ts.iteraciones}")
    
    print("\n🏭 Asignación:")
    for est, tareas in mejor.asignacion.items():
        tiempo = mejor.tiempos_estacion[est]
        util = (tiempo / instancia.tiempo_ciclo) * 100
        print(f"   {est}: {len(tareas)} tareas, {tiempo:.0f}s ({util:.0f}%)")
    
    print("\n" + "=" * 70)
    print("✅ Tabu Search validado")
    print("=" * 70)


if __name__ == "__main__":
    main()
