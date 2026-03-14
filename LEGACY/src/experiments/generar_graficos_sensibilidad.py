"""
DLBP Avícola - Generador de Gráficos de Sensibilidad
=====================================================
Genera visualizaciones para el análisis de sensibilidad de parámetros.

Autor: Daniel Castañeda
Fecha: Enero 2026
"""

import os
import sys
import json

# Verificar matplotlib
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    plt.style.use('seaborn-v0_8-whitegrid')
except ImportError:
    print("[ERROR] matplotlib no instalado")
    sys.exit(1)

# Configuración global
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.figsize': (10, 6),
    'axes.edgecolor': '#333333',
    'axes.labelcolor': '#333333',
    'text.color': '#333333'
})


def cargar_resultados():
    """Carga los resultados del análisis de sensibilidad."""
    results_file = os.path.join(
        os.path.dirname(__file__), '..', '..', 'results', 
        'sensibilidad_parametros.json'
    )
    with open(results_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def crear_directorio_figuras():
    """Crea el directorio para figuras de sensibilidad."""
    carpeta = os.path.join(
        os.path.dirname(__file__), '..', '..', 'docs', 'tesis', 'figuras'
    )
    os.makedirs(carpeta, exist_ok=True)
    return carpeta


def grafico_barras_parametro(resultados, algoritmo, parametro, carpeta):
    """
    Genera gráfico de barras con error para un parámetro específico.
    """
    data = resultados[algoritmo][parametro]['resultados']
    
    valores = list(data.keys())
    medias = [data[v]['estaciones_media'] for v in valores]
    stds = [data[v]['estaciones_std'] for v in valores]
    
    # Identificar valor base
    try:
        valor_base = str(resultados[algoritmo][parametro]['impacto'].get('valor_base', ''))
    except:
        valor_base = ''
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Colores: base diferente
    colores = ['#008B8B' if v == valor_base else '#666666' for v in valores]
    
    bars = ax.bar(valores, medias, yerr=stds, capsize=5, 
                  color=colores, edgecolor='black', alpha=0.8)
    
    ax.set_xlabel(f'Valor de {parametro}')
    ax.set_ylabel('Número de Estaciones')
    ax.set_title(f'Sensibilidad de {algoritmo}: {parametro}')
    
    # Añadir valores sobre barras
    for bar, media, std in zip(bars, medias, stds):
        ax.annotate(f'{media:.2f}±{std:.2f}',
                   xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                   xytext=(0, 5), textcoords='offset points',
                   ha='center', fontsize=9)
    
    # Leyenda para valor base
    if valor_base:
        base_patch = mpatches.Patch(color='#008B8B', label=f'Base ({valor_base})')
        other_patch = mpatches.Patch(color='#666666', label='Variación')
        ax.legend(handles=[base_patch, other_patch], loc='upper right')
    
    plt.tight_layout()
    filename = f'sensibilidad_{algoritmo}_{parametro}.png'
    filepath = os.path.join(carpeta, filename)
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"   [OK] {filename}")
    return filepath


def grafico_tornado(resultados, carpeta):
    """
    Genera diagrama de tornado mostrando impacto de cada parámetro.
    """
    # Recolectar datos de todos los parámetros
    datos = []
    for algo, params in resultados.items():
        for param, data in params.items():
            if 'impacto' in data and data['impacto']:
                rango = data['impacto'].get('rango_total', 0)
                critico = data['impacto'].get('es_critico', False)
                datos.append({
                    'nombre': f'{algo}: {param}',
                    'rango': rango,
                    'critico': critico
                })
    
    if not datos:
        print("   [WARN] No hay datos de impacto para diagrama tornado")
        return None
    
    # Ordenar por rango descendente
    datos.sort(key=lambda x: x['rango'], reverse=True)
    
    nombres = [d['nombre'] for d in datos]
    rangos = [d['rango'] for d in datos]
    colores = ['#EB8A3E' if d['critico'] else '#008B8B' for d in datos]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.barh(nombres, rangos, color=colores, edgecolor='black')
    
    ax.set_xlabel('Rango de Variación (estaciones)')
    ax.set_title('Diagrama de Tornado: Impacto de Parámetros')
    ax.axvline(x=0.5, color='red', linestyle='--', linewidth=1.5, 
               label='Umbral crítico')
    
    # Leyenda
    critico_patch = mpatches.Patch(color='#EB8A3E', label='Crítico')
    robusto_patch = mpatches.Patch(color='#008B8B', label='Robusto')
    ax.legend(handles=[critico_patch, robusto_patch], loc='lower right')
    
    plt.tight_layout()
    filepath = os.path.join(carpeta, 'sensibilidad_tornado.png')
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"   [OK] sensibilidad_tornado.png")
    return filepath


def grafico_heatmap_tiempos(resultados, carpeta):
    """
    Genera heatmap mostrando tiempos de cómputo por configuración.
    """
    # Extraer tiempos de GA
    ga_data = resultados.get('GA', {})
    
    if 'poblacion_size' not in ga_data:
        return None
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Panel 1: Tiempo vs Tamaño de población (GA)
    pob_data = ga_data['poblacion_size']['resultados']
    x = [int(k) for k in pob_data.keys()]
    y = [pob_data[k]['tiempo_medio'] for k in pob_data.keys()]
    
    axes[0].bar(x, y, color='#008B8B', edgecolor='black')
    axes[0].set_xlabel('Tamaño de Población')
    axes[0].set_ylabel('Tiempo Medio (s)')
    axes[0].set_title('GA: Tiempo vs Tamaño de Población')
    
    # Panel 2: Tiempo vs Tamaño de vecindario (TS)
    ts_data = resultados.get('TS', {})
    if 'tamano_vecindario' in ts_data:
        vec_data = ts_data['tamano_vecindario']['resultados']
        x2 = [int(k) for k in vec_data.keys()]
        y2 = [vec_data[k]['tiempo_medio'] for k in vec_data.keys()]
        
        axes[1].bar(x2, y2, color='#EB8A3E', edgecolor='black')
        axes[1].set_xlabel('Tamaño de Vecindario')
        axes[1].set_ylabel('Tiempo Medio (s)')
        axes[1].set_title('TS: Tiempo vs Tamaño de Vecindario')
    
    plt.tight_layout()
    filepath = os.path.join(carpeta, 'sensibilidad_tiempos.png')
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"   [OK] sensibilidad_tiempos.png")
    return filepath


def grafico_resumen_general(resultados, carpeta):
    """
    Genera gráfico resumen mostrando estabilidad de todos los algoritmos.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    algoritmos = list(resultados.keys())
    colores = {'GA': '#008B8B', 'TS': '#EB8A3E', 'Hybrid': '#365660'}
    
    x_pos = 0
    x_ticks = []
    x_labels = []
    
    for algo in algoritmos:
        params = resultados[algo]
        for param, data in params.items():
            res = data['resultados']
            medias = [res[k]['estaciones_media'] for k in res.keys()]
            stds = [res[k]['estaciones_std'] for k in res.keys()]
            
            media_prom = np.mean(medias)
            std_prom = np.mean(stds)
            
            ax.bar(x_pos, media_prom, yerr=std_prom, capsize=4,
                   color=colores[algo], edgecolor='black', alpha=0.8)
            
            x_ticks.append(x_pos)
            x_labels.append(f'{param[:8]}...' if len(param) > 8 else param)
            x_pos += 1
        x_pos += 0.5  # Espacio entre algoritmos
    
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45, ha='right')
    ax.set_ylabel('Número de Estaciones')
    ax.set_title('Resumen de Sensibilidad: Todos los Parámetros')
    
    # Leyenda de algoritmos
    patches = [mpatches.Patch(color=colores[a], label=a) for a in algoritmos]
    ax.legend(handles=patches, loc='upper right')
    
    plt.tight_layout()
    filepath = os.path.join(carpeta, 'sensibilidad_resumen.png')
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"   [OK] sensibilidad_resumen.png")
    return filepath


def generar_todos_los_graficos():
    """Genera todos los gráficos de sensibilidad."""
    print("\n" + "=" * 60)
    print("GENERANDO GRÁFICOS DE SENSIBILIDAD")
    print("=" * 60)
    
    resultados = cargar_resultados()
    carpeta = crear_directorio_figuras()
    
    # Gráficos por parámetro
    for algo, params in resultados.items():
        for param in params.keys():
            grafico_barras_parametro(resultados, algo, param, carpeta)
    
    # Gráficos generales
    grafico_tornado(resultados, carpeta)
    grafico_heatmap_tiempos(resultados, carpeta)
    grafico_resumen_general(resultados, carpeta)
    
    print("=" * 60)
    print("[OK] Todos los gráficos generados")
    print(f"[DIR] Ubicación: {carpeta}")
    print("=" * 60)


if __name__ == "__main__":
    generar_todos_los_graficos()
