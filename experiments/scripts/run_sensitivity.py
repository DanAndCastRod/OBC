"""
Runner de analisis de sensibilidad (Sprint 4.2).

Perturba un parametro a la vez sobre una instancia base y ejecuta
GA-SA con replicas para analizar impacto en la funcion objetivo.

Uso:
    python experiments/scripts/run_sensitivity.py
    python experiments/scripts/run_sensitivity.py --dry-run
    python experiments/scripts/run_sensitivity.py --resume --workers 7
    python experiments/scripts/run_sensitivity.py --resume  # default: cpu_count - 1

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 4.2
"""

from __future__ import annotations

import argparse
import copy
import csv
import json
import logging
import os
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

sys.path.insert(0, ".")

import numpy as np
import yaml

from experiments.scripts.metrics import compute_all_metrics
from src.metaheuristics.ga_sa import HybridGASA
from src.model.parameters import ProblemInstance

# ============================================================
# Logging
# ============================================================
LOG_FMT = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FMT)
logger = logging.getLogger("run_sensitivity")

# Lock global para escritura thread-safe al CSV
_csv_lock = Lock()


def _set_seed(seed: int) -> None:
    """Fijar seed global."""
    np.random.seed(seed)
    random.seed(seed)


def _load_config(config_path: str = "experiments/config/sensitivity.yaml") -> dict:
    """Cargar configuracion de sensibilidad."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _perturb_prices(instance: ProblemInstance, delta: float) -> ProblemInstance:
    """Perturbar precios de venta multiplicativamente."""
    inst = copy.deepcopy(instance)
    inst.prices = inst.prices * (1.0 + delta)
    inst.cost_pen = inst.cost_pen * (1.0 + delta)
    inst.name = f"{instance.name}_prices_{delta:+.0%}"
    return inst


def _perturb_costs(instance: ProblemInstance, delta: float) -> ProblemInstance:
    """Perturbar costos de produccion, setup e inventario."""
    inst = copy.deepcopy(instance)
    inst.cost_prod = inst.cost_prod * (1.0 + delta)
    inst.cost_setup = inst.cost_setup * (1.0 + delta)
    inst.cost_inv = inst.cost_inv * (1.0 + delta)
    inst.name = f"{instance.name}_costs_{delta:+.0%}"
    return inst


def _perturb_demand_variability(
    instance: ProblemInstance,
    delta: float,
) -> ProblemInstance:
    """Perturbar variabilidad de demanda en modo spread."""
    inst = copy.deepcopy(instance)
    d_mean = np.mean(inst.demand, axis=2, keepdims=True)
    deviation = inst.demand - d_mean
    inst.demand = d_mean + deviation * (1.0 + delta)
    inst.demand = np.maximum(inst.demand, 0.0)
    inst.name = f"{instance.name}_demvar_{delta:+.0%}"
    return inst


PERTURBATION_FUNCS = {
    "prices": _perturb_prices,
    "costs": _perturb_costs,
    "demand_variability": _perturb_demand_variability,
}


CSV_FIELDNAMES = [
    "parameter",
    "delta",
    "seed",
    "z_value",
    "gap_percent",
    "service_level",
    "avg_inventory",
    "low_rotation_inventory",
    "elapsed_seconds",
    "n_evaluations",
    "is_feasible",
    "instance_name",
]


def _append_row(results_csv: Path, row: dict) -> None:
    """Escritura thread-safe de una fila al CSV."""
    with _csv_lock:
        with open(results_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
            writer.writerow(row)


def _load_completed_keys(results_csv: Path) -> set[tuple[str, str, str]]:
    """Leer CSV existente y devolver set de (parameter, delta, seed) completados."""
    completed = set()
    if not results_csv.exists():
        return completed
    try:
        with open(results_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row["parameter"], row["delta"], row["seed"])
                completed.add(key)
    except Exception as exc:
        logger.warning("Error leyendo CSV para resume: %s", exc)
    return completed


def _to_float(value: str) -> float | None:
    """Convertir a float de forma segura."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_bool(value: str) -> bool:
    """Convertir texto a bool."""
    return str(value).strip().lower() in {"1", "true", "yes", "si"}


def _write_results_json(
    results_csv: Path,
    results_json: Path,
    experiment_name: str,
    total_runs_planned: int,
    resume: bool,
    workers: int,
) -> None:
    """Generar resumen JSON a partir del CSV de sensibilidad."""
    if not results_csv.exists():
        logger.warning("No se puede generar JSON: no existe %s", results_csv)
        return

    rows: list[dict] = []
    with open(results_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    grouped: dict[tuple[str, str], dict] = {}
    for row in rows:
        key = (row.get("parameter", ""), row.get("delta", ""))
        bucket = grouped.setdefault(
            key,
            {
                "parameter": key[0],
                "delta": _to_float(key[1]),
                "count": 0,
                "feasible_count": 0,
                "z_sum": 0.0,
                "gap_sum": 0.0,
                "time_sum": 0.0,
                "eval_sum": 0.0,
            },
        )

        bucket["count"] += 1
        bucket["feasible_count"] += int(_to_bool(row.get("is_feasible", "false")))
        bucket["z_sum"] += _to_float(row.get("z_value", "")) or 0.0
        bucket["gap_sum"] += _to_float(row.get("gap_percent", "")) or 0.0
        bucket["time_sum"] += _to_float(row.get("elapsed_seconds", "")) or 0.0
        bucket["eval_sum"] += _to_float(row.get("n_evaluations", "")) or 0.0

    summary = []
    for key in sorted(grouped.keys()):
        item = grouped[key]
        n = max(item["count"], 1)
        summary.append(
            {
                "parameter": item["parameter"],
                "delta": item["delta"],
                "count": item["count"],
                "feasible_rate_percent": 100.0 * item["feasible_count"] / n,
                "mean_z_value": item["z_sum"] / n,
                "mean_gap_percent": item["gap_sum"] / n,
                "mean_elapsed_seconds": item["time_sum"] / n,
                "mean_n_evaluations": item["eval_sum"] / n,
            }
        )

    payload = {
        "experiment": experiment_name,
        "generated_at_epoch": time.time(),
        "source_csv": str(results_csv),
        "total_planned": int(total_runs_planned),
        "completed_count": len(rows),
        "resume": bool(resume),
        "workers": int(workers),
        "parameter_delta_summary": summary,
    }

    results_json.parent.mkdir(parents=True, exist_ok=True)
    with open(results_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    logger.info("  Resumen JSON: %s", results_json)


def _run_single_task(task: dict) -> dict:
    """
    Worker function para ejecucion paralela.

    Recibe un dict con toda la info necesaria para ejecutar un run
    de forma independiente (sin compartir estado).
    """
    parameter = task["parameter"]
    delta = task["delta"]
    seed = task["seed"]
    base_instance_path = task["base_instance_path"]
    algo_params = task["algo_params"]
    z_reference = task["z_reference"]
    perturb_name = task["perturb_name"]

    # Cada worker carga su propia instancia (evita problemas de serialización)
    _set_seed(seed)
    base_instance = ProblemInstance.from_yaml(base_instance_path)
    perturb_func = PERTURBATION_FUNCS[perturb_name]
    instance = perturb_func(base_instance, delta)

    mh = HybridGASA(dict(algo_params))
    t0 = time.time()
    sol = mh.solve(instance)
    elapsed = time.time() - t0

    metrics = compute_all_metrics(
        solution=sol,
        instance=instance,
        z_reference=z_reference,
        elapsed_seconds=elapsed,
        n_evaluations=mh.n_evaluations,
    )

    return {
        "parameter": parameter,
        "delta": delta,
        "seed": seed,
        "instance_name": instance.name,
        **metrics.to_dict(),
    }


def _run_single_sequential(
    parameter: str,
    delta: float,
    seed: int,
    instance: ProblemInstance,
    algo_params: dict,
    z_reference: float,
) -> dict:
    """Ejecutar una corrida de sensibilidad (modo secuencial, original)."""
    _set_seed(seed)
    mh = HybridGASA(dict(algo_params))
    t0 = time.time()
    sol = mh.solve(instance)
    elapsed = time.time() - t0

    metrics = compute_all_metrics(
        solution=sol,
        instance=instance,
        z_reference=z_reference,
        elapsed_seconds=elapsed,
        n_evaluations=mh.n_evaluations,
    )

    return {
        "parameter": parameter,
        "delta": delta,
        "seed": seed,
        "instance_name": instance.name,
        **metrics.to_dict(),
    }


def run_sensitivity(
    config_path: str = "experiments/config/sensitivity.yaml",
    dry_run: bool = False,
    resume: bool = False,
    workers: int = -1,
) -> None:
    """Ejecutar analisis de sensibilidad completo."""
    config = _load_config(config_path)

    base_path = config["base_instance"]
    base_instance = ProblemInstance.from_yaml(base_path)
    logger.info("Instancia base: %s", base_instance.name)

    algo_params = config.get("algorithm_params", {})
    seeds = list(config["experiment"]["seeds"])
    n_replicas = int(config["experiment"]["n_replicas"])
    if n_replicas <= 0:
        raise ValueError("n_replicas debe ser >= 1")
    if n_replicas > len(seeds):
        raise ValueError(
            f"n_replicas={n_replicas} excede numero de seeds ({len(seeds)})"
        )
    selected_seeds = seeds[:n_replicas]

    parameters = config["parameters"]

    # Determinar workers
    if workers < 0:
        workers = max(1, (os.cpu_count() or 2) - 1)
    use_parallel = workers > 0
    if use_parallel:
        logger.info("Modo PARALELO con %d workers", workers)
    else:
        logger.info("Modo SECUENCIAL (workers=0)")

    # ============================================================
    # Calcular total de runs
    # ============================================================
    total_runs = 0
    for param_cfg in parameters.values():
        deltas = list(param_cfg["deltas"])
        control_runs = 0 if 0.0 in deltas else n_replicas
        total_runs += len(deltas) * n_replicas + control_runs

    # ============================================================
    # Resume: cargar runs completados
    # ============================================================
    results_csv = Path(config["output"]["results_csv"])
    completed_keys: set[tuple[str, str, str]] = set()

    if resume and results_csv.exists():
        completed_keys = _load_completed_keys(results_csv)
        logger.info(
            "RESUME: %d runs ya completados en %s", len(completed_keys), results_csv
        )
    else:
        # Crear CSV fresco
        results_csv.parent.mkdir(parents=True, exist_ok=True)
        with open(results_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()

    def _is_completed(parameter: str, delta: float, seed: int) -> bool:
        """Verificar si un run ya está completado."""
        key = (parameter, str(delta), str(seed))
        return key in completed_keys

    logger.info("=" * 72)
    logger.info("ANALISIS DE SENSIBILIDAD")
    logger.info("  Parametros: %s", ", ".join(parameters.keys()))
    logger.info("  Replicas por perturbacion: %d", n_replicas)
    logger.info("  Total runs (plan): %d", total_runs)
    logger.info("  Ya completados: %d", len(completed_keys))
    logger.info("  Workers: %d", workers if use_parallel else 0)
    logger.info("=" * 72)

    if dry_run:
        logger.info("DRY RUN - plan:")
        for param_name, param_cfg in parameters.items():
            deltas = list(param_cfg["deltas"])
            control_runs = 0 if 0.0 in deltas else n_replicas
            total_param = len(deltas) * n_replicas + control_runs
            skipped = sum(
                1
                for d in deltas
                for s in selected_seeds
                if _is_completed(param_name, d, s)
            )
            logger.info(
                "  %s: %d total, %d skipped (resume), %d pending",
                param_name,
                total_param,
                skipped,
                total_param - skipped,
            )
        return

    # ============================================================
    # FASE 1: Control runs (delta=0) — siempre secuencial
    # ============================================================
    # Los control runs se ejecutan primero porque necesitamos z_reference
    # para calcular gap_percent de las perturbaciones.
    # ============================================================
    control_by_param_seed: dict[str, dict[int, float]] = {}

    logger.info("--- FASE 1: Control runs (delta=0) ---")
    for param_name, param_cfg in parameters.items():
        deltas = list(param_cfg["deltas"])
        perturb_func = PERTURBATION_FUNCS[param_name]
        control_by_param_seed[param_name] = {}

        control_instance = perturb_func(base_instance, 0.0)
        for seed in selected_seeds:
            # Si ya fue completado en resume, leer z_value del CSV
            if _is_completed(param_name, 0.0, seed):
                # Buscar z_value en completed data
                z_val = _get_z_from_csv(results_csv, param_name, 0.0, seed)
                if z_val is not None:
                    control_by_param_seed[param_name][seed] = z_val
                    logger.info(
                        "  [SKIP] %s delta=0 seed=%d (Z=%.0f from resume)",
                        param_name,
                        seed,
                        z_val,
                    )
                    continue

            try:
                row = _run_single_sequential(
                    parameter=param_name,
                    delta=0.0,
                    seed=seed,
                    instance=control_instance,
                    algo_params=algo_params,
                    z_reference=float("nan"),
                )
                control_by_param_seed[param_name][seed] = float(row["z_value"])
                row["gap_percent"] = 0.0

                if 0.0 in deltas:
                    _append_row(results_csv, row)

                logger.info(
                    "  %s delta=0 seed=%d Z=%.0f t=%.1fs",
                    param_name,
                    seed,
                    row["z_value"],
                    row["elapsed_seconds"],
                )
            except Exception as exc:
                logger.error("ERROR %s/delta=0.0/seed=%d: %s", param_name, seed, exc)

    # ============================================================
    # FASE 2: Perturbation runs — paralelo si workers > 0
    # ============================================================
    logger.info("--- FASE 2: Perturbation runs (paralelo=%s) ---", use_parallel)

    # Construir lista de tareas pendientes
    pending_tasks: list[dict] = []
    for param_name, param_cfg in parameters.items():
        deltas = list(param_cfg["deltas"])
        for delta in deltas:
            if abs(delta) < 1e-12:
                continue  # delta=0 ya procesado en Fase 1
            for seed in selected_seeds:
                if _is_completed(param_name, delta, seed):
                    continue  # Ya completado en resume

                z_ref = control_by_param_seed.get(param_name, {}).get(
                    seed, float("nan")
                )
                pending_tasks.append(
                    {
                        "parameter": param_name,
                        "delta": float(delta),
                        "seed": seed,
                        "base_instance_path": base_path,
                        "algo_params": algo_params,
                        "z_reference": z_ref,
                        "perturb_name": param_name,
                    }
                )

    logger.info("  Tareas pendientes: %d", len(pending_tasks))

    if not pending_tasks:
        logger.info("  No hay tareas pendientes. Todo completado.")
    elif not use_parallel:
        # --- Modo secuencial ---
        try:
            from tqdm import tqdm

            progress = tqdm(total=len(pending_tasks), desc="Sensibilidad", unit="run")
        except ImportError:
            progress = None

        for i, task in enumerate(pending_tasks):
            try:
                row = _run_single_task(task)
                _append_row(results_csv, row)

                label = f"{task['parameter']} d={task['delta']:+.0%} s{task['seed']}"
                if progress:
                    progress.set_postfix_str(f"{label} Z={row['z_value']:,.0f}")
                    progress.update(1)
                else:
                    logger.info(
                        "[%d/%d] %s Z=%.0f t=%.1fs",
                        i + 1,
                        len(pending_tasks),
                        label,
                        row["z_value"],
                        row["elapsed_seconds"],
                    )
            except Exception as exc:
                logger.error("ERROR %s: %s", label, exc)
                if progress:
                    progress.update(1)

        if progress:
            progress.close()
    else:
        # --- Modo paralelo ---
        completed_count = 0
        error_count = 0

        try:
            from tqdm import tqdm

            progress = tqdm(
                total=len(pending_tasks), desc="Sensibilidad (parallel)", unit="run"
            )
        except ImportError:
            progress = None

        with ProcessPoolExecutor(max_workers=workers) as pool:
            future_to_task = {
                pool.submit(_run_single_task, task): task for task in pending_tasks
            }

            for future in as_completed(future_to_task):
                task = future_to_task[future]
                label = f"{task['parameter']} d={task['delta']:+.0%} s{task['seed']}"
                try:
                    row = future.result()
                    _append_row(results_csv, row)
                    completed_count += 1

                    if progress:
                        progress.set_postfix_str(f"{label} Z={row['z_value']:,.0f}")
                        progress.update(1)
                    else:
                        logger.info(
                            "[%d/%d] %s Z=%.0f t=%.1fs",
                            completed_count,
                            len(pending_tasks),
                            label,
                            row["z_value"],
                            row["elapsed_seconds"],
                        )
                except Exception as exc:
                    error_count += 1
                    logger.error("ERROR %s: %s", label, exc)
                    if progress:
                        progress.update(1)

        if progress:
            progress.close()

        logger.info("  Completados: %d, Errores: %d", completed_count, error_count)

    logger.info("=" * 72)
    logger.info("SENSIBILIDAD COMPLETADA")
    logger.info("  Resultados: %s", results_csv)
    results_json_path = config.get("output", {}).get("results_json")
    if results_json_path:
        _write_results_json(
            results_csv=results_csv,
            results_json=Path(results_json_path),
            experiment_name=config.get("experiment", {}).get("name", "sensitivity"),
            total_runs_planned=total_runs,
            resume=resume,
            workers=workers if use_parallel else 0,
        )
    logger.info("=" * 72)


def _get_z_from_csv(
    results_csv: Path, parameter: str, delta: float, seed: int
) -> float | None:
    """Buscar z_value de un run especifico en el CSV."""
    try:
        with open(results_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (
                    row["parameter"] == parameter
                    and row["delta"] == str(delta)
                    and row["seed"] == str(seed)
                ):
                    return float(row["z_value"])
    except Exception:
        pass
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Runner de analisis de sensibilidad (Sprint 4.2)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="experiments/config/sensitivity.yaml",
        help="Ruta al YAML de configuracion",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostrar plan sin ejecutar",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Continuar desde CSV existente (saltar runs completados)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=-1,
        help="Numero de workers paralelos (-1=auto, 0=secuencial, N=N workers)",
    )
    args = parser.parse_args()

    run_sensitivity(
        config_path=args.config,
        dry_run=args.dry_run,
        resume=args.resume,
        workers=args.workers,
    )


if __name__ == "__main__":
    main()
