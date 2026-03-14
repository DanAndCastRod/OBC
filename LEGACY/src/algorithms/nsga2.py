"""
DLBP Avícola - Algoritmo NSGA-II Multi-Objetivo
================================================
Implementación del algoritmo NSGA-II (Non-dominated Sorting GA II)
para optimización multi-objetivo del problema DLBP.

Autor: Daniel Castañeda
Fecha: Enero 2026
Extensión: Fase 5 - Optimización Multi-Objetivo

Objetivos optimizados:
1. Minimizar número de estaciones
2. Minimizar desbalance de carga (varianza de tiempos)
3. Maximizar eficiencia de línea

Basado en:
- Deb, K. (2002). A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Set
import numpy as np
import copy
import random
import sys
import os

# Agregar el directorio padre al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base import ProblemInstance, Solution, Optimizer, cargar_instancia_demo
from genetic_algorithm import GAConfig


@dataclass
class NSGA2Config:
    """Configuración del algoritmo NSGA-II."""
    poblacion_size: int = 100
    max_generaciones: int = 100
    prob_cruce: float = 0.9
    prob_mutacion: float = 0.1
    tipo_cruce: str = "OX"
    tipo_mutacion: str = "swap"
    objetivos: List[str] = field(default_factory=lambda: [
        "estaciones",      # Minimizar número de estaciones
        "desbalance",      # Minimizar desbalance de carga
        "eficiencia"       # Maximizar eficiencia (se invierte para minimizar)
    ])


@dataclass
class MultiObjectiveSolution:
    """
    Solución multi-objetivo para NSGA-II.
    Extiende Solution con atributos para dominancia de Pareto.
    """
    solucion: Solution
    objetivos: Dict[str, float] = field(default_factory=dict)
    rank: int = 0
    crowding_distance: float = 0.0
    
    def __post_init__(self):
        """Calcula los objetivos al crear la solución."""
        if not self.objetivos:
            self.calcular_objetivos()
    
    def calcular_objetivos(self):
        """Calcula todos los valores de objetivos."""
        # Objetivo 1: Minimizar estaciones
        self.objetivos['estaciones'] = self.solucion.n_estaciones
        
        # Objetivo 2: Minimizar desbalance (varianza de tiempos por estación)
        tiempos_estacion = self._calcular_tiempos_por_estacion()
        if len(tiempos_estacion) > 1:
            self.objetivos['desbalance'] = np.std(tiempos_estacion)
        else:
            self.objetivos['desbalance'] = 0.0
        
        # Objetivo 3: Minimizar 1/eficiencia (para convertir max en min)
        eficiencia = self.solucion.calcular_fitness("eficiencia")
        self.objetivos['eficiencia'] = 1.0 / max(eficiencia, 0.01)
    
    def _calcular_tiempos_por_estacion(self) -> List[float]:
        """Calcula el tiempo total de trabajo por estación."""
        instancia = self.solucion.instancia
        tiempos = []
        
        # Usar tiempos_estacion del objeto Solution directamente
        if hasattr(self.solucion, 'tiempos_estacion') and self.solucion.tiempos_estacion:
            tiempos = list(self.solucion.tiempos_estacion.values())
        else:
            # Fallback: calcular desde asignacion
            for estacion, tareas in self.solucion.asignacion.items():
                tiempo_estacion = sum(instancia.tiempos.get(t, 0) for t in tareas)
                tiempos.append(tiempo_estacion)
        
        return tiempos
    
    def domina(self, other: 'MultiObjectiveSolution') -> bool:
        """
        Verifica si esta solución domina a otra.
        A domina B si:
        - A es mejor o igual en todos los objetivos
        - A es estrictamente mejor en al menos un objetivo
        """
        dominated = False
        better_in_one = False
        
        for obj in self.objetivos:
            if self.objetivos[obj] > other.objetivos[obj]:
                dominated = True
            elif self.objetivos[obj] < other.objetivos[obj]:
                better_in_one = True
        
        return better_in_one and not dominated
    
    def __lt__(self, other: 'MultiObjectiveSolution') -> bool:
        """Comparación para ordenamiento (menor rank, mayor crowding)."""
        if self.rank != other.rank:
            return self.rank < other.rank
        return self.crowding_distance > other.crowding_distance


class NSGA2(Optimizer):
    """
    Algoritmo NSGA-II para el problema DLBP.
    
    Características:
    - Non-dominated sorting para clasificar soluciones
    - Crowding distance para mantener diversidad
    - Elitismo mediante selección de padres + hijos
    """
    
    def __init__(
        self, 
        instancia: ProblemInstance, 
        config: NSGA2Config = None,
        seed: int = 42
    ):
        super().__init__(instancia, seed)
        self.config = config or NSGA2Config()
        self.poblacion: List[MultiObjectiveSolution] = []
        self.frente_pareto: List[MultiObjectiveSolution] = []
        self.historial_frentes: List[List[Dict]] = []
    
    def generar_solucion_inicial(self) -> Solution:
        """Genera una solución usando orden topológico aleatorizado."""
        orden = self.generar_orden_topologico()
        return Solution(instancia=self.instancia, cromosoma=orden)
    
    def inicializar_poblacion(self):
        """Crea la población inicial."""
        self.poblacion = []
        for _ in range(self.config.poblacion_size):
            sol = self.generar_solucion_inicial()
            mo_sol = MultiObjectiveSolution(solucion=sol)
            self.poblacion.append(mo_sol)
    
    def non_dominated_sort(self, poblacion: List[MultiObjectiveSolution]) -> List[List[MultiObjectiveSolution]]:
        """
        Clasifica la población en frentes de Pareto.
        
        Returns:
            Lista de frentes, donde frentes[0] es el frente de Pareto
        """
        n = len(poblacion)
        dominados_por = {i: [] for i in range(n)}  # Quién domina a i
        n_dominadores = [0] * n  # Cuántos dominan a i
        frentes = [[]]
        
        # Calcular relaciones de dominancia
        for i in range(n):
            for j in range(i + 1, n):
                if poblacion[i].domina(poblacion[j]):
                    dominados_por[i].append(j)
                    n_dominadores[j] += 1
                elif poblacion[j].domina(poblacion[i]):
                    dominados_por[j].append(i)
                    n_dominadores[i] += 1
        
        # Identificar primer frente (no dominados)
        for i in range(n):
            if n_dominadores[i] == 0:
                poblacion[i].rank = 0
                frentes[0].append(poblacion[i])
        
        # Construir frentes siguientes
        k = 0
        while k < len(frentes) and frentes[k]:
            siguiente_frente = []
            for sol in frentes[k]:
                idx = poblacion.index(sol)
                for j in dominados_por[idx]:
                    n_dominadores[j] -= 1
                    if n_dominadores[j] == 0:
                        poblacion[j].rank = k + 1
                        siguiente_frente.append(poblacion[j])
            
            k += 1
            if siguiente_frente:
                frentes.append(siguiente_frente)
        
        # Filtrar frentes vacíos
        frentes = [f for f in frentes if f]
        
        return frentes
    
    def calcular_crowding_distance(self, frente: List[MultiObjectiveSolution]):
        """
        Calcula la crowding distance para cada solución en un frente.
        Mayor distancia = más aislado = mejor para diversidad.
        """
        n = len(frente)
        if n == 0:
            return
        
        for sol in frente:
            sol.crowding_distance = 0.0
        
        if n <= 2:
            for sol in frente:
                sol.crowding_distance = float('inf')
            return
        
        objetivos = list(frente[0].objetivos.keys())
        
        for obj in objetivos:
            # Ordenar por este objetivo
            frente.sort(key=lambda x: x.objetivos[obj])
            
            # Extremos tienen distancia infinita
            frente[0].crowding_distance = float('inf')
            frente[-1].crowding_distance = float('inf')
            
            # Calcular rango del objetivo
            obj_range = frente[-1].objetivos[obj] - frente[0].objetivos[obj]
            if obj_range == 0:
                continue
            
            # Calcular distancia para puntos intermedios
            for i in range(1, n - 1):
                distance = (frente[i + 1].objetivos[obj] - frente[i - 1].objetivos[obj]) / obj_range
                frente[i].crowding_distance += distance
    
    def seleccion_torneo_binario(self) -> MultiObjectiveSolution:
        """Selección por torneo binario basado en rank y crowding."""
        i, j = random.sample(range(len(self.poblacion)), 2)
        return min(self.poblacion[i], self.poblacion[j])
    
    def cruce_ox(
        self, 
        padre1: MultiObjectiveSolution, 
        padre2: MultiObjectiveSolution
    ) -> Tuple[MultiObjectiveSolution, MultiObjectiveSolution]:
        """Order Crossover adaptado para multi-objetivo."""
        crom1 = list(padre1.solucion.cromosoma)
        crom2 = list(padre2.solucion.cromosoma)
        n = len(crom1)
        
        # Seleccionar puntos de cruce
        p1, p2 = sorted(random.sample(range(n), 2))
        
        def crear_hijo(parent1, parent2):
            hijo = [None] * n
            hijo[p1:p2] = parent1[p1:p2]
            
            pos = p2
            for gen in parent2[p2:] + parent2[:p2]:
                if gen not in hijo:
                    if pos >= n:
                        pos = 0
                    while hijo[pos] is not None:
                        pos += 1
                        if pos >= n:
                            pos = 0
                    hijo[pos] = gen
            
            return hijo
        
        hijo1_crom = crear_hijo(crom1, crom2)
        hijo2_crom = crear_hijo(crom2, crom1)
        
        # Reparar precedencias
        hijo1_crom = self._reparar_precedencias(hijo1_crom)
        hijo2_crom = self._reparar_precedencias(hijo2_crom)
        
        hijo1 = MultiObjectiveSolution(
            solucion=Solution(instancia=self.instancia, cromosoma=hijo1_crom)
        )
        hijo2 = MultiObjectiveSolution(
            solucion=Solution(instancia=self.instancia, cromosoma=hijo2_crom)
        )
        
        return hijo1, hijo2
    
    def _reparar_precedencias(self, cromosoma: List[str]) -> List[str]:
        """Repara un cromosoma para respetar precedencias."""
        posiciones = {tarea: i for i, tarea in enumerate(cromosoma)}
        reparado = list(cromosoma)
        
        cambios = True
        while cambios:
            cambios = False
            for predecesor, sucesores in self.instancia.precedencias.items():
                for sucesor in sucesores:
                    if posiciones[predecesor] > posiciones[sucesor]:
                        # Mover predecesor antes del sucesor
                        idx_pred = reparado.index(predecesor)
                        idx_suc = reparado.index(sucesor)
                        reparado.pop(idx_pred)
                        reparado.insert(idx_suc, predecesor)
                        posiciones = {t: i for i, t in enumerate(reparado)}
                        cambios = True
        
        return reparado
    
    def mutacion_swap(self, solucion: MultiObjectiveSolution) -> MultiObjectiveSolution:
        """Mutación por intercambio."""
        cromosoma = list(solucion.solucion.cromosoma)
        n = len(cromosoma)
        i, j = random.sample(range(n), 2)
        cromosoma[i], cromosoma[j] = cromosoma[j], cromosoma[i]
        cromosoma = self._reparar_precedencias(cromosoma)
        
        return MultiObjectiveSolution(
            solucion=Solution(instancia=self.instancia, cromosoma=cromosoma)
        )
    
    def generar_descendencia(self) -> List[MultiObjectiveSolution]:
        """Genera población de descendientes."""
        descendientes = []
        
        while len(descendientes) < self.config.poblacion_size:
            padre1 = self.seleccion_torneo_binario()
            padre2 = self.seleccion_torneo_binario()
            
            if random.random() < self.config.prob_cruce:
                hijo1, hijo2 = self.cruce_ox(padre1, padre2)
            else:
                hijo1 = MultiObjectiveSolution(solucion=padre1.solucion.clonar())
                hijo2 = MultiObjectiveSolution(solucion=padre2.solucion.clonar())
            
            if random.random() < self.config.prob_mutacion:
                hijo1 = self.mutacion_swap(hijo1)
            if random.random() < self.config.prob_mutacion:
                hijo2 = self.mutacion_swap(hijo2)
            
            descendientes.extend([hijo1, hijo2])
        
        return descendientes[:self.config.poblacion_size]
    
    def evolucionar_generacion(self):
        """Ejecuta una generación del NSGA-II."""
        # Generar descendencia
        descendientes = self.generar_descendencia()
        
        # Combinar padres + hijos
        combinada = self.poblacion + descendientes
        
        # Non-dominated sorting
        frentes = self.non_dominated_sort(combinada)
        
        # Seleccionar siguiente generación
        nueva_poblacion = []
        for frente in frentes:
            self.calcular_crowding_distance(frente)
            
            if len(nueva_poblacion) + len(frente) <= self.config.poblacion_size:
                nueva_poblacion.extend(frente)
            else:
                # Ordenar por crowding distance y completar
                frente.sort(key=lambda x: x.crowding_distance, reverse=True)
                espacio = self.config.poblacion_size - len(nueva_poblacion)
                nueva_poblacion.extend(frente[:espacio])
                break
        
        self.poblacion = nueva_poblacion
        self.frente_pareto = [sol for sol in self.poblacion if sol.rank == 0]
    
    def optimizar(
        self, 
        max_iter: int = None, 
        verbose: bool = True
    ) -> List[MultiObjectiveSolution]:
        """
        Ejecuta el algoritmo NSGA-II.
        
        Returns:
            Lista de soluciones en el frente de Pareto
        """
        max_gen = max_iter or self.config.max_generaciones
        
        if verbose:
            print("\n" + "=" * 60)
            print("NSGA-II - Optimización Multi-Objetivo DLBP")
            print("=" * 60)
            print(f"Población: {self.config.poblacion_size}")
            print(f"Generaciones: {max_gen}")
            print(f"Objetivos: {self.config.objetivos}")
        
        # Inicializar
        self.inicializar_poblacion()
        
        # Clasificación inicial
        frentes = self.non_dominated_sort(self.poblacion)
        for frente in frentes:
            self.calcular_crowding_distance(frente)
        
        self.frente_pareto = frentes[0]
        
        # Evolucionar
        for gen in range(max_gen):
            self.evolucionar_generacion()
            
            # Guardar historial
            frente_actual = [
                {obj: sol.objetivos[obj] for obj in sol.objetivos}
                for sol in self.frente_pareto
            ]
            self.historial_frentes.append(frente_actual)
            
            if verbose and (gen + 1) % 10 == 0:
                print(f"\nGeneración {gen + 1}/{max_gen}")
                print(f"  Soluciones en Pareto: {len(self.frente_pareto)}")
                mejor_est = min(s.objetivos['estaciones'] for s in self.frente_pareto)
                print(f"  Mejor estaciones: {mejor_est:.0f}")
        
        if verbose:
            print("\n" + "=" * 60)
            print("FRENTE DE PARETO FINAL")
            print("=" * 60)
            print(f"{'Est.':<8} {'Desbal.':<12} {'1/Efic.':<12}")
            print("-" * 32)
            for sol in sorted(self.frente_pareto, key=lambda x: x.objetivos['estaciones']):
                print(f"{sol.objetivos['estaciones']:<8.0f} "
                      f"{sol.objetivos['desbalance']:<12.2f} "
                      f"{sol.objetivos['eficiencia']:<12.4f}")
        
        return self.frente_pareto
    
    def obtener_mejor_compromiso(self) -> MultiObjectiveSolution:
        """
        Retorna la solución de mejor compromiso del frente de Pareto.
        Usa la distancia normalizada al punto ideal.
        """
        if not self.frente_pareto:
            return None
        
        # Calcular punto ideal (mínimo en cada objetivo)
        objetivos = list(self.frente_pareto[0].objetivos.keys())
        ideal = {obj: min(s.objetivos[obj] for s in self.frente_pareto) for obj in objetivos}
        nadir = {obj: max(s.objetivos[obj] for s in self.frente_pareto) for obj in objetivos}
        
        mejor = None
        menor_distancia = float('inf')
        
        for sol in self.frente_pareto:
            distancia = 0
            for obj in objetivos:
                rango = nadir[obj] - ideal[obj]
                if rango > 0:
                    distancia += ((sol.objetivos[obj] - ideal[obj]) / rango) ** 2
            distancia = np.sqrt(distancia)
            
            if distancia < menor_distancia:
                menor_distancia = distancia
                mejor = sol
        
        return mejor


def main():
    """Función de demostración del NSGA-II."""
    print("\n" + "=" * 60)
    print("DLBP Avícola - Demostración NSGA-II")
    print("=" * 60 + "\n")
    
    # Cargar instancia
    instancia = cargar_instancia_demo()
    print(f"Instancia cargada: {instancia.n_tareas} tareas")
    
    # Configurar NSGA-II
    config = NSGA2Config(
        poblacion_size=50,
        max_generaciones=50,
        prob_cruce=0.9,
        prob_mutacion=0.1
    )
    
    # Ejecutar
    nsga2 = NSGA2(instancia, config, seed=42)
    frente = nsga2.optimizar(verbose=True)
    
    # Mejor compromiso
    mejor = nsga2.obtener_mejor_compromiso()
    if mejor:
        print("\n" + "-" * 40)
        print("SOLUCIÓN DE MEJOR COMPROMISO")
        print("-" * 40)
        print(f"Estaciones: {mejor.objetivos['estaciones']:.0f}")
        print(f"Desbalance: {mejor.objetivos['desbalance']:.2f}")
        print(f"Eficiencia: {1/mejor.objetivos['eficiencia']:.2%}")
    
    print("\n✅ NSGA-II ejecutado exitosamente")
    print(f"   Soluciones en Pareto: {len(frente)}")
    
    return nsga2


if __name__ == "__main__":
    main()
