"""
DLBP Avícola - Generador de Gráficos de Benchmarks
===================================================
Genera visualizaciones para la comparación con benchmarks y solver MILP.

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: Mejoras - Comparación con Benchmarks
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
    print("[ERROR] matplotlib no instalado. Ejecute: pip install matplotlib")
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

# Colores corporativos
COLORES = {
    'GA': '#008B8B',      # Teal
    'TS': '#EB8A3E',      # Naranja
    'Hybrid': '#365660',  # Azul pizarra
    'MILP': '#6B5B95'     # Púrpura
}


def cargar_resultados():
    """Carga los resultados del benchmark desde JSON."""
    results_file = os.path.join(
        os.path.dirname(__file__), '..', '..', 'results', 
        'benchmark_comparison.json'
    )
    with open(results_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def crear_directorios():
    """Crea los directorios para guardar figuras."""
    base = os.path.dirname(__file__)
    dirs = {
        'tesis': os.path.join(base, '..', '..', 'docs', 'tesis', 'figuras'),
        'presentacion': os.path.join(base, '..', '..', 'docs', 'presentacion', 'figuras')
    }
    for d in dirs.values():
        os.makedirs(d, exist_ok=True)
    return dirs


def grafico_1_comparacion_instancias(resultados, carpetas):
    """
    Gráfico 1: Barras agrupadas comparando algoritmos por instancia.
    """
    # Filtrar metadata
    instancias = [k for k in resultados.keys() if k != 'metadata']
    
    nombres = []
    ga_vals = []
    ts_vals = []
    hy_vals = []
    optimos = []
    
    for inst in instancias:
        data = resultados[inst]
        nombres.append(inst.replace('_', '\n'))
        ga_vals.append(data['algoritmos']['GA']['media'])
        ts_vals.append(data['algoritmos']['TS']['media'])
        hy_vals.append(data['algoritmos']['Hybrid']['media'])
        optimos.append(data.get('optimo', 0))
    
    x = np.arange(len(nombres))
    width = 0.2
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars1 = ax.bar(x - width*1.5, optimos, width, label='Óptimo (MILP)', 
                   color=COLORES['MILP'], edgecolor='black', alpha=0.9)
    bars2 = ax.bar(x - width/2, ga_vals, width, label='GA', 
                   color=COLORES['GA'], edgecolor='black', alpha=0.9)
    bars3 = ax.bar(x + width/2, ts_vals, width, label='TS', 
                   color=COLORES['TS'], edgecolor='black', alpha=0.9)
    bars4 = ax.bar(x + width*1.5, hy_vals, width, label='Híbrido', 
                   color=COLORES['Hybrid'], edgecolor='black', alpha=0.9)
    
    ax.set_xlabel('Instancia')
    ax.set_ylabel('Número de Estaciones')
    ax.set_title('Comparación de Algoritmos por Instancia')
    ax.set_xticks(x)
    ax.set_xticklabels(nombres)
    ax.legend(loc='upper right')
    ax.set_ylim(0, max(max(ga_vals), max(ts_vals), max(hy_vals)) + 1)
    
    # Añadir valores sobre barras
    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                       xy=(bar.get_x() + bar.get_width()/2, height),
                       xytext=(0, 3), textcoords='offset points',
                       ha='center', fontsize=8)
    
    plt.tight_layout()
    
    for dest, carpeta in carpetas.items():
        filepath = os.path.join(carpeta, 'benchmark_comparacion_instancias.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"   [OK] {dest}: benchmark_comparacion_instancias.png")
    
    plt.close()


def grafico_2_gap_vs_optimo(resultados, carpetas):
    """
    Gráfico 2: Barras horizontales mostrando gap % por algoritmo.
    """
    instancias = [k for k in resultados.keys() if k != 'metadata']
    
    algoritmos = ['GA', 'TS', 'Hybrid']
    gaps = {algo: [] for algo in algoritmos}
    
    for inst in instancias:
        data = resultados[inst]
        for algo in algoritmos:
            gap = data['algoritmos'][algo].get('gap_pct', 0) or 0
            gaps[algo].append(gap)
    
    # Calcular gap promedio por algoritmo
    gap_promedio = {algo: np.mean(gaps[algo]) for algo in algoritmos}
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    y_pos = np.arange(len(algoritmos))
    valores = [gap_promedio[a] for a in algoritmos]
    colores = [COLORES[a] for a in algoritmos]
    
    bars = ax.barh(y_pos, valores, color=colores, edgecolor='black', alpha=0.9)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(algoritmos)
    ax.set_xlabel('Gap Promedio vs Óptimo (%)')
    ax.set_title('Gap Promedio por Algoritmo')
    ax.axvline(x=5, color='red', linestyle='--', linewidth=1.5, label='Umbral 5%')
    
    # Añadir valores
    for bar, val in zip(bars, valores):
        ax.annotate(f'{val:.1f}%',
                   xy=(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2),
                   va='center', fontsize=10)
    
    # Añadir nota
    ax.text(0.95, 0.05, '✓ Gap = 0% es óptimo', transform=ax.transAxes,
            ha='right', va='bottom', fontsize=9, style='italic',
            bbox=dict(boxstyle='round', facecolor='#e8f5e9', alpha=0.8))
    
    plt.tight_layout()
    
    for dest, carpeta in carpetas.items():
        filepath = os.path.join(carpeta, 'benchmark_gap_optimo.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"   [OK] {dest}: benchmark_gap_optimo.png")
    
    plt.close()


def grafico_3_tiempos_ejecucion(resultados, carpetas):
    """
    Gráfico 3: Comparación de tiempos de ejecución MILP vs metaheurísticas.
    """
    instancias = [k for k in resultados.keys() if k != 'metadata']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(instancias))
    width = 0.2
    
    tiempos_milp = []
    tiempos_ga = []
    tiempos_ts = []
    tiempos_hy = []
    
    for inst in instancias:
        data = resultados[inst]
        tiempos_milp.append(data['milp'].get('tiempo', 0))
        tiempos_ga.append(data['algoritmos']['GA']['tiempo_medio'])
        tiempos_ts.append(data['algoritmos']['TS']['tiempo_medio'])
        tiempos_hy.append(data['algoritmos']['Hybrid']['tiempo_medio'])
    
    bars1 = ax.bar(x - width*1.5, tiempos_milp, width, label='MILP', 
                   color=COLORES['MILP'], edgecolor='black')
    bars2 = ax.bar(x - width/2, tiempos_ga, width, label='GA', 
                   color=COLORES['GA'], edgecolor='black')
    bars3 = ax.bar(x + width/2, tiempos_ts, width, label='TS', 
                   color=COLORES['TS'], edgecolor='black')
    bars4 = ax.bar(x + width*1.5, tiempos_hy, width, label='Híbrido', 
                   color=COLORES['Hybrid'], edgecolor='black')
    
    ax.set_xlabel('Instancia')
    ax.set_ylabel('Tiempo de Ejecución (segundos)')
    ax.set_title('Comparación de Tiempos de Ejecución')
    ax.set_xticks(x)
    ax.set_xticklabels([i.replace('_', '\n') for i in instancias])
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    
    for dest, carpeta in carpetas.items():
        filepath = os.path.join(carpeta, 'benchmark_tiempos_ejecucion.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"   [OK] {dest}: benchmark_tiempos_ejecucion.png")
    
    plt.close()


def grafico_4_performance_profile(resultados, carpetas):
    """
    Gráfico 4: Performance profile (estándar en optimización).
    Muestra la fracción de instancias resueltas dentro de un factor τ del mejor.
    """
    instancias = [k for k in resultados.keys() if k != 'metadata']
    algoritmos = ['GA', 'TS', 'Hybrid']
    
    # Calcular ratios (resultado / mejor resultado por instancia)
    ratios = {algo: [] for algo in algoritmos}
    
    for inst in instancias:
        data = resultados[inst]
        resultados_inst = [data['algoritmos'][a]['media'] for a in algoritmos]
        mejor = min(resultados_inst)
        
        for algo in algoritmos:
            ratio = data['algoritmos'][algo]['media'] / mejor if mejor > 0 else 1
            ratios[algo].append(ratio)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Crear performance profile
    tau_max = 2.0
    tau_values = np.linspace(1.0, tau_max, 100)
    
    for algo in algoritmos:
        probs = []
        for tau in tau_values:
            fraccion = sum(1 for r in ratios[algo] if r <= tau) / len(ratios[algo])
            probs.append(fraccion)
        ax.plot(tau_values, probs, label=algo, color=COLORES[algo], linewidth=2)
    
    ax.set_xlabel('Factor de rendimiento (τ)')
    ax.set_ylabel('Fracción de instancias')
    ax.set_title('Performance Profile')
    ax.legend(loc='lower right')
    ax.set_xlim(1.0, tau_max)
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3)
    
    # Añadir nota explicativa
    ax.text(0.05, 0.95, 'τ=1 → mejor resultado\nCurva más alta = mejor algoritmo',
            transform=ax.transAxes, ha='left', va='top', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    
    for dest, carpeta in carpetas.items():
        filepath = os.path.join(carpeta, 'benchmark_performance_profile.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"   [OK] {dest}: benchmark_performance_profile.png")
    
    plt.close()


def grafico_5_resumen_general(resultados, carpetas):
    """
    Gráfico 5: Resumen tipo "scorecard" con métricas principales.
    """
    instancias = [k for k in resultados.keys() if k != 'metadata']
    algoritmos = ['GA', 'TS', 'Hybrid']
    
    # Calcular métricas resumen
    metricas = {}
    for algo in algoritmos:
        gaps = []
        tiempos = []
        for inst in instancias:
            data = resultados[inst]
            gap = data['algoritmos'][algo].get('gap_pct', 0) or 0
            gaps.append(gap)
            tiempos.append(data['algoritmos'][algo]['tiempo_medio'])
        
        metricas[algo] = {
            'gap_promedio': np.mean(gaps),
            'tiempo_promedio': np.mean(tiempos),
            'optimos': sum(1 for g in gaps if g == 0)
        }
    
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    
    # Panel 1: Gap promedio
    ax1 = axes[0]
    vals = [metricas[a]['gap_promedio'] for a in algoritmos]
    bars1 = ax1.bar(algoritmos, vals, color=[COLORES[a] for a in algoritmos], edgecolor='black')
    ax1.set_ylabel('Gap (%)')
    ax1.set_title('Gap Promedio vs Óptimo')
    ax1.axhline(y=5, color='red', linestyle='--', alpha=0.5)
    for bar, val in zip(bars1, vals):
        ax1.annotate(f'{val:.1f}%', xy=(bar.get_x() + bar.get_width()/2, val + 0.5),
                    ha='center', fontsize=10)
    
    # Panel 2: Tiempo promedio
    ax2 = axes[1]
    vals = [metricas[a]['tiempo_promedio'] for a in algoritmos]
    bars2 = ax2.bar(algoritmos, vals, color=[COLORES[a] for a in algoritmos], edgecolor='black')
    ax2.set_ylabel('Tiempo (s)')
    ax2.set_title('Tiempo Promedio de Ejecución')
    for bar, val in zip(bars2, vals):
        ax2.annotate(f'{val:.2f}s', xy=(bar.get_x() + bar.get_width()/2, val + 0.02),
                    ha='center', fontsize=10)
    
    # Panel 3: Óptimos encontrados
    ax3 = axes[2]
    vals = [metricas[a]['optimos'] for a in algoritmos]
    bars3 = ax3.bar(algoritmos, vals, color=[COLORES[a] for a in algoritmos], edgecolor='black')
    ax3.set_ylabel('Cantidad')
    ax3.set_title(f'Óptimos Encontrados (de {len(instancias)})')
    ax3.set_ylim(0, len(instancias) + 0.5)
    for bar, val in zip(bars3, vals):
        ax3.annotate(f'{val}', xy=(bar.get_x() + bar.get_width()/2, val + 0.1),
                    ha='center', fontsize=10, fontweight='bold')
    
    plt.suptitle('Resumen de Comparación con Benchmarks', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    for dest, carpeta in carpetas.items():
        filepath = os.path.join(carpeta, 'benchmark_resumen_general.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"   [OK] {dest}: benchmark_resumen_general.png")
    
    plt.close()


def generar_todos_los_graficos():
    """Genera todos los gráficos de benchmarks."""
    print("\n" + "=" * 60)
    print("GENERANDO GRÁFICOS DE BENCHMARKS")
    print("=" * 60)
    
    resultados = cargar_resultados()
    carpetas = crear_directorios()
    
    print(f"\n📁 Guardando en:")
    for dest, path in carpetas.items():
        print(f"   {dest}: {path}")
    
    print("\n📊 Generando gráficos...")
    
    # Gráfico 1: Comparación por instancia
    print("\n[1/5] Comparación de algoritmos por instancia")
    grafico_1_comparacion_instancias(resultados, carpetas)
    
    # Gráfico 2: Gap vs óptimo
    print("\n[2/5] Gap promedio vs óptimo")
    grafico_2_gap_vs_optimo(resultados, carpetas)
    
    # Gráfico 3: Tiempos de ejecución
    print("\n[3/5] Tiempos de ejecución")
    grafico_3_tiempos_ejecucion(resultados, carpetas)
    
    # Gráfico 4: Performance profile
    print("\n[4/5] Performance profile")
    grafico_4_performance_profile(resultados, carpetas)
    
    # Gráfico 5: Resumen general
    print("\n[5/5] Resumen general")
    grafico_5_resumen_general(resultados, carpetas)
    
    print("\n" + "=" * 60)
    print("[OK] 5 gráficos generados en:")
    print(f"     - docs/tesis/figuras/")
    print(f"     - docs/presentacion/figuras/")
    print("=" * 60)


if __name__ == "__main__":
    generar_todos_los_graficos()
