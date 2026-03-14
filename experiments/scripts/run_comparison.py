"""
Runner de comparacion experimental (Sprint 4.2).

Ejecuta combinaciones (algoritmo x instancia x seed) definidas
en comparison.yaml y guarda resultados incrementales en CSV
con soporte de checkpoint/reanudacion.

Uso:
    python experiments/scripts/run_comparison.py
    python experiments/scripts/run_comparison.py --dry-run
    python experiments/scripts/run_comparison.py --resume
    python experiments/scripts/run_comparison.py --algorithms ga sa --sizes small

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 4.2
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

sys.path.insert(0, ".")

import numpy as np
import yaml

from experiments.scripts.baseline import solve_baseline
from experiments.scripts.metrics import compute_all_metrics
from src.metaheuristics.de import DifferentialEvolution
from src.metaheuristics.ga import GeneticAlgorithm
from src.metaheuristics.ga_sa import HybridGASA
from src.metaheuristics.sa import SimulatedAnnealing
from src.model.parameters import ProblemInstance
from src.model.solver import SolverStatus, solve_exact

# ============================================================
# Logging
# ============================================================
LOG_FMT = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FMT)
logger = logging.getLogger("run_comparison")


# ============================================================
# Constants
# ============================================================
ALGORITHM_CLASSES = {
    "ga": GeneticAlgorithm,
    "sa": SimulatedAnnealing,
    "de": DifferentialEvolution,
    "ga_sa": HybridGASA,
}

DEFAULT_DETERMINISTIC_ALGORITHMS = {"baseline", "cbc_exact"}

DEFAULT_RUNTIME_ESTIMATE_SECONDS = {
    "baseline": 1.0,
    "cbc_exact": 12.0,
    "sa": 20.0,
    "ga": 90.0,
    "de": 110.0,
    "ga_sa": 75.0,
}

CSV_FIELDNAMES = [
    "algorithm",
    "instance",
    "seed",
    "z_value",
    "gap_percent",
    "service_level",
    "avg_inventory",
    "low_rotation_inventory",
    "elapsed_seconds",
    "n_evaluations",
    "is_feasible",
]

TRACE_FIELDNAMES = [
    "algorithm",
    "instance",
    "seed",
    "iteration",
    "n_evaluations",
    "best_fitness",
    "current_fitness",
    "elapsed_seconds",
    "diversity",
]


@dataclass
class SingleRunPayload:
    row: dict
    traces: list[dict]


def _set_seed(seed: int) -> None:
    """Fijar seed global para reproducibilidad."""
    np.random.seed(seed)
    random.seed(seed)


def _load_config(config_path: str = "experiments/config/comparison.yaml") -> dict:
    """Cargar configuracion del experimento."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_instances(
    config: dict,
    sizes: Optional[list[str]] = None,
) -> dict[str, ProblemInstance]:
    """Cargar instancias filtradas por tamano."""
    instances: dict[str, ProblemInstance] = {}
    for size, paths in config["instances"].items():
        if sizes and size not in sizes:
            continue
        for inst_path in paths:
            path = Path(inst_path)
            name = path.stem
            logger.info("Cargando instancia: %s (%s)", name, size)
            instances[name] = ProblemInstance.from_yaml(path)
    return instances


def _resolve_seeds(exp_cfg: dict) -> list[int]:
    """Resolver seeds aplicando n_replicas."""
    seeds = list(exp_cfg.get("seeds", []))
    if not seeds:
        raise ValueError("experiment.seeds no puede estar vacio")

    n_replicas = int(exp_cfg.get("n_replicas", len(seeds)))
    if n_replicas <= 0:
        raise ValueError("experiment.n_replicas debe ser >= 1")
    if n_replicas > len(seeds):
        raise ValueError(
            f"experiment.n_replicas={n_replicas} excede cantidad de seeds ({len(seeds)})"
        )
    return seeds[:n_replicas]


def _resolve_deterministic_algorithms(exp_cfg: dict) -> set[str]:
    """Algoritmos que se ejecutan una sola vez por instancia."""
    values = exp_cfg.get("deterministic_algorithms")
    if values is None:
        return set(DEFAULT_DETERMINISTIC_ALGORITHMS)
    return set(values)


def _resolve_runtime_estimate(exp_cfg: dict) -> dict[str, float]:
    """Mapa de segundos esperados por algoritmo para estimacion de tiempo."""
    runtime = dict(DEFAULT_RUNTIME_ESTIMATE_SECONDS)
    runtime.update(exp_cfg.get("runtime_estimation_seconds", {}))
    return runtime


def _estimate_total_seconds(runs: list[dict], runtime_map: dict[str, float]) -> float:
    """Estimar duracion total en segundos de los runs pendientes."""
    total = 0.0
    for run in runs:
        algo = run["algorithm"]
        total += float(runtime_map.get(algo, 30.0))
    return total


def _get_completed_runs(results_csv: Path) -> set[tuple[str, str, int]]:
    """Leer runs completados desde CSV."""
    completed: set[tuple[str, str, int]] = set()
    if not results_csv.exists():
        return completed

    with open(results_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["algorithm"], row["instance"], int(row["seed"]))
            completed.add(key)

    logger.info("Encontrados %d runs completados en %s", len(completed), results_csv)
    return completed


def _load_checkpoint(checkpoint_path: Path) -> set[tuple[str, str, int]]:
    """Leer runs completados desde checkpoint JSON."""
    completed: set[tuple[str, str, int]] = set()
    if not checkpoint_path.exists():
        return completed

    with open(checkpoint_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for row in data.get("completed_runs", []):
        try:
            key = (row["algorithm"], row["instance"], int(row["seed"]))
            completed.add(key)
        except KeyError:
            continue

    logger.info(
        "Encontrados %d runs completados en checkpoint %s",
        len(completed),
        checkpoint_path,
    )
    return completed


def _load_cbc_cache_from_results(results_csv: Path) -> dict[str, float]:
    """Cargar referencias CBC por instancia desde resultados previos."""
    z_cbc_cache: dict[str, float] = {}
    if not results_csv.exists():
        return z_cbc_cache

    with open(results_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("algorithm") != "cbc_exact":
                continue
            inst = row["instance"]
            try:
                z = float(row["z_value"])
            except (TypeError, ValueError):
                continue
            if np.isnan(z):
                continue
            if inst not in z_cbc_cache or z > z_cbc_cache[inst]:
                z_cbc_cache[inst] = z

    return z_cbc_cache


def _build_run_list(
    config: dict,
    instances: dict[str, ProblemInstance],
    seeds: list[int],
    deterministic_algorithms: set[str],
    algorithms: Optional[list[str]] = None,
    completed: Optional[set[tuple[str, str, int]]] = None,
) -> list[dict]:
    """Construir lista de runs pendientes."""
    algo_configs = config["algorithms"]
    completed = completed or set()
    runs: list[dict] = []

    algo_keys = list(algo_configs.keys())
    if algorithms:
        algo_keys = [a for a in algo_keys if a in algorithms]

    for algo_key in algo_keys:
        algo_cfg = algo_configs[algo_key]
        algo_seeds = [seeds[0]] if algo_key in deterministic_algorithms else seeds
        for inst_name in instances:
            for seed in algo_seeds:
                if (algo_key, inst_name, seed) in completed:
                    continue
                runs.append(
                    {
                        "algorithm": algo_key,
                        "instance_name": inst_name,
                        "seed": seed,
                        "algo_config": algo_cfg,
                    }
                )

    return runs


def _run_single(
    algo_key: str,
    algo_config: dict,
    instance: ProblemInstance,
    seed: int,
    time_limit: int,
    z_cbc_cache: dict[str, float],
) -> SingleRunPayload:
    """Ejecutar una sola combinacion (algoritmo, instancia, seed)."""
    _set_seed(seed)
    inst_name = instance.name or "unknown"
    traces: list[dict] = []

    t0 = time.time()

    if algo_key == "baseline":
        strategy = algo_config.get("params", {}).get("strategy", "best")
        sol = solve_baseline(instance, strategy=strategy)
        n_evals = 1

    elif algo_key == "cbc_exact":
        params = algo_config.get("params", {})
        tl = params.get("time_limit", time_limit)
        solver_name = params.get("solver", "cbc")

        result = solve_exact(instance, time_limit=tl, solver=solver_name)
        sol = result.solution

        if sol is None:
            elapsed = time.time() - t0
            row = {
                "algorithm": algo_key,
                "instance": inst_name,
                "seed": seed,
                "z_value": float("nan"),
                "gap_percent": float("nan"),
                "service_level": float("nan"),
                "avg_inventory": float("nan"),
                "low_rotation_inventory": float("nan"),
                "elapsed_seconds": elapsed,
                "n_evaluations": 0,
                "is_feasible": False,
            }
            return SingleRunPayload(row=row, traces=traces)

        n_evals = 0
        if result.status == SolverStatus.OPTIMAL:
            z_cbc_cache[inst_name] = float(result.objective_value)

    else:
        cls = ALGORITHM_CLASSES[algo_key]
        params = dict(algo_config.get("params", {}))
        mh = cls(params)
        sol = mh.solve(instance)
        n_evals = mh.n_evaluations

        traces = [
            {
                "algorithm": algo_key,
                "instance": inst_name,
                "seed": seed,
                "iteration": int(log.iteration),
                "n_evaluations": int(log.n_evaluations),
                "best_fitness": float(log.best_fitness),
                "current_fitness": float(log.current_fitness),
                "elapsed_seconds": float(log.elapsed_seconds),
                "diversity": (
                    float(log.diversity) if log.diversity is not None else float("nan")
                ),
            }
            for log in mh.history
        ]

    elapsed = time.time() - t0
    z_ref = z_cbc_cache.get(inst_name, float("nan"))

    metrics = compute_all_metrics(
        solution=sol,
        instance=instance,
        z_reference=z_ref,
        elapsed_seconds=elapsed,
        n_evaluations=n_evals,
    )

    row = {
        "algorithm": algo_key,
        "instance": inst_name,
        "seed": seed,
        **metrics.to_dict(),
    }

    if algo_key == "cbc_exact":
        row["gap_percent"] = 0.0

    return SingleRunPayload(row=row, traces=traces)


def _write_csv_header(csv_path: Path, fieldnames: list[str]) -> None:
    """Escribir encabezado del CSV si no existe."""
    if csv_path.exists():
        return
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()


def _append_csv_row(csv_path: Path, row: dict, fieldnames: list[str]) -> None:
    """Agregar una fila al CSV."""
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(row)


def _append_csv_rows(csv_path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    """Agregar multiples filas al CSV."""
    if not rows:
        return
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(rows)


def _save_checkpoint(checkpoint_path: Path, completed: set, total_planned: int) -> None:
    """Guardar checkpoint con runs completados."""
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "completed_count": len(completed),
        "total_planned": total_planned,
        "timestamp": time.time(),
        "completed_runs": [
            {"algorithm": a, "instance": i, "seed": int(s)}
            for a, i, s in sorted(completed)
        ],
    }
    with open(checkpoint_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _save_results_json(
    output_path: Path,
    experiment_name: str,
    total_planned: int,
    completed_count: int,
    new_success: int,
    errors: list[str],
) -> None:
    """Guardar resumen JSON de ejecucion."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "experiment": experiment_name,
        "generated_at_epoch": time.time(),
        "total_planned": total_planned,
        "completed_count": completed_count,
        "new_successful_runs": new_success,
        "new_errors_count": len(errors),
        "errors": errors,
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def run_comparison(
    config_path: str = "experiments/config/comparison.yaml",
    algorithms: Optional[list[str]] = None,
    sizes: Optional[list[str]] = None,
    resume: bool = False,
    dry_run: bool = False,
) -> None:
    """Ejecutar el experimento comparativo completo."""
    config = _load_config(config_path)
    exp = config["experiment"]
    output_cfg = config["output"]

    results_csv = Path(output_cfg["results_csv"])
    results_json = Path(
        output_cfg.get("results_json", "experiments/results/comparison.json")
    )
    traces_csv = Path(
        output_cfg.get("traces_csv", "experiments/results/comparison_traces.csv")
    )
    save_traces = bool(output_cfg.get("save_traces", True))
    checkpoint_dir = Path(output_cfg["checkpoint_dir"])
    checkpoint_path = checkpoint_dir / "comparison_checkpoint.json"
    time_limit = int(exp["time_limit_seconds"])
    checkpoint_every = int(exp.get("checkpoint_every", 50))

    logger.info("=" * 72)
    logger.info("EXPERIMENTO COMPARATIVO: %s", exp["name"])
    logger.info("=" * 72)

    instances = _load_instances(config, sizes)
    logger.info("Instancias cargadas: %d", len(instances))

    seeds = _resolve_seeds(exp)
    deterministic_algorithms = _resolve_deterministic_algorithms(exp)
    runtime_estimate = _resolve_runtime_estimate(exp)

    logger.info("Replicas activas: %d seeds", len(seeds))
    logger.info("Algoritmos deterministas: %s", sorted(deterministic_algorithms))

    completed: set[tuple[str, str, int]] = set()
    restart_from_scratch = False
    if resume:
        completed_csv = (
            _get_completed_runs(results_csv) if results_csv.exists() else set()
        )
        completed_ckpt = _load_checkpoint(checkpoint_path)

        if completed_ckpt and not results_csv.exists():
            logger.warning(
                "Checkpoint encontrado pero CSV no existe. "
                "Se reiniciaran los runs para no perder metricas historicas."
            )
            completed = set()
            restart_from_scratch = True
        else:
            completed = completed_csv | completed_ckpt
            extra_from_ckpt = len(completed - completed_csv)
            if extra_from_ckpt > 0:
                logger.info("Checkpoint agrego %d runs a reanudar", extra_from_ckpt)

    elif not dry_run and results_csv.exists():
        logger.warning(
            "CSV existente sera sobreescrito: %s (use --resume para reanudar)",
            results_csv,
        )
        results_csv.unlink()

    if not resume and not dry_run and save_traces and traces_csv.exists():
        logger.warning(
            "CSV de trazas existente sera sobreescrito: %s (use --resume para reanudar)",
            traces_csv,
        )
        traces_csv.unlink()
    elif restart_from_scratch and not dry_run and save_traces and traces_csv.exists():
        logger.warning(
            "CSV de trazas sera reiniciado por falta de CSV principal: %s",
            traces_csv,
        )
        traces_csv.unlink()

    runs = _build_run_list(
        config=config,
        instances=instances,
        seeds=seeds,
        deterministic_algorithms=deterministic_algorithms,
        algorithms=algorithms,
        completed=completed,
    )

    total_runs = len(runs)
    total_planned = len(completed) + total_runs
    estimated_seconds = _estimate_total_seconds(runs, runtime_estimate)

    logger.info("Runs pendientes: %d", total_runs)
    logger.info(
        "Tiempo estimado: %.1f horas (modelo por algoritmo)",
        estimated_seconds / 3600.0,
    )

    if dry_run:
        logger.info("DRY RUN - mostrando plan")
        algo_counts: dict[str, int] = {}
        inst_counts: dict[str, int] = {}
        for run in runs:
            algo_counts[run["algorithm"]] = algo_counts.get(run["algorithm"], 0) + 1
            inst_counts[run["instance_name"]] = (
                inst_counts.get(run["instance_name"], 0) + 1
            )

        logger.info("  Por algoritmo:")
        for algo, count in sorted(algo_counts.items()):
            logger.info("    %s: %d runs", algo, count)
        logger.info("  Por instancia:")
        for inst_name, count in sorted(inst_counts.items()):
            logger.info("    %s: %d runs", inst_name, count)
        return

    _write_csv_header(results_csv, CSV_FIELDNAMES)
    if save_traces:
        _write_csv_header(traces_csv, TRACE_FIELDNAMES)

    z_cbc_cache = _load_cbc_cache_from_results(results_csv)

    cbc_runs = [r for r in runs if r["algorithm"] == "cbc_exact"]
    other_runs = [r for r in runs if r["algorithm"] != "cbc_exact"]
    ordered_runs = cbc_runs + other_runs

    try:
        from tqdm import tqdm

        progress = tqdm(total=total_runs, desc="Comparacion", unit="run")
    except ImportError:
        logger.warning("tqdm no disponible, usando progreso por consola")
        progress = None

    errors: list[str] = []
    successful_new_runs = 0
    processed_runs = 0

    for run_spec in ordered_runs:
        algo = run_spec["algorithm"]
        inst_name = run_spec["instance_name"]
        seed = int(run_spec["seed"])

        try:
            payload = _run_single(
                algo_key=algo,
                algo_config=run_spec["algo_config"],
                instance=instances[inst_name],
                seed=seed,
                time_limit=time_limit,
                z_cbc_cache=z_cbc_cache,
            )

            _append_csv_row(results_csv, payload.row, CSV_FIELDNAMES)
            if save_traces:
                _append_csv_rows(traces_csv, payload.traces, TRACE_FIELDNAMES)

            completed.add((algo, inst_name, seed))
            successful_new_runs += 1

            if progress:
                z = payload.row["z_value"]
                z_str = f"{z:,.0f}" if not np.isnan(z) else "NaN"
                progress.set_postfix_str(
                    f"{algo}/{inst_name}/s{seed} Z={z_str} t={payload.row['elapsed_seconds']:.1f}s"
                )
                progress.update(1)
            else:
                logger.info(
                    "[%d/%d] %s | %s | seed=%d | Z=%.0f | t=%.1fs | ok=%s",
                    successful_new_runs,
                    total_runs,
                    algo,
                    inst_name,
                    seed,
                    payload.row["z_value"],
                    payload.row["elapsed_seconds"],
                    payload.row["is_feasible"],
                )

        except Exception as exc:  # pragma: no cover
            msg = f"ERROR {algo}/{inst_name}/seed={seed}: {exc}"
            logger.error(msg)
            errors.append(msg)
            if progress:
                progress.update(1)

        processed_runs += 1
        if processed_runs % checkpoint_every == 0:
            _save_checkpoint(checkpoint_path, completed, total_planned)
            logger.info(
                "Checkpoint guardado (%d/%d procesados)", processed_runs, total_runs
            )

    if progress:
        progress.close()

    _save_checkpoint(checkpoint_path, completed, total_planned)
    _save_results_json(
        output_path=results_json,
        experiment_name=exp["name"],
        total_planned=total_planned,
        completed_count=len(completed),
        new_success=successful_new_runs,
        errors=errors,
    )

    logger.info("=" * 72)
    logger.info("EXPERIMENTO COMPLETADO")
    logger.info("  Runs exitosos nuevos:   %d / %d", successful_new_runs, total_runs)
    logger.info("  Errores nuevos:         %d", len(errors))
    logger.info("  Completados acumulados: %d / %d", len(completed), total_planned)
    logger.info("  Resultados:             %s", results_csv)
    if save_traces:
        logger.info("  Trazas:                 %s", traces_csv)
    logger.info("  Checkpoint:             %s", checkpoint_path)
    logger.info("  Resumen JSON:           %s", results_json)
    if errors:
        logger.warning("Errores encontrados:")
        for err in errors:
            logger.warning("  %s", err)
    logger.info("=" * 72)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Runner de comparacion experimental (Sprint 4.2)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="experiments/config/comparison.yaml",
        help="Ruta al YAML de configuracion",
    )
    parser.add_argument(
        "--algorithms",
        nargs="+",
        type=str,
        default=None,
        help="Algoritmos a ejecutar (ej: ga sa de ga_sa cbc_exact baseline)",
    )
    parser.add_argument(
        "--sizes",
        nargs="+",
        type=str,
        default=None,
        help="Tamanos de instancia (ej: small medium large)",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Reanudar desde checkpoint/CSV existentes",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostrar plan sin ejecutar",
    )
    args = parser.parse_args()

    run_comparison(
        config_path=args.config,
        algorithms=args.algorithms,
        sizes=args.sizes,
        resume=args.resume,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
