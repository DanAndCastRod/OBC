"""
DLBP Avícola - Comparación con Benchmarks y Solver Exacto
==========================================================
Compara el desempeño de los algoritmos metaheurísticos contra
soluciones óptimas obtenidas con programación lineal.

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: Mejoras - Comparación con Benchmarks
"""

import sys
import os
import json
import time
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Agregar paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'algorithms'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'models'))

import numpy as np

# Importar algoritmos
from base import ProblemInstance, Solution
from genetic_algorithm import GeneticAlgorithm, GAConfig
from tabu_search import TabuSearch, TSConfig
from hybrid import HybridAlgorithm, HybridConfig

# Importar PuLP para solver exacto
try:
    from pulp import LpProblem, LpMinimize, LpVariable, LpBinary, lpSum, LpStatus, value
    PULP_DISPONIBLE = True
except ImportError:
    PULP_DISPONIBLE = False
    print("[WARN] PuLP no disponible - no se podrá resolver óptimo exacto")


# =============================================================================
# Definición de Instancias Benchmark
# =============================================================================

INSTANCIAS_BENCHMARK = [
    {
        "nombre": "demo_15t",
        "descripcion": "Instancia demo avícola (15 tareas)",
        "n_tareas": 15,
        "tiempo_ciclo": 40,
        "tareas": [
            "T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08",
            "T09", "T10", "T11", "T12", "T13", "T14", "T15"
        ],
        "tiempos": {
            "T01": 5, "T02": 20, "T03": 12, "T04": 8, "T05": 6,
            "T06": 4, "T07": 15, "T08": 10, "T09": 10, "T10": 18,
            "T11": 12, "T12": 8, "T13": 14, "T14": 16, "T15": 7
        },
        "precedencias": {
            "T01": [], "T02": ["T01"], "T03": ["T02"], "T04": ["T03"],
            "T05": ["T04"], "T06": ["T05"], "T07": ["T06"], "T08": ["T07"],
            "T09": ["T07"], "T10": ["T09"], "T11": ["T10"], "T12": ["T06"],
            "T13": ["T06"], "T14": ["T13"], "T15": ["T11", "T14", "T12"]
        },
        "optimo_conocido": None  # Se calculará con solver
    },
    {
        "nombre": "lineal_10t",
        "descripcion": "Cadena lineal de 10 tareas (baseline simple)",
        "n_tareas": 10,
        "tiempo_ciclo": 25,
        "tareas": [f"T{i:02d}" for i in range(1, 11)],
        "tiempos": {f"T{i:02d}": 8 for i in range(1, 11)},  # Todas 8s
        "precedencias": {
            f"T{i:02d}": [f"T{i-1:02d}"] if i > 1 else [] 
            for i in range(1, 11)
        },
        "optimo_conocido": 4  # ceil(80/25) = 4, con restricciones 4
    },
    {
        "nombre": "paralelo_12t",
        "descripcion": "Tareas paralelas (sin precedencias internas)",
        "n_tareas": 12,
        "tiempo_ciclo": 30,
        "tareas": [f"T{i:02d}" for i in range(1, 13)],
        "tiempos": {f"T{i:02d}": 10 for i in range(1, 13)},  # Todas 10s
        "precedencias": {f"T{i:02d}": [] for i in range(1, 13)},  # Sin precedencias
        "optimo_conocido": 4  # ceil(120/30) = 4, caben 3 por estación
    },
    {
        "nombre": "mixto_20t",
        "descripcion": "Mezcla de tareas cortas y largas",
        "n_tareas": 20,
        "tiempo_ciclo": 35,
        "tareas": [f"T{i:02d}" for i in range(1, 21)],
        "tiempos": {
            "T01": 5, "T02": 25, "T03": 10, "T04": 8, "T05": 12,
            "T06": 15, "T07": 6, "T08": 20, "T09": 9, "T10": 11,
            "T11": 7, "T12": 18, "T13": 4, "T14": 14, "T15": 8,
            "T16": 10, "T17": 6, "T18": 12, "T19": 5, "T20": 10
        },
        "precedencias": {
            "T01": [], "T02": ["T01"], "T03": ["T01"], "T04": ["T02"],
            "T05": ["T02", "T03"], "T06": ["T04"], "T07": ["T05"],
            "T08": ["T06", "T07"], "T09": ["T08"], "T10": ["T08"],
            "T11": ["T09"], "T12": ["T10"], "T13": ["T11", "T12"],
            "T14": ["T13"], "T15": ["T14"], "T16": ["T14"], "T17": ["T15"],
            "T18": ["T16"], "T19": ["T17", "T18"], "T20": ["T19"]
        },
        "optimo_conocido": None  # Se calculará
    },
    {
        "nombre": "grande_20t",
        "descripcion": "Instancia con 20 tareas en 4 áreas",
        "n_tareas": 20,
        "tiempo_ciclo": 40,
        "tareas": [f"T{i:02d}" for i in range(1, 21)],
        "tiempos": {f"T{i:02d}": np.random.RandomState(42).randint(5, 18) for i in range(1, 21)},
        "precedencias": None,  # Se generará
        "optimo_conocido": None
    }
]


def generar_precedencias_cadena(n_tareas: int, n_areas: int) -> Dict[str, List[str]]:
    """Genera precedencias de cadena por áreas."""
    tareas_por_area = n_tareas // n_areas
    precedencias = {}
    
    for i in range(1, n_tareas + 1):
        tarea = f"T{i:02d}"
        if i == 1:
            precedencias[tarea] = []
        elif i % tareas_por_area == 1:
            # Primera tarea de área - depende de última de área anterior
            pred = f"T{i-1:02d}"
            precedencias[tarea] = [pred]
        else:
            # Dentro del área - cadena
            pred = f"T{i-1:02d}"
            precedencias[tarea] = [pred]
    
    return precedencias


def crear_instancia_desde_benchmark(benchmark: Dict) -> ProblemInstance:
    """Convierte un benchmark a ProblemInstance."""
    precs = benchmark["precedencias"]
    if precs is None:
        precs = generar_precedencias_cadena(benchmark["n_tareas"], 5)
    
    return ProblemInstance(
        tareas=benchmark["tareas"],
        tiempos=benchmark["tiempos"],
        precedencias=precs,
        tiempo_ciclo=benchmark["tiempo_ciclo"]
    )


def resolver_optimo_milp(instancia: ProblemInstance, tiempo_limite: int = 30) -> Dict:
    """
    Resuelve la instancia usando MILP (PuLP) para obtener el óptimo.
    
    Returns:
        Dict con óptimo, gap, tiempo de resolución
    """
    if not PULP_DISPONIBLE:
        return {"optimo": None, "status": "PuLP no disponible"}
    
    inicio = time.time()
    
    # Crear modelo
    modelo = LpProblem("DLBP_Optimo", LpMinimize)
    
    # Número máximo de estaciones (cota superior)
    M = instancia.n_tareas
    
    # Variables: x[i,k] = 1 si tarea i está en estación k
    x = {
        (tarea, k): LpVariable(f"x_{tarea}_{k}", cat=LpBinary)
        for tarea in instancia.tareas
        for k in range(1, M + 1)
    }
    
    # Variable: y[k] = 1 si estación k se usa
    y = {k: LpVariable(f"y_{k}", cat=LpBinary) for k in range(1, M + 1)}
    
    # Objetivo: minimizar número de estaciones usadas
    modelo += lpSum(y[k] for k in range(1, M + 1))
    
    # Restricción: cada tarea asignada a exactamente una estación
    for tarea in instancia.tareas:
        modelo += lpSum(x[tarea, k] for k in range(1, M + 1)) == 1
    
    # Restricción: tiempo por estación no excede ciclo
    for k in range(1, M + 1):
        modelo += lpSum(
            instancia.tiempos[tarea] * x[tarea, k] 
            for tarea in instancia.tareas
        ) <= instancia.tiempo_ciclo * y[k]
    
    # Restricción: precedencias (tarea j después de i => estación_j >= estación_i)
    for tarea_j, predecesoras in instancia.precedencias.items():
        for tarea_i in predecesoras:
            # sum(k * x[j,k]) >= sum(k * x[i,k])
            modelo += lpSum(k * x[tarea_j, k] for k in range(1, M + 1)) >= \
                      lpSum(k * x[tarea_i, k] for k in range(1, M + 1))
    
    # Resolver
    modelo.solve()
    tiempo_total = time.time() - inicio
    
    status = LpStatus[modelo.status]
    optimo = int(value(modelo.objective)) if status == "Optimal" else None
    
    return {
        "optimo": optimo,
        "status": status,
        "tiempo": tiempo_total,
        "n_variables": len(x) + len(y),
        "n_restricciones": len(modelo.constraints)
    }


def ejecutar_algoritmo(algoritmo: str, instancia: ProblemInstance, 
                       max_iter: int = 100, seed: int = 42) -> Dict:
    """Ejecuta un algoritmo y retorna resultados."""
    inicio = time.time()
    
    if algoritmo == "GA":
        config = GAConfig(max_generaciones=max_iter, poblacion_size=50)
        opt = GeneticAlgorithm(instancia, config=config, seed=seed)
    elif algoritmo == "TS":
        config = TSConfig(max_iteraciones=max_iter * 2)
        opt = TabuSearch(instancia, config=config, seed=seed)
    elif algoritmo == "Hybrid":
        config = HybridConfig(generaciones_ga=max_iter, poblacion_size=30)
        opt = HybridAlgorithm(instancia, config=config, seed=seed)
    else:
        raise ValueError(f"Algoritmo desconocido: {algoritmo}")
    
    mejor = opt.optimizar(max_iter=max_iter, verbose=False)
    tiempo = time.time() - inicio
    
    return {
        "estaciones": mejor.n_estaciones,
        "tiempo": tiempo,
        "factible": mejor.es_factible
    }


def ejecutar_comparacion_completa(n_replicas: int = 10):
    """Ejecuta la comparación completa contra benchmarks."""
    print("\n" + "=" * 70)
    print("COMPARACIÓN CON BENCHMARKS - DLBP AVÍCOLA")
    print("=" * 70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Réplicas por algoritmo: {n_replicas}")
    print("=" * 70)
    
    resultados = {}
    
    for bench in INSTANCIAS_BENCHMARK:
        nombre = bench["nombre"]
        print(f"\n{'='*50}")
        print(f"BENCHMARK: {nombre}")
        print(f"Descripción: {bench['descripcion']}")
        print(f"{'='*50}")
        
        # Crear instancia
        instancia = crear_instancia_desde_benchmark(bench)
        print(f"Tareas: {instancia.n_tareas}, Ciclo: {instancia.tiempo_ciclo}s")
        print(f"Tiempo total: {instancia.tiempo_total}s")
        print(f"LB teórico: {int(np.ceil(instancia.tiempo_total / instancia.tiempo_ciclo))}")
        
        # Resolver óptimo con MILP
        print("\n[MILP] Resolviendo óptimo exacto...")
        resultado_milp = resolver_optimo_milp(instancia, tiempo_limite=120)
        optimo = resultado_milp.get("optimo") or bench.get("optimo_conocido")
        
        if optimo:
            print(f"   ✓ Óptimo: {optimo} estaciones ({resultado_milp['status']})")
            print(f"   ✓ Tiempo: {resultado_milp.get('tiempo', 0):.2f}s")
        else:
            print(f"   ✗ No se encontró óptimo ({resultado_milp['status']})")
        
        # Ejecutar metaheurísticas
        resultados_bench = {
            "instancia": nombre,
            "n_tareas": instancia.n_tareas,
            "tiempo_ciclo": instancia.tiempo_ciclo,
            "tiempo_total": instancia.tiempo_total,
            "optimo": optimo,
            "milp": resultado_milp,
            "algoritmos": {}
        }
        
        for algo in ["GA", "TS", "Hybrid"]:
            print(f"\n[{algo}] Ejecutando {n_replicas} réplicas...")
            
            resultados_rep = []
            for rep in range(n_replicas):
                seed = 42 + rep * 100
                res = ejecutar_algoritmo(algo, instancia, max_iter=100, seed=seed)
                resultados_rep.append(res)
            
            estaciones = [r["estaciones"] for r in resultados_rep]
            tiempos = [r["tiempo"] for r in resultados_rep]
            
            media = np.mean(estaciones)
            std = np.std(estaciones)
            mejor = min(estaciones)
            peor = max(estaciones)
            
            # Calcular gap vs óptimo
            gap = ((media - optimo) / optimo * 100) if optimo else None
            
            resultados_bench["algoritmos"][algo] = {
                "media": float(media),
                "std": float(std),
                "mejor": int(mejor),
                "peor": int(peor),
                "tiempo_medio": float(np.mean(tiempos)),
                "gap_pct": float(gap) if gap else None
            }
            
            gap_str = f"{gap:.2f}%" if gap is not None else "N/A"
            print(f"   Estaciones: {media:.2f} ± {std:.2f} (mejor: {mejor})")
            print(f"   Gap vs óptimo: {gap_str}")
            print(f"   Tiempo medio: {np.mean(tiempos):.3f}s")
        
        resultados[nombre] = resultados_bench
    
    # Guardar resultados
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'results')
    os.makedirs(output_dir, exist_ok=True)
    
    # Convertir numpy types
    def convert(obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert(i) for i in obj]
        return obj
    
    output_file = os.path.join(output_dir, 'benchmark_comparison.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(convert(resultados), f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*70}")
    print(f"[OK] Resultados guardados en: {output_file}")
    print(f"{'='*70}")
    
    return resultados


def generar_resumen_markdown(resultados: Dict) -> str:
    """Genera resumen en Markdown."""
    md = []
    md.append("# Resumen de Comparación con Benchmarks\n")
    md.append(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    
    md.append("## Resultados por Instancia\n\n")
    md.append("| Instancia | n | Óptimo | GA | TS | Híbrido | Mejor Gap |\n")
    md.append("|-----------|---|--------|----|----|---------|----------|\n")
    
    for nombre, data in resultados.items():
        optimo = data.get("optimo", "?")
        ga = data["algoritmos"]["GA"]["media"]
        ts = data["algoritmos"]["TS"]["media"]
        hy = data["algoritmos"]["Hybrid"]["media"]
        
        gaps = [
            data["algoritmos"][a].get("gap_pct", 999) or 999 
            for a in ["GA", "TS", "Hybrid"]
        ]
        mejor_gap = min(gaps)
        mejor_gap_str = f"{mejor_gap:.1f}%" if mejor_gap < 999 else "N/A"
        
        md.append(f"| {nombre} | {data['n_tareas']} | {optimo} | "
                  f"{ga:.1f} | {ts:.1f} | {hy:.1f} | {mejor_gap_str} |\n")
    
    return "".join(md)


if __name__ == "__main__":
    resultados = ejecutar_comparacion_completa(n_replicas=10)
    
    # Generar resumen
    resumen = generar_resumen_markdown(resultados)
    
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'results')
    resumen_file = os.path.join(output_dir, 'benchmark_resumen.md')
    
    with open(resumen_file, 'w', encoding='utf-8') as f:
        f.write(resumen)
    
    print(f"[OK] Resumen: {resumen_file}")
