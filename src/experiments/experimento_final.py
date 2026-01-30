"""
DLBP Avícola - Experimento Final con Parámetros Calibrados
===========================================================
Ejecuta el experimento completo sobre todas las instancias
usando los parámetros calibrados por Optuna.

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: 4 - Experimentación Final
"""

import sys
import os
import time
import json
import yaml
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
import numpy as np

# Agregar paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "algorithms"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "models"))

from base import ProblemInstance, Solution
from genetic_algorithm import GeneticAlgorithm, GAConfig
from tabu_search import TabuSearch, TSConfig
from hybrid import HybridAlgorithm, HybridConfig
from generar_instancias import generar_conjunto_instancias


@dataclass
class ResultadoExperimento:
    """Resultado detallado de un experimento."""
    algoritmo: str
    instancia: str
    replica: int
    semilla: int
    n_estaciones: int
    fitness: float
    tiempo_segundos: float
    eficiencia_linea: float  # % utilización
    es_factible: bool
    iteraciones: int


def cargar_configuracion(path: str = None) -> Dict:
    """Carga los parámetros calibrados desde YAML."""
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "..", "..", "config", "algorithm_params.yaml")
    
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    return config["calibracion"]


def ejecutar_experimento_individual(
    instancia: ProblemInstance,
    nombre_instancia: str,
    algoritmo: str,
    config_calibrada: Dict,
    replica: int,
    semilla: int
) -> ResultadoExperimento:
    """Ejecuta un experimento individual con parámetros calibrados."""
    inicio = time.time()
    
    if algoritmo == "GA":
        params = config_calibrada["GA"]["parametros"]
        cfg = GAConfig(
            poblacion_size=params["poblacion_size"],
            prob_cruce=params["prob_cruce"],
            prob_mutacion=params["prob_mutacion"],
            tamano_torneo=params["tamano_torneo"],
            elitismo=params["elitismo"],
            max_generaciones=100
        )
        optimizer = GeneticAlgorithm(instancia, cfg, seed=semilla)
        mejor = optimizer.optimizar(max_iter=100, verbose=False)
        iteraciones = optimizer.iteraciones
        
    elif algoritmo == "TS":
        params = config_calibrada["TS"]["parametros"]
        cfg = TSConfig(
            tamano_lista_tabu=params["tamano_lista_tabu"],
            tamano_vecindario=params["tamano_vecindario"],
            tipo_movimiento=params["tipo_movimiento"],
            max_iteraciones=200
        )
        optimizer = TabuSearch(instancia, cfg, seed=semilla)
        mejor = optimizer.optimizar(max_iter=200, verbose=False)
        iteraciones = optimizer.iteraciones
        
    elif algoritmo == "Hybrid":
        params = config_calibrada["Hybrid"]["parametros"]
        cfg = HybridConfig(
            poblacion_size=params["poblacion_size"],
            prob_cruce=params["prob_cruce"],
            aplicar_ts_cada=params["aplicar_ts_cada"],
            iter_ts_por_individuo=params["iter_ts_por_individuo"],
            top_n_para_ts=params["top_n_para_ts"],
            generaciones_ga=100
        )
        optimizer = HybridAlgorithm(instancia, cfg, seed=semilla)
        mejor = optimizer.optimizar(max_iter=100, verbose=False)
        iteraciones = optimizer.iteraciones
    else:
        raise ValueError(f"Algoritmo desconocido: {algoritmo}")
    
    tiempo = time.time() - inicio
    
    # Calcular eficiencia de línea
    if mejor.n_estaciones > 0 and mejor.es_factible:
        eficiencia = (instancia.tiempo_total / (mejor.n_estaciones * instancia.tiempo_ciclo)) * 100
    else:
        eficiencia = 0.0
    
    return ResultadoExperimento(
        algoritmo=algoritmo,
        instancia=nombre_instancia,
        replica=replica,
        semilla=semilla,
        n_estaciones=mejor.n_estaciones,
        fitness=mejor.fitness,
        tiempo_segundos=tiempo,
        eficiencia_linea=eficiencia,
        es_factible=mejor.es_factible,
        iteraciones=iteraciones
    )


def ejecutar_experimento_completo(
    instancias: Dict[str, ProblemInstance],
    algoritmos: List[str],
    config_calibrada: Dict,
    n_replicas: int = 30,
    semilla_base: int = 42,
    verbose: bool = True
) -> List[ResultadoExperimento]:
    """
    Ejecuta el experimento completo sobre todas las instancias.
    
    Args:
        instancias: Diccionario de instancias
        algoritmos: Lista de algoritmos a evaluar
        config_calibrada: Parámetros calibrados
        n_replicas: Número de réplicas por combinación
        semilla_base: Semilla inicial
        verbose: Mostrar progreso
    
    Returns:
        Lista de resultados
    """
    resultados = []
    total = len(instancias) * len(algoritmos) * n_replicas
    contador = 0
    
    if verbose:
        print(f"\n🧪 EXPERIMENTO FINAL")
        print(f"   Instancias: {len(instancias)}")
        print(f"   Algoritmos: {algoritmos}")
        print(f"   Réplicas: {n_replicas}")
        print(f"   Total ejecuciones: {total}")
        print("-" * 60)
    
    for nombre_inst, instancia in instancias.items():
        if verbose:
            print(f"\n📦 Instancia: {nombre_inst} ({instancia.n_tareas} tareas)")
        
        for alg in algoritmos:
            tiempos_alg = []
            estaciones_alg = []
            
            for rep in range(n_replicas):
                semilla = semilla_base + rep * 1000
                
                resultado = ejecutar_experimento_individual(
                    instancia=instancia,
                    nombre_instancia=nombre_inst,
                    algoritmo=alg,
                    config_calibrada=config_calibrada,
                    replica=rep,
                    semilla=semilla
                )
                resultados.append(resultado)
                contador += 1
                
                tiempos_alg.append(resultado.tiempo_segundos)
                estaciones_alg.append(resultado.n_estaciones)
            
            if verbose:
                media_est = np.mean(estaciones_alg)
                std_est = np.std(estaciones_alg)
                media_t = np.mean(tiempos_alg)
                print(f"   {alg}: {media_est:.1f}±{std_est:.2f} estaciones, {media_t:.2f}s")
    
    return resultados


def calcular_estadisticas(resultados: List[ResultadoExperimento]) -> Dict:
    """Calcula estadísticas agregadas por algoritmo e instancia."""
    stats = {}
    
    # Agrupar por instancia y algoritmo
    for r in resultados:
        key = (r.instancia, r.algoritmo)
        if key not in stats:
            stats[key] = {"estaciones": [], "tiempos": [], "eficiencias": []}
        stats[key]["estaciones"].append(r.n_estaciones)
        stats[key]["tiempos"].append(r.tiempo_segundos)
        stats[key]["eficiencias"].append(r.eficiencia_linea)
    
    # Calcular estadísticos
    resumen = {}
    for (inst, alg), data in stats.items():
        if inst not in resumen:
            resumen[inst] = {}
        resumen[inst][alg] = {
            "n": len(data["estaciones"]),
            "estaciones_media": float(np.mean(data["estaciones"])),
            "estaciones_std": float(np.std(data["estaciones"])),
            "estaciones_min": int(np.min(data["estaciones"])),
            "estaciones_max": int(np.max(data["estaciones"])),
            "tiempo_media": float(np.mean(data["tiempos"])),
            "tiempo_std": float(np.std(data["tiempos"])),
            "eficiencia_media": float(np.mean(data["eficiencias"]))
        }
    
    return resumen


def imprimir_tabla_resultados(resumen: Dict):
    """Imprime tabla de resultados formateada."""
    print("\n" + "=" * 80)
    print("📊 TABLA DE RESULTADOS COMPARATIVOS")
    print("=" * 80)
    
    header = f"{'Instancia':<15} | {'Algoritmo':<8} | {'Est (μ±σ)':<12} | {'Min-Max':<9} | {'Tiempo(s)':<10} | {'Efic(%)':<8}"
    print(header)
    print("-" * 80)
    
    for inst, algs in resumen.items():
        for alg, stats in algs.items():
            est_str = f"{stats['estaciones_media']:.1f}±{stats['estaciones_std']:.2f}"
            rango = f"{stats['estaciones_min']}-{stats['estaciones_max']}"
            tiempo = f"{stats['tiempo_media']:.2f}±{stats['tiempo_std']:.2f}"
            efic = f"{stats['eficiencia_media']:.1f}%"
            print(f"{inst:<15} | {alg:<8} | {est_str:<12} | {rango:<9} | {tiempo:<10} | {efic:<8}")
    
    print("=" * 80)


def exportar_resultados(resultados: List[ResultadoExperimento], resumen: Dict, carpeta: str):
    """Exporta resultados a JSON y CSV."""
    os.makedirs(carpeta, exist_ok=True)
    
    # JSON detallado
    json_path = os.path.join(carpeta, "resultados_experimento_final.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "resultados_detallados": [asdict(r) for r in resultados],
            "resumen_estadistico": resumen
        }, f, indent=2, ensure_ascii=False)
    
    # CSV para análisis en Excel/R
    csv_path = os.path.join(carpeta, "resultados_experimento_final.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("instancia,algoritmo,replica,semilla,n_estaciones,fitness,tiempo_seg,eficiencia,factible\n")
        for r in resultados:
            f.write(f"{r.instancia},{r.algoritmo},{r.replica},{r.semilla},{r.n_estaciones},"
                    f"{r.fitness},{r.tiempo_segundos:.4f},{r.eficiencia_linea:.2f},{r.es_factible}\n")
    
    return json_path, csv_path


def main():
    """Función principal del experimento."""
    print("=" * 70)
    print("DLBP AVÍCOLA - EXPERIMENTO FINAL FASE 4")
    print("=" * 70)
    
    # Cargar configuración calibrada
    try:
        config = cargar_configuracion()
        print("\n✅ Configuración calibrada cargada")
    except FileNotFoundError:
        print("\n❌ Error: No se encontró config/algorithm_params.yaml")
        print("   Ejecutar primero: python src/experiments/tuning_optuna.py")
        return
    
    # Generar instancias
    print("\n📦 Generando instancias de prueba...")
    instancias = generar_conjunto_instancias()
    
    # Definir algoritmos
    algoritmos = ["GA", "TS", "Hybrid"]
    
    # Ejecutar experimento (usar menos réplicas para demo)
    n_replicas = 10  # Cambiar a 30 para experimento completo
    
    resultados = ejecutar_experimento_completo(
        instancias=instancias,
        algoritmos=algoritmos,
        config_calibrada=config,
        n_replicas=n_replicas,
        verbose=True
    )
    
    # Calcular estadísticas
    resumen = calcular_estadisticas(resultados)
    
    # Mostrar tabla
    imprimir_tabla_resultados(resumen)
    
    # Exportar
    carpeta_salida = os.path.join(os.path.dirname(__file__), "..", "..", "results")
    json_path, csv_path = exportar_resultados(resultados, resumen, carpeta_salida)
    
    print(f"\n💾 Resultados exportados a:")
    print(f"   JSON: {json_path}")
    print(f"   CSV:  {csv_path}")
    print("\n" + "=" * 70)
    print("✅ EXPERIMENTO COMPLETADO")
    print("=" * 70)


if __name__ == "__main__":
    main()
