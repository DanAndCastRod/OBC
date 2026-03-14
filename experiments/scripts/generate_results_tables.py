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


# ============================================================
# Graficos
# ============================================================


def plot_boxplot_fitness(df: pd.DataFrame, output_path: Path) -> None:
    """Boxplot de Z por algoritmo."""
    fig, ax = plt.subplots(figsize=(10, 6))

    algos = [a for a in ALGO_ORDER if a in df["algorithm"].unique()]
    data = [df[df["algorithm"] == a]["z_value"].values for a in algos]
    labels = [ALGO_LABELS.get(a, a) for a in algos]

    bp = ax.boxplot(data, labels=labels, patch_artist=True)

    colors = ["#95a5a6", "#3498db", "#e74c3c", "#2ecc71", "#9b59b6", "#f39c12"]
    for patch, color in zip(bp["boxes"], colors[: len(algos)]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_title("Distribucion de Z por Algoritmo", fontsize=14, fontweight="bold")
    ax.set_ylabel("Z (Funcion Objetivo, COP)", fontsize=12)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))

    fig.tight_layout()
    fig.savefig(output_path / "boxplot_fitness.png", dpi=200)
    plt.close(fig)
    print(f"  Boxplot guardado: {output_path / 'boxplot_fitness.png'}")


def plot_pareto_quality_time(df: pd.DataFrame, output_path: Path) -> None:
    """Grafico de Pareto: calidad (Z medio) vs tiempo medio."""
    fig, ax = plt.subplots(figsize=(8, 6))

    summary = (
        df.groupby("algorithm")
        .agg(
            z_mean=("z_value", "mean"),
            time_mean=("elapsed_seconds", "mean"),
        )
        .reset_index()
    )

    colors = {
        "baseline": "#95a5a6",
        "ga": "#3498db",
        "sa": "#e74c3c",
        "de": "#2ecc71",
        "ga_sa": "#9b59b6",
        "cbc_exact": "#f39c12",
    }

    for _, row in summary.iterrows():
        algo = row["algorithm"]
        ax.scatter(
            row["time_mean"],
            row["z_mean"],
            s=150,
            c=colors.get(algo, "gray"),
            label=ALGO_LABELS.get(algo, algo),
            zorder=5,
            edgecolors="black",
            linewidth=0.5,
        )

    ax.set_xlabel("Tiempo Medio (seg)", fontsize=12)
    ax.set_ylabel("Z Medio (COP)", fontsize=12)
    ax.set_title(
        "Pareto: Calidad vs Tiempo Computacional", fontsize=14, fontweight="bold"
    )
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3, linestyle="--")
    ax.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
    ax.set_xscale("log")

    fig.tight_layout()
    fig.savefig(output_path / "pareto_quality_time.png", dpi=200)
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

    colors = ["#95a5a6", "#3498db", "#e74c3c", "#2ecc71", "#9b59b6", "#f39c12"]
    labels = [ALGO_LABELS.get(a, a) for a in summary["algorithm"]]
    x = np.arange(len(labels))

    bars = ax.bar(
        x,
        summary["mean"],
        yerr=summary["std"],
        color=colors[: len(labels)],
        capsize=4,
        alpha=0.8,
    )
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15)
    ax.set_ylabel("Nivel de Servicio (%)")
    ax.set_title("Nivel de Servicio por Algoritmo", fontsize=14, fontweight="bold")
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.set_ylim(0, 105)

    fig.tight_layout()
    fig.savefig(output_path / "service_level_comparison.png", dpi=200)
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

    # Guardar tablas
    main_table.to_csv(output_path / "main_results_table.csv", index=False)
    inst_table.to_csv(output_path / "instance_results_table.csv", index=False)
    print(f"  Tabla principal: {output_path / 'main_results_table.csv'}")
    print(f"  Tabla instancias: {output_path / 'instance_results_table.csv'}")

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

    # Reporte Markdown
    print("\n--- Generando reporte ---")
    report_dir = Path("documentacion/reportes")
    report_dir.mkdir(parents=True, exist_ok=True)
    generate_markdown_report(main_table, output_path, report_dir)

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
