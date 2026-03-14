"""
Runner de contraste de perfiles de demanda (stable vs seasonal).

Objetivo:
  - Cuantificar cuanto cambian resultados y veredictos de hipotesis
    cuando se pasa de demanda sintetica estable a demanda estacional.
  - Ejecutar rapido con paralelismo, resume y checkpoint.

Uso:
  python experiments/scripts/run_data_profile_contrast.py
  python experiments/scripts/run_data_profile_contrast.py --dry-run
  python experiments/scripts/run_data_profile_contrast.py --resume --workers 8
  python experiments/scripts/run_data_profile_contrast.py --config experiments/config/data_profile_contrast_smoke.yaml
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import random
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

sys.path.insert(0, ".")

import numpy as np
import pandas as pd
import yaml
from concurrent.futures import ProcessPoolExecutor, as_completed

from experiments.scripts.baseline import solve_baseline
from experiments.scripts.metrics import compute_all_metrics
from experiments.scripts.run_statistical_tests import (
    compute_ranking,
    test_h1,
    test_h2,
    test_h3,
)
from src.instances.generator import InstanceGenerator
from src.metaheuristics.de import DifferentialEvolution
from src.metaheuristics.ga import GeneticAlgorithm
from src.metaheuristics.ga_sa import HybridGASA
from src.metaheuristics.sa import SimulatedAnnealing
from src.model.solver import SolverStatus, solve_exact

# ============================================================
# Logging
# ============================================================

LOG_FMT = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FMT)
logger = logging.getLogger("run_data_profile_contrast")


# ============================================================
# Config
# ============================================================

ALGORITHM_CLASSES = {
    "ga": GeneticAlgorithm,
    "sa": SimulatedAnnealing,
    "de": DifferentialEvolution,
    "ga_sa": HybridGASA,
}

RUNS_FIELDNAMES = [
    "algorithm",
    "instance",
    "seed",
    "size_profile",
    "demand_profile",
    "instance_seed",
    "run_seed",
    "z_value",
    "gap_percent",
    "service_level",
    "avg_inventory",
    "low_rotation_inventory",
    "elapsed_seconds",
    "n_evaluations",
    "is_feasible",
]


def _set_seed(seed: int) -> None:
    np.random.seed(seed)
    random.seed(seed)


def _load_config(config_path: str) -> dict[str, Any]:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _resolve_run_seeds(exp_cfg: dict) -> list[int]:
    seeds = list(exp_cfg.get("run_seeds", []))
    if not seeds:
        raise ValueError("experiment.run_seeds no puede estar vacio")

    n_replicas = int(exp_cfg.get("n_replicas", len(seeds)))
    if n_replicas <= 0:
        raise ValueError("experiment.n_replicas debe ser >= 1")
    if n_replicas > len(seeds):
        raise ValueError(
            f"experiment.n_replicas={n_replicas} excede run_seeds ({len(seeds)})"
        )
    return seeds[:n_replicas]


def _get_completed_keys(results_csv: Path) -> set[tuple[str, str, str, int, int]]:
    completed: set[tuple[str, str, str, int, int]] = set()
    if not results_csv.exists():
        return completed
    with open(results_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                key = (
                    row["algorithm"],
                    row["size_profile"],
                    row["demand_profile"],
                    int(row["instance_seed"]),
                    int(row["run_seed"]),
                )
                completed.add(key)
            except Exception:
                continue
    return completed


def _write_csv_header(path: Path, fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()


def _append_csv_row(path: Path, row: dict, fieldnames: list[str]) -> None:
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(row)


def _save_checkpoint(
    path: Path,
    completed: set[tuple[str, str, str, int, int]],
    total_planned: int,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": time.time(),
        "completed_count": len(completed),
        "total_planned": int(total_planned),
        "completed_runs": [
            {
                "algorithm": k[0],
                "size_profile": k[1],
                "demand_profile": k[2],
                "instance_seed": int(k[3]),
                "run_seed": int(k[4]),
            }
            for k in sorted(completed)
        ],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def _instance_name(size_profile: str, demand_profile: str, instance_seed: int) -> str:
    return f"{size_profile}_{demand_profile}_seed{instance_seed}"


def _build_run_list(
    config: dict,
    run_seeds: list[int],
    completed: set[tuple[str, str, str, int, int]],
) -> list[dict]:
    exp_cfg = config["experiment"]
    deterministic = set(exp_cfg.get("deterministic_algorithms", []))
    size_profiles = list(exp_cfg["size_profiles"])
    demand_profiles = list(exp_cfg["demand_profiles"])
    instance_seeds = list(exp_cfg["instance_seeds"])
    distribution = str(config.get("generation", {}).get("distribution", "lognormal"))

    runs: list[dict] = []
    for algo_key, algo_cfg in config["algorithms"].items():
        algo_run_seeds = [run_seeds[0]] if algo_key in deterministic else run_seeds
        for size_profile in size_profiles:
            for demand_profile in demand_profiles:
                for instance_seed in instance_seeds:
                    for run_seed in algo_run_seeds:
                        key = (
                            algo_key,
                            size_profile,
                            demand_profile,
                            int(instance_seed),
                            int(run_seed),
                        )
                        if key in completed:
                            continue
                        runs.append(
                            {
                                "algorithm": algo_key,
                                "algo_config": algo_cfg,
                                "size_profile": size_profile,
                                "demand_profile": demand_profile,
                                "instance_seed": int(instance_seed),
                                "run_seed": int(run_seed),
                                "distribution": distribution,
                            }
                        )
    return runs


def _dedupe_runs(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Deduplicar runs por clave experimental.

    Puede haber duplicados cuando una ejecucion se interrumpe despues de escribir
    CSV pero antes de actualizar checkpoint. Para analisis estadistico usamos
    una sola fila por combinacion unica.
    """
    key_cols = [
        "algorithm",
        "size_profile",
        "demand_profile",
        "instance_seed",
        "run_seed",
    ]
    before = len(df)
    dedup = df.drop_duplicates(subset=key_cols, keep="last").copy()
    dedup = dedup.sort_values(key_cols).reset_index(drop=True)
    removed = before - len(dedup)
    return dedup, int(removed)


def _execute_single(task: dict) -> dict:
    algo_key = task["algorithm"]
    algo_cfg = task["algo_config"]
    size_profile = task["size_profile"]
    demand_profile = task["demand_profile"]
    instance_seed = int(task["instance_seed"])
    run_seed = int(task["run_seed"])
    distribution = task["distribution"]

    _set_seed(run_seed)

    gen = InstanceGenerator()
    instance = gen.generate(
        size_profile=size_profile,
        demand_profile=demand_profile,
        seed=instance_seed,
        distribution=distribution,
    )
    instance.name = _instance_name(size_profile, demand_profile, instance_seed)

    t0 = time.time()
    n_evals = 0
    z_ref = float("nan")

    if algo_key == "baseline":
        strategy = algo_cfg.get("params", {}).get("strategy", "best")
        solution = solve_baseline(instance, strategy=strategy)
        n_evals = 1
    elif algo_key == "cbc_exact":
        params = dict(algo_cfg.get("params", {}))
        result = solve_exact(
            instance=instance,
            time_limit=int(params.get("time_limit", 300)),
            solver=str(params.get("solver", "cbc")),
        )
        solution = result.solution
        if solution is None:
            elapsed = time.time() - t0
            return {
                "algorithm": algo_key,
                "instance": instance.name,
                "seed": run_seed,
                "size_profile": size_profile,
                "demand_profile": demand_profile,
                "instance_seed": instance_seed,
                "run_seed": run_seed,
                "z_value": float("nan"),
                "gap_percent": float("nan"),
                "service_level": float("nan"),
                "avg_inventory": float("nan"),
                "low_rotation_inventory": float("nan"),
                "elapsed_seconds": elapsed,
                "n_evaluations": 0,
                "is_feasible": False,
            }
        if result.status == SolverStatus.OPTIMAL:
            z_ref = float(result.objective_value)
    else:
        mh_class = ALGORITHM_CLASSES[algo_key]
        mh = mh_class(dict(algo_cfg.get("params", {})))
        solution = mh.solve(instance)
        n_evals = int(mh.n_evaluations)

    elapsed = time.time() - t0
    metrics = compute_all_metrics(
        solution=solution,
        instance=instance,
        z_reference=z_ref,
        elapsed_seconds=elapsed,
        n_evaluations=n_evals,
    )
    row = {
        "algorithm": algo_key,
        "instance": instance.name,
        "seed": run_seed,
        "size_profile": size_profile,
        "demand_profile": demand_profile,
        "instance_seed": instance_seed,
        "run_seed": run_seed,
        **metrics.to_dict(),
    }
    if algo_key == "cbc_exact":
        row["gap_percent"] = 0.0
    return row


def _build_summary_tables(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    base = df.copy()

    summary = (
        base.groupby(["demand_profile", "algorithm"], as_index=False)
        .agg(
            n_runs=("z_value", "count"),
            feasible_rate_pct=("is_feasible", lambda x: 100.0 * float(np.mean(x))),
            mean_z=("z_value", "mean"),
            std_z=("z_value", "std"),
            mean_service=("service_level", "mean"),
            mean_low_rotation_inv=("low_rotation_inventory", "mean"),
            mean_elapsed_seconds=("elapsed_seconds", "mean"),
        )
        .sort_values(["demand_profile", "algorithm"])
        .reset_index(drop=True)
    )

    keys = ["algorithm", "size_profile", "instance_seed", "run_seed"]
    stable = base[base["demand_profile"] == "stable"][keys + [
        "z_value",
        "service_level",
        "low_rotation_inventory",
        "elapsed_seconds",
    ]].rename(
        columns={
            "z_value": "z_stable",
            "service_level": "service_stable",
            "low_rotation_inventory": "low_rotation_stable",
            "elapsed_seconds": "elapsed_stable",
        }
    )
    seasonal = base[base["demand_profile"] == "seasonal"][keys + [
        "z_value",
        "service_level",
        "low_rotation_inventory",
        "elapsed_seconds",
    ]].rename(
        columns={
            "z_value": "z_seasonal",
            "service_level": "service_seasonal",
            "low_rotation_inventory": "low_rotation_seasonal",
            "elapsed_seconds": "elapsed_seasonal",
        }
    )
    paired = stable.merge(seasonal, on=keys, how="inner")
    if not paired.empty:
        paired["delta_z_pct"] = (
            (paired["z_seasonal"] - paired["z_stable"])
            / np.maximum(np.abs(paired["z_stable"]), 1e-9)
            * 100.0
        )
        paired["delta_service_pp"] = paired["service_seasonal"] - paired["service_stable"]
        paired["delta_low_rotation_pct"] = (
            (paired["low_rotation_seasonal"] - paired["low_rotation_stable"])
            / np.maximum(np.abs(paired["low_rotation_stable"]), 1e-9)
            * 100.0
        )
        paired["delta_elapsed_pct"] = (
            (paired["elapsed_seasonal"] - paired["elapsed_stable"])
            / np.maximum(np.abs(paired["elapsed_stable"]), 1e-9)
            * 100.0
        )

    paired_summary = pd.DataFrame()
    if not paired.empty:
        paired_summary = (
            paired.groupby(["algorithm", "size_profile"], as_index=False)
            .agg(
                n_pairs=("delta_z_pct", "count"),
                mean_delta_z_pct=("delta_z_pct", "mean"),
                p05_delta_z_pct=("delta_z_pct", lambda x: float(np.quantile(x, 0.05))),
                p95_delta_z_pct=("delta_z_pct", lambda x: float(np.quantile(x, 0.95))),
                mean_delta_service_pp=("delta_service_pp", "mean"),
                mean_delta_low_rotation_pct=("delta_low_rotation_pct", "mean"),
                mean_delta_elapsed_pct=("delta_elapsed_pct", "mean"),
            )
            .sort_values(["algorithm", "size_profile"])
            .reset_index(drop=True)
        )

    return summary, paired, paired_summary


def _evaluate_hypotheses_by_profile(df: pd.DataFrame) -> dict:
    out: dict[str, Any] = {}
    profiles = sorted(df["demand_profile"].unique())
    for profile in profiles:
        sub = df[df["demand_profile"] == profile].copy()
        h1 = test_h1(sub)
        h2 = test_h2(sub)
        h3 = test_h3(sub)
        ranking = compute_ranking(sub)
        out[profile] = {
            "n_rows": int(len(sub)),
            "algorithms": sorted(sub["algorithm"].unique().tolist()),
            "hypothesis_tests": [asdict(x) for x in (h1 + h2 + h3)],
            "ranking": {
                "algorithms": ranking.ranking,
                "anova_f": ranking.anova_f,
                "anova_p": ranking.anova_p,
                "tukey": ranking.tukey_results,
            },
            "summary": {
                "H1_supported_count": int(sum(1 for x in h1 if x.verdict == "SUPPORTED")),
                "H2_supported_count": int(sum(1 for x in h2 if x.verdict == "SUPPORTED")),
                "H3_supported_count": int(sum(1 for x in h3 if x.verdict == "SUPPORTED")),
            },
        }
    return out


def _write_report_md(
    report_path: Path,
    config: dict,
    df: pd.DataFrame,
    summary: pd.DataFrame,
    paired_summary: pd.DataFrame,
    hypotheses: dict,
) -> None:
    exp_cfg = config["experiment"]
    lines = [
        "# Contraste Stable vs Seasonal",
        "",
        "## Configuracion",
        "",
        f"- Nombre: `{exp_cfg.get('name', 'data_profile_contrast')}`",
        f"- Size profiles: `{exp_cfg.get('size_profiles', [])}`",
        f"- Demand profiles: `{exp_cfg.get('demand_profiles', [])}`",
        f"- Instance seeds: `{exp_cfg.get('instance_seeds', [])}`",
        f"- Run seeds (n_replicas): `{exp_cfg.get('n_replicas', 0)}`",
        "",
        "## Totales",
        "",
        f"- Filas en runs CSV: **{len(df)}**",
        f"- Algoritmos: **{df['algorithm'].nunique()}**",
        "",
        "## Resumen por perfil y algoritmo",
        "",
    ]

    if summary.empty:
        lines.append("_Sin datos de resumen._")
    else:
        for row in summary.itertuples(index=False):
            lines.append(
                f"- `{row.demand_profile}` / `{row.algorithm}`: "
                f"n={int(row.n_runs)}, Z_mean={row.mean_z:,.0f}, "
                f"service_mean={row.mean_service:.2f}%, "
                f"feasible={row.feasible_rate_pct:.1f}%"
            )

    lines.extend(["", "## Delta seasonal vs stable", ""])
    if paired_summary.empty:
        lines.append("_No hay pares matching stable-seasonal para comparar._")
    else:
        for row in paired_summary.itertuples(index=False):
            lines.append(
                f"- `{row.algorithm}` / `{row.size_profile}`: "
                f"delta Z mean={row.mean_delta_z_pct:.2f}%, "
                f"delta service={row.mean_delta_service_pp:.2f} pp, "
                f"delta low-rotation={row.mean_delta_low_rotation_pct:.2f}%"
            )

    lines.extend(["", "## Hipotesis por perfil", ""])
    for profile, payload in hypotheses.items():
        s = payload.get("summary", {})
        lines.append(
            f"- `{profile}`: H1 soportadas={s.get('H1_supported_count', 0)}, "
            f"H2 soportadas={s.get('H2_supported_count', 0)}, "
            f"H3 soportadas={s.get('H3_supported_count', 0)}"
        )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def run_contrast(
    config_path: str = "experiments/config/data_profile_contrast.yaml",
    dry_run: bool = False,
    resume: bool = False,
    workers: int = -1,
) -> None:
    config = _load_config(config_path)
    exp_cfg = config["experiment"]
    out_cfg = config["output"]

    run_seeds = _resolve_run_seeds(exp_cfg)
    if workers < 0:
        workers = max(1, (os.cpu_count() or 2) - 1)
    use_parallel = workers > 0

    runs_csv = Path(out_cfg["runs_csv"])
    summary_csv = Path(out_cfg["summary_csv"])
    paired_csv = Path(out_cfg["paired_csv"])
    paired_summary_csv = Path(out_cfg["paired_summary_csv"])
    hypotheses_json = Path(out_cfg["hypotheses_json"])
    report_md = Path(out_cfg["report_md"])
    checkpoint_json = Path(out_cfg["checkpoint_json"])
    checkpoint_every = int(exp_cfg.get("checkpoint_every", 20))

    completed = _get_completed_keys(runs_csv) if (resume and runs_csv.exists()) else set()
    if not resume or not runs_csv.exists():
        _write_csv_header(runs_csv, RUNS_FIELDNAMES)

    tasks = _build_run_list(config=config, run_seeds=run_seeds, completed=completed)
    total_planned = len(tasks) + len(completed)

    logger.info("=" * 72)
    logger.info("CONTRASTE DE PERFILES DE DEMANDA")
    logger.info("  Config: %s", config_path)
    logger.info("  Workers: %d (%s)", workers if use_parallel else 0, "parallel" if use_parallel else "sequential")
    logger.info("  Total planificado: %d", total_planned)
    logger.info("  Ya completados: %d", len(completed))
    logger.info("  Pendientes: %d", len(tasks))
    logger.info("=" * 72)

    if dry_run:
        by_algo: dict[str, int] = {}
        for t in tasks:
            by_algo[t["algorithm"]] = by_algo.get(t["algorithm"], 0) + 1
        logger.info("DRY RUN:")
        for algo, n in sorted(by_algo.items()):
            logger.info("  %s: %d runs pendientes", algo, n)
        return

    errors: list[str] = []
    done_new = 0
    t0 = time.time()

    if not tasks:
        logger.info("No hay runs pendientes. Saltando ejecucion.")
    elif use_parallel:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            future_to_task = {pool.submit(_execute_single, t): t for t in tasks}
            for i, future in enumerate(as_completed(future_to_task), start=1):
                task = future_to_task[future]
                key = (
                    task["algorithm"],
                    task["size_profile"],
                    task["demand_profile"],
                    int(task["instance_seed"]),
                    int(task["run_seed"]),
                )
                label = (
                    f"{task['algorithm']}|{task['size_profile']}|"
                    f"{task['demand_profile']}|i{task['instance_seed']}|r{task['run_seed']}"
                )
                try:
                    row = future.result()
                    _append_csv_row(runs_csv, row, RUNS_FIELDNAMES)
                    completed.add(key)
                    done_new += 1
                    if i % 10 == 0 or i == len(tasks):
                        logger.info("[%d/%d] OK %s Z=%.0f t=%.1fs", i, len(tasks), label, row["z_value"], row["elapsed_seconds"])
                    if checkpoint_every > 0 and done_new % checkpoint_every == 0:
                        _save_checkpoint(checkpoint_json, completed, total_planned)
                except Exception as exc:
                    errors.append(f"{label}: {exc}")
                    logger.error("ERROR %s: %s", label, exc)
    else:
        for i, task in enumerate(tasks, start=1):
            key = (
                task["algorithm"],
                task["size_profile"],
                task["demand_profile"],
                int(task["instance_seed"]),
                int(task["run_seed"]),
            )
            label = (
                f"{task['algorithm']}|{task['size_profile']}|"
                f"{task['demand_profile']}|i{task['instance_seed']}|r{task['run_seed']}"
            )
            try:
                row = _execute_single(task)
                _append_csv_row(runs_csv, row, RUNS_FIELDNAMES)
                completed.add(key)
                done_new += 1
                logger.info("[%d/%d] OK %s Z=%.0f t=%.1fs", i, len(tasks), label, row["z_value"], row["elapsed_seconds"])
                if checkpoint_every > 0 and done_new % checkpoint_every == 0:
                    _save_checkpoint(checkpoint_json, completed, total_planned)
            except Exception as exc:
                errors.append(f"{label}: {exc}")
                logger.error("ERROR %s: %s", label, exc)

    elapsed = time.time() - t0
    _save_checkpoint(checkpoint_json, completed, total_planned)

    # Post-procesado
    df = pd.read_csv(runs_csv)
    df, removed_dups = _dedupe_runs(df)
    if removed_dups > 0:
        logger.warning("Se removieron %d filas duplicadas en runs CSV", removed_dups)
        df.to_csv(runs_csv, index=False, encoding="utf-8")

    summary, paired, paired_summary = _build_summary_tables(df)
    hypotheses = _evaluate_hypotheses_by_profile(df)

    summary.to_csv(summary_csv, index=False, encoding="utf-8")
    paired.to_csv(paired_csv, index=False, encoding="utf-8")
    paired_summary.to_csv(paired_summary_csv, index=False, encoding="utf-8")

    hypotheses_payload = {
        "experiment": exp_cfg.get("name", "data_profile_contrast"),
        "generated_at_epoch": time.time(),
        "config_path": config_path,
        "runs_csv": str(runs_csv),
        "summary_csv": str(summary_csv),
        "paired_csv": str(paired_csv),
        "paired_summary_csv": str(paired_summary_csv),
        "total_completed": int(len(df)),
        "new_runs": int(done_new),
        "errors": errors,
        "duplicates_removed": int(removed_dups),
        "elapsed_seconds": float(elapsed),
        "profiles": hypotheses,
    }
    hypotheses_json.parent.mkdir(parents=True, exist_ok=True)
    with open(hypotheses_json, "w", encoding="utf-8") as f:
        json.dump(hypotheses_payload, f, indent=2, ensure_ascii=False)

    _write_report_md(
        report_path=report_md,
        config=config,
        df=df,
        summary=summary,
        paired_summary=paired_summary,
        hypotheses=hypotheses,
    )

    logger.info("=" * 72)
    logger.info("CONTRASTE COMPLETADO")
    logger.info("  Runs CSV: %s", runs_csv)
    logger.info("  Summary CSV: %s", summary_csv)
    logger.info("  Paired summary CSV: %s", paired_summary_csv)
    logger.info("  Hypotheses JSON: %s", hypotheses_json)
    logger.info("  Report MD: %s", report_md)
    logger.info("  New runs: %d | Errors: %d | Elapsed: %.1fs", done_new, len(errors), elapsed)
    logger.info("=" * 72)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Contraste stable vs seasonal con paralelismo y evaluacion de hipotesis"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="experiments/config/data_profile_contrast.yaml",
        help="Ruta al archivo YAML de configuracion",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostrar plan y salir sin ejecutar",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Reanudar desde runs_csv existente",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=-1,
        help="Numero de workers (-1=auto, 0=secuencial, N=paralelo)",
    )
    args = parser.parse_args()

    run_contrast(
        config_path=args.config,
        dry_run=args.dry_run,
        resume=args.resume,
        workers=args.workers,
    )


if __name__ == "__main__":
    main()
