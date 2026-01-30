"""
DLBP Avícola - Análisis de Sensibilidad de Parámetros
======================================================
Analiza la sensibilidad de los algoritmos metaheurísticos a variaciones
en los parámetros calibrados.

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: Mejoras - Análisis de Sensibilidad
"""

import sys
import os
import json
import time
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any
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


# =============================================================================
# Configuración del Análisis
# =============================================================================

# Parámetros calibrados (base)
PARAMS_BASE = {
    'GA': {
        'poblacion_size': 75,
        'prob_cruce': 0.93,
        'prob_mutacion': 0.20,
        'tamano_torneo': 4,
        'elitismo': 1
    },
    'TS': {
        'tamano_lista_tabu': 15,
        'tamano_vecindario': 49,
        'tipo_movimiento': 'swap'
    },
    'Hybrid': {
        'poblacion_size': 45,
        'prob_cruce': 0.94,
        'aplicar_ts_cada': 24,
        'iter_ts_por_individuo': 28,
        'top_n_para_ts': 4
    }
}

# Parámetros a analizar con sus variaciones
PARAMETROS_SENSIBILIDAD = {
    'GA': {
        'poblacion_size': [50, 75, 100, 125],
        'prob_cruce': [0.80, 0.85, 0.90, 0.95],
        'prob_mutacion': [0.10, 0.15, 0.20, 0.25],
    },
    'TS': {
        'tamano_lista_tabu': [10, 15, 20, 25],
        'tamano_vecindario': [30, 40, 50, 60],
    },
    'Hybrid': {
        'aplicar_ts_cada': [15, 20, 25, 30],
    }
}

# Configuración experimental
N_REPLICAS = 10
SEMILLA_BASE = 42
MAX_GENERACIONES = 50  # Reducido para rapidez


def crear_instancia_test() -> ProblemInstance:
    """Crea una instancia de prueba para el análisis."""
    return ProblemInstance(
        tareas=[
            "T01_Colgado", "T02_Evisceracion", "T03_SepararCabezaPatas",
            "T04_Chiller", "T05_Seleccion", "T06_AreaDespresado",
            "T07_CortarPernil", "T08_Contramuslo", "T09_Muslo",
            "T10_DeshuesarMuslo", "T11_FiletearMuslo", "T12_Alas",
            "T13_Pechuga", "T14_FiletePechuga", "T15_Empaque"
        ],
        tiempos={
            "T01_Colgado": 5, "T02_Evisceracion": 20, "T03_SepararCabezaPatas": 12,
            "T04_Chiller": 8, "T05_Seleccion": 6, "T06_AreaDespresado": 4,
            "T07_CortarPernil": 15, "T08_Contramuslo": 10, "T09_Muslo": 10,
            "T10_DeshuesarMuslo": 18, "T11_FiletearMuslo": 12, "T12_Alas": 8,
            "T13_Pechuga": 14, "T14_FiletePechuga": 16, "T15_Empaque": 7
        },
        precedencias={
            "T01_Colgado": [],
            "T02_Evisceracion": ["T01_Colgado"],
            "T03_SepararCabezaPatas": ["T02_Evisceracion"],
            "T04_Chiller": ["T03_SepararCabezaPatas"],
            "T05_Seleccion": ["T04_Chiller"],
            "T06_AreaDespresado": ["T05_Seleccion"],
            "T07_CortarPernil": ["T06_AreaDespresado"],
            "T08_Contramuslo": ["T07_CortarPernil"],
            "T09_Muslo": ["T07_CortarPernil"],
            "T10_DeshuesarMuslo": ["T09_Muslo"],
            "T11_FiletearMuslo": ["T10_DeshuesarMuslo"],
            "T12_Alas": ["T06_AreaDespresado"],
            "T13_Pechuga": ["T06_AreaDespresado"],
            "T14_FiletePechuga": ["T13_Pechuga"],
            "T15_Empaque": ["T11_FiletearMuslo", "T14_FiletePechuga", "T12_Alas"]
        },
        tiempo_ciclo=40
    )


def ejecutar_algoritmo(algoritmo: str, instancia: ProblemInstance, 
                       params: Dict, seed: int) -> Dict:
    """
    Ejecuta un algoritmo con parámetros específicos.
    
    Returns:
        Dict con resultados (estaciones, eficiencia, tiempo)
    """
    inicio = time.time()
    
    if algoritmo == 'GA':
        config = GAConfig(
            poblacion_size=params.get('poblacion_size', 75),
            prob_cruce=params.get('prob_cruce', 0.93),
            prob_mutacion=params.get('prob_mutacion', 0.20),
            tamano_torneo=params.get('tamano_torneo', 4),
            elitismo=params.get('elitismo', 1),
            max_generaciones=MAX_GENERACIONES
        )
        optimizador = GeneticAlgorithm(instancia, config=config, seed=seed)
        
    elif algoritmo == 'TS':
        config = TSConfig(
            tamano_lista_tabu=params.get('tamano_lista_tabu', 15),
            tamano_vecindario=params.get('tamano_vecindario', 49),
            tipo_movimiento=params.get('tipo_movimiento', 'swap'),
            max_iteraciones=MAX_GENERACIONES * 2
        )
        optimizador = TabuSearch(instancia, config=config, seed=seed)
        
    elif algoritmo == 'Hybrid':
        config = HybridConfig(
            poblacion_size=params.get('poblacion_size', 45),
            prob_cruce=params.get('prob_cruce', 0.94),
            aplicar_ts_cada=params.get('aplicar_ts_cada', 24),
            iter_ts_por_individuo=params.get('iter_ts_por_individuo', 28),
            top_n_para_ts=params.get('top_n_para_ts', 4),
            generaciones_ga=MAX_GENERACIONES
        )
        optimizador = HybridAlgorithm(instancia, config=config, seed=seed)
    else:
        raise ValueError(f"Algoritmo desconocido: {algoritmo}")
    
    # Ejecutar
    mejor = optimizador.optimizar(verbose=False)
    tiempo_total = time.time() - inicio
    
    # Calcular eficiencia
    eficiencia = (instancia.tiempo_total / 
                  (mejor.n_estaciones * instancia.tiempo_ciclo)) * 100
    
    return {
        'estaciones': mejor.n_estaciones,
        'eficiencia': eficiencia,
        'tiempo': tiempo_total,
        'factible': mejor.es_factible
    }


def analizar_parametro(algoritmo: str, parametro: str, valores: List,
                       instancia: ProblemInstance) -> Dict:
    """
    Analiza la sensibilidad de un parámetro específico.
    
    Args:
        algoritmo: Nombre del algoritmo (GA, TS, Hybrid)
        parametro: Nombre del parámetro a variar
        valores: Lista de valores a probar
        instancia: Instancia del problema
        
    Returns:
        Dict con resultados por valor
    """
    resultados = {}
    
    for valor in valores:
        # Crear configuración con el parámetro modificado
        params = PARAMS_BASE[algoritmo].copy()
        params[parametro] = valor
        
        resultados_rep = []
        
        for rep in range(N_REPLICAS):
            seed = SEMILLA_BASE + rep * 1000
            try:
                res = ejecutar_algoritmo(algoritmo, instancia, params, seed)
                resultados_rep.append(res)
            except Exception as e:
                print(f"    [ERROR] {algoritmo}/{parametro}={valor}, rep={rep}: {e}")
        
        if resultados_rep:
            estaciones = [r['estaciones'] for r in resultados_rep]
            eficiencias = [r['eficiencia'] for r in resultados_rep]
            tiempos = [r['tiempo'] for r in resultados_rep]
            
            resultados[valor] = {
                'estaciones_media': np.mean(estaciones),
                'estaciones_std': np.std(estaciones),
                'estaciones_min': min(estaciones),
                'estaciones_max': max(estaciones),
                'eficiencia_media': np.mean(eficiencias),
                'tiempo_medio': np.mean(tiempos),
                'n_factibles': sum(1 for r in resultados_rep if r['factible']),
                'n_replicas': len(resultados_rep)
            }
    
    return resultados


def calcular_impacto(resultados: Dict, valor_base) -> Dict:
    """
    Calcula el impacto de variar un parámetro respecto al valor base.
    
    Returns:
        Dict con métricas de impacto
    """
    if valor_base not in resultados:
        return {}
    
    base = resultados[valor_base]['estaciones_media']
    
    impactos = {}
    for valor, res in resultados.items():
        media = res['estaciones_media']
        variacion_pct = ((media - base) / base) * 100 if base > 0 else 0
        impactos[valor] = {
            'estaciones_media': media,
            'variacion_vs_base': media - base,
            'variacion_pct': variacion_pct
        }
    
    # Calcular rango total de variación
    medias = [res['estaciones_media'] for res in resultados.values()]
    rango = max(medias) - min(medias)
    
    return {
        'impactos_por_valor': impactos,
        'rango_total': rango,
        'valor_base': valor_base,
        'es_critico': rango > 0.5  # Más de 0.5 estaciones de diferencia
    }


def ejecutar_analisis_completo():
    """Ejecuta el análisis de sensibilidad completo."""
    print("\n" + "=" * 70)
    print("ANÁLISIS DE SENSIBILIDAD DE PARÁMETROS - DLBP AVÍCOLA")
    print("=" * 70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Réplicas por configuración: {N_REPLICAS}")
    print(f"Generaciones máximas: {MAX_GENERACIONES}")
    print("=" * 70)
    
    # Crear instancia
    instancia = crear_instancia_test()
    print(f"\nInstancia: {instancia.n_tareas} tareas, ciclo={instancia.tiempo_ciclo}s")
    print(f"Tiempo total: {instancia.tiempo_total}s")
    print(f"Estaciones mín. teóricas: {int(np.ceil(instancia.tiempo_total / instancia.tiempo_ciclo))}")
    
    resultados_globales = {}
    
    for algoritmo, parametros in PARAMETROS_SENSIBILIDAD.items():
        print(f"\n{'='*50}")
        print(f"ALGORITMO: {algoritmo}")
        print(f"{'='*50}")
        
        resultados_globales[algoritmo] = {}
        
        for parametro, valores in parametros.items():
            print(f"\n  Parámetro: {parametro}")
            print(f"  Valores a probar: {valores}")
            print(f"  Valor base: {PARAMS_BASE[algoritmo].get(parametro, 'N/A')}")
            
            # Ejecutar análisis
            resultados = analizar_parametro(algoritmo, parametro, valores, instancia)
            
            # Mostrar resultados
            print(f"\n  Resultados:")
            for valor, res in resultados.items():
                marcador = " ← BASE" if valor == PARAMS_BASE[algoritmo].get(parametro) else ""
                print(f"    {parametro}={valor}: "
                      f"Est={res['estaciones_media']:.2f}±{res['estaciones_std']:.2f}, "
                      f"Efic={res['eficiencia_media']:.1f}%{marcador}")
            
            # Calcular impacto
            valor_base = PARAMS_BASE[algoritmo].get(parametro)
            impacto = calcular_impacto(resultados, valor_base)
            
            if impacto:
                print(f"\n  Análisis de impacto:")
                print(f"    Rango de variación: {impacto['rango_total']:.3f} estaciones")
                print(f"    ¿Parámetro crítico?: {'SÍ' if impacto['es_critico'] else 'NO'}")
            
            resultados_globales[algoritmo][parametro] = {
                'valores': valores,
                'resultados': resultados,
                'impacto': impacto
            }
    
    # Guardar resultados
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'results')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'sensibilidad_parametros.json')
    
    # Convertir numpy types para JSON (incluyendo claves de diccionario)
    def convert_numpy(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif isinstance(obj, dict):
            # Convertir claves a string si son numéricas
            return {str(k) if isinstance(k, (int, float, np.integer, np.floating)) else k: convert_numpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy(i) for i in obj]
        return obj
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(convert_numpy(resultados_globales), f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*70}")
    print(f"[OK] Resultados guardados en: {output_file}")
    print(f"{'='*70}")
    
    return resultados_globales


def generar_resumen_markdown(resultados: Dict) -> str:
    """Genera un resumen en formato Markdown."""
    md = []
    md.append("# Resumen de Análisis de Sensibilidad\n")
    md.append(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    md.append(f"**Réplicas:** {N_REPLICAS} por configuración\n\n")
    
    md.append("## Ranking de Parámetros por Impacto\n")
    md.append("| Algoritmo | Parámetro | Rango (est.) | Crítico |\n")
    md.append("|-----------|-----------|--------------|--------|\n")
    
    ranking = []
    for algo, params in resultados.items():
        for param, data in params.items():
            if 'impacto' in data and data['impacto']:
                rango = data['impacto']['rango_total']
                critico = data['impacto']['es_critico']
                ranking.append((algo, param, rango, critico))
    
    # Ordenar por rango descendente
    ranking.sort(key=lambda x: x[2], reverse=True)
    
    for algo, param, rango, critico in ranking:
        md.append(f"| {algo} | {param} | {rango:.3f} | {'⚠️ SÍ' if critico else '✅ No'} |\n")
    
    md.append("\n## Conclusiones\n\n")
    
    criticos = [f"`{r[0]}.{r[1]}`" for r in ranking if r[3]]
    robustos = [f"`{r[0]}.{r[1]}`" for r in ranking if not r[3]]
    
    if criticos:
        md.append(f"**Parámetros críticos:** {', '.join(criticos)}\n\n")
    if robustos:
        md.append(f"**Parámetros robustos:** {', '.join(robustos)}\n\n")
    
    return "".join(md)


if __name__ == "__main__":
    resultados = ejecutar_analisis_completo()
    
    # Generar resumen markdown
    resumen = generar_resumen_markdown(resultados)
    
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'results')
    resumen_file = os.path.join(output_dir, 'sensibilidad_resumen.md')
    
    with open(resumen_file, 'w', encoding='utf-8') as f:
        f.write(resumen)
    
    print(f"[OK] Resumen guardado en: {resumen_file}")
