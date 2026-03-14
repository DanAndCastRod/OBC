"""
Analisis estadistico del banco de instancias de Fase 3.

Genera visualizaciones con:
- KDE + ECDF + boxenplot para distribuciones de demanda
- Series temporales con intervalos percentiles de incertidumbre
- Comparativas entre perfiles con pruebas no parametrica
- Heatmaps de correlacion Spearman entre coproductos

Uso:
    python notebooks/01_instance_analysis.py
"""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

sys.path.insert(0, ".")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

from src.model.parameters import ProblemInstance

OUTPUT_DIR = Path("notebooks/figures")
CATALOG_PATH = Path("data/instances/instance_catalog.json")
PROFILE_ORDER = ["toy", "small", "medium", "large", "industrial"]

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", context="notebook", palette="colorblind")

# Seaborn/Pandas emit FutureWarning from internals in some estimators/plots.
warnings.filterwarnings("ignore", category=FutureWarning, module=r"seaborn\..*")
warnings.filterwarnings("ignore", category=FutureWarning, module=r"pandas\..*")


def load_catalog(path: Path = CATALOG_PATH) -> list[dict]:
    """Cargar catalogo de instancias."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _resolve_instance_path(entry: dict, base_dir: Path) -> Path:
    yaml_path = Path(entry.get("yaml_path", ""))
    if not yaml_path or yaml_path.as_posix() == ".":
        yaml_path = base_dir / f"{entry['name']}.yaml"
    if not yaml_path.is_absolute():
        yaml_path = Path(".") / yaml_path
    if not yaml_path.exists():
        yaml_path = base_dir / f"{entry['name']}.yaml"
    return yaml_path


def load_instances(catalog: list[dict], base_dir: Path = Path("data/instances")) -> dict[str, ProblemInstance]:
    """Cargar instancias YAML del catalogo."""
    instances: dict[str, ProblemInstance] = {}
    for entry in catalog:
        yaml_path = _resolve_instance_path(entry, base_dir)
        instances[entry["name"]] = ProblemInstance.from_yaml(yaml_path)
    return instances


def build_demand_frame(catalog: list[dict], instances: dict[str, ProblemInstance]) -> pd.DataFrame:
    """Construir DataFrame largo de demanda: perfil/seed/forma/periodo/escenario."""
    records: list[pd.DataFrame] = []

    for entry in catalog:
        inst = instances[entry["name"]]
        f_count, t_count, w_count = inst.demand.shape

        period_idx = np.repeat(np.arange(t_count), w_count)
        scenario_idx = np.tile(np.arange(w_count), t_count)

        for f in range(f_count):
            form_name = (
                inst.cut_form_names[f]
                if f < len(inst.cut_form_names)
                else f"F{f}"
            )
            flat = inst.demand[f].reshape(-1)
            records.append(
                pd.DataFrame(
                    {
                        "instance": entry["name"],
                        "profile": entry["profile"],
                        "seed": int(entry["seed"]),
                        "form_idx": f,
                        "form_name": form_name,
                        "period": period_idx,
                        "scenario": scenario_idx,
                        "demand": flat,
                    }
                )
            )

    df = pd.concat(records, ignore_index=True)
    df["profile"] = pd.Categorical(df["profile"], categories=PROFILE_ORDER, ordered=True)
    return df


def _sample_per_profile(df: pd.DataFrame, n_per_profile: int, random_state: int = 42) -> pd.DataFrame:
    chunks = []
    for profile in PROFILE_ORDER:
        sub = df[df["profile"] == profile]
        if sub.empty:
            continue
        n = min(n_per_profile, len(sub))
        chunks.append(sub.sample(n=n, random_state=random_state))
    return pd.concat(chunks, ignore_index=True)


def plot_demand_histograms(demand_df: pd.DataFrame) -> None:
    """Distribucion de demanda con herramientas estadisticas robustas."""
    sample = _sample_per_profile(demand_df, n_per_profile=15_000, random_state=42).copy()
    sample["log_demand"] = np.log1p(sample["demand"])

    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
    fig.suptitle("Distribucion de demanda por perfil (KDE/ECDF/Boxen)", fontsize=14, fontweight="bold")

    sns.histplot(
        data=sample,
        x="log_demand",
        hue="profile",
        stat="density",
        common_norm=False,
        bins=60,
        element="step",
        fill=False,
        kde=True,
        ax=axes[0],
    )
    axes[0].set_title("Histograma + KDE (log1p demanda)")
    axes[0].set_xlabel("log(1 + demanda)")
    axes[0].set_ylabel("Densidad")

    sns.ecdfplot(
        data=sample,
        x="demand",
        hue="profile",
        ax=axes[1],
    )
    axes[1].set_xscale("log")
    axes[1].set_title("ECDF (escala log)")
    axes[1].set_xlabel("Demanda")
    axes[1].set_ylabel("F(x)")

    sns.boxenplot(
        data=sample,
        x="profile",
        y="demand",
        ax=axes[2],
    )
    axes[2].set_yscale("log")
    axes[2].set_title("Boxen por perfil (escala log)")
    axes[2].set_xlabel("Perfil")
    axes[2].set_ylabel("Demanda")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "demand_histograms.png", dpi=180)
    plt.close(fig)
    print(f"  Guardado: {OUTPUT_DIR / 'demand_histograms.png'}")


def _top_forms_for_profile(sub: pd.DataFrame, top_k: int = 3) -> list[str]:
    return (
        sub.groupby("form_name")["demand"]
        .mean()
        .sort_values(ascending=False)
        .head(top_k)
        .index.tolist()
    )


def plot_demand_by_period(demand_df: pd.DataFrame) -> None:
    """Demanda temporal con bandas de incertidumbre percentil 90%."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 5.5), sharey=False)
    fig.suptitle("Demanda por periodo con incertidumbre (P5-P95)", fontsize=14, fontweight="bold")

    for ax, profile in zip(axes, ["small", "large"]):
        sub = demand_df[demand_df["profile"] == profile]
        top_forms = _top_forms_for_profile(sub, top_k=3)

        for form_name in top_forms:
            form_sub = sub[sub["form_name"] == form_name]
            agg = (
                form_sub.groupby("period")["demand"]
                .agg(
                    mean="mean",
                    p05=lambda x: np.quantile(x, 0.05),
                    p95=lambda x: np.quantile(x, 0.95),
                )
                .reset_index()
            )
            ax.plot(agg["period"], agg["mean"], linewidth=2, label=form_name[:18])
            ax.fill_between(agg["period"], agg["p05"], agg["p95"], alpha=0.15)

        ax.set_title(f"{profile} - formas de mayor demanda")
        ax.set_xlabel("Periodo")
        ax.set_ylabel("Demanda (kg)")
        ax.legend(fontsize=8, loc="upper left")
        ax.grid(alpha=0.25, linestyle="--")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "demand_by_period.png", dpi=180)
    plt.close(fig)
    print(f"  Guardado: {OUTPUT_DIR / 'demand_by_period.png'}")


def plot_instance_catalog(catalog_df: pd.DataFrame) -> None:
    """Resumen del banco con estadistica inferencial entre perfiles."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
    fig.suptitle("Banco de instancias - resumen estadistico", fontsize=14, fontweight="bold")

    # 1) CV de demanda por perfil + prueba Kruskal-Wallis
    sns.boxplot(
        data=catalog_df,
        x="profile",
        y="demand_cv",
        order=PROFILE_ORDER,
        ax=axes[0],
        color="#D8ECFF",
        fliersize=0,
    )
    sns.stripplot(
        data=catalog_df,
        x="profile",
        y="demand_cv",
        order=PROFILE_ORDER,
        ax=axes[0],
        color="#1F4E79",
        size=5,
        jitter=0.18,
    )
    groups = [
        catalog_df.loc[catalog_df["profile"] == p, "demand_cv"].dropna().values
        for p in PROFILE_ORDER
        if (catalog_df["profile"] == p).any()
    ]
    if len(groups) >= 2:
        _, pval = stats.kruskal(*groups)
        axes[0].set_title(f"CV por perfil (Kruskal-Wallis p={pval:.3g})")
    else:
        axes[0].set_title("CV por perfil")
    axes[0].set_xlabel("Perfil")
    axes[0].set_ylabel("Coeficiente de variacion")

    # 2) Complejidad vs demanda media + correlacion Spearman
    sns.scatterplot(
        data=catalog_df,
        x="complexity",
        y="demand_mean",
        hue="profile",
        style="profile",
        s=90,
        ax=axes[1],
    )
    axes[1].set_xscale("log")
    rho, pval = stats.spearmanr(catalog_df["complexity"], catalog_df["demand_mean"])
    axes[1].set_title("Complejidad vs demanda media")
    axes[1].set_xlabel("Complejidad F*T*W (log)")
    axes[1].set_ylabel("Demanda media")
    axes[1].text(
        0.02,
        0.98,
        f"Spearman rho={rho:.2f}\np={pval:.3g}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none"},
    )

    # 3) Tiempo de solver por perfil resoluble (toy/small)
    solvable = catalog_df.dropna(subset=["solver_time"]).copy()
    if not solvable.empty:
        sns.pointplot(
            data=solvable,
            x="profile",
            y="solver_time",
            order=["toy", "small"],
            errorbar=("ci", 95),
            n_boot=2000,
            ax=axes[2],
            color="#D95F02",
        )
        sns.stripplot(
            data=solvable,
            x="profile",
            y="solver_time",
            order=["toy", "small"],
            ax=axes[2],
            color="#4A4A4A",
            size=6,
            jitter=0.08,
        )
        if {"toy", "small"}.issubset(set(solvable["profile"].unique())):
            toy_t = solvable.loc[solvable["profile"] == "toy", "solver_time"].values
            small_t = solvable.loc[solvable["profile"] == "small", "solver_time"].values
            _, p_mw = stats.mannwhitneyu(toy_t, small_t, alternative="two-sided")
            axes[2].set_title(f"Tiempo CBC (Mann-Whitney p={p_mw:.3g})")
        else:
            axes[2].set_title("Tiempo CBC por perfil")
        axes[2].set_xlabel("Perfil")
        axes[2].set_ylabel("Tiempo (s)")
    else:
        axes[2].text(0.5, 0.5, "Sin datos de solver", ha="center", va="center")
        axes[2].set_axis_off()

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "instance_catalog_overview.png", dpi=180)
    plt.close(fig)
    print(f"  Guardado: {OUTPUT_DIR / 'instance_catalog_overview.png'}")


def plot_optimal_solutions(catalog_df: pd.DataFrame) -> None:
    """Analisis de Z* y trade-off tiempo vs objetivo para instancias resolubles."""
    solvable = catalog_df.dropna(subset=["optimal_z", "solver_time"]).copy()
    if solvable.empty:
        print("  No hay instancias con solucion optima.")
        return

    solvable["optimal_z_mcop"] = solvable["optimal_z"] / 1e6

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    fig.suptitle("Soluciones optimas CBC - analisis estadistico", fontsize=14, fontweight="bold")

    sns.pointplot(
        data=solvable,
        x="profile",
        y="optimal_z_mcop",
        order=["toy", "small"],
        errorbar=("ci", 95),
        n_boot=2000,
        ax=axes[0],
        color="#2A9D8F",
    )
    sns.stripplot(
        data=solvable,
        x="profile",
        y="optimal_z_mcop",
        order=["toy", "small"],
        ax=axes[0],
        color="#2F2F2F",
        size=6,
        jitter=0.1,
    )
    if {"toy", "small"}.issubset(set(solvable["profile"].unique())):
        toy_z = solvable.loc[solvable["profile"] == "toy", "optimal_z_mcop"].values
        small_z = solvable.loc[solvable["profile"] == "small", "optimal_z_mcop"].values
        _, p_mw = stats.mannwhitneyu(toy_z, small_z, alternative="two-sided")
        axes[0].set_title(f"Z* por perfil (Mann-Whitney p={p_mw:.3g})")
    else:
        axes[0].set_title("Z* por perfil")
    axes[0].set_xlabel("Perfil")
    axes[0].set_ylabel("Z* (millones COP)")

    sns.scatterplot(
        data=solvable,
        x="solver_time",
        y="optimal_z_mcop",
        hue="profile",
        style="profile",
        s=90,
        ax=axes[1],
    )
    for _, row in solvable.iterrows():
        axes[1].annotate(
            row["name"],
            (row["solver_time"], row["optimal_z_mcop"]),
            textcoords="offset points",
            xytext=(4, 4),
            fontsize=8,
        )
    axes[1].set_title("Trade-off: tiempo vs Z*")
    axes[1].set_xlabel("Tiempo solver (s)")
    axes[1].set_ylabel("Z* (millones COP)")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "optimal_solutions.png", dpi=180)
    plt.close(fig)
    print(f"  Guardado: {OUTPUT_DIR / 'optimal_solutions.png'}")


def plot_demand_correlation_heatmaps(catalog: list[dict], instances: dict[str, ProblemInstance]) -> None:
    """Heatmaps de correlacion Spearman entre coproductos (perfiles clave)."""
    target_profiles = ["small", "medium", "industrial"]
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
    fig.suptitle("Correlacion Spearman de demanda entre coproductos", fontsize=14, fontweight="bold")

    for idx, profile in enumerate(target_profiles):
        ax = axes[idx]
        candidates = [e for e in catalog if e["profile"] == profile]
        if not candidates:
            ax.set_axis_off()
            continue

        ref = sorted(candidates, key=lambda x: x["seed"])[0]
        inst = instances[ref["name"]]

        mat = inst.demand.reshape(inst.n_cut_forms, -1).T  # [T*W, F]
        names = [
            (inst.cut_form_names[i][:14] if i < len(inst.cut_form_names) else f"F{i}")
            for i in range(inst.n_cut_forms)
        ]
        corr = pd.DataFrame(mat, columns=names).corr(method="spearman")

        sns.heatmap(
            corr,
            ax=ax,
            cmap="coolwarm",
            vmin=-1.0,
            vmax=1.0,
            square=True,
            cbar=(idx == len(target_profiles) - 1),
            annot=False,
            linewidths=0.2,
        )
        ax.set_title(f"{profile} (seed {ref['seed']})")
        ax.tick_params(axis="x", rotation=45, labelsize=7)
        ax.tick_params(axis="y", labelsize=7)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "demand_correlation_heatmaps.png", dpi=180)
    plt.close(fig)
    print(f"  Guardado: {OUTPUT_DIR / 'demand_correlation_heatmaps.png'}")


def print_summary_table(catalog_df: pd.DataFrame, demand_df: pd.DataFrame) -> None:
    """Resumen tabular para trazabilidad en reporte."""
    print(f"\n{'='*106}")
    print(
        f"{'Nombre':<22} {'Perfil':<11} {'F':>2} {'T':>3} {'W':>4} "
        f"{'Demand mu':>10} {'CV':>5} {'Z* (M)':>10} {'t(s)':>6}"
    )
    print("-" * 106)
    for _, row in catalog_df.iterrows():
        z_str = f"{row['optimal_z']/1e6:,.1f}" if pd.notna(row["optimal_z"]) else "-"
        t_str = f"{row['solver_time']:.2f}" if pd.notna(row["solver_time"]) else "-"
        print(
            f"{row['name']:<22} {row['profile']:<11} {int(row['n_cut_forms']):>2} "
            f"{int(row['n_periods']):>3} {int(row['n_scenarios']):>4} "
            f"{row['demand_mean']:>10,.1f} {row['demand_cv']:>5.3f} "
            f"{z_str:>10} {t_str:>6}"
        )
    print(f"{'='*106}")

    profile_stats = (
        demand_df.groupby("profile", observed=False)["demand"]
        .agg(mean="mean", std="std", median="median")
        .reset_index()
    )
    profile_stats["cv"] = profile_stats["std"] / profile_stats["mean"]
    profile_stats["skew"] = [
        stats.skew(demand_df.loc[demand_df["profile"] == p, "demand"], bias=False)
        for p in profile_stats["profile"]
    ]
    profile_stats["kurtosis"] = [
        stats.kurtosis(demand_df.loc[demand_df["profile"] == p, "demand"], fisher=True, bias=False)
        for p in profile_stats["profile"]
    ]

    print("\nResumen por perfil (demanda):")
    print(profile_stats.to_string(index=False, float_format=lambda x: f"{x:,.4f}"))


def main() -> None:
    print("=" * 72)
    print("Analisis estadistico del banco de instancias - Sprint 3.3")
    print("=" * 72)

    catalog = load_catalog()
    catalog_df = pd.DataFrame(catalog).copy()
    catalog_df["profile"] = pd.Categorical(catalog_df["profile"], categories=PROFILE_ORDER, ordered=True)
    catalog_df["complexity"] = (
        catalog_df["n_cut_forms"] * catalog_df["n_periods"] * catalog_df["n_scenarios"]
    )
    catalog_df["solver_time"] = pd.to_numeric(catalog_df["solver_time"], errors="coerce")
    catalog_df["optimal_z"] = pd.to_numeric(catalog_df["optimal_z"], errors="coerce")

    print(f"Instancias en catalogo: {len(catalog_df)}")
    print(f"Perfiles: {sorted(catalog_df['profile'].dropna().unique())}")
    print(f"Seeds: {sorted(catalog_df['seed'].unique())}")
    print(
        "Chequeo rapido: "
        f"{len(catalog_df)} instancias, "
        f"{catalog_df['optimal_z'].notna().sum()} con Z* CBC, "
        f"{catalog_df['solver_time'].notna().sum()} con tiempo CBC."
    )

    instances = load_instances(catalog)
    demand_df = build_demand_frame(catalog, instances)

    print("\nGenerando graficas...")
    plot_demand_histograms(demand_df)
    plot_demand_by_period(demand_df)
    plot_instance_catalog(catalog_df)
    plot_optimal_solutions(catalog_df)
    plot_demand_correlation_heatmaps(catalog, instances)

    print_summary_table(catalog_df, demand_df)

    print(f"\nFiguras guardadas en: {OUTPUT_DIR.resolve()}")
    print("Analisis completado.")


if __name__ == "__main__":
    main()
