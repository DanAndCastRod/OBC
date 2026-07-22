"""
Regenerador de figuras v1 con el tema visual de la tesis/presentacion.

Reconstruye, con la paleta Okabe-Ito y tipografias legibles en proyector
(>=13 pt), las tres figuras de la campana v1 que hoy salen con la paleta por
defecto de matplotlib y fuentes de 6-8 pt:

  1. boxplot_fitness.png          -> Distribucion de Z por algoritmo
  2. performance_profile.png      -> Perfil de desempeno de Dolan-More
  3. complexity_loglog_scaling.png-> Escalabilidad empirica O(N) (log-log)

Fuentes de datos (CSV v1, no se recalcula nada):
  - experiments/results/comparison.csv
  - experiments/results/complexity/performance_profile.csv
  - experiments/results/complexity/complexity_scaling_by_size.csv
  - experiments/results/complexity/complexity_exponent_fit.csv

Salida: tesis/figuras/ y, en copia identica, docs/presentacion/figuras/.

Uso:
    python experiments/scripts/plot_v1_figures.py

El estilo (rcParams, _estilizar_ejes, ALGO_COLORS, TINTA) replica el patron ya
aplicado en experiments/scripts/generate_results_tables.py, subiendo todas las
tipografias al minimo proyectable.

Autor: Daniel Andres Castaneda Rodriguez
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, ".")

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ============================================================
# Paleta y estilo (identico a generate_results_tables.py)
# ============================================================

ALGO_ORDER = ["baseline", "ga", "sa", "de", "ga_sa", "cbc_exact"]

# Etiquetas en espanol para las figuras.
ALGO_LABELS_PLOT = {
    "baseline": "Baseline",
    "ga": "GA",
    "sa": "SA",
    "de": "DE",
    "ga_sa": "GA-SA",
    "cbc_exact": "CBC (exacto)",
}

# Paleta Okabe-Ito (segura para daltonismo), fija por algoritmo.
# El texto SIEMPRE va en tinta, nunca en el color de la serie.
TINTA = "#1a1a1a"
ALGO_COLORS = {
    "baseline": "#666666",
    "ga": "#0072B2",
    "sa": "#E69F00",
    "de": "#009E73",
    "ga_sa": "#CC79A7",
    "cbc_exact": "#1a1a1a",
}

# Tipografias: minimo 13 pt para lectura proyectada.
FS_TITULO = 16
FS_EJE = 14
FS_TICK = 13
FS_LEYENDA = 13

plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.dpi": 300,
        "text.color": TINTA,
        "axes.labelcolor": TINTA,
        "axes.edgecolor": TINTA,
        "xtick.color": TINTA,
        "ytick.color": TINTA,
        "font.family": "sans-serif",
        "font.size": FS_TICK,
    }
)

_FMT_MILLONES = FuncFormatter(lambda v, _pos: f"{v:,.0f}")

# Destinos: la tesis es la fuente de verdad; la presentacion recibe una copia.
DEST_TESIS = Path("tesis/figuras")
DEST_PRESENTACION = Path("docs/presentacion/figuras")


def _estilizar_ejes(ax: plt.Axes, grid_axis: str = "y") -> None:
    """Estilo comun: spines superior/derecho fuera, grid sutil bajo los datos."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.8)
    ax.spines["bottom"].set_linewidth(0.8)
    ax.grid(axis=grid_axis, alpha=0.25, linewidth=0.8, color="#999999")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=FS_TICK, color="#999999")


def _guardar(fig: plt.Figure, nombre: str) -> Path:
    """Guardar en tesis/figuras y copiar identico a docs/presentacion/figuras."""
    DEST_TESIS.mkdir(parents=True, exist_ok=True)
    DEST_PRESENTACION.mkdir(parents=True, exist_ok=True)
    ruta_tesis = DEST_TESIS / nombre
    fig.savefig(ruta_tesis, dpi=300)
    plt.close(fig)
    ruta_pres = DEST_PRESENTACION / nombre
    shutil.copyfile(ruta_tesis, ruta_pres)
    print(f"  {nombre}: {ruta_tesis}  ->  {ruta_pres}")
    return ruta_tesis


# ============================================================
# 1) Boxplot de Z por algoritmo
# ============================================================


def plot_boxplot_fitness(comparison_csv: Path) -> None:
    df = pd.read_csv(comparison_csv)
    fig, ax = plt.subplots(figsize=(11, 6.5))

    algos = [a for a in ALGO_ORDER if a in df["algorithm"].unique()]
    data = [df[df["algorithm"] == a]["z_value"].to_numpy() / 1e6 for a in algos]
    labels = [ALGO_LABELS_PLOT.get(a, a) for a in algos]

    bp = ax.boxplot(data, patch_artist=True, widths=0.55)

    for i, algo in enumerate(algos):
        color = ALGO_COLORS.get(algo, "#666666")
        bp["boxes"][i].set(
            facecolor=color, alpha=0.35, edgecolor=color, linewidth=1.8
        )
        for whisker in bp["whiskers"][2 * i : 2 * i + 2]:
            whisker.set(color=color, linewidth=1.6)
        for cap in bp["caps"][2 * i : 2 * i + 2]:
            cap.set(color=color, linewidth=1.6)
        bp["medians"][i].set(color=TINTA, linewidth=2.2)
        for flier in bp["fliers"][i : i + 1]:
            flier.set(
                marker="o",
                markersize=6,
                markerfacecolor=color,
                markeredgecolor="white",
                markeredgewidth=1.0,
                alpha=0.9,
            )

    ax.set_xticks(range(1, len(labels) + 1))
    ax.set_xticklabels(labels, fontsize=FS_TICK)
    ax.set_title(
        "Distribución de Z por algoritmo",
        fontsize=FS_TITULO,
        fontweight="bold",
        color=TINTA,
        pad=12,
    )
    ax.set_ylabel("Z, función objetivo (millones de COP)", fontsize=FS_EJE)
    ax.yaxis.set_major_formatter(_FMT_MILLONES)
    _estilizar_ejes(ax, grid_axis="y")

    fig.tight_layout()
    _guardar(fig, "boxplot_fitness.png")


# ============================================================
# 2) Performance profile (Dolan-More)
# ============================================================


def plot_performance_profile(profile_csv: Path) -> None:
    df = pd.read_csv(profile_csv)
    fig, ax = plt.subplots(figsize=(11, 6.5))

    algos = [a for a in ALGO_ORDER if a in df["algorithm"].unique()]
    n_series = len(algos)
    for idx, algo in enumerate(algos):
        g = df[df["algorithm"] == algo].sort_values("tau")
        color = ALGO_COLORS.get(algo, "#666666")
        # Marcadores desfasados por serie para separar curvas superpuestas.
        offset = 6 + int(idx * (24 / max(n_series, 1)))
        ax.plot(
            g["tau"].to_numpy(),
            g["rho"].to_numpy(),
            color=color,
            linewidth=2.6,
            marker="o",
            markersize=8,
            markevery=(offset, 26),
            markeredgecolor="white",
            markeredgewidth=1.0,
            label=ALGO_LABELS_PLOT.get(algo, algo),
            zorder=4,
        )

    ax.set_xlabel("τ = tiempo respecto al mejor por caso", fontsize=FS_EJE)
    ax.set_ylabel("Fracción de casos con razón ≤ τ", fontsize=FS_EJE)
    ax.set_title(
        "Perfil de desempeño (Dolan-Moré)",
        fontsize=FS_TITULO,
        fontweight="bold",
        color=TINTA,
        pad=12,
    )
    ax.set_ylim(-0.02, 1.03)
    ax.set_xlim(left=1.0)
    _estilizar_ejes(ax, grid_axis="both")
    leg = ax.legend(
        fontsize=FS_LEYENDA,
        loc="lower right",
        frameon=True,
        framealpha=0.95,
        edgecolor="#CCCCCC",
        title="Algoritmo",
    )
    leg.get_title().set_fontsize(FS_LEYENDA)
    leg.get_title().set_color(TINTA)

    fig.tight_layout()
    _guardar(fig, "performance_profile.png")


# ============================================================
# 3) Escalabilidad empirica log-log O(N)
# ============================================================


def plot_complexity_loglog(scaling_csv: Path, fit_csv: Path) -> None:
    scaling = pd.read_csv(scaling_csv)
    fit = pd.read_csv(fit_csv).set_index("algorithm")
    fig, ax = plt.subplots(figsize=(11, 6.5))

    algos = [a for a in ALGO_ORDER if a in scaling["algorithm"].unique()]
    for algo in algos:
        g = scaling[scaling["algorithm"] == algo].sort_values("complexity")
        color = ALGO_COLORS.get(algo, "#666666")
        etiqueta = ALGO_LABELS_PLOT.get(algo, algo)
        if algo in fit.index and pd.notna(fit.loc[algo, "k"]):
            etiqueta = f"{etiqueta}  (k={fit.loc[algo, 'k']:.2f})"
        ax.plot(
            g["complexity"].to_numpy(),
            g["elapsed_mean"].to_numpy(),
            color=color,
            linewidth=2.6,
            marker="o",
            markersize=8,
            markeredgecolor="white",
            markeredgewidth=1.0,
            label=etiqueta,
            zorder=4,
        )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Complejidad n = F · T · W (escala log)", fontsize=FS_EJE)
    ax.set_ylabel("Tiempo medio de cómputo (s, escala log)", fontsize=FS_EJE)
    ax.set_title(
        "Escalabilidad empírica por algoritmo",
        fontsize=FS_TITULO,
        fontweight="bold",
        color=TINTA,
        pad=12,
    )
    _estilizar_ejes(ax, grid_axis="both")
    leg = ax.legend(
        fontsize=FS_LEYENDA,
        loc="upper left",
        frameon=True,
        framealpha=0.95,
        edgecolor="#CCCCCC",
        ncol=2,
        columnspacing=1.2,
        title="Algoritmo (exponente k del ajuste T ≈ a·nᵏ)",
    )
    leg.get_title().set_fontsize(FS_LEYENDA)
    leg.get_title().set_color(TINTA)

    fig.tight_layout()
    _guardar(fig, "complexity_loglog_scaling.png")


# ============================================================
# Main
# ============================================================


def main() -> None:
    results = Path("experiments/results")
    complexity = results / "complexity"

    comparison_csv = results / "comparison.csv"
    profile_csv = complexity / "performance_profile.csv"
    scaling_csv = complexity / "complexity_scaling_by_size.csv"
    fit_csv = complexity / "complexity_exponent_fit.csv"

    faltantes = [
        str(p)
        for p in (comparison_csv, profile_csv, scaling_csv, fit_csv)
        if not p.exists()
    ]
    if faltantes:
        print("ERROR: faltan CSV de entrada:")
        for f in faltantes:
            print(f"  - {f}")
        sys.exit(1)

    print("Regenerando figuras v1 con el tema visual de la tesis...")
    plot_boxplot_fitness(comparison_csv)
    plot_performance_profile(profile_csv)
    plot_complexity_loglog(scaling_csv, fit_csv)
    print("Listo. Figuras en tesis/figuras/ y docs/presentacion/figuras/.")


if __name__ == "__main__":
    main()
