"""
Figura central de la tesis: el valor de la optimización depende del régimen.

Compara el gap% frente a la mejor solución exacta (CBC) por tamaño de instancia
en dos paneles con el mismo eje Y: régimen v1 (izquierda) y régimen operativo v2
(derecha), para el baseline proporcional y el híbrido GA-SA.

Lee experiments/results/size_results_table.csv y
experiments/results_v2/size_results_table.csv; si la tabla por tamaño no existe
(caso v1), la deriva del comparison.csv del mismo directorio.

Uso:
    python experiments/scripts/plot_regimes.py

Salida:
    tesis/figuras/regimes_comparison.png (300 dpi)

Autor: Daniel Andres Castaneda Rodriguez
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Colores del proyecto (paleta Okabe-Ito validada); el texto siempre en tinta.
TINTA = "#1a1a1a"
COLOR_BASELINE = "#666666"
COLOR_GA_SA = "#CC79A7"

SIZES = ["small", "medium", "large"]
SIZE_LABELS = {"small": "Small", "medium": "Medium", "large": "Large"}

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
    }
)


def cargar_tabla_tamanos(results_dir: Path) -> pd.DataFrame:
    """Cargar la tabla por tamaño; si no existe, derivarla de comparison.csv."""
    tabla = results_dir / "size_results_table.csv"
    if tabla.exists():
        return pd.read_csv(tabla)

    comp = results_dir / "comparison.csv"
    if not comp.exists():
        print(f"ERROR: no existe ni {tabla} ni {comp}")
        sys.exit(1)

    df = pd.read_csv(comp)
    df["size"] = df["instance"].astype(str).str.split("_").str[0]
    return (
        df.groupby(["size", "algorithm"])
        .agg(gap_mean=("gap_percent", "mean"))
        .reset_index()
    )


def gaps_por_tamano(df: pd.DataFrame, algoritmo: str) -> list[float]:
    """Gap medio (%) del algoritmo en el orden small/medium/large."""
    sub = df[df["algorithm"] == algoritmo].set_index("size")["gap_mean"]
    return [float(sub.get(s, np.nan)) for s in SIZES]


def _estilizar_ejes(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.8)
    ax.spines["bottom"].set_linewidth(0.8)
    ax.grid(axis="y", alpha=0.25, linewidth=0.8, color="#999999")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=10, color="#999999")


def _panel_barras(
    ax: plt.Axes,
    titulo: str,
    gaps_baseline: list[float],
    gaps_ga_sa: list[float],
) -> None:
    x = np.arange(len(SIZES))
    ancho = 0.36

    barras = [
        (x - ancho / 2 - 0.01, gaps_baseline, COLOR_BASELINE),
        (x + ancho / 2 + 0.01, gaps_ga_sa, COLOR_GA_SA),
    ]
    for pos, valores, color in barras:
        ax.bar(pos, valores, width=ancho, color=color, zorder=3)
        for xi, v in zip(pos, valores):
            if np.isnan(v):
                continue
            ax.annotate(
                f"{v:.1f}%",
                xy=(xi, v),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
                color=TINTA,
                zorder=4,
            )

    ax.set_title(titulo, fontsize=12.5, fontweight="bold", color=TINTA, pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels([SIZE_LABELS[s] for s in SIZES], fontsize=11)
    ax.set_xlabel("Tamaño de instancia", fontsize=11)
    _estilizar_ejes(ax)


def generar_figura(
    v1_dir: str = "experiments/results",
    v2_dir: str = "experiments/results_v2",
    salida: str = "tesis/figuras/regimes_comparison.png",
) -> None:
    tabla_v1 = cargar_tabla_tamanos(Path(v1_dir))
    tabla_v2 = cargar_tabla_tamanos(Path(v2_dir))

    base_v1 = gaps_por_tamano(tabla_v1, "baseline")
    gasa_v1 = gaps_por_tamano(tabla_v1, "ga_sa")
    base_v2 = gaps_por_tamano(tabla_v2, "baseline")
    gasa_v2 = gaps_por_tamano(tabla_v2, "ga_sa")

    fig, ejes = plt.subplots(1, 2, figsize=(11, 5.6), sharey=True)

    _panel_barras(ejes[0], "Régimen v1", base_v1, gasa_v1)
    _panel_barras(ejes[1], "Régimen operativo v2", base_v2, gasa_v2)

    # Mismo eje Y en ambos paneles (sharey) con techo comun para comparar alturas.
    tope = np.nanmax([base_v1, gasa_v1, base_v2, gasa_v2])
    ejes[0].set_ylim(0, tope * 1.16)
    ejes[0].set_ylabel("Gap frente al óptimo certificado (%)", fontsize=11.5)

    # Leyenda unica: la identidad la llevan las marcas de color, el texto en tinta.
    manijas = [
        plt.Rectangle((0, 0), 1, 1, color=COLOR_BASELINE),
        plt.Rectangle((0, 0), 1, 1, color=COLOR_GA_SA),
    ]
    ejes[0].legend(
        manijas,
        ["Baseline (plan proporcional)", "GA-SA (híbrido propuesto)"],
        loc="upper left",
        frameon=False,
        fontsize=10.5,
    )

    fig.suptitle(
        "El valor de la optimización depende del régimen",
        fontsize=15,
        fontweight="bold",
        color=TINTA,
        y=0.99,
    )
    fig.text(
        0.5,
        0.915,
        "En el régimen v1 el plan proporcional queda cerca del óptimo; "
        "en el régimen operativo v2 deja 10–29% sobre la mesa y GA-SA lo reduce a ~5–6%.",
        ha="center",
        fontsize=10.5,
        color="#444444",
    )
    fig.text(
        0.01,
        0.005,
        "Nota: la referencia de v1-Large se registró sin certificado en la campaña original, pero una "
        "re-corrida instrumentada verificó optimalidad (best bound = Z, 17–19 s); todos los gaps son frente al óptimo.",
        ha="left",
        fontsize=8.5,
        color="#666666",
    )

    fig.tight_layout(rect=(0, 0.035, 1, 0.90))

    ruta = Path(salida)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(ruta, dpi=300)
    plt.close(fig)

    print(f"Figura guardada: {ruta}")
    print(f"  v1  baseline: {[f'{v:.1f}' for v in base_v1]}  ga_sa: {[f'{v:.1f}' for v in gasa_v1]}")
    print(f"  v2  baseline: {[f'{v:.1f}' for v in base_v2]}  ga_sa: {[f'{v:.1f}' for v in gasa_v2]}")


if __name__ == "__main__":
    generar_figura()
