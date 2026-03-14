"""
Analisis de complejidad computacional (Sprint 4.5).

Genera:
1) Escalabilidad empirica (log-log y ajuste T(n)=a*n^k)
2) Performance profiles (Dolan-More) por tiempo
3) Convergence profiles normalizados por evaluaciones
4) Diversidad poblacional (GA, DE, GA-SA)
5) Profiling por componentes con cProfile (opcional)

Uso:
    python experiments/scripts/run_complexity_analysis.py
    python experiments/scripts/run_complexity_analysis.py --run-cprofile
"""

from __future__ import annotations

import argparse
import cProfile
import io
import json
import logging
import pstats
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, ".")

import matplotlib
import numpy as np
import pandas as pd
import yaml

from src.metaheuristics.de import DifferentialEvolution
from src.metaheuristics.ga import GeneticAlgorithm
from src.metaheuristics.ga_sa import HybridGASA
from src.metaheuristics.sa import SimulatedAnnealing
from src.model.parameters import ProblemInstance

matplotlib.use("Agg")
import matplotlib.pyplot as plt

LOG_FMT = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FMT)
logger = logging.getLogger("run_complexity")

ALGO_ORDER = ["ga", "sa", "de", "ga_sa"]
ALGO_LABELS = {
    "ga": "GA",
    "sa": "SA",
    "de": "DE",
    "ga_sa": "GA-SA",
    "baseline": "Baseline",
    "cbc_exact": "CBC",
}
ALGORITHM_CLASSES = {
    "ga": GeneticAlgorithm,
    "sa": SimulatedAnnealing,
    "de": DifferentialEvolution,
    "ga_sa": HybridGASA,
}


def _set_seed(seed: int) -> None:
    np.random.seed(seed)
    random.seed(seed)


def _load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_instance_metadata(config_path: Path) -> tuple[dict[str, dict], dict]:
    """Mapear instancia -> metadata (tamano, complejidad)."""
    cfg = _load_yaml(config_path)
    metadata: dict[str, dict] = {}
    for size, paths in cfg["instances"].items():
        for p in paths:
            pth = Path(p)
            inst = ProblemInstance.from_yaml(pth)
            name = pth.stem
            metadata[name] = {
                "size": size,
                "path": str(pth),
                "complexity": int(inst.n_cut_forms * inst.n_periods * inst.n_scenarios),
                "n_cut_forms": int(inst.n_cut_forms),
                "n_periods": int(inst.n_periods),
                "n_scenarios": int(inst.n_scenarios),
            }
    return metadata, cfg


def _enrich_comparison(df: pd.DataFrame, metadata: dict[str, dict]) -> pd.DataFrame:
    """Agregar columnas size/complexity/case_id."""
    out = df.copy()
    out["size"] = out["instance"].map(
        lambda x: metadata.get(x, {}).get("size", "unknown")
    )
    out["complexity"] = out["instance"].map(
        lambda x: metadata.get(x, {}).get("complexity", np.nan)
    )
    out["case_id"] = out["instance"] + "_s" + out["seed"].astype(int).astype(str)
    return out


def _save_plot(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
    logger.info("Grafico guardado: %s", path)


def analyze_scalability(
    df: pd.DataFrame, output_dir: Path
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Escalabilidad por tamano y ajuste log-log."""
    agg = (
        df.groupby(["algorithm", "size", "complexity"], as_index=False)
        .agg(
            elapsed_mean=("elapsed_seconds", "mean"),
            elapsed_std=("elapsed_seconds", "std"),
            eval_mean=("n_evaluations", "mean"),
            n_runs=("elapsed_seconds", "count"),
        )
        .sort_values(["algorithm", "complexity"])
    )

    fit_rows: list[dict] = []
    for algo, g in agg.groupby("algorithm"):
        fit_data = g[g["elapsed_mean"] > 0].drop_duplicates(subset=["complexity"])
        fit_data = fit_data.sort_values("complexity")
        if len(fit_data) < 2:
            fit_rows.append(
                {
                    "algorithm": algo,
                    "a": np.nan,
                    "k": np.nan,
                    "r2": np.nan,
                    "n_points": int(len(fit_data)),
                }
            )
            continue

        x = np.log(fit_data["complexity"].to_numpy(dtype=float))
        y = np.log(fit_data["elapsed_mean"].to_numpy(dtype=float))
        k, b = np.polyfit(x, y, deg=1)
        y_hat = k * x + b
        ss_res = float(np.sum((y - y_hat) ** 2))
        ss_tot = float(np.sum((y - np.mean(y)) ** 2))
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-12 else 1.0

        fit_rows.append(
            {
                "algorithm": algo,
                "a": float(np.exp(b)),
                "k": float(k),
                "r2": float(r2),
                "n_points": int(len(fit_data)),
            }
        )

    fit_df = pd.DataFrame(fit_rows).sort_values("algorithm")

    agg.to_csv(output_dir / "complexity_scaling_by_size.csv", index=False)
    fit_df.to_csv(output_dir / "complexity_exponent_fit.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 6))
    for algo, g in agg.groupby("algorithm"):
        g = g.sort_values("complexity")
        fit_row = fit_df[fit_df["algorithm"] == algo]
        k_text = ""
        if not fit_row.empty and pd.notna(fit_row.iloc[0]["k"]):
            k_text = f" (k={fit_row.iloc[0]['k']:.2f})"
        ax.plot(
            g["complexity"],
            g["elapsed_mean"],
            marker="o",
            linewidth=2,
            label=f"{ALGO_LABELS.get(algo, algo)}{k_text}",
        )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Complejidad n = F*T*W (log)")
    ax.set_ylabel("Tiempo medio (s, log)")
    ax.set_title("Escalabilidad empirica por algoritmo")
    ax.grid(alpha=0.25, linestyle="--")
    ax.legend()
    _save_plot(fig, output_dir / "complexity_loglog_scaling.png")

    return agg, fit_df


def analyze_performance_profile(df: pd.DataFrame, output_dir: Path) -> pd.DataFrame:
    """Perfil de performance Dolan-More basado en tiempo."""
    data = df[df["algorithm"].isin(ALGO_ORDER)].copy()
    if data.empty:
        return pd.DataFrame()

    pivot = data.pivot_table(
        index="case_id",
        columns="algorithm",
        values="elapsed_seconds",
        aggfunc="mean",
    )
    pivot = pivot.dropna(axis=0, how="any")
    if pivot.empty:
        return pd.DataFrame()

    best = pivot.min(axis=1)
    ratios = pivot.div(best, axis=0)

    tau_max = float(max(3.0, np.nanpercentile(ratios.to_numpy(), 95)))
    tau_grid = np.linspace(1.0, tau_max, 200)
    rows = []
    for algo in [a for a in ALGO_ORDER if a in ratios.columns]:
        r = ratios[algo].to_numpy(dtype=float)
        for tau in tau_grid:
            rows.append(
                {
                    "algorithm": algo,
                    "tau": float(tau),
                    "rho": float(np.mean(r <= tau)),
                    "n_cases": int(len(r)),
                }
            )

    profile_df = pd.DataFrame(rows)
    profile_df.to_csv(output_dir / "performance_profile.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 6))
    for algo, g in profile_df.groupby("algorithm"):
        ax.plot(g["tau"], g["rho"], linewidth=2, label=ALGO_LABELS.get(algo, algo))

    ax.set_xlabel("Tau (ratio de tiempo respecto al mejor por caso)")
    ax.set_ylabel("rho_a(tau) = P(r_a,i <= tau)")
    ax.set_title("Performance Profiles (Dolan-More)")
    ax.grid(alpha=0.25, linestyle="--")
    ax.legend()
    _save_plot(fig, output_dir / "performance_profile.png")

    return profile_df


def analyze_convergence_profiles(
    traces_df: pd.DataFrame, output_dir: Path
) -> pd.DataFrame:
    """Convergencia normalizada sobre eje de evaluaciones."""
    traces = traces_df[traces_df["algorithm"].isin(ALGO_ORDER)].copy()
    if traces.empty:
        return pd.DataFrame()

    run_series: dict[str, list[tuple[np.ndarray, np.ndarray]]] = {}
    grouped = traces.groupby(["algorithm", "instance", "seed"], sort=False)
    for (algo, _inst, _seed), g in grouped:
        g = g.sort_values(["n_evaluations", "iteration"])
        x = g["n_evaluations"].to_numpy(dtype=float)
        if len(x) == 0:
            continue
        if np.allclose(x, x[0]):
            x = np.arange(len(g), dtype=float)

        z_best = g["best_fitness"].to_numpy(dtype=float)
        z_curr = g["current_fitness"].to_numpy(dtype=float)
        z_max = float(np.nanmax(z_best))
        z_min = float(np.nanmin(z_curr))
        denom = z_max - z_min
        if denom <= 1e-12:
            y = np.ones_like(z_best, dtype=float)
        else:
            y = (z_best - z_min) / denom
            y = np.clip(y, 0.0, 1.0)

        run_series.setdefault(algo, []).append((x, y))

    rows: list[dict] = []
    fig, ax = plt.subplots(figsize=(9, 6))
    for algo in [a for a in ALGO_ORDER if a in run_series]:
        runs = run_series[algo]
        max_eval = max(float(np.max(x)) for x, _ in runs)
        if max_eval <= 0:
            continue

        x_grid = np.linspace(0.0, max_eval, 160)
        interp_values = []
        for x, y in runs:
            order = np.argsort(x)
            x_sorted = x[order]
            y_sorted = y[order]
            x_unique, idx = np.unique(x_sorted, return_index=True)
            y_unique = y_sorted[idx]
            if len(x_unique) < 2:
                y_grid = np.full_like(x_grid, y_unique[0], dtype=float)
            else:
                y_grid = np.interp(
                    x_grid,
                    x_unique,
                    y_unique,
                    left=y_unique[0],
                    right=y_unique[-1],
                )
            interp_values.append(y_grid)

        arr = np.vstack(interp_values)
        mean_curve = np.mean(arr, axis=0)
        std_curve = np.std(arr, axis=0)

        for x_val, m_val, s_val in zip(x_grid, mean_curve, std_curve):
            rows.append(
                {
                    "algorithm": algo,
                    "n_evaluations": float(x_val),
                    "mean_norm_z": float(m_val),
                    "std_norm_z": float(s_val),
                    "n_runs": int(len(runs)),
                }
            )

        ax.plot(
            x_grid,
            mean_curve,
            linewidth=2,
            label=ALGO_LABELS.get(algo, algo),
        )
        ax.fill_between(
            x_grid, mean_curve - std_curve, mean_curve + std_curve, alpha=0.2
        )

    ax.set_xlabel("Evaluaciones de fitness")
    ax.set_ylabel("Convergencia normalizada")
    ax.set_ylim(0, 1.05)
    ax.set_title("Convergence Profiles (media +/- std)")
    ax.grid(alpha=0.25, linestyle="--")
    ax.legend()
    _save_plot(fig, output_dir / "convergence_profiles.png")

    out = pd.DataFrame(rows)
    out.to_csv(output_dir / "convergence_profiles.csv", index=False)
    return out


def analyze_diversity_profiles(
    traces_df: pd.DataFrame, output_dir: Path
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Analizar diversidad en GA/DE/GA-SA."""
    div_data = traces_df[
        traces_df["algorithm"].isin(["ga", "de", "ga_sa"])
        & traces_df["diversity"].notna()
    ].copy()
    if div_data.empty:
        return pd.DataFrame(), pd.DataFrame()

    profile = (
        div_data.groupby(["algorithm", "iteration"], as_index=False)
        .agg(
            diversity_mean=("diversity", "mean"),
            diversity_std=("diversity", "std"),
            n_runs=("diversity", "count"),
        )
        .sort_values(["algorithm", "iteration"])
    )
    profile.to_csv(output_dir / "diversity_profiles.csv", index=False)

    # Convergencia prematura: diversidad <= 0.05 antes del 70% del horizonte
    run_flags = []
    for (algo, inst, seed), g in div_data.groupby(
        ["algorithm", "instance", "seed"], sort=False
    ):
        g = g.sort_values("iteration")
        max_iter = int(g["iteration"].max()) if not g.empty else 0
        threshold_iter = int(0.7 * max_iter)
        low_div = g[g["diversity"] <= 0.05]
        premature = False
        first_low_iter = np.nan
        if not low_div.empty and max_iter > 0:
            first_low_iter = int(low_div["iteration"].iloc[0])
            premature = first_low_iter <= threshold_iter
        run_flags.append(
            {
                "algorithm": algo,
                "instance": inst,
                "seed": int(seed),
                "max_iteration": max_iter,
                "first_low_div_iter": first_low_iter,
                "premature_convergence": premature,
            }
        )

    run_flags_df = pd.DataFrame(run_flags)
    summary = (
        run_flags_df.groupby("algorithm", as_index=False)
        .agg(
            premature_rate=("premature_convergence", "mean"),
            n_runs=("premature_convergence", "count"),
        )
        .sort_values("algorithm")
    )
    summary["premature_rate"] = summary["premature_rate"] * 100.0
    summary.to_csv(output_dir / "diversity_premature_summary.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 6))
    for algo, g in profile.groupby("algorithm"):
        x = g["iteration"].to_numpy(dtype=float)
        m = g["diversity_mean"].to_numpy(dtype=float)
        s = g["diversity_std"].to_numpy(dtype=float)
        ax.plot(x, m, linewidth=2, label=ALGO_LABELS.get(algo, algo))
        ax.fill_between(x, m - s, m + s, alpha=0.2)
    ax.axhline(0.05, color="black", linestyle="--", linewidth=1, label="umbral 0.05")
    ax.set_xlabel("Generacion / Iteracion")
    ax.set_ylabel("Diversidad promedio")
    ax.set_title("Diversidad poblacional")
    ax.grid(alpha=0.25, linestyle="--")
    ax.legend()
    _save_plot(fig, output_dir / "diversity_profiles.png")

    return profile, summary


def _categorize_profile_row(file_name: str, func_name: str) -> str:
    text = f"{file_name}::{func_name}".lower()
    if "decoder" in text or "decode" in text:
        return "decoder"
    if "objective" in text or "evaluate_vectorized" in text:
        return "objective"
    if "_local_search" in text:
        return "local_search"
    if "tournament" in text or "select" in text:
        return "selection"
    if (
        "crossover" in text
        or "mutate" in text
        or "neighborhood" in text
        or "_mutate_de" in text
        or "_crossover_de" in text
    ):
        return "operators"
    return "other"


def run_component_profiling(
    config: dict,
    output_dir: Path,
    profile_instance: str | None = None,
    seed: int = 1,
) -> pd.DataFrame:
    """Ejecutar cProfile para cada metaheuristica y resumir componentes."""
    profile_dir = output_dir / "cprofile"
    profile_dir.mkdir(parents=True, exist_ok=True)

    if profile_instance:
        inst_path = Path(profile_instance)
    else:
        medium = config["instances"].get("medium", [])
        inst_path = (
            Path(medium[0])
            if medium
            else Path(next(iter(config["instances"].values()))[0])
        )
    instance = ProblemInstance.from_yaml(inst_path)
    logger.info("cProfile sobre instancia: %s", inst_path)

    rows = []
    for algo in ALGO_ORDER:
        params = dict(config["algorithms"][algo].get("params", {}))
        cls = ALGORITHM_CLASSES[algo]

        _set_seed(seed)
        mh = cls(params)

        profiler = cProfile.Profile()
        t0 = time.time()
        profiler.enable()
        mh.solve(instance)
        profiler.disable()
        elapsed = time.time() - t0

        stats = pstats.Stats(profiler)
        stats.sort_stats("cumulative")
        txt_stream = io.StringIO()
        stats.stream = txt_stream
        stats.print_stats(60)
        txt_path = profile_dir / f"{algo}_profile.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(txt_stream.getvalue())

        totals = {
            "decoder": 0.0,
            "objective": 0.0,
            "operators": 0.0,
            "selection": 0.0,
            "local_search": 0.0,
            "other": 0.0,
        }

        for (file_name, _line_no, func_name), stat in stats.stats.items():
            tt = float(stat[2])  # self time
            bucket = _categorize_profile_row(file_name, func_name)
            totals[bucket] += tt

        total_tt = float(stats.total_tt)
        rows.append(
            {
                "algorithm": algo,
                "instance": inst_path.stem,
                "profile_elapsed_seconds": elapsed,
                "profile_total_tt": total_tt,
                "n_evaluations": int(mh.n_evaluations),
                "best_fitness": float(mh.best_fitness),
                **{f"{k}_tt": float(v) for k, v in totals.items()},
                **{
                    f"{k}_pct": (
                        float((v / total_tt) * 100.0) if total_tt > 1e-12 else np.nan
                    )
                    for k, v in totals.items()
                },
            }
        )

        logger.info("cProfile %s completado en %.2fs", algo, elapsed)

    out = pd.DataFrame(rows).sort_values("algorithm")
    out.to_csv(output_dir / "cprofile_component_breakdown.csv", index=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    categories = [
        "decoder",
        "objective",
        "operators",
        "selection",
        "local_search",
        "other",
    ]
    x = np.arange(len(out))
    bottom = np.zeros(len(out))
    for cat in categories:
        vals = out[f"{cat}_pct"].to_numpy(dtype=float)
        ax.bar(x, vals, bottom=bottom, label=cat)
        bottom += vals

    ax.set_xticks(x)
    ax.set_xticklabels([ALGO_LABELS.get(a, a) for a in out["algorithm"]], rotation=20)
    ax.set_ylabel("% tiempo (self-time)")
    ax.set_title("Descomposicion de tiempo por componente (cProfile)")
    ax.grid(axis="y", alpha=0.25, linestyle="--")
    ax.legend()
    _save_plot(fig, output_dir / "cprofile_component_breakdown.png")

    return out


def write_markdown_report(
    output_dir: Path,
    scaling_fit: pd.DataFrame,
    perf_df: pd.DataFrame,
    conv_df: pd.DataFrame,
    div_summary: pd.DataFrame,
    cprofile_df: pd.DataFrame | None,
) -> None:
    """Reporte markdown consolidado de sprint 4.5."""
    lines = [
        "# Reporte Sprint 4.5 - Complejidad Computacional",
        "",
        "## 1) Escalabilidad empirica",
        "",
        "Archivo: `complexity_exponent_fit.csv`",
        "",
        "| Algoritmo | a | k | R2 |",
        "|---|---:|---:|---:|",
    ]

    for _, row in scaling_fit.iterrows():
        lines.append(
            f"| {ALGO_LABELS.get(row['algorithm'], row['algorithm'])} "
            f"| {row['a']:.4g} | {row['k']:.3f} | {row['r2']:.3f} |"
        )

    lines.extend(
        [
            "",
            "## 2) Performance profiles",
            "",
            f"Casos completos utilizados: {int(perf_df['n_cases'].max()) if not perf_df.empty else 0}",
            "Grafico: `performance_profile.png`",
            "",
            "## 3) Convergence profiles",
            "",
            f"Curvas generadas: {'si' if not conv_df.empty else 'no'}",
            "Grafico: `convergence_profiles.png`",
            "",
            "## 4) Diversidad poblacional",
            "",
            "Resumen de convergencia prematura:",
            "",
            "| Algoritmo | % convergencia prematura | N runs |",
            "|---|---:|---:|",
        ]
    )

    if not div_summary.empty:
        for _, row in div_summary.iterrows():
            lines.append(
                f"| {ALGO_LABELS.get(row['algorithm'], row['algorithm'])} "
                f"| {row['premature_rate']:.2f}% | {int(row['n_runs'])} |"
            )
    else:
        lines.append("| n/a | n/a | 0 |")

    lines.extend(
        [
            "",
            "## 5) cProfile por componente",
            "",
            f"Ejecutado: {'si' if cprofile_df is not None and not cprofile_df.empty else 'no'}",
            "CSV: `cprofile_component_breakdown.csv`",
            "Grafico: `cprofile_component_breakdown.png`",
            "",
            "## Archivos generados",
            "",
            "- `complexity_scaling_by_size.csv`",
            "- `complexity_exponent_fit.csv`",
            "- `complexity_loglog_scaling.png`",
            "- `performance_profile.csv`",
            "- `performance_profile.png`",
            "- `convergence_profiles.csv`",
            "- `convergence_profiles.png`",
            "- `diversity_profiles.csv`",
            "- `diversity_profiles.png`",
            "- `diversity_premature_summary.csv`",
            "- `complexity_report.md`",
        ]
    )

    report_path = output_dir / "complexity_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    logger.info("Reporte guardado: %s", report_path)


def run_complexity_analysis(
    comparison_csv: str = "experiments/results/comparison.csv",
    traces_csv: str = "experiments/results/comparison_traces.csv",
    comparison_config: str = "experiments/config/comparison.yaml",
    output_dir: str = "experiments/results/complexity",
    run_cprofile: bool = False,
    profile_instance: str | None = None,
    profile_seed: int = 1,
) -> None:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    comp_path = Path(comparison_csv)
    if not comp_path.exists():
        raise FileNotFoundError(f"No existe CSV de comparacion: {comp_path}")

    metadata, cfg = _load_instance_metadata(Path(comparison_config))
    comparison_df = pd.read_csv(comp_path)
    comparison_df = _enrich_comparison(comparison_df, metadata)
    comparison_df.to_csv(out_dir / "comparison_enriched.csv", index=False)

    logger.info("Comparacion cargada: %d filas", len(comparison_df))

    scaling_by_size, scaling_fit = analyze_scalability(comparison_df, out_dir)
    perf_df = analyze_performance_profile(comparison_df, out_dir)

    traces_path = Path(traces_csv)
    conv_df = pd.DataFrame()
    div_profile = pd.DataFrame()
    div_summary = pd.DataFrame()
    if traces_path.exists():
        traces_df = pd.read_csv(traces_path)
        logger.info("Trazas cargadas: %d filas", len(traces_df))
        conv_df = analyze_convergence_profiles(traces_df, out_dir)
        div_profile, div_summary = analyze_diversity_profiles(traces_df, out_dir)
    else:
        logger.warning(
            "No existe archivo de trazas (%s). Se omiten convergence/diversity profiles.",
            traces_path,
        )

    cprofile_df = None
    if run_cprofile:
        cprofile_df = run_component_profiling(
            config=cfg,
            output_dir=out_dir,
            profile_instance=profile_instance,
            seed=profile_seed,
        )

    write_markdown_report(
        output_dir=out_dir,
        scaling_fit=scaling_fit,
        perf_df=perf_df,
        conv_df=conv_df,
        div_summary=div_summary,
        cprofile_df=cprofile_df,
    )

    summary = {
        "generated_at_epoch": time.time(),
        "n_comparison_rows": int(len(comparison_df)),
        "n_scaling_rows": int(len(scaling_by_size)),
        "n_performance_rows": int(len(perf_df)),
        "n_convergence_rows": int(len(conv_df)),
        "n_diversity_rows": int(len(div_profile)),
        "run_cprofile": bool(run_cprofile),
    }
    with open(out_dir / "complexity_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    logger.info("Resumen JSON guardado: %s", out_dir / "complexity_summary.json")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analisis de complejidad computacional (Sprint 4.5)"
    )
    parser.add_argument(
        "--comparison-csv",
        type=str,
        default="experiments/results/comparison.csv",
        help="CSV de resultados de comparacion",
    )
    parser.add_argument(
        "--traces-csv",
        type=str,
        default="experiments/results/comparison_traces.csv",
        help="CSV de trazas de convergencia/diversidad",
    )
    parser.add_argument(
        "--comparison-config",
        type=str,
        default="experiments/config/comparison.yaml",
        help="Config YAML de comparacion (para metadata de instancias)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="experiments/results/complexity",
        help="Directorio de salida para analisis 4.5",
    )
    parser.add_argument(
        "--run-cprofile",
        action="store_true",
        help="Ejecutar profiling de componentes con cProfile",
    )
    parser.add_argument(
        "--profile-instance",
        type=str,
        default=None,
        help="Ruta YAML de instancia para cProfile (opcional)",
    )
    parser.add_argument(
        "--profile-seed",
        type=int,
        default=1,
        help="Seed para corridas de cProfile",
    )
    args = parser.parse_args()

    run_complexity_analysis(
        comparison_csv=args.comparison_csv,
        traces_csv=args.traces_csv,
        comparison_config=args.comparison_config,
        output_dir=args.output_dir,
        run_cprofile=args.run_cprofile,
        profile_instance=args.profile_instance,
        profile_seed=args.profile_seed,
    )


if __name__ == "__main__":
    main()
