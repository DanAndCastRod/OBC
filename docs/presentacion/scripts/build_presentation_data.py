"""Build data bundle consumed by docs/presentacion/sustentacion_coproductos.html.

This script consolidates experiment outputs into a single JS payload:
    window.PRESENTATION_DATA = { ... }

Run:
    python docs/presentacion/scripts/build_presentation_data.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (float, int, np.floating, np.integer)):
        if np.isnan(value):
            return None
        return float(value)
    try:
        f = float(value)
        if np.isnan(f):
            return None
        return f
    except Exception:
        return None


def _safe_int(value: Any) -> int | None:
    f = _safe_float(value)
    if f is None:
        return None
    return int(round(f))


def _algorithm_label(algorithm: str) -> str:
    mapping = {
        "ga_sa": "GA-SA",
        "de": "DE",
        "ga": "GA",
        "sa": "SA",
        "baseline": "Baseline",
        "cbc_exact": "CBC exacto",
    }
    return mapping.get(algorithm, algorithm.upper())


def _algorithm_color(algorithm: str) -> str:
    mapping = {
        "ga_sa": "#008B8B",
        "de": "#00b3b3",
        "ga": "#365660",
        "sa": "#F28C28",
        "baseline": "#64748b",
        "cbc_exact": "#111827",
    }
    return mapping.get(algorithm, "#334155")


def _load_optuna_trials(tuning_dir: Path) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for algo in ["ga", "sa", "de", "ga_sa"]:
        csv_path = tuning_dir / f"tuning_{algo}_trials.csv"
        if not csv_path.exists():
            continue
        df = pd.read_csv(csv_path)
        param_cols = [c for c in df.columns if c.startswith("param_")]
        param_names = [c.replace("param_", "") for c in param_cols]

        trials = []
        for _, row in df.iterrows():
            params = {
                c.replace("param_", ""): _safe_float(row[c]) for c in param_cols
            }
            trials.append(
                {
                    "trial": _safe_int(row.get("trial")),
                    "state": row.get("state"),
                    "value": _safe_float(row.get("value")),
                    "best_so_far": _safe_float(row.get("best_so_far")),
                    "duration_seconds": _safe_float(row.get("duration_seconds")),
                    "eval_status": row.get("user_eval_status"),
                    "params": params,
                }
            )

        completed = df[df["state"] == "COMPLETE"].copy()
        param_ranges = {}
        for c in param_cols:
            valid = completed[c].dropna()
            if valid.empty:
                continue
            param_ranges[c.replace("param_", "")] = {
                "min": _safe_float(valid.min()),
                "max": _safe_float(valid.max()),
            }

        payload[algo] = {
            "label": _algorithm_label(algo),
            "trial_count": int(len(df)),
            "param_names": param_names,
            "param_ranges": param_ranges,
            "trials": trials,
        }
    return payload


def _build_scientific_audit(
    results_dir: Path,
    comparison: pd.DataFrame,
    stats_json: dict[str, Any],
) -> dict[str, Any]:
    """Construir metadatos de auditoria cientifica para la presentacion."""
    audit: dict[str, Any] = {}

    meta_algos = ["ga_sa", "de", "ga", "sa"]
    meta = comparison[comparison["algorithm"].isin(meta_algos)].copy()
    grouped = (
        meta.groupby(["algorithm", "instance"], as_index=False)
        .agg(
            z_nunique=("z_value", "nunique"),
            low_rot_nunique=("low_rotation_inventory", "nunique"),
            n_runs=("z_value", "size"),
        )
    )

    if not grouped.empty:
        audit["constancy"] = {
            "z_constant_group_pct": _safe_float(
                100.0 * float((grouped["z_nunique"] == 1).mean())
            ),
            "low_rotation_constant_group_pct": _safe_float(
                100.0 * float((grouped["low_rot_nunique"] == 1).mean())
            ),
            "groups_total": int(len(grouped)),
        }
    else:
        audit["constancy"] = {
            "z_constant_group_pct": None,
            "low_rotation_constant_group_pct": None,
            "groups_total": 0,
        }

    baseline_inv = (
        comparison[comparison["algorithm"] == "baseline"]
        .groupby("instance", as_index=True)["low_rotation_inventory"]
        .mean()
    )
    informative = baseline_inv[np.abs(baseline_inv.values) > 1e-9]
    audit["h3_sample"] = {
        "total_instances": int(len(baseline_inv)),
        "informative_instances_baseline_gt_zero": int(len(informative)),
    }

    # Gap vs CBC exacto por algoritmo
    gap_vs_cbc = []
    for algo in meta_algos:
        rows = comparison[comparison["algorithm"] == algo]
        if rows.empty:
            continue
        gap_vs_cbc.append(
            {
                "algorithm": algo,
                "label": _algorithm_label(algo),
                "mean_gap_percent": _safe_float(rows["gap_percent"].mean()),
                "median_gap_percent": _safe_float(rows["gap_percent"].median()),
                "p90_gap_percent": _safe_float(rows["gap_percent"].quantile(0.90)),
            }
        )
    audit["gap_vs_cbc"] = gap_vs_cbc

    # Ratio de tiempos GA-SA / CBC por instancia
    cbc_t = (
        comparison[comparison["algorithm"] == "cbc_exact"]
        .groupby("instance", as_index=False)["elapsed_seconds"]
        .mean()
        .rename(columns={"elapsed_seconds": "t_cbc"})
    )
    gasa_t = (
        comparison[comparison["algorithm"] == "ga_sa"]
        .groupby("instance", as_index=False)["elapsed_seconds"]
        .mean()
        .rename(columns={"elapsed_seconds": "t_gasa"})
    )
    time_ratio_payload = {
        "mean_ratio": None,
        "median_ratio": None,
        "min_ratio": None,
        "max_ratio": None,
        "n_instances": 0,
    }
    if not cbc_t.empty and not gasa_t.empty:
        ratio_df = gasa_t.merge(cbc_t, on="instance", how="inner")
        if not ratio_df.empty:
            ratio = ratio_df["t_gasa"] / ratio_df["t_cbc"].clip(lower=1e-9)
            time_ratio_payload = {
                "mean_ratio": _safe_float(ratio.mean()),
                "median_ratio": _safe_float(ratio.median()),
                "min_ratio": _safe_float(ratio.min()),
                "max_ratio": _safe_float(ratio.max()),
                "n_instances": int(len(ratio)),
            }
    audit["time_ratio_gasa_vs_cbc"] = time_ratio_payload

    # Hipotesis principales desde statistical_tests.json
    protocol = stats_json.get("protocol", {})
    audit["protocol"] = {
        "version": protocol.get("version"),
        "updated_at": protocol.get("updated_at"),
        "primary_analysis_unit": protocol.get("primary_analysis_unit"),
        "multiple_testing": protocol.get("multiple_testing"),
        "h3_primary_endpoint": protocol.get("h3_primary_endpoint"),
        "h3_secondary_endpoint": protocol.get("h3_secondary_endpoint"),
    }

    htests = stats_json.get("hypothesis_tests", [])
    h2_main = next((x for x in htests if x.get("hypothesis") == "H2"), None)
    h2_run = next((x for x in htests if x.get("hypothesis") == "H2-run"), None)
    audit["h2_summary"] = {
        "instance_level_p_value": _safe_float(
            h2_main.get("p_value") if h2_main else None
        ),
        "instance_level_gap_percent": _safe_float(
            h2_main.get("metric_value") if h2_main else None
        ),
        "run_level_p_value": _safe_float(h2_run.get("p_value") if h2_run else None),
        "run_level_gap_percent": _safe_float(
            h2_run.get("metric_value") if h2_run else None
        ),
    }

    def _hypothesis_group_summary(name: str) -> dict[str, Any]:
        rows = [x for x in htests if x.get("hypothesis") == name]
        if not rows:
            return {
                "n_tests": 0,
                "supported_algorithms": [],
                "mean_metric_value": None,
                "min_p_value": None,
            }
        supported = [
            x.get("description", "n/a")
            for x in rows
            if str(x.get("verdict", "")) == "SUPPORTED"
        ]
        metrics = pd.Series([_safe_float(x.get("metric_value")) for x in rows]).dropna()
        pvals = pd.Series([_safe_float(x.get("p_value")) for x in rows]).dropna()
        return {
            "n_tests": int(len(rows)),
            "supported_algorithms": supported,
            "mean_metric_value": _safe_float(metrics.mean() if not metrics.empty else None),
            "min_p_value": _safe_float(pvals.min() if not pvals.empty else None),
        }

    audit["h3_summary"] = {
        "primary": _hypothesis_group_summary("H3"),
        "low_rotation": _hypothesis_group_summary("H3-lowrot"),
    }

    # Validacion externa FENAVI
    fenavi_summary_path = results_dir / "fenavi_validation" / "fenavi_validation_summary.json"
    fenavi_external_path = (
        results_dir / "fenavi_validation" / "fenavi_external_monthly_comparison.csv"
    )
    fenavi_external_summary_path = (
        results_dir / "fenavi_validation" / "fenavi_external_monthly_summary.csv"
    )
    fenavi_payload: dict[str, Any] = {}
    if fenavi_summary_path.exists():
        with open(fenavi_summary_path, "r", encoding="utf-8") as f:
            fenavi_summary = json.load(f)
        fenavi_payload.update(
            {
                "price_within_range_pct": _safe_float(
                    fenavi_summary.get("price_within_range_pct")
                ),
                "external_comparison_products": _safe_int(
                    fenavi_summary.get("external_comparison_products")
                ),
                "external_comparison_series": _safe_int(
                    fenavi_summary.get("external_comparison_series")
                ),
                "external_variable_types": fenavi_summary.get("external_variable_types", []),
            }
        )

    if fenavi_external_path.exists():
        ext = pd.read_csv(fenavi_external_path)
        if not ext.empty and "spearman_rho" in ext.columns:
            fenavi_payload["spearman_rho_mean"] = _safe_float(ext["spearman_rho"].mean())
            fenavi_payload["spearman_rho_abs_mean"] = _safe_float(
                ext["spearman_rho"].abs().mean()
            )
            fenavi_payload["ks_stat_mean"] = _safe_float(ext["ks_statistic"].mean())
            if "best_lag_spearman_rho" in ext.columns:
                fenavi_payload["best_lag_spearman_abs_mean"] = _safe_float(
                    ext["best_lag_spearman_rho"].abs().mean()
                )
            if "peak_month_shift_abs" in ext.columns:
                fenavi_payload["peak_month_shift_abs_mean"] = _safe_float(
                    ext["peak_month_shift_abs"].mean()
                )

    if fenavi_external_summary_path.exists():
        ext_sum = pd.read_csv(fenavi_external_summary_path)
        if not ext_sum.empty:
            fenavi_payload["by_variable_type"] = []
            for _, row in ext_sum.iterrows():
                fenavi_payload["by_variable_type"].append(
                    {
                        "variable_type": row.get("variable_type"),
                        "n_products": _safe_int(row.get("n_products")),
                        "spearman_rho_abs_mean": _safe_float(
                            row.get("spearman_rho_abs_mean")
                        ),
                        "best_lag_spearman_abs_mean": _safe_float(
                            row.get("best_lag_spearman_abs_mean")
                        ),
                        "mean_peak_month_shift_abs": _safe_float(
                            row.get("mean_peak_month_shift_abs")
                        ),
                    }
                )

    audit["fenavi_validation"] = fenavi_payload

    warnings: list[str] = []
    if not audit["protocol"].get("version"):
        warnings.append(
            "No se encontro metadato de protocolo estadistico en statistical_tests.json."
        )
    if audit["h3_sample"]["informative_instances_baseline_gt_zero"] < 5:
        warnings.append(
            "H3 tiene baja potencia: pocas instancias con baseline de baja rotacion > 0."
        )
    if audit["h3_summary"]["primary"]["n_tests"] == 0:
        warnings.append(
            "No hay resultados para H3 primario (inventario promedio total)."
        )
    mean_ratio = audit["time_ratio_gasa_vs_cbc"]["mean_ratio"]
    if mean_ratio is not None and mean_ratio > 1.0:
        warnings.append(
            "GA-SA no fue mas rapido que CBC en las instancias medidas."
        )
    abs_rho = audit.get("fenavi_validation", {}).get("spearman_rho_abs_mean")
    if abs_rho is not None and abs_rho < 0.3:
        warnings.append(
            "La correlacion temporal sintetico vs referencia externa FENAVI es baja."
        )
    lag_abs_rho = audit.get("fenavi_validation", {}).get("best_lag_spearman_abs_mean")
    if lag_abs_rho is not None and lag_abs_rho < 0.3:
        warnings.append(
            "Incluso con desfase temporal (lag), la alineacion sintetico-FENAVI sigue baja."
        )
    audit["warnings"] = warnings

    return audit


def _build_payload(root: Path) -> dict[str, Any]:
    results = root / "experiments" / "results"
    comparison = pd.read_csv(results / "comparison.csv")
    traces = pd.read_csv(results / "comparison_traces.csv")
    conv = pd.read_csv(results / "complexity" / "convergence_profiles.csv")
    div = pd.read_csv(results / "complexity" / "diversity_profiles.csv")

    with open(results / "sensitivity.json", "r", encoding="utf-8") as f:
        sensitivity_json = json.load(f)
    with open(results / "statistical_tests.json", "r", encoding="utf-8") as f:
        stats_json = json.load(f)

    comparison["size"] = comparison["instance"].str.extract(
        r"^(small|medium|large)", expand=False
    )

    algo_order = ["ga_sa", "de", "ga", "sa", "baseline", "cbc_exact"]
    algorithm_summary = []
    for algo, group in comparison.groupby("algorithm"):
        algorithm_summary.append(
            {
                "algorithm": algo,
                "label": _algorithm_label(algo),
                "mean_z_mcop": _safe_float(group["z_value"].mean() / 1e6),
                "std_z_mcop": _safe_float(group["z_value"].std(ddof=0) / 1e6),
                "mean_gap_percent": _safe_float(group["gap_percent"].mean()),
                "mean_service_level": _safe_float(group["service_level"].mean()),
                "mean_inventory": _safe_float(group["avg_inventory"].mean()),
                "mean_elapsed_seconds": _safe_float(group["elapsed_seconds"].mean()),
                "median_elapsed_seconds": _safe_float(group["elapsed_seconds"].median()),
                "mean_n_evaluations": _safe_float(group["n_evaluations"].mean()),
                "feasible_rate_percent": _safe_float(100.0 * group["is_feasible"].mean()),
                "n": int(len(group)),
                "color": _algorithm_color(algo),
            }
        )
    algorithm_summary = sorted(
        algorithm_summary,
        key=lambda x: algo_order.index(x["algorithm"])
        if x["algorithm"] in algo_order
        else 99,
    )

    algorithm_by_size = []
    grouped = comparison.groupby(["algorithm", "size"], as_index=False).agg(
        mean_z_value=("z_value", "mean"),
        mean_gap_percent=("gap_percent", "mean"),
        mean_elapsed_seconds=("elapsed_seconds", "mean"),
    )
    for _, row in grouped.iterrows():
        algorithm_by_size.append(
            {
                "algorithm": row["algorithm"],
                "label": _algorithm_label(row["algorithm"]),
                "size": row["size"],
                "mean_z_mcop": _safe_float(row["mean_z_value"] / 1e6),
                "mean_gap_percent": _safe_float(row["mean_gap_percent"]),
                "mean_elapsed_seconds": _safe_float(row["mean_elapsed_seconds"]),
            }
        )

    convergence_profiles: dict[str, Any] = {}
    for algo in ["ga_sa", "de", "ga", "sa"]:
        sub = conv[conv["algorithm"] == algo].sort_values("n_evaluations")
        if sub.empty:
            continue
        idx = np.linspace(0, len(sub) - 1, min(40, len(sub)), dtype=int)
        sampled = sub.iloc[idx].drop_duplicates(subset=["n_evaluations"])
        convergence_profiles[algo] = {
            "label": _algorithm_label(algo),
            "color": _algorithm_color(algo),
            "n_evaluations": [float(v) for v in sampled["n_evaluations"].values],
            "mean_norm_z": [float(v) for v in sampled["mean_norm_z"].values],
            "std_norm_z": [float(v) for v in sampled["std_norm_z"].values],
        }

    diversity_profiles: dict[str, Any] = {}
    for algo in ["ga_sa", "de", "ga", "sa"]:
        sub = div[div["algorithm"] == algo].sort_values("iteration")
        if sub.empty:
            continue
        idx = np.linspace(0, len(sub) - 1, min(40, len(sub)), dtype=int)
        sampled = sub.iloc[idx].drop_duplicates(subset=["iteration"])
        diversity_profiles[algo] = {
            "label": _algorithm_label(algo),
            "color": _algorithm_color(algo),
            "iteration": [int(v) for v in sampled["iteration"].values],
            "diversity_mean": [float(v) for v in sampled["diversity_mean"].values],
        }

    sensitivity = {}
    for row in sensitivity_json.get("parameter_delta_summary", []):
        p = row["parameter"]
        sensitivity.setdefault(p, []).append(
            {
                "delta": _safe_float(row.get("delta")),
                "mean_gap_percent": _safe_float(row.get("mean_gap_percent")),
                "mean_elapsed_seconds": _safe_float(row.get("mean_elapsed_seconds")),
                "mean_z_mcop": _safe_float(row.get("mean_z_value", 0.0) / 1e6),
                "feasible_rate_percent": _safe_float(row.get("feasible_rate_percent")),
            }
        )
    for p in sensitivity:
        sensitivity[p] = sorted(sensitivity[p], key=lambda x: x["delta"])

    heatmap_rows = []
    grouped_heat = comparison.groupby(["algorithm", "instance"], as_index=False).agg(
        mean_gap_percent=("gap_percent", "mean"),
        mean_elapsed_seconds=("elapsed_seconds", "mean"),
        mean_service_level=("service_level", "mean"),
        mean_z_value=("z_value", "mean"),
        n_runs=("z_value", "size"),
    )
    for _, row in grouped_heat.iterrows():
        heatmap_rows.append(
            {
                "algorithm": row["algorithm"],
                "label": _algorithm_label(row["algorithm"]),
                "instance": row["instance"],
                "size": str(row["instance"]).split("_", maxsplit=1)[0],
                "mean_gap_percent": _safe_float(row["mean_gap_percent"]),
                "mean_elapsed_seconds": _safe_float(row["mean_elapsed_seconds"]),
                "mean_service_level": _safe_float(row["mean_service_level"]),
                "mean_z_mcop": _safe_float(row["mean_z_value"] / 1e6),
                "n_runs": int(row["n_runs"]),
            }
        )

    low_rotation_quantiles = {"all": []}
    for algo, group in comparison.groupby("algorithm"):
        q = group["low_rotation_inventory"].quantile([0.1, 0.25, 0.5, 0.75, 0.9])
        low_rotation_quantiles["all"].append(
            {
                "algorithm": algo,
                "label": _algorithm_label(algo),
                "q10": _safe_float(q.loc[0.1]),
                "q25": _safe_float(q.loc[0.25]),
                "q50": _safe_float(q.loc[0.5]),
                "q75": _safe_float(q.loc[0.75]),
                "q90": _safe_float(q.loc[0.9]),
                "mean": _safe_float(group["low_rotation_inventory"].mean()),
            }
        )
    for size in ["small", "medium", "large"]:
        low_rotation_quantiles[size] = []
        subset = comparison[comparison["size"] == size]
        for algo, group in subset.groupby("algorithm"):
            q = group["low_rotation_inventory"].quantile([0.1, 0.25, 0.5, 0.75, 0.9])
            low_rotation_quantiles[size].append(
                {
                    "algorithm": algo,
                    "label": _algorithm_label(algo),
                    "q10": _safe_float(q.loc[0.1]),
                    "q25": _safe_float(q.loc[0.25]),
                    "q50": _safe_float(q.loc[0.5]),
                    "q75": _safe_float(q.loc[0.75]),
                    "q90": _safe_float(q.loc[0.9]),
                    "mean": _safe_float(group["low_rotation_inventory"].mean()),
                }
            )

    pareto_points = []
    for _, row in comparison.iterrows():
        pareto_points.append(
            {
                "algorithm": row["algorithm"],
                "label": _algorithm_label(row["algorithm"]),
                "size": row["size"],
                "instance": row["instance"],
                "seed": _safe_int(row["seed"]),
                "elapsed_seconds": _safe_float(row["elapsed_seconds"]),
                "z_mcop": _safe_float(row["z_value"] / 1e6),
                "gap_percent": _safe_float(row["gap_percent"]),
                "service_level": _safe_float(row["service_level"]),
            }
        )

    optuna_trials = _load_optuna_trials(results / "tuning")
    scientific_audit = _build_scientific_audit(
        results_dir=results,
        comparison=comparison,
        stats_json=stats_json,
    )

    payload = {
        "generated_from": {
            "comparison_csv": str(results / "comparison.csv"),
            "comparison_traces_csv": str(results / "comparison_traces.csv"),
            "convergence_csv": str(results / "complexity" / "convergence_profiles.csv"),
            "diversity_csv": str(results / "complexity" / "diversity_profiles.csv"),
            "sensitivity_json": str(results / "sensitivity.json"),
            "statistical_tests_json": str(results / "statistical_tests.json"),
        },
        "algorithm_summary": algorithm_summary,
        "algorithm_by_size": algorithm_by_size,
        "convergence_profiles": convergence_profiles,
        "diversity_profiles": diversity_profiles,
        "sensitivity": sensitivity,
        "optuna_trials": optuna_trials,
        "instance_heatmap": heatmap_rows,
        "low_rotation_quantiles": low_rotation_quantiles,
        "pareto_points": pareto_points,
        "hypotheses": {
            "H1": stats_json.get("summary", {}).get("H1"),
            "H2": stats_json.get("summary", {}).get("H2"),
            "H3": stats_json.get("summary", {}).get("H3"),
        },
        "trace_counts": {
            "comparison_rows": int(len(comparison)),
            "trace_rows": int(len(traces)),
        },
        "scientific_audit": scientific_audit,
    }
    return payload


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    payload = _build_payload(root)
    out_js = root / "docs" / "presentacion" / "presentation_data.js"
    out_js.write_text(
        "window.PRESENTATION_DATA = "
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    print(f"Updated {out_js}")


if __name__ == "__main__":
    main()
