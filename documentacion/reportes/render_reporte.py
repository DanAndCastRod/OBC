"""
Renderizador del Informe de Avance — Fases 1-3.

Genera diagramas ilustrativos (matplotlib) y renderiza el reporte
Markdown a HTML con estilo academico, listo para exportar a PDF.

IMPORTANTE: Este script es de SOLO LECTURA. No modifica datos
existentes ni interrumpe procesos en ejecucion.

Uso:
    python documentacion/reportes/render_reporte.py

Salida:
    documentacion/reportes/figuras/   — Diagramas PNG
    documentacion/reportes/reporte_avance_fases_1_3.html — Reporte HTML

Autor: Daniel Andres Castaneda Rodriguez
Fecha: Marzo 2026
"""

from __future__ import annotations

import sys
from pathlib import Path
import textwrap

# Configurar paths
REPORT_DIR = Path(__file__).parent
FIGURAS_DIR = REPORT_DIR / "figuras"
FIGURAS_DIR.mkdir(exist_ok=True)

# Agregar root al path para imports (solo lectura)
ROOT = REPORT_DIR.parent.parent
sys.path.insert(0, str(ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np


# ============================================================
# Paleta de colores corporativa
# ============================================================
COLORS = {
    "teal":     "#008B8B",
    "teal_lt":  "#66C2C2",
    "orange":   "#EB8A3E",
    "slate":    "#365660",
    "gray":     "#555555",
    "bg":       "#F8FAFC",
    "phase1":   "#2E86AB",
    "phase2":   "#A23B72",
    "phase3":   "#F18F01",
    "phase4":   "#C73E1D",
    "phase5":   "#95A5A6",
    "ga":       "#3498db",
    "sa":       "#e74c3c",
    "de":       "#2ecc71",
    "gasa":     "#9b59b6",
    "cbc":      "#f39c12",
    "baseline": "#95a5a6",
}


def _style_axis(ax, title="", xlabel="", ylabel=""):
    """Aplicar estilo consistente a un eje."""
    ax.set_title(title, fontsize=13, fontweight="bold", color="#1E293B", pad=12)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10, color="#475569")
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10, color="#475569")
    ax.tick_params(colors="#475569", labelsize=9)
    ax.grid(axis="y", alpha=0.2, linestyle="--", color="#94A3B8")
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#E2E8F0")
    ax.spines["left"].set_color("#E2E8F0")


# ============================================================
# Diagrama 1: Cronograma Gantt de las 5 fases
# ============================================================
def fig_gantt():
    """Cronograma tipo Gantt con estado de cada fase."""
    fig, ax = plt.subplots(figsize=(11, 4))

    phases = [
        ("Fase 1: Modelo MILP",      1,  8, COLORS["phase1"], "Completada"),
        ("Fase 2: Metaheuristicas",   9, 18, COLORS["phase2"], "Completada"),
        ("Fase 3: Instancias",       19, 22, COLORS["phase3"], "Completada"),
        ("Fase 4: Experimentos",     23, 27, COLORS["phase4"], "En ejecucion"),
        ("Fase 5: Tesis",            28, 30, COLORS["phase5"], "Pendiente"),
    ]

    y_pos = list(range(len(phases)))[::-1]
    for i, (name, start, end, color, status) in enumerate(phases):
        y = y_pos[i]
        width = end - start + 1
        alpha = 1.0 if "Completada" in status else (0.7 if "ejecucion" in status else 0.35)
        bar = ax.barh(y, width, left=start, height=0.55, color=color, alpha=alpha,
                      edgecolor="white", linewidth=1.5, zorder=3)

        # Label dentro de la barra
        ax.text(start + width / 2, y, f"{name}",
                ha="center", va="center", fontsize=8.5, fontweight="bold",
                color="white" if alpha > 0.5 else "#555", zorder=4)

        # Estado al final
        icon = {"Completada": "✓", "En ejecucion": "⟳", "Pendiente": "○"}
        ax.text(end + 0.6, y, f"{icon.get(status, '')} {status}",
                ha="left", va="center", fontsize=7.5,
                color=color if alpha > 0.5 else "#999",
                fontstyle="italic")

    # Linea de "hoy" (semana ~23)
    ax.axvline(x=23, color=COLORS["orange"], linewidth=1.5, linestyle="--", alpha=0.7, zorder=2)
    ax.text(23, len(phases) - 0.3, "Hoy", ha="center", va="bottom",
            fontsize=8, color=COLORS["orange"], fontweight="bold")

    ax.set_xlim(0, 34)
    ax.set_yticks([])
    ax.set_xlabel("Semanas", fontsize=10, color="#475569")
    ax.set_title("Cronograma del Proyecto (30 semanas)", fontsize=14,
                 fontweight="bold", color="#1E293B", pad=15)

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors="#475569", labelsize=9)
    ax.grid(axis="x", alpha=0.15, linestyle="--")
    ax.set_axisbelow(True)

    fig.tight_layout()
    fig.savefig(FIGURAS_DIR / "01_cronograma_gantt.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("  [1/7] Cronograma Gantt")


# ============================================================
# Diagrama 2: Pipeline del modelo (Fase 1)
# ============================================================
def fig_pipeline_modelo():
    """Pipeline: cromosoma -> repair -> decode -> evaluate."""
    fig, ax = plt.subplots(figsize=(11, 3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2)
    ax.axis("off")
    ax.set_title("Pipeline de Evaluacion del Modelo MILP", fontsize=14,
                 fontweight="bold", color="#1E293B", pad=15)

    boxes = [
        (0.3, "Cromosoma\n(y, q)",     COLORS["phase2"], "white"),
        (2.2, "Reparacion\nrepair()",   "#6C757D",        "white"),
        (4.1, "Decodificador\ndecode()", COLORS["phase1"], "white"),
        (6.0, "Evaluador\nevaluate()",  COLORS["phase1"], "white"),
        (7.9, "Restricciones\ncheck()",  COLORS["phase3"], "white"),
        (9.0, "Z, factible",           COLORS["teal"],    "white"),
    ]

    for x, label, color, tc in boxes:
        w = 1.6 if x < 8.5 else 0.9
        rect = FancyBboxPatch((x, 0.6), w, 0.8, boxstyle="round,pad=0.08",
                              facecolor=color, edgecolor="white", linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w / 2, 1.0, label, ha="center", va="center",
                fontsize=8, fontweight="bold", color=tc)

    # Flechas
    arrow_kw = dict(arrowstyle="->", color="#94A3B8", lw=2, connectionstyle="arc3,rad=0")
    arrow_positions = [(1.9, 2.2), (3.8, 4.1), (5.7, 6.0), (7.6, 7.9)]
    for x_start, x_end in arrow_positions:
        ax.annotate("", xy=(x_end, 1.0), xytext=(x_start, 1.0),
                    arrowprops=arrow_kw)

    # Segunda etapa label
    ax.text(5.1, 0.35, "Variables de 2da etapa: v (ventas), I (inventario), u (insatisfaccion)",
            ha="center", va="center", fontsize=7.5, color="#94A3B8", fontstyle="italic")

    fig.tight_layout()
    fig.savefig(FIGURAS_DIR / "02_pipeline_modelo.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("  [2/7] Pipeline del Modelo")


# ============================================================
# Diagrama 3: Arquitectura de metaheuristicas (Fase 2)
# ============================================================
def fig_arquitectura_mh():
    """Diagrama UML simplificado de la jerarquia de clases."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("Arquitectura de Metaheuristicas", fontsize=14,
                 fontweight="bold", color="#1E293B", pad=15)

    # Base class
    base_x, base_y = 3.5, 4.5
    base_w, base_h = 3.0, 1.2
    rect = FancyBboxPatch((base_x, base_y), base_w, base_h,
                          boxstyle="round,pad=0.06",
                          facecolor=COLORS["slate"], edgecolor="white", linewidth=2)
    ax.add_patch(rect)
    ax.text(base_x + base_w/2, base_y + base_h - 0.25,
            "BaseMetaheuristic (ABC)", ha="center", va="center",
            fontsize=9, fontweight="bold", color="white")
    ax.text(base_x + base_w/2, base_y + 0.35,
            "solve()  evaluate_fitness()\ngenerate_random()  convergence_data()",
            ha="center", va="center", fontsize=7, color="#B0C4DE", family="monospace")

    # Children
    children = [
        (0.2,  1.5, "GeneticAlgorithm",       COLORS["ga"],   "pop=80, cx=0.74\nmut=0.09, elite=3"),
        (2.6,  1.5, "SimulatedAnnealing",      COLORS["sa"],   "T₀=204K, cool=0.78\nreheat=1.29"),
        (5.0,  1.5, "DifferentialEvolution",   COLORS["de"],   "pop=51, CR=0.51\nF=0.32, best/1/bin"),
        (7.4,  1.5, "HybridGASA",             COLORS["gasa"], "GA + SA local\ncada 9 gen, top-10"),
    ]

    for cx, cy, name, color, params in children:
        cw, ch = 2.2, 1.2
        rect = FancyBboxPatch((cx, cy), cw, ch,
                              boxstyle="round,pad=0.06",
                              facecolor=color, edgecolor="white", linewidth=2, alpha=0.85)
        ax.add_patch(rect)
        ax.text(cx + cw/2, cy + ch - 0.3, name,
                ha="center", va="center", fontsize=7.5, fontweight="bold", color="white")
        ax.text(cx + cw/2, cy + 0.35, params,
                ha="center", va="center", fontsize=6.5, color="white", alpha=0.9,
                family="monospace")

        # Linea de herencia
        ax.plot([cx + cw/2, cx + cw/2], [cy + ch, base_y],
                color="#B0C4DE", linewidth=1.2, linestyle="-", alpha=0.5)
        ax.plot([cx + cw/2, base_x + base_w/2], [base_y, base_y],
                color="#B0C4DE", linewidth=1.2, linestyle="-", alpha=0.5)

    # Shared encoding
    enc_x, enc_y = 7.5, 4.5
    rect = FancyBboxPatch((enc_x, enc_y), 2.3, 1.2,
                          boxstyle="round,pad=0.06",
                          facecolor=COLORS["phase3"], edgecolor="white", linewidth=2, alpha=0.8)
    ax.add_patch(rect)
    ax.text(enc_x + 1.15, enc_y + 0.85, "encoding.py", ha="center", va="center",
            fontsize=8, fontweight="bold", color="white")
    ax.text(enc_x + 1.15, enc_y + 0.35,
            "crossover, mutate\nrepair, neighborhood",
            ha="center", va="center", fontsize=6.5, color="white", alpha=0.9)

    ax.annotate("", xy=(base_x + base_w, 5.1), xytext=(enc_x, 5.1),
                arrowprops=dict(arrowstyle="<-", color="#B0C4DE", lw=1.5, linestyle="--"))
    ax.text(7.2, 5.3, "usa", ha="center", fontsize=7, color="#94A3B8", fontstyle="italic")

    fig.tight_layout()
    fig.savefig(FIGURAS_DIR / "03_arquitectura_mh.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("  [3/7] Arquitectura de Metaheuristicas")


# ============================================================
# Diagrama 4: Benchmark de algoritmos (Fase 2)
# ============================================================
def fig_benchmark_gap():
    """Grafico de barras: gap vs exacto por algoritmo."""
    fig, ax = plt.subplots(figsize=(8, 4.5))

    algos = ["CBC\n(Exacto)", "GA", "SA", "DE", "GA-SA"]
    gaps = [0.0, 1.87, 2.05, 1.81, 1.49]
    colors = [COLORS["cbc"], COLORS["ga"], COLORS["sa"], COLORS["de"], COLORS["gasa"]]

    bars = ax.bar(algos, gaps, color=colors, width=0.55, edgecolor="white",
                  linewidth=1.5, alpha=0.85, zorder=3)

    # Valor sobre cada barra
    for bar, gap in zip(bars, gaps):
        y = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, y + 0.06,
                f"{gap:.2f}%", ha="center", va="bottom",
                fontsize=10, fontweight="bold", color="#1E293B")

    # Linea de referencia H2 (2%)
    ax.axhline(y=2.0, color=COLORS["orange"], linewidth=1.5, linestyle="--", alpha=0.7, zorder=2)
    ax.text(4.4, 2.08, "Umbral H2: 2%", fontsize=7.5, color=COLORS["orange"],
            ha="right", fontstyle="italic")

    _style_axis(ax, title="Gap de Optimalidad vs Solver Exacto (CBC)",
                ylabel="Gap (%)")
    ax.set_ylim(0, 2.5)

    fig.tight_layout()
    fig.savefig(FIGURAS_DIR / "04_benchmark_gap.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("  [4/7] Benchmark Gap")


# ============================================================
# Diagrama 5: Perfiles de instancias (Fase 3)
# ============================================================
def fig_perfiles_instancias():
    """Comparacion visual de los 5 perfiles de instancias."""
    fig, axes = plt.subplots(1, 3, figsize=(11, 4))

    profiles = ["Toy", "Small", "Medium", "Large", "Industrial"]
    n_f =      [3,     6,       6,        8,       10]
    n_t =      [4,     12,      12,       24,      52]
    n_w =      [5,     20,      50,       100,     500]

    bar_colors = [COLORS["phase1"], COLORS["phase2"], COLORS["phase3"],
                  COLORS["phase4"], COLORS["phase5"]]

    # n_f (Formas de corte)
    axes[0].bar(profiles, n_f, color=bar_colors, alpha=0.85, edgecolor="white", linewidth=1.5)
    _style_axis(axes[0], title="Formas de Corte ($n_f$)", ylabel="Cantidad")
    for i, v in enumerate(n_f):
        axes[0].text(i, v + 0.2, str(v), ha="center", fontsize=9, fontweight="bold", color="#1E293B")
    axes[0].tick_params(axis='x', rotation=25)

    # n_t (Periodos)
    axes[1].bar(profiles, n_t, color=bar_colors, alpha=0.85, edgecolor="white", linewidth=1.5)
    _style_axis(axes[1], title="Periodos ($n_t$)", ylabel="Cantidad")
    for i, v in enumerate(n_t):
        axes[1].text(i, v + 0.5, str(v), ha="center", fontsize=9, fontweight="bold", color="#1E293B")
    axes[1].tick_params(axis='x', rotation=25)

    # n_w (Escenarios)
    axes[2].bar(profiles, n_w, color=bar_colors, alpha=0.85, edgecolor="white", linewidth=1.5)
    _style_axis(axes[2], title="Escenarios ($n_\\omega$)", ylabel="Cantidad")
    for i, v in enumerate(n_w):
        axes[2].text(i, v + 8, str(v), ha="center", fontsize=9, fontweight="bold", color="#1E293B")
    axes[2].tick_params(axis='x', rotation=25)

    fig.suptitle("Perfiles del Banco de Instancias (15 instancias, 3 seeds por perfil)",
                 fontsize=13, fontweight="bold", color="#1E293B", y=1.02)
    fig.tight_layout()
    fig.savefig(FIGURAS_DIR / "05_perfiles_instancias.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("  [5/7] Perfiles de Instancias")


# ============================================================
# Diagrama 6: Resumen de tests por fase
# ============================================================
def fig_tests_summary():
    """Barras horizontales: tests por modulo, coloreados por fase."""
    fig, ax = plt.subplots(figsize=(9, 5))

    modules = [
        "test_parameters",
        "test_constraints",
        "test_solver",
        "test_encoding",
        "test_ga",
        "test_sa",
        "test_de",
        "test_ga_sa",
        "test_generator",
        "test_calibration",
        "test_baseline",
    ]
    counts = [16, 15, 7, 15, 7, 8, 8, 5, 79, 44, 25]
    phases = [1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 4]
    phase_colors = {1: COLORS["phase1"], 2: COLORS["phase2"],
                    3: COLORS["phase3"], 4: COLORS["phase4"]}

    colors = [phase_colors[p] for p in phases]
    y_pos = range(len(modules))

    bars = ax.barh(y_pos, counts, color=colors, height=0.6,
                   edgecolor="white", linewidth=1.5, alpha=0.85, zorder=3)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(modules, fontsize=8.5, family="monospace")
    ax.invert_yaxis()

    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                str(count), ha="left", va="center", fontsize=9,
                fontweight="bold", color="#1E293B")

    # Leyenda
    legend_patches = [
        mpatches.Patch(color=COLORS["phase1"], label="Fase 1: Modelo MILP"),
        mpatches.Patch(color=COLORS["phase2"], label="Fase 2: Metaheuristicas"),
        mpatches.Patch(color=COLORS["phase3"], label="Fase 3: Instancias"),
        mpatches.Patch(color=COLORS["phase4"], label="Fase 4: Experimentos"),
    ]
    ax.legend(handles=legend_patches, loc="lower right", fontsize=8, framealpha=0.9)

    _style_axis(ax, title="Suite de Tests Automatizados — 234 tests, 0 fallos",
                xlabel="Numero de tests")
    ax.grid(axis="x", alpha=0.15, linestyle="--")

    fig.tight_layout()
    fig.savefig(FIGURAS_DIR / "06_tests_summary.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("  [6/7] Resumen de Tests")


# ============================================================
# Diagrama 7: Calibracion - proporciones anatomicas
# ============================================================
def fig_calibracion():
    """Pie chart de proporciones anatomicas calibradas + barras de costos."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # Pie: proporciones anatomicas
    parts = ["Pechuga", "Muslo", "Contramuslo", "Ala", "Menudencias", "Otros"]
    props = [0.30, 0.18, 0.14, 0.08, 0.05, 0.25]
    pie_colors = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#2ecc71", "#95a5a6"]

    wedges, texts, autotexts = axes[0].pie(
        props, labels=parts, autopct="%1.0f%%", colors=pie_colors,
        startangle=90, pctdistance=0.75,
        wedgeprops=dict(width=0.5, edgecolor="white", linewidth=2),
        textprops=dict(fontsize=8.5, color="#1E293B"),
    )
    for at in autotexts:
        at.set_fontsize(7.5)
        at.set_fontweight("bold")
        at.set_color("white")

    axes[0].set_title("Proporciones Anatomicas\n(Fuente: FENAVI, Cobb 500)",
                      fontsize=11, fontweight="bold", color="#1E293B", pad=10)

    # Barras: precios COP/kg
    products = ["Pechuga", "Muslo", "C.muslo", "Ala", "Menud.", "Otros"]
    prices_min = [12000, 8000, 7000, 5000, 3000, 2000]
    prices_max = [15000, 10000, 9000, 7500, 5000, 4000]
    prices_mid = [(lo + hi) / 2 for lo, hi in zip(prices_min, prices_max)]
    prices_err = [(hi - lo) / 2 for lo, hi in zip(prices_min, prices_max)]

    bars = axes[1].barh(products, prices_mid, xerr=prices_err,
                        color=pie_colors, alpha=0.85, height=0.5,
                        edgecolor="white", linewidth=1.5, capsize=3,
                        error_kw={"ecolor": "#94A3B8", "linewidth": 1.2})
    axes[1].invert_yaxis()
    _style_axis(axes[1], title="Precios de Venta (COP/kg)\n(Fuente: FENAVI 2024)",
                xlabel="COP/kg")
    axes[1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))

    fig.tight_layout()
    fig.savefig(FIGURAS_DIR / "07_calibracion.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("  [7/8] Calibracion")


# ============================================================
# Diagrama 8: Resumen de calibracion Optuna
# ============================================================
def fig_optuna_tuning():
    """Barras comparativas: mejor fitness + tiempo de calibracion por algoritmo."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    algos = ["GA", "SA", "DE", "GA-SA"]
    best_z = [396_845_202, 396_512_715, 397_086_621, 396_887_162]
    elapsed_h = [1415.5 / 3600, 9190.5 / 3600, 4784.1 / 3600, 62929.8 / 3600]
    timeouts = [0, 4, 0, 0]
    algo_colors = [COLORS["ga"], COLORS["sa"], COLORS["de"], COLORS["gasa"]]

    # Panel izquierdo: Mejor Z
    bars1 = axes[0].bar(algos, [z / 1e6 for z in best_z], color=algo_colors,
                        width=0.5, edgecolor="white", linewidth=1.5, alpha=0.85, zorder=3)
    for bar, z in zip(bars1, best_z):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                     f"{z/1e6:.1f}M", ha="center", va="bottom",
                     fontsize=9, fontweight="bold", color="#1E293B")
    _style_axis(axes[0], title="Mejor Fitness Alcanzado (30 trials)",
                ylabel="Z (millones COP)")
    axes[0].set_ylim(395, 398)

    # Panel derecho: Tiempo de calibracion
    bars2 = axes[1].bar(algos, elapsed_h, color=algo_colors,
                        width=0.5, edgecolor="white", linewidth=1.5, alpha=0.85, zorder=3)
    for bar, t, to in zip(bars2, elapsed_h, timeouts):
        label = f"{t:.1f}h"
        if to > 0:
            label += f"\n({to} timeouts)"
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                     label, ha="center", va="bottom",
                     fontsize=8.5, fontweight="bold", color="#1E293B")
    _style_axis(axes[1], title="Tiempo de Calibracion Optuna",
                ylabel="Horas")

    fig.suptitle("Calibracion Automatica de Hiperparametros con Optuna (TPE, seed=42)",
                 fontsize=13, fontweight="bold", color="#1E293B", y=1.02)
    fig.tight_layout()
    fig.savefig(FIGURAS_DIR / "08_optuna_tuning.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("  [8/8] Optuna Tuning")


# ============================================================
# Renderizador HTML
# ============================================================

HTML_TEMPLATE = textwrap.dedent("""\
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe Parcial de Avance — Fases 1-3</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700&family=Space+Grotesk:wght@400;500;700&display=swap');

        :root {
            --color-bg: #FFFFFF;
            --color-text: #1E293B;
            --color-text-body: #475569;
            --color-text-light: #94A3B8;
            --color-border: #E2E8F0;
            --color-accent: #008B8B;
            --color-phase1: #2E86AB;
            --color-phase2: #A23B72;
            --color-phase3: #F18F01;
            --color-phase4: #C73E1D;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', sans-serif;
            font-size: 11pt;
            line-height: 1.7;
            color: var(--color-text-body);
            background: var(--color-bg);
            max-width: 850px;
            margin: 0 auto;
            padding: 40px 50px;
        }

        @media print {
            body { padding: 20px 30px; font-size: 10pt; }
            .page-break { page-break-before: always; }
            h2 { page-break-before: always; }
            h2:first-of-type { page-break-before: avoid; }
            figure { page-break-inside: avoid; }
            table { page-break-inside: avoid; }
        }

        /* Encabezado */
        .header {
            text-align: center;
            border-bottom: 3px solid var(--color-accent);
            padding-bottom: 25px;
            margin-bottom: 35px;
        }

        .header h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 18pt;
            color: var(--color-text);
            line-height: 1.3;
            margin-bottom: 12px;
        }

        .header .meta {
            font-size: 9.5pt;
            color: var(--color-text-light);
            line-height: 1.8;
        }

        .header .meta strong { color: var(--color-text-body); }

        /* Secciones */
        h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 15pt;
            color: var(--color-text);
            margin-top: 35px;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--color-border);
        }

        h3 {
            font-family: 'Outfit', sans-serif;
            font-size: 12pt;
            color: var(--color-text);
            margin-top: 22px;
            margin-bottom: 10px;
        }

        h4 {
            font-size: 10.5pt;
            font-weight: 600;
            color: var(--color-text);
            margin-top: 15px;
            margin-bottom: 6px;
        }

        p { margin-bottom: 10px; }

        /* Tablas */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 9.5pt;
        }

        thead th {
            background: #F1F5F9;
            color: var(--color-text);
            font-weight: 600;
            font-family: 'Space Grotesk', monospace;
            padding: 8px 10px;
            border-bottom: 2px solid var(--color-border);
            text-align: left;
        }

        tbody td {
            padding: 7px 10px;
            border-bottom: 1px solid var(--color-border);
        }

        tbody tr:hover { background: #F8FAFC; }

        td:first-child { font-weight: 500; }

        .center { text-align: center; }
        .right { text-align: right; }

        td.number, th.number {
            font-family: 'Space Grotesk', monospace;
            text-align: right;
        }

        /* Figuras */
        figure {
            margin: 20px 0;
            text-align: center;
        }

        figure img {
            max-width: 100%;
            border: 1px solid var(--color-border);
            border-radius: 6px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        }

        figcaption {
            margin-top: 8px;
            font-size: 9pt;
            color: var(--color-text-light);
            font-style: italic;
        }

        /* Codigo */
        code {
            font-family: 'Space Grotesk', monospace;
            font-size: 9pt;
            background: #F1F5F9;
            padding: 1px 5px;
            border-radius: 3px;
            color: var(--color-text);
        }

        pre {
            background: #F8FAFC;
            border: 1px solid var(--color-border);
            border-radius: 6px;
            padding: 12px 16px;
            overflow-x: auto;
            font-family: 'Space Grotesk', monospace;
            font-size: 8.5pt;
            line-height: 1.5;
            margin: 12px 0;
        }

        /* Badges */
        .badge {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 8pt;
            font-weight: 600;
            color: white;
        }
        .badge-done { background: #22C55E; }
        .badge-progress { background: var(--color-phase4); }
        .badge-pending { background: var(--color-text-light); }

        /* Firma */
        .signature {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid var(--color-border);
            text-align: left;
        }

        /* Highlight box */
        .highlight-box {
            background: #F0FDFA;
            border-left: 4px solid var(--color-accent);
            padding: 12px 16px;
            margin: 15px 0;
            border-radius: 0 6px 6px 0;
            font-size: 10pt;
        }

        ul, ol { margin-left: 20px; margin-bottom: 10px; }
        li { margin-bottom: 3px; }
    </style>
</head>
<body>

<!-- ENCABEZADO -->
<div class="header">
    <h1>Informe Parcial de Avance de Investigacion</h1>
    <div class="meta">
        <strong>Titulo:</strong> Modelo de Optimizacion para la Planificacion de la Produccion de Coproductos Avicolas Perecibles bajo Demanda Estocastica: Un Enfoque con Metaheuristicas Hibridas<br>
        <strong>Autor:</strong> Daniel Andres Castaneda Rodriguez<br>
        <strong>Directora:</strong> Ing. Eliana Mirledy Ocampo Toro, PhD.<br>
        <strong>Programa:</strong> Maestria en Investigacion Operativa y Estadistica — Universidad Tecnologica de Pereira<br>
        <strong>Fecha:</strong> 3 de marzo de 2026 &nbsp;|&nbsp; <strong>Periodo:</strong> Fases 1–3 (Semanas 1–22)
    </div>
</div>

<!-- 1. INTRODUCCION -->
<h2>1. Introduccion</h2>
<p>El presente informe documenta el avance del proyecto de investigacion correspondiente a las primeras tres fases de un cronograma de cinco. El trabajo consiste en la formulacion, implementacion computacional y evaluacion de un modelo de programacion lineal entera mixta (MILP) estocastico para la planificacion de la produccion de coproductos avicolas perecibles, complementado por cuatro algoritmos metaheuristicos (GA, SA, DE y un hibrido GA-SA) calibrados para resolver instancias de escala industrial.</p>

<div class="highlight-box">
    <strong>Estado general:</strong> Fases 1, 2 y 3 completadas y validadas con <strong>234 tests automatizados</strong>. Fase 4 (Experimentacion) en ejecucion activa. Fase 5 (Tesis y sustentacion) pendiente.
</div>

<figure>
    <img src="figuras/01_cronograma_gantt.png" alt="Cronograma Gantt">
    <figcaption>Figura 1. Cronograma general del proyecto (30 semanas). La linea punteada indica el momento actual.</figcaption>
</figure>

<h3>1.1 Cronograma General</h3>
<table>
    <thead>
        <tr><th class="center">Fase</th><th>Alcance</th><th class="center">Semanas</th><th class="center">Estado</th></tr>
    </thead>
    <tbody>
        <tr><td class="center"><strong>1</strong></td><td>Formulacion del modelo MILP estocastico</td><td class="center">1–8</td><td class="center"><span class="badge badge-done">Completada</span></td></tr>
        <tr><td class="center"><strong>2</strong></td><td>Diseno e implementacion de metaheuristicas</td><td class="center">9–18</td><td class="center"><span class="badge badge-done">Completada</span></td></tr>
        <tr><td class="center"><strong>3</strong></td><td>Generacion de datos y escenarios de prueba</td><td class="center">19–22</td><td class="center"><span class="badge badge-done">Completada</span></td></tr>
        <tr><td class="center"><strong>4</strong></td><td>Diseno experimental, ejecucion y analisis estadistico</td><td class="center">23–27</td><td class="center"><span class="badge badge-progress">En ejecucion</span></td></tr>
        <tr><td class="center"><strong>5</strong></td><td>Validacion, escritura de tesis y sustentacion</td><td class="center">28–30</td><td class="center"><span class="badge badge-pending">Pendiente</span></td></tr>
    </tbody>
</table>

<!-- 2. FASE 1 -->
<h2>2. Fase 1: Formulacion del Modelo Matematico MILP</h2>

<h3>2.1 Objetivo</h3>
<p>Implementar el modelo MILP estocastico de dos etapas como codigo Python ejecutable y validarlo con el solver CBC, de forma que sirva como (a) evaluador de fitness para las metaheuristicas y (b) baseline exacto para el calculo del gap de optimalidad.</p>

<h3>2.2 Modelo Matematico</h3>
<p>El problema se formula como un <em>lot-sizing estocastico multi-periodo</em> con coproductos perecibles. Las variables de decision se dividen en dos etapas:</p>
<ul>
    <li><strong>Primera etapa (determinista):</strong> <em>y<sub>t</sub></em> ∈ {0,1} (setup) y <em>q<sub>t</sub></em> ∈ [Q<sup>min</sup>, Q<sup>max</sup>] (carcasas procesadas).</li>
    <li><strong>Segunda etapa (por escenario ω):</strong> <em>v<sub>ftω</sub></em> (ventas), <em>I<sub>ftω</sub></em> (inventario), <em>u<sub>ftω</sub></em> (insatisfaccion).</li>
</ul>
<p>La funcion objetivo maximiza el beneficio esperado total (Eq. 1) sujeto a 7 restricciones: balance de material (Eq. 2), satisfaccion de demanda (Eq. 3), capacidad maxima y minima (Eqs. 4-5), limite de ventas (Eq. 6), perecibilidad con descarte total (Eq. 7) y dominios (Eq. 8). La complejidad del problema es <strong>NP-hard</strong> (Florian 1980, Bitran &amp; Yanasse 1982).</p>

<figure>
    <img src="figuras/02_pipeline_modelo.png" alt="Pipeline del Modelo">
    <figcaption>Figura 2. Pipeline de evaluacion: el cromosoma (y, q) se repara, decodifica a una solucion completa via asignacion greedy, y se evalua con la funcion objetivo y las restricciones.</figcaption>
</figure>

<h3>2.3 Modulos Implementados</h3>
<table>
    <thead>
        <tr><th>Modulo</th><th>Archivo</th><th>Descripcion</th></tr>
    </thead>
    <tbody>
        <tr><td>Parametros</td><td><code>src/model/parameters.py</code></td><td>Clase <code>ProblemInstance</code> con carga/exportacion YAML y 15+ validaciones</td></tr>
        <tr><td>Solucion</td><td><code>src/model/solution.py</code></td><td>Clase <code>Solution</code> + <code>SolutionBreakdown</code> (5 componentes de Z)</td></tr>
        <tr><td>F. Objetivo</td><td><code>src/model/objective.py</code></td><td>Evaluador vectorizado con <code>numpy.einsum</code></td></tr>
        <tr><td>Restricciones</td><td><code>src/model/constraints.py</code></td><td>7 restricciones (Eqs. 2-8) incluyendo perecibilidad</td></tr>
        <tr><td>Decodificador</td><td><code>src/model/decoder.py</code></td><td>Greedy FIFO con asignacion por rentabilidad descendente</td></tr>
        <tr><td>Solver exacto</td><td><code>src/model/solver.py</code></td><td>PuLP/CBC con soporte HiGHS y Gurobi</td></tr>
    </tbody>
</table>

<h3>2.4 Validacion Cruzada</h3>
<ul>
    <li>Solver CBC encontro el optimo en instancia de referencia (Z* ≈ 275 millones COP).</li>
    <li><code>constraints.check_all()</code> verifica las 7 restricciones sin violaciones.</li>
    <li>Valor Z del evaluador coincide con el del solver (tolerancia &lt; 1.0 COP).</li>
    <li>Se verifica Z<sub>solver</sub> ≥ Z<sub>greedy</sub> (optimalidad correcta).</li>
</ul>
<p><strong>Tests Fase 1:</strong> 38 tests automatizados (16 + 15 + 7), todos aprobados.</p>

<!-- 3. FASE 2 -->
<h2>3. Fase 2: Diseno e Implementacion de Metaheuristicas</h2>

<h3>3.1 Objetivo</h3>
<p>Implementar cuatro algoritmos metaheuristicos con interfaz unificada, codificacion compartida y calibracion automatizada de hiperparametros.</p>

<figure>
    <img src="figuras/03_arquitectura_mh.png" alt="Arquitectura de Metaheuristicas">
    <figcaption>Figura 3. Arquitectura de clases. Los cuatro algoritmos heredan de <code>BaseMetaheuristic</code> y comparten la codificacion de <code>encoding.py</code> para operadores geneticos y vecindarios.</figcaption>
</figure>

<h3>3.2 Algoritmos Implementados</h3>
<h4>a) Algoritmo Genetico (GA)</h4>
<p>Evolucion poblacional con seleccion por torneo, cruce de dos puntos y mutacion combinada (toggle + perturbacion gaussiana). Incorpora elitismo (top-k preservados) y criterio de parada por estancamiento.</p>

<h4>b) Recocido Simulado (SA)</h4>
<p>Busqueda de vecindario con criterio de Metropolis, enfriamiento geometrico y mecanismo de recalentamiento. Incluye auto-estimacion de T<sub>0</sub> para ~80% de aceptacion inicial.</p>

<h4>c) Evolucion Diferencial (DE)</h4>
<p>Mutacion diferencial con estrategias <em>rand/1/bin</em> y <em>best/1/bin</em>, adaptadas a variables mixtas mediante discretizacion. Seleccion greedy: trial reemplaza target solo si su fitness es superior.</p>

<h4>d) Hibrido GA-SA</h4>
<p>Combina la exploracion global del GA con la explotacion local del SA: cada N generaciones se aplica SA como busqueda local a los top-k individuos. Configuracion basada en Akbari-Aghghaleh (2025).</p>

<h3>3.3 Calibracion de Hiperparametros (Optuna/TPE)</h3>
<p>Se utilizo <strong>Optuna</strong> con el sampler TPE (Tree-Parzen Estimator) para calibrar cada algoritmo, ejecutando <strong>30 trials por algoritmo</strong> sobre un conjunto de 5 instancias (3 small + 2 medium), con timeout de 900 s por trial y seed fija (42) para reproducibilidad. Los resultados completos se almacenan en <code>experiments/config/tuning_*.yaml</code>.</p>

<figure>
    <img src="figuras/08_optuna_tuning.png" alt="Optuna Tuning">
    <figcaption>Figura 4. Resumen del proceso de calibracion con Optuna: mejor fitness alcanzado y tiempo de ejecucion por algoritmo.</figcaption>
</figure>

<h4>Tabla 1. Hiperparametros calibrados — Algoritmo Genetico (GA)</h4>
<table>
    <thead><tr><th>Parametro</th><th class="center">Valor calibrado</th><th>Descripcion</th></tr></thead>
    <tbody>
        <tr><td><code>pop_size</code></td><td class="center">80</td><td>Tamano de poblacion</td></tr>
        <tr><td><code>crossover_rate</code></td><td class="center">0.7437</td><td>Tasa de cruce</td></tr>
        <tr><td><code>mutation_rate</code></td><td class="center">0.0889</td><td>Tasa de mutacion</td></tr>
        <tr><td><code>elitism_count</code></td><td class="center">3</td><td>Individuos preservados por elitismo</td></tr>
        <tr><td><code>selection_size</code></td><td class="center">3</td><td>Tamano del torneo de seleccion</td></tr>
    </tbody>
</table>
<p><em>Mejor fitness:</em> 396,845,202 COP &nbsp;|&nbsp; <em>Trials:</em> 30 (0 errores, 0 timeouts) &nbsp;|&nbsp; <em>Tiempo total:</em> 23.6 min</p>

<h4>Tabla 2. Hiperparametros calibrados — Recocido Simulado (SA)</h4>
<table>
    <thead><tr><th>Parametro</th><th class="center">Valor calibrado</th><th>Descripcion</th></tr></thead>
    <tbody>
        <tr><td><code>T_initial</code></td><td class="center">203,952</td><td>Temperatura inicial</td></tr>
        <tr><td><code>T_final</code></td><td class="center">586.3</td><td>Temperatura final</td></tr>
        <tr><td><code>cooling_rate</code></td><td class="center">0.7817</td><td>Tasa de enfriamiento geometrico</td></tr>
        <tr><td><code>max_iterations</code></td><td class="center">27</td><td>Iteraciones por nivel de temperatura</td></tr>
        <tr><td><code>p_toggle</code></td><td class="center">0.4941</td><td>Probabilidad de perturbacion toggle</td></tr>
        <tr><td><code>p_quantity</code></td><td class="center">0.2825</td><td>Probabilidad de perturbacion de cantidad</td></tr>
        <tr><td><code>delta</code></td><td class="center">0.0661</td><td>Magnitud de perturbacion</td></tr>
        <tr><td><code>reheat_factor</code></td><td class="center">1.2870</td><td>Factor de recalentamiento</td></tr>
        <tr><td><code>reheat_threshold</code></td><td class="center">54</td><td>Iteraciones sin mejora para recalentar</td></tr>
    </tbody>
</table>
<p><em>Mejor fitness:</em> 396,512,715 COP &nbsp;|&nbsp; <em>Trials:</em> 30 (0 errores, 4 timeouts) &nbsp;|&nbsp; <em>Tiempo total:</em> 2.55 h</p>

<h4>Tabla 3. Hiperparametros calibrados — Evolucion Diferencial (DE)</h4>
<table>
    <thead><tr><th>Parametro</th><th class="center">Valor calibrado</th><th>Descripcion</th></tr></thead>
    <tbody>
        <tr><td><code>pop_size</code></td><td class="center">51</td><td>Tamano de poblacion</td></tr>
        <tr><td><code>CR</code></td><td class="center">0.5112</td><td>Tasa de cruce binomial</td></tr>
        <tr><td><code>F</code></td><td class="center">0.3165</td><td>Factor de escala de mutacion</td></tr>
        <tr><td><code>strategy</code></td><td class="center">best/1/bin</td><td>Estrategia de mutacion diferencial</td></tr>
    </tbody>
</table>
<p><em>Mejor fitness:</em> 397,086,621 COP &nbsp;|&nbsp; <em>Trials:</em> 30 (0 errores, 0 timeouts) &nbsp;|&nbsp; <em>Tiempo total:</em> 1.33 h</p>

<h4>Tabla 4. Hiperparametros calibrados — Hibrido GA-SA</h4>
<table>
    <thead><tr><th>Parametro</th><th class="center">Valor calibrado</th><th>Descripcion</th></tr></thead>
    <tbody>
        <tr><td><code>pop_size</code></td><td class="center">39</td><td>Tamano de poblacion del GA</td></tr>
        <tr><td><code>crossover_rate</code></td><td class="center">0.8589</td><td>Tasa de cruce</td></tr>
        <tr><td><code>mutation_rate</code></td><td class="center">0.0505</td><td>Tasa de mutacion</td></tr>
        <tr><td><code>elitism_count</code></td><td class="center">1</td><td>Individuos preservados</td></tr>
        <tr><td><code>selection_size</code></td><td class="center">3</td><td>Tamano del torneo</td></tr>
        <tr><td><code>local_search_freq</code></td><td class="center">9</td><td>Frecuencia de busqueda local SA (cada N gen.)</td></tr>
        <tr><td><code>local_search_top_k</code></td><td class="center">10</td><td>Top-k individuos para SA local</td></tr>
        <tr><td><code>local_search_iters</code></td><td class="center">26</td><td>Iteraciones del SA local</td></tr>
        <tr><td><code>local_search_T</code></td><td class="center">3,226.6</td><td>Temperatura del SA local</td></tr>
        <tr><td><code>local_search_cooling</code></td><td class="center">0.7126</td><td>Enfriamiento del SA local</td></tr>
    </tbody>
</table>
<p><em>Mejor fitness:</em> 396,887,162 COP &nbsp;|&nbsp; <em>Trials:</em> 30 (0 errores, 0 timeouts) &nbsp;|&nbsp; <em>Tiempo total:</em> 17.5 h</p>

<h3>3.4 Benchmark Preliminar</h3>

<figure>
    <img src="figuras/04_benchmark_gap.png" alt="Benchmark Gap">
    <figcaption>Figura 5. Gap de optimalidad respecto al solver CBC. El hibrido GA-SA obtiene el menor gap (1.49%), consistente con la literatura (Akbari-Aghghaleh, 2025). Linea punteada: umbral H2 del 2%.</figcaption>
</figure>

<table>
    <thead>
        <tr><th>Algoritmo</th><th class="center">Gap vs Exacto</th><th class="center">Factible</th></tr>
    </thead>
    <tbody>
        <tr><td>CBC (Exacto)</td><td class="center">0.00%</td><td class="center">Si</td></tr>
        <tr><td>GA</td><td class="center">1.87%</td><td class="center">Si</td></tr>
        <tr><td>SA</td><td class="center">2.05%</td><td class="center">Si</td></tr>
        <tr><td>DE</td><td class="center">1.81%</td><td class="center">Si</td></tr>
        <tr><td><strong>GA-SA</strong></td><td class="center"><strong>1.49%</strong></td><td class="center"><strong>Si</strong></td></tr>
    </tbody>
</table>

<p><strong>Tests Fase 2:</strong> 43 tests automatizados (15 + 7 + 8 + 8 + 5), todos aprobados.</p>

<!-- 4. FASE 3 -->
<h2>4. Fase 3: Generacion de Datos y Escenarios</h2>

<h3>4.1 Objetivo</h3>
<p>Crear un generador de instancias sinteticas calibradas contra parametros de la industria avicola colombiana, y producir un banco de 15 instancias para la fase experimental.</p>

<figure>
    <img src="figuras/05_perfiles_instancias.png" alt="Perfiles de Instancias">
    <figcaption>Figura 5. Caracterizacion de los 5 perfiles de instancias. Cada perfil se genera con 3 semillas distintas (42, 123, 456) para analisis estadistico.</figcaption>
</figure>

<h3>4.2 Banco de Instancias</h3>
<table>
    <thead>
        <tr><th>Perfil</th><th class="center">n<sub>f</sub></th><th class="center">n<sub>t</sub></th><th class="center">n<sub>ω</sub></th><th class="center">Seeds</th><th class="center">Solver CBC</th></tr>
    </thead>
    <tbody>
        <tr><td>Toy</td><td class="center">3</td><td class="center">4</td><td class="center">5</td><td class="center">42, 123, 456</td><td class="center">Optimo (&lt; 0.3 s)</td></tr>
        <tr><td>Small</td><td class="center">6</td><td class="center">12</td><td class="center">20</td><td class="center">42, 123, 456</td><td class="center">Optimo (&lt; 2.8 s)</td></tr>
        <tr><td>Medium</td><td class="center">6</td><td class="center">12</td><td class="center">50</td><td class="center">42, 123, 456</td><td class="center">—</td></tr>
        <tr><td>Large</td><td class="center">8</td><td class="center">24</td><td class="center">100</td><td class="center">42, 123, 456</td><td class="center">—</td></tr>
        <tr><td>Industrial</td><td class="center">10</td><td class="center">52</td><td class="center">500</td><td class="center">42, 123, 456</td><td class="center">—</td></tr>
    </tbody>
</table>
<p><strong>Total:</strong> 15 instancias YAML, 22.8 MB. Soluciones optimas conocidas: Toy Z* ∈ [269M, 283M] COP, Small Z* ∈ [571M, 578M] COP.</p>

<h3>4.3 Calibracion contra la Industria Avicola Colombiana</h3>

<figure>
    <img src="figuras/07_calibracion.png" alt="Calibracion">
    <figcaption>Figura 6. Proporciones anatomicas y rangos de precios de venta calibrados con datos de FENAVI (2024) y la guia Cobb 500.</figcaption>
</figure>

<table>
    <thead>
        <tr><th>Parametro</th><th>Rango</th><th>Fuente</th></tr>
    </thead>
    <tbody>
        <tr><td>Proporciones anatomicas</td><td>Pechuga 30%, Muslo 18%, Ala 8%, ...</td><td>FENAVI, Cobb 500</td></tr>
        <tr><td>Precios de venta (COP/kg)</td><td>5,000 – 15,000</td><td>FENAVI 2024</td></tr>
        <tr><td>Costo de procesamiento</td><td>1,500 – 2,500 COP/carcasa</td><td>Solano-Blanco (2022)</td></tr>
        <tr><td>Costo de setup</td><td>500,000 – 1,500,000 COP/periodo</td><td>Referencia industrial</td></tr>
        <tr><td>Capacidad maxima</td><td>5,000 – 20,000 carcasas/periodo</td><td>Plantas medianas Colombia</td></tr>
        <tr><td>Vida util (refrigerado)</td><td>4 – 7 dias</td><td>NTC 3644-2, Codex Alimentarius</td></tr>
    </tbody>
</table>

<h3>4.4 Tests de Calibracion (<code>test_calibration.py</code> — 44 tests)</h3>
<p>Los datos de calibracion industrial se validan automaticamente con 44 tests agrupados en 3 categorias:</p>

<h4>A. Integridad de los datos de referencia (14 tests)</h4>
<table>
    <thead><tr><th>Test</th><th>Verifica</th></tr></thead>
    <tbody>
        <tr><td><code>test_anatomical_proportions_sum_one</code></td><td>sum(alpha) == 1.0 exacto</td></tr>
        <tr><td><code>test_anatomical_proportions_all_positive</code></td><td>Todas las proporciones > 0</td></tr>
        <tr><td><code>test_prices_min_less_than_max</code></td><td>min < max en todos los rangos de precios</td></tr>
        <tr><td><code>test_prices_default_in_range</code></td><td>Precio default entre min y max</td></tr>
        <tr><td><code>test_costs_min_less_than_max</code></td><td>min < max en costos</td></tr>
        <tr><td><code>test_costs_default_in_range</code></td><td>Costo default entre min y max</td></tr>
        <tr><td><code>test_inv_cost_less_than_all_prices</code></td><td>cost_inv < precio minimo (coherencia economica)</td></tr>
        <tr><td><code>test_capacity_q_min_less_than_q_max</code></td><td>Q<sup>min</sup> < Q<sup>max</sup></td></tr>
        <tr><td><code>test_shelf_life_positive</code></td><td>Vida util default > 0</td></tr>
        <tr><td><code>test_shelf_life_min_less_than_max</code></td><td>min &le; max en vida util</td></tr>
        <tr><td><code>test_weight_positive</code></td><td>Peso default > 0</td></tr>
        <tr><td><code>test_weight_range</code></td><td>Peso en rango razonable (1-5 kg)</td></tr>
        <tr><td><code>test_validate_calibration_data_passes</code></td><td><code>validate_calibration_data()</code> sin errores</td></tr>
    </tbody>
</table>

<h4>B. Funcion <code>calibrate_instance()</code> (20 tests, 5 perfiles x 4 propiedades)</h4>
<table>
    <thead><tr><th>Test</th><th>Verifica</th></tr></thead>
    <tbody>
        <tr><td><code>test_calibrated_instance_valid</code></td><td>Instancia calibrada pasa <code>validate()</code> (5 perfiles)</td></tr>
        <tr><td><code>test_calibrate_preserves_demand</code></td><td>Calibracion no modifica demanda original</td></tr>
        <tr><td><code>test_calibrate_preserves_structure</code></td><td>No modifica n_f, n_t, n_w</td></tr>
        <tr><td><code>test_calibrate_does_not_mutate_original</code></td><td>Instancia original no se muta (deep copy)</td></tr>
        <tr><td><code>test_calibrate_applies_overrides</code></td><td>Overrides personalizados se aplican</td></tr>
        <tr><td><code>test_calibrate_applies_defaults</code></td><td>Sin overrides usa defaults de <code>COST_REFERENCE</code></td></tr>
        <tr><td><code>test_calibrate_large_uses_large_capacity</code></td><td>Perfil large usa <code>CAPACITY_REFERENCE['large']</code></td></tr>
        <tr><td><code>test_calibrate_invalid_source</code></td><td>Fuente invalida lanza <code>ValueError</code></td></tr>
        <tr><td><code>test_all_profiles_calibrate</code></td><td>Los 5 perfiles se calibran sin errores</td></tr>
        <tr><td><code>test_calibrated_costs_less_than_prices</code></td><td>cost_inv < prices despues de calibrar</td></tr>
    </tbody>
</table>

<h4>C. Matriz de correlacion (10 tests)</h4>
<table>
    <thead><tr><th>Test</th><th>Verifica</th></tr></thead>
    <tbody>
        <tr><td><code>test_correlation_shape</code></td><td>Dimension n x n correcta</td></tr>
        <tr><td><code>test_correlation_symmetric</code></td><td>Matriz simetrica</td></tr>
        <tr><td><code>test_correlation_diagonal_one</code></td><td>Diagonal = 1.0 (correlacion consigo mismo)</td></tr>
        <tr><td><code>test_correlation_positive_definite</code></td><td>Todos los eigenvalores > 0 (valida para Cholesky)</td></tr>
        <tr><td><code>test_correlation_various_sizes</code></td><td>Funciona para n = 3, 6, 8, 10</td></tr>
    </tbody>
</table>

<p><strong>Tests Fase 3 (total):</strong> 123 tests automatizados (<code>test_generator</code>: 79 + <code>test_calibration</code>: 44), todos aprobados.</p>

<!-- 5. EVIDENCIAS -->
<h2>5. Evidencias de Calidad del Software</h2>

<figure>
    <img src="figuras/06_tests_summary.png" alt="Tests Summary">
    <figcaption>Figura 7. Distribucion de tests automatizados por modulo y fase. Total: 234 tests, 0 fallos (14.14 s).</figcaption>
</figure>

<h3>5.1 Metricas del Codigo</h3>
<table>
    <thead>
        <tr><th>Indicador</th><th class="center">Valor</th></tr>
    </thead>
    <tbody>
        <tr><td>Modulos fuente en <code>src/</code></td><td class="center">15</td></tr>
        <tr><td>Lineas de codigo fuente</td><td class="center">~3,180</td></tr>
        <tr><td>Tests automatizados</td><td class="center"><strong>234 (0 fallos)</strong></td></tr>
        <tr><td>Instancias generadas</td><td class="center">15 archivos YAML (22.8 MB)</td></tr>
        <tr><td>Configuraciones de calibracion</td><td class="center">4 archivos YAML</td></tr>
        <tr><td>Documentos tecnicos</td><td class="center">9 archivos Markdown</td></tr>
    </tbody>
</table>

<!-- 6. TRABAJO PENDIENTE -->
<h2>6. Trabajo en Progreso y Pendiente</h2>

<h3>6.1 Fase 4: Experimentacion (Semanas 23–27) — En ejecucion</h3>
<p>Los scripts de ejecucion y analisis estan implementados. El experimento comparativo (1,620 ejecuciones: 6 algoritmos &times; 9 instancias &times; 30 replicas) se encuentra en ejecucion activa. Los entregables incluyen:</p>
<ul>
    <li><strong>Sprint 4.1 (Completado):</strong> Metricas (Z, gap, servicio, inventario), heuristica baseline, configuraciones YAML.</li>
    <li><strong>Sprint 4.2 (En ejecucion):</strong> Runner comparativo con checkpoint/reanudacion y runner de sensibilidad (precios &plusmn;20%, costos &plusmn;20%, demanda &plusmn;50%).</li>
    <li><strong>Sprints 4.3-4.4 (Scripts listos):</strong> Tests estadisticos (Shapiro-Wilk, t-test/Wilcoxon, ANOVA+Tukey HSD, Cohen's d, IC 95%) y generacion de tablas y graficos para la tesis.</li>
</ul>

<h3>6.2 Fase 5: Tesis y Sustentacion (Semanas 28–30) — Pendiente</h3>
<ul>
    <li>Validacion operativa y reproducibilidad completa.</li>
    <li>Escritura de la tesis (7 capitulos, formato UTP/MIOE).</li>
    <li>Presentacion de sustentacion (Reveal.js con graficos interactivos).</li>
    <li>Publicacion del repositorio con tag <code>v1.0.0-thesis</code>.</li>
</ul>

<!-- FIRMA -->
<div class="signature">
    <p><strong>Daniel Andres Castaneda Rodriguez</strong><br>
    Maestria en Investigacion Operativa y Estadistica<br>
    Universidad Tecnologica de Pereira<br>
    Marzo de 2026</p>
</div>

</body>
</html>
""")


# ============================================================
# Main
# ============================================================
def main():
    print("=" * 60)
    print("GENERANDO INFORME DE AVANCE — Fases 1-3")
    print("=" * 60)
    print(f"\nDirectorio de figuras: {FIGURAS_DIR}")
    print("\nGenerando diagramas...")

    fig_gantt()
    fig_pipeline_modelo()
    fig_arquitectura_mh()
    fig_benchmark_gap()
    fig_perfiles_instancias()
    fig_tests_summary()
    fig_calibracion()
    fig_optuna_tuning()

    print("\nRenderizando HTML...")
    html_path = REPORT_DIR / "reporte_avance_fases_1_3.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)
    print(f"  Reporte HTML: {html_path}")

    print("\n" + "=" * 60)
    print("COMPLETADO")
    print("=" * 60)
    print(f"\nPara exportar a PDF:")
    print(f"  1. Abrir {html_path} en el navegador")
    print(f"  2. Ctrl+P → Guardar como PDF")
    print(f"  3. Opciones: margenes 'Predeterminado', sin encabezado/pie")


if __name__ == "__main__":
    main()
