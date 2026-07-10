"""
Análisis anytime desde las trazas de convergencia ya guardadas.

Usa experiments/results/comparison_traces.csv (una fila por iteración de cada
corrida de metaheurística, con best_fitness y elapsed_seconds) para producir,
SIN ejecutar ninguna corrida nueva:

1. Curvas anytime por tamaño de instancia: calidad normalizada (best-so-far /
   mejor Z conocido de la instancia) vs tiempo de pared (escala log).
   → tesis/figuras/anytime_curves.png
2. Tabla time-to-target: tiempo (mediana por corrida) en alcanzar el 90/95/99%
   del mejor Z conocido de la instancia, y el 99% de la calidad final de la
   propia corrida.
   → experiments/results/time_to_target.csv

Motivación: el reporte de tiempo de la tesis ("GA-SA usa 52.5x el tiempo de
CBC") ignora que las metaheurísticas son algoritmos anytime — casi toda su
calidad se alcanza en una fracción del tiempo total. Estas salidas lo
cuantifican.

Uso:
    python experiments/scripts/analyze_traces.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, ".")

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Colores fijos por algoritmo (Okabe-Ito, seguros para daltonismo). El WARN de
# contraste del naranja/rosa se mitiga con etiquetas directas en tinta.
ALGO_COLORS = {
    "ga": "#0072B2",
    "sa": "#E69F00",
    "de": "#009E73",
    "ga_sa": "#CC79A7",
}
ALGO_LABELS = {"ga": "GA", "sa": "SA", "de": "DE", "ga_sa": "GA-SA"}
ALGO_ORDER = ["ga", "sa", "de", "ga_sa"]
SIZE_ORDER = ["small", "medium", "large"]

TARGETS = (0.90, 0.95, 0.99)


def _instance_size(name: str) -> str:
    return str(name).split("_")[0]


def load_traces(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["size"] = df["instance"].map(_instance_size)
    return df


def compute_time_to_target(df: pd.DataFrame) -> pd.DataFrame:
    """Tiempo por corrida en alcanzar fracciones del mejor Z de la instancia.

    best_known(instancia) = max best_fitness sobre TODAS las corridas de esa
    instancia (cualquier algoritmo), de modo que los targets son comparables
    entre algoritmos. t99_own usa la calidad final de la propia corrida.
    """
    best_known = df.groupby("instance")["best_fitness"].max()

    rows = []
    run_cols = ["algorithm", "instance", "seed"]
    for (algo, inst, seed), g in df.groupby(run_cols, sort=False):
        g = g.sort_values("elapsed_seconds")
        best = g["best_fitness"].to_numpy()
        t = g["elapsed_seconds"].to_numpy()
        final_own = float(best[-1])
        ref = float(best_known.loc[inst])

        row = {
            "algorithm": algo,
            "instance": inst,
            "size": _instance_size(inst),
            "seed": seed,
            "final_quality_vs_best": final_own / ref if ref else np.nan,
            "total_time_s": float(t[-1]),
        }
        for q in TARGETS:
            idx = np.argmax(best >= q * ref)
            reached = bool(best[idx] >= q * ref)
            row[f"t{int(q*100)}_best_s"] = float(t[idx]) if reached else np.nan
        idx99 = np.argmax(best >= 0.99 * final_own)
        row["t99_own_s"] = float(t[idx99])
        rows.append(row)

    return pd.DataFrame(rows)


def summarize_time_to_target(runs: pd.DataFrame) -> pd.DataFrame:
    """Mediana por algoritmo × tamaño (y % de corridas que alcanzan el target)."""
    aggs: dict[str, tuple[str, object]] = {
        "n_runs": ("seed", "count"),
        "total_time_med_s": ("total_time_s", "median"),
        "t99_own_med_s": ("t99_own_s", "median"),
        "final_quality_med": ("final_quality_vs_best", "median"),
    }
    for q in TARGETS:
        col = f"t{int(q*100)}_best_s"
        aggs[f"{col.replace('_s', '')}_med_s"] = (col, "median")
        aggs[f"pct_reach_{int(q*100)}"] = (
            col,
            lambda s: 100.0 * s.notna().mean(),
        )

    out = runs.groupby(["size", "algorithm"]).agg(**aggs).reset_index()
    out["size_key"] = out["size"].map({s: i for i, s in enumerate(SIZE_ORDER)})
    out["algo_key"] = out["algorithm"].map({a: i for i, a in enumerate(ALGO_ORDER)})
    out = out.sort_values(["size_key", "algo_key"]).drop(columns=["size_key", "algo_key"])
    return out


def plot_anytime_curves(df: pd.DataFrame, output_path: Path) -> None:
    """Curvas anytime promedio por algoritmo, un panel por tamaño."""
    best_known = df.groupby("instance")["best_fitness"].max()

    sizes = [s for s in SIZE_ORDER if s in set(df["size"])]
    fig, axes = plt.subplots(1, len(sizes), figsize=(4.2 * len(sizes), 3.4), dpi=300)
    if len(sizes) == 1:
        axes = [axes]

    for ax, size in zip(axes, sizes):
        sub = df[df["size"] == size]
        t_max = sub["elapsed_seconds"].quantile(0.99)
        grid = np.logspace(np.log10(max(0.05, sub["elapsed_seconds"].min())),
                           np.log10(t_max), 120)

        labeled_ends: list[float] = []
        for algo in ALGO_ORDER:
            sa = sub[sub["algorithm"] == algo]
            if sa.empty:
                continue
            curves = []
            for (_, _), g in sa.groupby(["instance", "seed"], sort=False):
                g = g.sort_values("elapsed_seconds")
                ref = float(best_known.loc[g["instance"].iloc[0]])
                y = g["best_fitness"].to_numpy() / ref
                x = g["elapsed_seconds"].to_numpy()
                # best-so-far es escalonada: interp mantiene el último valor
                curves.append(np.interp(grid, x, y, left=y[0], right=y[-1]))
            mean_curve = np.mean(curves, axis=0)
            ax.plot(grid, mean_curve, lw=1.8, color=ALGO_COLORS[algo],
                    label=ALGO_LABELS[algo])
            # Etiqueta directa SOLO si no colisiona con otra ya puesta
            # (las curvas que convergen a 1.0 comparten extremo; para esas
            # la identidad la da la leyenda).
            end_val = float(mean_curve[-1])
            if all(abs(end_val - prev) > 0.025 for prev in labeled_ends):
                labeled_ends.append(end_val)
                ax.annotate(
                    ALGO_LABELS[algo], xy=(grid[-1], end_val),
                    xytext=(4, 0), textcoords="offset points",
                    fontsize=8, color="#1a1a1a", va="center",
                )

        ax.set_xscale("log")
        ax.set_ylim(0.55, 1.02)
        ax.set_title(f"Instancias {size}", fontsize=10, color="#1a1a1a")
        ax.set_xlabel("Tiempo de pared (s, escala log)", fontsize=9)
        ax.grid(True, which="both", axis="both", alpha=0.25, lw=0.5)
        ax.tick_params(labelsize=8, colors="#333333")
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)

    axes[0].set_ylabel("Calidad relativa al mejor Z conocido", fontsize=9)
    axes[0].legend(fontsize=8, frameon=False, loc="lower right")
    fig.suptitle(
        "Curvas anytime: calidad best-so-far vs tiempo (promedio sobre corridas)",
        fontsize=11, color="#1a1a1a",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(output_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Curvas anytime guardadas en: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Análisis anytime desde traces")
    parser.add_argument(
        "--traces", type=str,
        default="experiments/results/comparison_traces.csv",
    )
    parser.add_argument(
        "--output-csv", type=str,
        default="experiments/results/time_to_target.csv",
    )
    parser.add_argument(
        "--output-fig", type=str,
        default="tesis/figuras/anytime_curves.png",
    )
    args = parser.parse_args()

    df = load_traces(Path(args.traces))
    print(f"Traces: {len(df):,} filas, {df['instance'].nunique()} instancias, "
          f"{df['algorithm'].nunique()} algoritmos")

    runs = compute_time_to_target(df)
    summary = summarize_time_to_target(runs)
    summary.to_csv(args.output_csv, index=False)
    print(f"Tabla time-to-target guardada en: {args.output_csv}\n")

    cols = ["size", "algorithm", "total_time_med_s", "t99_best_med_s",
            "pct_reach_99", "t99_own_med_s"]
    print(summary[cols].to_string(index=False))

    plot_anytime_curves(df, Path(args.output_fig))


if __name__ == "__main__":
    main()
