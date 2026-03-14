"""
Generate practical-results figures for thesis Chapter 7.
Outputs PNG files to tesis/figuras/.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import json
import os

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Inter", "Segoe UI", "Arial"],
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})

TEAL = "#008B8B"
ORANGE = "#EB8A3E"
SLATE = "#365660"
GREEN = "#4caf50"
COLORS = [TEAL, "#00b3b3", SLATE, ORANGE]
OUT = os.path.join(os.path.dirname(__file__), "..", "tesis", "figuras")
os.makedirs(OUT, exist_ok=True)


def load_comparison():
    return pd.read_csv("experiments/results/comparison.csv")


def load_sensitivity():
    with open("experiments/results/sensitivity.json", encoding="utf-8") as f:
        return json.load(f)


def fig_ranking_heatmap(df):
    """Heatmap: Z medio por algoritmo × tamaño de instancia."""
    algos = ["ga_sa", "de", "ga", "sa"]
    algo_labels = ["GA-SA", "DE", "GA", "SA"]
    mh = df[df["algorithm"].isin(algos)].copy()
    mh["size"] = mh["instance"].str.extract(r"(small|medium|large)", expand=False)
    pivot = mh.groupby(["algorithm", "size"])["z_value"].mean().unstack()
    pivot = pivot.reindex(algos)[["small", "medium", "large"]]
    pivot.index = algo_labels

    fig, ax = plt.subplots(figsize=(7, 3.5))
    im = ax.imshow(pivot.values / 1e6, cmap="YlGnBu", aspect="auto")
    ax.set_xticks(range(3))
    ax.set_xticklabels(["Small\n(T=6, P=5)", "Medium\n(T=12, P=8)", "Large\n(T=24, P=10)"])
    ax.set_yticks(range(4))
    ax.set_yticklabels(algo_labels)
    for i in range(4):
        for j in range(3):
            val = pivot.values[i, j]
            ax.text(j, i, f"${val/1e6:,.0f}M", ha="center", va="center",
                    fontsize=10, fontweight="bold",
                    color="white" if val > pivot.values.mean() else "black")
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Z medio (millones COP)", fontsize=10)
    ax.set_title("Beneficio esperado por algoritmo y tamaño de instancia")
    fig.savefig(os.path.join(OUT, "heatmap_z_by_algo_size.png"))
    plt.close(fig)
    print("  ✓ heatmap_z_by_algo_size.png")


def fig_gap_distribution(df):
    """Histograma de gaps por algoritmo."""
    algos = ["ga_sa", "de", "ga", "sa"]
    labels = ["GA-SA", "DE", "GA", "SA"]
    mh = df[df["algorithm"].isin(algos)].copy()

    fig, axes = plt.subplots(1, 4, figsize=(12, 3), sharey=True)
    for ax, algo, label, color in zip(axes, algos, labels, COLORS):
        data = mh[mh["algorithm"] == algo]["gap_percent"].dropna()
        ax.hist(data, bins=20, color=color, alpha=0.85, edgecolor="white")
        ax.axvline(data.median(), color="red", linestyle="--", linewidth=1.5, label=f"Mediana: {data.median():.2f}%")
        ax.set_title(label, fontweight="bold")
        ax.set_xlabel("Gap (%)")
        ax.legend(fontsize=8)
    axes[0].set_ylabel("Frecuencia")
    fig.suptitle("Distribución de gaps respecto al solver exacto CBC", fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "gap_distribution_by_algo.png"))
    plt.close(fig)
    print("  ✓ gap_distribution_by_algo.png")


def fig_sensitivity_tornado(sens):
    """Tornado chart de sensibilidad."""
    params = {}
    for item in sens["parameter_delta_summary"]:
        p = item["parameter"]
        d = item["delta"]
        g = item["mean_gap_percent"]
        if p not in params:
            params[p] = {}
        params[p][d] = g

    fig, ax = plt.subplots(figsize=(8, 4))
    labels_map = {"prices": "Precios", "costs": "Costos", "demand_variability": "Var. demanda"}
    y_pos = list(range(len(params)))
    bars_left = []
    bars_right = []
    labels = []

    for p in ["prices", "costs", "demand_variability"]:
        if p not in params:
            continue
        deltas = params[p]
        neg = min(deltas.values())
        pos = max(deltas.values())
        bars_left.append(neg)
        bars_right.append(pos)
        labels.append(labels_map.get(p, p))

    y_pos = list(range(len(labels)))
    ax.barh(y_pos, bars_left, color=ORANGE, alpha=0.8, height=0.5, label="Peor caso")
    ax.barh(y_pos, bars_right, color=TEAL, alpha=0.8, height=0.5, label="Mejor caso")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Variación en Z (%)")
    ax.set_title("Análisis de Sensibilidad — Impacto en la Función Objetivo")
    ax.axvline(0, color="black", linewidth=0.8)
    ax.legend(loc="lower right")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "sensitivity_tornado.png"))
    plt.close(fig)
    print("  ✓ sensitivity_tornado.png")


def fig_convergence_comparison():
    """Convergence curves from traces data."""
    try:
        traces = pd.read_csv("experiments/results/comparison_traces.csv")
    except FileNotFoundError:
        print("  ⚠ comparison_traces.csv not found — skipping convergence")
        return

    algos = ["ga_sa", "de", "ga", "sa"]
    labels = ["GA-SA", "DE", "GA", "SA"]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for algo, label, color in zip(algos, labels, COLORS):
        subset = traces[traces["algorithm"] == algo]
        if "evaluation" in subset.columns and "best_z" in subset.columns:
            grouped = subset.groupby("evaluation")["best_z"].mean()
            ax.plot(grouped.index, grouped.values / 1e6, label=label, color=color, linewidth=2)
    ax.set_xlabel("Evaluaciones")
    ax.set_ylabel("Mejor Z (millones COP)")
    ax.set_title("Convergencia promedio por algoritmo")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "convergence_comparison.png"))
    plt.close(fig)
    print("  ✓ convergence_comparison.png")


def fig_hypothesis_verdict():
    """Visual summary of hypothesis verdicts."""
    fig, ax = plt.subplots(figsize=(8, 3.5))
    hypotheses = ["H1: Mejora ≥5%\nvs baseline", "H2: GA-SA gap\n≤2% vs mejor MH", "H3: Reducción inv.\n≥15%"]
    thresholds = [5.0, 2.0, 15.0]
    actuals = [1.1, 0.007, 11.0]
    verdicts = ["No soportada", "Soportada", "No soportada"]
    colors_v = [ORANGE, GREEN, ORANGE]

    x = np.arange(len(hypotheses))
    bars_thresh = ax.bar(x - 0.18, thresholds, 0.32, label="Umbral esperado",
                          color="#ddd", edgecolor="#999", linewidth=1.2)
    bars_actual = ax.bar(x + 0.18, actuals, 0.32, label="Resultado real",
                          color=colors_v, edgecolor="white", linewidth=1)

    for i, (bar, v) in enumerate(zip(bars_actual, verdicts)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                v, ha="center", va="bottom", fontsize=9, fontweight="bold",
                color=colors_v[i])

    ax.set_xticks(x)
    ax.set_xticklabels(hypotheses, fontsize=9)
    ax.set_ylabel("Porcentaje (%)")
    ax.set_title("Veredicto de Hipótesis — Umbral vs Resultado Real")
    ax.legend()
    ax.set_ylim(0, 20)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "hypothesis_verdicts_visual.png"))
    plt.close(fig)
    print("  ✓ hypothesis_verdicts_visual.png")


if __name__ == "__main__":
    print("\n  Generando figuras de resultados prácticos...")
    df = load_comparison()
    sens = load_sensitivity()

    fig_ranking_heatmap(df)
    fig_gap_distribution(df)
    fig_sensitivity_tornado(sens)
    fig_convergence_comparison()
    fig_hypothesis_verdict()

    print(f"\n  ✓ Figuras guardadas en {OUT}/")
