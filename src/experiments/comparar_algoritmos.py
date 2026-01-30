"""
DLBP Avícola - Comparación de Algoritmos
=========================================
Script para comparar el desempeño de GA, TS e Híbrido
sobre múltiples instancias y ejecutar análisis estadístico.

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: 4 - Experimentación
"""

import sys
import os
import time
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import numpy as np

# Agregar paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "algorithms"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "models"))

from base import ProblemInstance, Solution, cargar_instancia_demo
from genetic_algorithm import GeneticAlgorithm, GAConfig
from tabu_search import TabuSearch, TSConfig
from hybrid import HybridAlgorithm, HybridConfig


@dataclass
class ExperimentResult:
    """Resultado de un experimento individual."""
    algoritmo: str
    instancia: str
    semilla: int
    n_estaciones: int
    fitness: float
    tiempo_segundos: float
    iteraciones: int
    es_factible: bool
    historial_fitness: List[float]


def ejecutar_experimento(
    instancia: ProblemInstance,
    nombre_instancia: str,
    algoritmo: str,
    semilla: int,
    config: Dict = None
) -> ExperimentResult:
    """
    Ejecuta un experimento individual.
    
    Args:
        instancia: Instancia del problema
        nombre_instancia: Nombre identificador
        algoritmo: "GA", "TS", o "Hybrid"
        semilla: Semilla para reproducibilidad
        config: Configuración específica del algoritmo
        
    Returns:
        ExperimentResult con métricas del experimento
    """
    inicio = time.time()
    
    if algoritmo == "GA":
        cfg = GAConfig(**(config or {}))
        optimizer = GeneticAlgorithm(instancia, cfg, seed=semilla)
        mejor = optimizer.optimizar(verbose=False)
        iteraciones = optimizer.iteraciones
        
    elif algoritmo == "TS":
        cfg = TSConfig(**(config or {}))
        optimizer = TabuSearch(instancia, cfg, seed=semilla)
        mejor = optimizer.optimizar(verbose=False)
        iteraciones = optimizer.iteraciones
        
    elif algoritmo == "Hybrid":
        cfg = HybridConfig(**(config or {}))
        optimizer = HybridAlgorithm(instancia, cfg, seed=semilla)
        mejor = optimizer.optimizar(verbose=False)
        iteraciones = optimizer.iteraciones
        
    else:
        raise ValueError(f"Algoritmo desconocido: {algoritmo}")
    
    tiempo = time.time() - inicio
    
    return ExperimentResult(
        algoritmo=algoritmo,
        instancia=nombre_instancia,
        semilla=semilla,
        n_estaciones=mejor.n_estaciones,
        fitness=mejor.fitness,
        tiempo_segundos=tiempo,
        iteraciones=iteraciones,
        es_factible=mejor.es_factible,
        historial_fitness=optimizer.historial_fitness[-10:]  # Últimos 10 para no sobrecargar
    )


def ejecutar_bateria_experimentos(
    instancias: Dict[str, ProblemInstance],
    algoritmos: List[str],
    n_repeticiones: int = 5,
    semilla_base: int = 42,
    verbose: bool = True
) -> List[ExperimentResult]:
    """
    Ejecuta una batería completa de experimentos.
    
    Args:
        instancias: Dict {nombre: instancia}
        algoritmos: Lista de algoritmos a probar
        n_repeticiones: Número de ejecuciones por combinación
        semilla_base: Semilla inicial
        verbose: Mostrar progreso
        
    Returns:
        Lista de ExperimentResult
    """
    resultados = []
    total = len(instancias) * len(algoritmos) * n_repeticiones
    contador = 0
    
    if verbose:
        print(f"\n🧪 Iniciando batería de experimentos")
        print(f"   Instancias: {len(instancias)}")
        print(f"   Algoritmos: {algoritmos}")
        print(f"   Repeticiones: {n_repeticiones}")
        print(f"   Total experimentos: {total}")
        print("-" * 50)
    
    for nombre_inst, instancia in instancias.items():
        for alg in algoritmos:
            for rep in range(n_repeticiones):
                semilla = semilla_base + rep * 1000
                
                resultado = ejecutar_experimento(
                    instancia=instancia,
                    nombre_instancia=nombre_inst,
                    algoritmo=alg,
                    semilla=semilla
                )
                resultados.append(resultado)
                contador += 1
                
                if verbose:
                    print(f"   [{contador}/{total}] {nombre_inst} | {alg} | Rep {rep+1}: "
                          f"{resultado.n_estaciones} est, {resultado.tiempo_segundos:.2f}s")
    
    return resultados


def generar_reporte(resultados: List[ExperimentResult]) -> Dict:
    """
    Genera un reporte estadístico de los resultados.
    
    Returns:
        Diccionario con estadísticas agregadas
    """
    # Agrupar por algoritmo
    por_algoritmo = {}
    for r in resultados:
        if r.algoritmo not in por_algoritmo:
            por_algoritmo[r.algoritmo] = []
        por_algoritmo[r.algoritmo].append(r)
    
    reporte = {"algoritmos": {}}
    
    for alg, res_alg in por_algoritmo.items():
        estaciones = [r.n_estaciones for r in res_alg if r.es_factible]
        tiempos = [r.tiempo_segundos for r in res_alg]
        
        reporte["algoritmos"][alg] = {
            "n_experimentos": len(res_alg),
            "factibles": len(estaciones),
            "estaciones_min": min(estaciones) if estaciones else None,
            "estaciones_max": max(estaciones) if estaciones else None,
            "estaciones_media": np.mean(estaciones) if estaciones else None,
            "estaciones_std": np.std(estaciones) if estaciones else None,
            "tiempo_medio": np.mean(tiempos),
            "tiempo_std": np.std(tiempos)
        }
    
    return reporte


def imprimir_tabla_resultados(reporte: Dict):
    """Imprime una tabla formateada de resultados."""
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 70)
    
    print(f"\n{'Algoritmo':<12} | {'Exp':<4} | {'Fact':<4} | {'Est (min)':<9} | "
          f"{'Est (μ±σ)':<12} | {'Tiempo (μ±σ)':<15}")
    print("-" * 70)
    
    for alg, stats in reporte["algoritmos"].items():
        est_media = stats.get("estaciones_media")
        est_std = stats.get("estaciones_std")
        est_min = stats.get("estaciones_min")
        
        est_str = f"{est_media:.1f}±{est_std:.1f}" if est_media else "N/A"
        tiempo_str = f"{stats['tiempo_medio']:.2f}±{stats['tiempo_std']:.2f}s"
        
        print(f"{alg:<12} | {stats['n_experimentos']:<4} | {stats['factibles']:<4} | "
              f"{est_min if est_min else 'N/A':<9} | {est_str:<12} | {tiempo_str:<15}")
    
    print("=" * 70)


def main():
    """Función principal de experimentación."""
    print("=" * 70)
    print("DLBP AVÍCOLA - EXPERIMENTACIÓN COMPARATIVA")
    print("=" * 70)
    
    # Cargar instancia(s)
    instancias = {
        "avicola_45t": cargar_instancia_demo()
    }
    
    # Definir algoritmos
    algoritmos = ["GA", "TS", "Hybrid"]
    
    # Ejecutar experimentos
    resultados = ejecutar_bateria_experimentos(
        instancias=instancias,
        algoritmos=algoritmos,
        n_repeticiones=5,
        semilla_base=42,
        verbose=True
    )
    
    # Generar reporte
    reporte = generar_reporte(resultados)
    imprimir_tabla_resultados(reporte)
    
    # Exportar resultados
    output_path = os.path.join(os.path.dirname(__file__), "resultados_comparacion.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "resultados": [asdict(r) for r in resultados],
            "reporte": reporte
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados exportados a: {output_path}")


if __name__ == "__main__":
    main()
