"""
DLBP Avícola - Tests Estadísticos
==================================
Ejecuta test de Friedman y comparaciones post-hoc Nemenyi
sobre los resultados del experimento final.

Autor: Daniel Castañeda
Fecha: Febrero 2026
Fase: Mejora Experimental
"""

import sys
import os
import json
import numpy as np
from datetime import datetime
from typing import Dict, List

# Intentar importar dependencias estadísticas
try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("⚠️ scipy no disponible. Instalar con: pip install scipy")

try:
    import scikit_posthocs as sp
    POSTHOCS_AVAILABLE = True
except ImportError:
    POSTHOCS_AVAILABLE = False
    print("⚠️ scikit-posthocs no disponible. Instalar con: pip install scikit-posthocs")


def cargar_resultados(path: str = None) -> Dict:
    """Carga resultados del experimento final."""
    if path is None:
        path = os.path.join(os.path.dirname(__file__), '..', '..', 'results', 
                           'resultados_experimento_final.json')
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró: {path}. Ejecutar primero experimento_final.py")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extraer_datos_por_instancia(resultados: Dict) -> Dict:
    """
    Extrae los datos organizados por instancia para los tests.
    
    Returns:
        Dict {instancia: {algoritmo: [lista_de_estaciones]}}
    """
    datos = {}
    
    for r in resultados.get('resultados_detallados', []):
        inst = r['instancia']
        alg = r['algoritmo']
        est = r['n_estaciones']
        
        if inst not in datos:
            datos[inst] = {}
        if alg not in datos[inst]:
            datos[inst][alg] = []
        datos[inst][alg].append(est)
    
    return datos


def test_friedman(datos_instancia: Dict) -> Dict:
    """
    Ejecuta el test de Friedman sobre una instancia.
    
    Args:
        datos_instancia: {algoritmo: [estaciones]}
    
    Returns:
        Dict con resultados del test
    """
    if not SCIPY_AVAILABLE:
        return {"error": "scipy no disponible"}
    
    algoritmos = sorted(datos_instancia.keys())
    muestras = [datos_instancia[alg] for alg in algoritmos]
    
    # Verificar que todas las muestras tengan el mismo tamaño
    min_n = min(len(m) for m in muestras)
    muestras = [m[:min_n] for m in muestras]
    
    # Test de Friedman
    try:
        stat, p_value = stats.friedmanchisquare(*muestras)
        stat = float(stat)
        p_value = float(p_value)
    except ValueError:
        stat, p_value = 0.0, 1.0
    
    # Handle NaN (occurs when all samples are identical)
    if np.isnan(stat) or np.isnan(p_value):
        stat, p_value = 0.0, 1.0
    
    return {
        "estadistico_chi2": round(stat, 4),
        "p_valor": p_value,
        "significativo_005": bool(p_value < 0.05),
        "significativo_001": bool(p_value < 0.001),
        "n_muestras": int(min_n),
        "algoritmos": algoritmos,
        "medias": {alg: round(float(np.mean(datos_instancia[alg][:min_n])), 2) for alg in algoritmos},
        "medianas": {alg: round(float(np.median(datos_instancia[alg][:min_n])), 2) for alg in algoritmos},
        "nota": "Todos los algoritmos obtuvieron el mismo resultado" if stat == 0.0 else None
    }


def test_nemenyi(datos_instancia: Dict) -> Dict:
    """
    Ejecuta comparaciones post-hoc Nemenyi.
    
    Args:
        datos_instancia: {algoritmo: [estaciones]}
    
    Returns:
        Dict con resultados post-hoc
    """
    if not POSTHOCS_AVAILABLE:
        # Fallback: Wilcoxon pairwise con Bonferroni
        if not SCIPY_AVAILABLE:
            return {"error": "ni scipy ni scikit-posthocs disponibles"}
        
        algoritmos = sorted(datos_instancia.keys())
        min_n = min(len(datos_instancia[alg]) for alg in algoritmos)
        
        comparaciones = {}
        n_comparaciones = len(algoritmos) * (len(algoritmos) - 1) // 2
        
        for i in range(len(algoritmos)):
            for j in range(i + 1, len(algoritmos)):
                alg_i = algoritmos[i]
                alg_j = algoritmos[j]
                datos_i = datos_instancia[alg_i][:min_n]
                datos_j = datos_instancia[alg_j][:min_n]
                
                # Wilcoxon signed-rank test
                try:
                    stat, p_val = stats.wilcoxon(datos_i, datos_j)
                    p_bonferroni = min(p_val * n_comparaciones, 1.0)
                except ValueError:
                    # All differences are zero
                    stat, p_val, p_bonferroni = 0, 1.0, 1.0
                
                comparaciones[f"{alg_i} vs {alg_j}"] = {
                    "estadistico": round(float(stat), 4),
                    "p_valor_raw": round(float(p_val), 6),
                    "p_valor_bonferroni": round(float(p_bonferroni), 6),
                    "significativo_005": p_bonferroni < 0.05,
                    "diferencia_medias": round(float(np.mean(datos_i) - np.mean(datos_j)), 3)
                }
        
        return {
            "metodo": "Wilcoxon signed-rank con corrección Bonferroni",
            "comparaciones": comparaciones
        }
    
    # Usar Nemenyi de scikit-posthocs
    algoritmos = sorted(datos_instancia.keys())
    min_n = min(len(datos_instancia[alg]) for alg in algoritmos)
    
    data_matrix = np.array([datos_instancia[alg][:min_n] for alg in algoritmos]).T
    
    p_values = sp.posthoc_nemenyi_friedman(data_matrix)
    
    comparaciones = {}
    for i in range(len(algoritmos)):
        for j in range(i + 1, len(algoritmos)):
            p_val = float(p_values.iloc[i, j])
            comparaciones[f"{algoritmos[i]} vs {algoritmos[j]}"] = {
                "p_valor": round(p_val, 6),
                "significativo_005": p_val < 0.05,
                "diferencia_medias": round(
                    float(np.mean(datos_instancia[algoritmos[i]][:min_n]) - 
                          np.mean(datos_instancia[algoritmos[j]][:min_n])), 3
                )
            }
    
    return {
        "metodo": "Nemenyi post-hoc",
        "comparaciones": comparaciones
    }


def calcular_rankings(datos: Dict) -> Dict:
    """Calcula rankings promedio por algoritmo."""
    algoritmos = set()
    for inst_data in datos.values():
        algoritmos.update(inst_data.keys())
    algoritmos = sorted(algoritmos)
    
    rankings_globales = {alg: [] for alg in algoritmos}
    
    for inst_name, inst_data in datos.items():
        # Para cada réplica, rankear los algoritmos
        min_n = min(len(inst_data[alg]) for alg in algoritmos if alg in inst_data)
        
        for i in range(min_n):
            valores = {alg: inst_data[alg][i] for alg in algoritmos if alg in inst_data}
            # Rankear (menor es mejor)
            sorted_algs = sorted(valores.items(), key=lambda x: x[1])
            
            rank = 1
            for idx, (alg, val) in enumerate(sorted_algs):
                # Manejo de empates: rank promedio
                if idx > 0 and val == sorted_algs[idx-1][1]:
                    rank = rankings_globales[alg][-1] if rankings_globales[alg] else rank
                rankings_globales[alg].append(rank)
                rank = idx + 2
    
    return {
        alg: {
            "ranking_medio": round(float(np.mean(ranks)), 3),
            "ranking_std": round(float(np.std(ranks)), 3),
            "n_observaciones": len(ranks)
        }
        for alg, ranks in rankings_globales.items()
    }


def ejecutar_tests_completos(verbose: bool = True) -> Dict:
    """Ejecuta todos los tests estadísticos."""
    print("\n" + "=" * 70)
    print("TESTS ESTADÍSTICOS - DLBP AVÍCOLA")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    
    # Cargar datos
    try:
        resultados = cargar_resultados()
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        return {}
    
    datos = extraer_datos_por_instancia(resultados)
    
    if not datos:
        print("❌ No se encontraron datos para analizar")
        return {}
    
    resultados_tests = {"instancias": {}}
    
    for inst_name, inst_data in datos.items():
        if verbose:
            print(f"\n📦 Instancia: {inst_name}")
            for alg, vals in inst_data.items():
                print(f"   {alg}: μ={np.mean(vals):.2f}, σ={np.std(vals):.2f}, "
                      f"min={min(vals)}, max={max(vals)}, n={len(vals)}")
        
        # Friedman
        friedman = test_friedman(inst_data)
        if verbose and "error" not in friedman:
            sig = "SÍ (p<0.05)" if friedman['significativo_005'] else "NO"
            print(f"   Friedman: χ²={friedman['estadistico_chi2']}, p={friedman['p_valor']:.6f} → {sig}")
        
        # Post-hoc
        posthoc = {}
        if friedman.get('significativo_005', False):
            posthoc = test_nemenyi(inst_data)
            if verbose and "comparaciones" in posthoc:
                print(f"   Post-hoc ({posthoc.get('metodo', 'N/A')}):")
                for comp, res in posthoc['comparaciones'].items():
                    p = res.get('p_valor_bonferroni', res.get('p_valor', 'N/A'))
                    sig = "✅ SÍ" if res.get('significativo_005', False) else "❌ No"
                    diff = res.get('diferencia_medias', 0)
                    print(f"     {comp}: p={p}, Δ={diff:+.3f}, Sig: {sig}")
        
        resultados_tests["instancias"][inst_name] = {
            "friedman": friedman,
            "posthoc": posthoc
        }
    
    # Rankings globales
    rankings = calcular_rankings(datos)
    resultados_tests["rankings_globales"] = rankings
    
    if verbose:
        print(f"\n{'='*70}")
        print("📊 RANKINGS GLOBALES")
        print(f"{'='*70}")
        for alg, rank_data in sorted(rankings.items(), key=lambda x: x[1]['ranking_medio']):
            print(f"  {alg}: Ranking medio = {rank_data['ranking_medio']:.3f} ± {rank_data['ranking_std']:.3f}")
    
    return resultados_tests


def main():
    resultados = ejecutar_tests_completos()
    
    if not resultados:
        return
    
    # Guardar
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'results')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'tests_estadisticos.json')
    
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            if isinstance(obj, (np.bool_,)):
                return bool(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return super().default(obj)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "fecha": datetime.now().isoformat(),
            **resultados
        }, f, indent=2, ensure_ascii=False, cls=NumpyEncoder)
    
    print(f"\n💾 Guardado en: {output_file}")


if __name__ == "__main__":
    main()
