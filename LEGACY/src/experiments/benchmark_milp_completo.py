"""
DLBP Avícola - Benchmark MILP Completo
=======================================
Ejecuta MILP sobre las 4 instancias estándar con timeout.
Compara contra metaheurísticas (GA, TS, Hybrid).

Autor: Daniel Castañeda
Fecha: Febrero 2026
Fase: Mejora Experimental
"""

import sys
import os
import json
import time
import math
from typing import Dict
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'algorithms'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'models'))

from pulp import LpProblem, LpVariable, LpMinimize, LpBinary, lpSum, LpStatus, value, PULP_CBC_CMD
from base import ProblemInstance
from generar_instancias import generar_conjunto_instancias


def resolver_milp_instancia(instancia: ProblemInstance, timeout: int = 120, verbose: bool = True) -> Dict:
    """
    Resuelve una instancia DLBP con MILP (PuLP/CBC) con timeout.
    
    Args:
        instancia: ProblemInstance a resolver
        timeout: Tiempo límite en segundos
        verbose: Mostrar progreso
        
    Returns:
        Dict con resultados MILP
    """
    tareas = instancia.tareas
    n = len(tareas)
    C = instancia.tiempo_ciclo
    tiempos = instancia.tiempos
    precedencias = instancia.precedencias
    
    # Máximo posible de estaciones
    max_estaciones = n
    estaciones = list(range(1, max_estaciones + 1))
    
    # Crear problema
    prob = LpProblem("DLBP", LpMinimize)
    
    # Variables: x[i][s] = 1 si tarea i asignada a estación s
    x = {
        i: {s: LpVariable(f"x_{i}_{s}", cat=LpBinary) for s in estaciones}
        for i in tareas
    }
    
    # y[s] = 1 si estación s activa
    y = {s: LpVariable(f"y_{s}", cat=LpBinary) for s in estaciones}
    
    # Objetivo: minimizar estaciones
    prob += lpSum(y[s] for s in estaciones)
    
    # R1: Cada tarea a exactamente una estación
    for i in tareas:
        prob += lpSum(x[i][s] for s in estaciones) == 1
    
    # R2: Precedencias
    for i in tareas:
        for j in precedencias.get(i, []):
            prob += lpSum(s * x[j][s] for s in estaciones) <= lpSum(s * x[i][s] for s in estaciones)
    
    # R3: Tiempo de ciclo
    for s in estaciones:
        prob += lpSum(tiempos[i] * x[i][s] for i in tareas) <= C * y[s]
    
    # R4: Activación
    for i in tareas:
        for s in estaciones:
            prob += x[i][s] <= y[s]
    
    # Resolver con timeout
    inicio = time.time()
    solver = PULP_CBC_CMD(timeLimit=timeout, msg=0)
    prob.solve(solver)
    tiempo_total = time.time() - inicio
    
    status = LpStatus[prob.status]
    
    resultado = {
        "status": status,
        "tiempo_segundos": round(tiempo_total, 2),
        "timeout": timeout
    }
    
    if status in ["Optimal", "Feasible"]:  
        obj_val = int(value(prob.objective))
        resultado["estaciones"] = obj_val
        resultado["es_optimo"] = status == "Optimal"
        
        # Calcular gap si es factible pero no óptimo
        if hasattr(prob, 'bestBound') and prob.bestBound is not None:
            lb = prob.bestBound
            resultado["lower_bound"] = lb
            if obj_val > 0:
                resultado["gap_pct"] = round(((obj_val - lb) / obj_val) * 100, 2)
        
        if verbose:
            print(f"    → {status}: {obj_val} estaciones en {tiempo_total:.1f}s")
    else:
        resultado["estaciones"] = None
        resultado["es_optimo"] = False
        if verbose:
            print(f"    → {status} después de {timeout}s timeout")
    
    return resultado


def ejecutar_benchmark_completo(verbose: bool = True) -> Dict:
    """Ejecuta MILP sobre las 4 instancias estándar."""
    print("\n" + "=" * 70)
    print("BENCHMARK MILP COMPLETO - DLBP AVÍCOLA")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    
    instancias = generar_conjunto_instancias()
    
    # Timeouts progresivos
    timeouts = {
        "pequeña_20t": 120,
        "mediana_40t": 300,
        "grande_70t": 300,
        "muy_grande_100t": 300
    }
    
    resultados = {}
    
    for nombre, instancia in instancias.items():
        timeout = timeouts.get(nombre, 120)
        
        if verbose:
            print(f"\n📦 {nombre}: {instancia.n_tareas} tareas, ciclo={instancia.tiempo_ciclo}s")
            print(f"   Tiempo total: {instancia.tiempo_total}s")
            lb = math.ceil(instancia.tiempo_total / instancia.tiempo_ciclo)
            print(f"   Lower bound teórico: {lb} estaciones")
            print(f"   Timeout: {timeout}s")
        
        resultado = resolver_milp_instancia(instancia, timeout=timeout, verbose=verbose)
        resultados[nombre] = {
            "n_tareas": instancia.n_tareas,
            "tiempo_ciclo": instancia.tiempo_ciclo,
            "tiempo_total": instancia.tiempo_total,
            "milp": resultado
        }
    
    # Resumen
    if verbose:
        print("\n" + "=" * 70)
        print("📊 RESUMEN BENCHMARK MILP")
        print("=" * 70)
        print(f"{'Instancia':<20} | {'Tareas':<7} | {'MILP Est.':<10} | {'Status':<10} | {'Tiempo(s)':<10}")
        print("-" * 70)
        for nombre, data in resultados.items():
            est = data['milp'].get('estaciones', 'N/A')
            status = data['milp']['status']
            tiempo = data['milp']['tiempo_segundos']
            print(f"{nombre:<20} | {data['n_tareas']:<7} | {str(est):<10} | {status:<10} | {tiempo:<10}")
    
    return resultados


def main():
    import numpy as np
    
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return super().default(obj)
    
    resultados = ejecutar_benchmark_completo()
    
    # Guardar
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'results')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'benchmark_milp_completo.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "fecha": datetime.now().isoformat(),
            "resultados": resultados
        }, f, indent=2, ensure_ascii=False, cls=NumpyEncoder)
    
    print(f"\n💾 Guardado en: {output_file}")


if __name__ == "__main__":
    main()
