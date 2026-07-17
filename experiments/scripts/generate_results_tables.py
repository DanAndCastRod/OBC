"""
Generador de tablas y graficos para la tesis (Sprint 4.4).

Produce:
  1. Tabla de resultados principal (algoritmo x metricas)
  2. Tabla de hipotesis (H1/H2/H3)
  3. Boxplot de fitness por algoritmo
  4. Grafico de Pareto: calidad vs tiempo
  5. Reporte en Markdown listo para la tesis

Uso:
    python experiments/scripts/generate_results_tables.py
    python experiments/scripts/generate_results_tables.py --csv experiments/results/comparison.csv

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 4.4
"""

from __future__ import annotations

import argparse
import json
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
# Tabla de resultados principal
# ============================================================

ALGO_ORDER = ["baseline", "ga", "sa", "de", "ga_sa", "cbc_exact"]
ALGO_LABELS = {
    "baseline": "Baseline",
    "ga": "GA",
    "sa": "SA",
    "de": "DE",
    "ga_sa": "GA-SA",
    "cbc_exact": "CBC (Exact)",
}

# Etiquetas en español solo para las figuras (las tablas conservan ALGO_LABELS).
ALGO_LABELS_PLOT = {**ALGO_LABELS, "cbc_exact": "CBC (exacto)"}

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

_FMT_MILLONES = FuncFormatter(lambda v, _pos: f"{v:,.0f}")


def _estilizar_ejes(ax: plt.Axes, grid_axis: str = "y") -> None:
    """Estilo comun: spines superior/derecho fuera, grid sutil bajo los datos."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.8)
    ax.spines["bottom"].set_linewidth(0.8)
    ax.grid(axis=grid_axis, alpha=0.25, linewidth=0.8, color="#999999")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=10, color="#999999")


def generate_main_table(df: pd.DataFrame) -> pd.DataFrame:
    """Generar tabla principal: algoritmo x metricas agregadas."""
    summary = (
        df.groupby("algorithm")
        .agg(
            z_mean=("z_value", "mean"),
            z_std=("z_value", "std"),
            gap_mean=("gap_percent", "mean"),
            service_mean=("service_level", "mean"),
            inv_mean=("avg_inventory", "mean"),
            time_mean=("elapsed_seconds", "mean"),
            n_runs=("z_value", "count"),
            feasible_pct=("is_feasible", "mean"),
        )
        .reset_index()
    )

    # Reordenar
    summary["sort_key"] = summary["algorithm"].map(
        {a: i for i, a in enumerate(ALGO_ORDER)}
    )
    summary = summary.sort_values("sort_key").drop(columns="sort_key")
    summary["algorithm_label"] = summary["algorithm"].map(ALGO_LABELS)
    summary["feasible_pct"] = summary["feasible_pct"] * 100

    return summary


def generate_instance_table(df: pd.DataFrame) -> pd.DataFrame:
    """Generar tabla por algoritmo × instancia."""
    summary = (
        df.groupby(["algorithm", "instance"])
        .agg(
            z_mean=("z_value", "mean"),
            z_std=("z_value", "std"),
            gap_mean=("gap_percent", "mean"),
            service_mean=("service_level", "mean"),
            time_mean=("elapsed_seconds", "mean"),
            n_runs=("z_value", "count"),
        )
        .reset_index()
    )
    return summary


def generate_size_table(df: pd.DataFrame) -> pd.DataFrame:
    """Generar tabla por tamaño de instancia × algoritmo.

    El promedio global de gap mezcla referencias heterogéneas (óptimo probado en
    small/medium vs posible incumbente en large), así que la tabla reportable
    para la tesis es esta: cada celda agrega solo instancias del mismo tamaño.
    Incluye gap_vs_bound_percent (gap contra la cota dual del solver) cuando el
    CSV lo trae — esa columna es defendible aunque CBC no haya convergido.
    """
    work = df.copy()
    work["size"] = work["instance"].astype(str).str.split("_").str[0]

    aggs = {
        "z_mean": ("z_value", "mean"),
        "z_std": ("z_value", "std"),
        "gap_mean": ("gap_percent", "mean"),
        "service_mean": ("service_level", "mean"),
        "inv_mean": ("avg_inventory", "mean"),
        "time_mean": ("elapsed_seconds", "mean"),
        "n_runs": ("z_value", "count"),
    }
    if "gap_vs_bound_percent" in work.columns:
        aggs["gap_vs_bound_mean"] = ("gap_vs_bound_percent", "mean")

    summary = work.groupby(["size", "algorithm"]).agg(**aggs).reset_index()

    summary["sort_key"] = summary["algorithm"].map(
        {a: i for i, a in enumerate(ALGO_ORDER)}
    )
    size_order = {"toy": 0, "small": 1, "medium": 2, "large": 3, "industrial": 4}
    summary["size_key"] = summary["size"].map(size_order).fillna(99)
    summary = (
        summary.sort_values(["size_key", "sort_key"])
        .drop(columns=["sort_key", "size_key"])
    )
    summary["algorithm_label"] = summary["algorithm"].map(ALGO_LABELS)
    return summary


# ============================================================
# Graficos
# ============================================================


def plot_boxplot_fitness(df: pd.DataFrame, output_path: Path) -> None:
    """Boxplot de Z por algoritmo."""
    fig, ax = plt.subplots(figsize=(10, 6))

    algos = [a for a in ALGO_ORDER if a in df["algorithm"].unique()]
    data = [df[df["algorithm"] == a]["z_value"].values / 1e6 for a in algos]
    labels = [ALGO_LABELS_PLOT.get(a, a) for a in algos]

    bp = ax.boxplot(data, patch_artist=True, widths=0.55)

    for i, algo in enumerate(algos):
        color = ALGO_COLORS.get(algo, "#666666")
        bp["boxes"][i].set(facecolor=color, alpha=0.35, edgecolor=color, linewidth=1.6)
        for whisker in bp["whiskers"][2 * i : 2 * i + 2]:
            whisker.set(color=color, linewidth=1.4)
        for cap in bp["caps"][2 * i : 2 * i + 2]:
            cap.set(color=color, linewidth=1.4)
        bp["medians"][i].set(color=TINTA, linewidth=1.8)
        for flier in bp["fliers"][i : i + 1]:
            flier.set(
                marker="o",
                markersize=5,
                markerfacecolor=color,
                markeredgecolor="white",
                markeredgewidth=1.0,
                alpha=0.9,
            )

    ax.set_xticks(range(1, len(labels) + 1))
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_title(
        "Distribución de Z por algoritmo", fontsize=14, fontweight="bold", color=TINTA
    )
    ax.set_ylabel("Z, función objetivo (millones de COP)", fontsize=12)
    ax.yaxis.set_major_formatter(_FMT_MILLONES)
    _estilizar_ejes(ax, grid_axis="y")

    fig.tight_layout()
    fig.savefig(output_path / "boxplot_fitness.png", dpi=300)
    plt.close(fig)
    print(f"  Boxplot guardado: {output_path / 'boxplot_fitness.png'}")


def plot_pareto_quality_time(df: pd.DataFrame, output_path: Path) -> None:
    """Grafico de Pareto: calidad (Z medio) vs tiempo medio, con etiquetas directas."""
    fig, ax = plt.subplots(figsize=(8.5, 6))

    summary = (
        df.groupby("algorithm")
        .agg(
            z_mean=("z_value", "mean"),
            time_mean=("elapsed_seconds", "mean"),
        )
        .reset_index()
    )
    summary["sort_key"] = summary["algorithm"].map(
        {a: i for i, a in enumerate(ALGO_ORDER)}
    )
    summary = summary.sort_values("sort_key")

    puntos = []  # (algo, x, y_millones)
    for _, row in summary.iterrows():
        algo = row["algorithm"]
        x, y = row["time_mean"], row["z_mean"] / 1e6
        puntos.append((algo, x, y))
        ax.scatter(
            x,
            y,
            s=170,
            color=ALGO_COLORS.get(algo, "#666666"),
            zorder=5,
            edgecolors="white",
            linewidth=2,
        )

    # Etiquetas directas en tinta. Los puntos que comparten zona (tiempos en la
    # misma decada y Z cercano) forman un cluster y reparten sus etiquetas
    # alrededor: el mas alto arriba, el siguiente al costado, el mas bajo abajo.
    ys = [p[2] for p in puntos]
    y_span = (max(ys) - min(ys)) or 1.0
    lxs = [np.log10(max(p[1], 1e-9)) for p in puntos]
    cluster_de = list(range(len(puntos)))
    for i in range(len(puntos)):
        for j in range(i):
            cerca_x = abs(lxs[i] - lxs[j]) < 0.22
            cerca_y = abs(puntos[i][2] - puntos[j][2]) < 0.18 * y_span
            if cerca_x and cerca_y:
                cluster_de[i] = cluster_de[j]
                break

    por_cluster: dict[int, list[int]] = {}
    for i, c in enumerate(cluster_de):
        por_cluster.setdefault(c, []).append(i)

    # (dx, dy, ha, va) segun el rango de Z descendente dentro del cluster
    posiciones_cluster = [
        (0, 11, "center", "bottom"),
        (12, -4, "left", "center"),
        (0, -19, "center", "top"),
        (-12, -4, "right", "center"),
    ]
    for indices in por_cluster.values():
        if len(indices) == 1:
            asignaciones = {indices[0]: (10, 5, "left", "bottom")}
        else:
            orden = sorted(indices, key=lambda i: -puntos[i][2])
            asignaciones = {
                i: posiciones_cluster[k % len(posiciones_cluster)]
                for k, i in enumerate(orden)
            }
        for i, (dx, dy, ha, va) in asignaciones.items():
            algo, x, y = puntos[i]
            ax.annotate(
                ALGO_LABELS_PLOT.get(algo, algo),
                xy=(x, y),
                xytext=(dx, dy),
                textcoords="offset points",
                ha=ha,
                va=va,
                fontsize=10.5,
                fontweight="bold",
                color=TINTA,
                zorder=6,
            )

    ax.set_xlabel("Tiempo medio (s, escala logarítmica)", fontsize=12)
    ax.set_ylabel("Z medio (millones de COP)", fontsize=12)
    ax.set_title(
        "Frente calidad vs. tiempo computacional",
        fontsize=14,
        fontweight="bold",
        color=TINTA,
    )
    ax.set_xscale("log")
    ax.yaxis.set_major_formatter(_FMT_MILLONES)
    ax.margins(x=0.12, y=0.12)
    _estilizar_ejes(ax, grid_axis="both")

    fig.tight_layout()
    fig.savefig(output_path / "pareto_quality_time.png", dpi=300)
    plt.close(fig)
    print(f"  Pareto guardado: {output_path / 'pareto_quality_time.png'}")


def plot_service_level_comparison(df: pd.DataFrame, output_path: Path) -> None:
    """Barplot del nivel de servicio por algoritmo."""
    fig, ax = plt.subplots(figsize=(8, 5))

    summary = (
        df.groupby("algorithm")["service_level"].agg(["mean", "std"]).reset_index()
    )
    summary["sort_key"] = summary["algorithm"].map(
        {a: i for i, a in enumerate(ALGO_ORDER)}
    )
    summary = summary.sort_values("sort_key")

    colors = [ALGO_COLORS.get(a, "#666666") for a in summary["algorithm"]]
    labels = [ALGO_LABELS_PLOT.get(a, a) for a in summary["algorithm"]]
    x = np.arange(len(labels))

    ax.bar(
        x,
        summary["mean"],
        yerr=summary["std"],
        width=0.6,
        color=colors,
        error_kw={"ecolor": "#999999", "capsize": 3, "elinewidth": 1.2},
        zorder=3,
    )

    # Valor medio anotado en tinta encima de cada barra (sobre la barra de error).
    for xi, media, desv in zip(x, summary["mean"], summary["std"].fillna(0.0)):
        ax.annotate(
            f"{media:.1f}",
            xy=(xi, media + desv),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color=TINTA,
            zorder=4,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylabel("Nivel de servicio (%)", fontsize=12)
    ax.set_title(
        "Nivel de servicio por algoritmo", fontsize=14, fontweight="bold", color=TINTA
    )
    ax.set_ylim(0, 105)
    _estilizar_ejes(ax, grid_axis="y")

    fig.tight_layout()
    fig.savefig(output_path / "service_level_comparison.png", dpi=300)
    plt.close(fig)
    print(f"  Service level guardado: {output_path / 'service_level_comparison.png'}")


# ============================================================
# Reporte Markdown
# ============================================================


def generate_markdown_report(
    main_table: pd.DataFrame,
    stats_path: Path,
    output_path: Path,
) -> None:
    """Generar reporte Markdown para la tesis."""
    lines = [
        "# Reporte de Resultados - Fase 4",
        "",
        "## Tabla de Resultados Principal",
        "",
        "| Algoritmo | Z Medio | Std | Gap (%) | Servicio (%) | Inv. Medio | Tiempo (s) | N |",
        "|-----------|---------|-----|---------|-------------|-----------|------------|---|",
    ]

    for _, row in main_table.iterrows():
        gap_str = f"{row['gap_mean']:.2f}" if not np.isnan(row["gap_mean"]) else "—"
        lines.append(
            f"| {row['algorithm_label']} "
            f"| {row['z_mean']:,.0f} "
            f"| {row['z_std']:,.0f} "
            f"| {gap_str} "
            f"| {row['service_mean']:.1f} "
            f"| {row['inv_mean']:,.1f} "
            f"| {row['time_mean']:.1f} "
            f"| {int(row['n_runs'])} |"
        )

    lines.extend(["", "## Tabla de Hipotesis", ""])

    # Cargar resultados estadisticos si existen
    stats_file = stats_path / "statistical_tests.json"
    if stats_file.exists():
        with open(stats_file, "r", encoding="utf-8") as f:
            stats_data = json.load(f)

        lines.extend(
            [
                "| Hipotesis | Resultado | p-valor | Efecto | Veredicto |",
                "|-----------|-----------|---------|--------|-----------|",
            ]
        )

        for test in stats_data.get("hypothesis_tests", []):
            icon = "APROBADA" if test["verdict"] == "SUPPORTED" else "RECHAZADA"
            lines.append(
                f"| {test['hypothesis']} ({test['description'][:30]}...) "
                f"| {test['metric_value']:.2f}% "
                f"| {test['p_value']:.4f} "
                f"| d={test['effect_size']:.3f} ({test['effect_label']}) "
                f"| {icon} |"
            )
    else:
        lines.append("*Ejecute run_statistical_tests.py primero.*")

    lines.extend(
        [
            "",
            "## Graficos",
            "",
            "### Boxplot de Fitness por Algoritmo",
            "![Boxplot](boxplot_fitness.png)",
            "",
            "### Pareto: Calidad vs Tiempo",
            "![Pareto](pareto_quality_time.png)",
            "",
            "### Nivel de Servicio",
            "![Service Level](service_level_comparison.png)",
            "",
            "## Limitaciones",
            "",
            "1. Instancias generadas sinteticamente (no datos reales de planta)",
            "2. Time limit de 300s puede limitar convergencia en instancias Large",
            "3. CBC no garantiza optimo en instancias Medium/Large dentro del time limit",
            "4. Baseline simple (proporcional) puede no representar practica industrial real",
        ]
    )

    report_path = output_path / "reporte_fase4.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\nReporte guardado: {report_path}")


# ============================================================
# Main
# ============================================================


def generate_all(
    csv_path: str = "experiments/results/comparison.csv",
    output_dir: str = "experiments/results",
) -> None:
    """Generar todas las tablas y graficos."""
    csv_file = Path(csv_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not csv_file.exists():
        print(f"ERROR: No se encontro {csv_file}")
        print("Ejecute run_comparison.py primero.")
        sys.exit(1)

    df = pd.read_csv(csv_file)
    print(
        f"Datos: {len(df)} filas, {df['algorithm'].nunique()} algoritmos, "
        f"{df['instance'].nunique()} instancias"
    )

    # Tablas
    print("\n--- Generando tablas ---")
    main_table = generate_main_table(df)
    inst_table = generate_instance_table(df)
    size_table = generate_size_table(df)

    # Guardar tablas
    main_table.to_csv(output_path / "main_results_table.csv", index=False)
    inst_table.to_csv(output_path / "instance_results_table.csv", index=False)
    size_table.to_csv(output_path / "size_results_table.csv", index=False)
    print(f"  Tabla principal: {output_path / 'main_results_table.csv'}")
    print(f"  Tabla instancias: {output_path / 'instance_results_table.csv'}")
    print(f"  Tabla por tamaño: {output_path / 'size_results_table.csv'}")

    # Imprimir tabla principal
    print("\n" + "=" * 100)
    print("TABLA PRINCIPAL DE RESULTADOS")
    print("=" * 100)
    print(
        f"\n{'Algoritmo':<12} {'Z Medio':>15} {'Std':>12} {'Gap%':>8} "
        f"{'Svc%':>8} {'Inv':>10} {'t(s)':>8} {'N':>5} {'OK%':>6}"
    )
    print("-" * 92)
    for _, row in main_table.iterrows():
        gap_s = f"{row['gap_mean']:.2f}" if not np.isnan(row["gap_mean"]) else "—"
        print(
            f"{row['algorithm_label']:<12} {row['z_mean']:>15,.0f} "
            f"{row['z_std']:>12,.0f} {gap_s:>8} "
            f"{row['service_mean']:>7.1f}% {row['inv_mean']:>10,.1f} "
            f"{row['time_mean']:>7.1f}s {int(row['n_runs']):>5} "
            f"{row['feasible_pct']:>5.0f}%"
        )

    # Graficos
    print("\n--- Generando graficos ---")
    plot_boxplot_fitness(df, output_path)
    plot_pareto_quality_time(df, output_path)
    plot_service_level_comparison(df, output_path)

    # Reporte Markdown: se escribe JUNTO a las tablas (output_dir), no en una
    # ruta fija, para no sobreescribir el reporte de otro experimento (p.ej. una
    # corrida v2 clobbereaba el reporte histórico v1 en documentacion/reportes/).
    print("\n--- Generando reporte ---")
    generate_markdown_report(main_table, output_path, output_path)

    print("\n" + "=" * 80)
    print("GENERACION COMPLETADA")
    print("=" * 80)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generador de tablas y graficos para la tesis (Sprint 4.4)"
    )
    parser.add_argument(
        "--csv",
        type=str,
        default="experiments/results/comparison.csv",
        help="Ruta al CSV de resultados",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="experiments/results",
        help="Directorio de salida",
    )
    args = parser.parse_args()

    generate_all(csv_path=args.csv, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
