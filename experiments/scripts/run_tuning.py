"""
Calibracion de hiperparametros con Optuna (TPE).

Para cada metaheuristica:
- define espacio de busqueda
- evalua fitness promedio sobre instancias de calibracion
- guarda mejores hiperparametros
- persiste historial de trials (CSV/JSON) y graficas de evolucion

Uso:
    python experiments/scripts/run_tuning.py --n-trials 30 --algo all
"""

from __future__ import annotations

import argparse
import csv
import json
import multiprocessing as mp
import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, ".")

import matplotlib
import numpy as np
import optuna
import yaml

from experiments.scripts.generate_instances import (
    create_medium_instance,
    create_small_instance,
)
from src.metaheuristics.de import DifferentialEvolution
from src.metaheuristics.ga import GeneticAlgorithm
from src.metaheuristics.ga_sa import HybridGASA
from src.metaheuristics.sa import SimulatedAnnealing

matplotlib.use("Agg")
import matplotlib.pyplot as plt

optuna.logging.set_verbosity(optuna.logging.WARNING)


ALGORITHM_CLASSES = {
    "ga": GeneticAlgorithm,
    "sa": SimulatedAnnealing,
    "de": DifferentialEvolution,
    "ga_sa": HybridGASA,
}


def get_calibration_instances():
    """3 small + 2 medium instances."""
    return [
        create_small_instance(seed=100),
        create_small_instance(seed=101),
        create_small_instance(seed=102),
        create_medium_instance(seed=200),
        create_medium_instance(seed=201),
    ]


def objective_ga(
    trial: optuna.Trial,
    instances,
    seed: int,
    trial_timeout: int,
) -> float:
    config = {
        "pop_size": trial.suggest_int("pop_size", 20, 80),
        "n_generations": 50,
        "crossover_rate": trial.suggest_float("crossover_rate", 0.5, 0.95),
        "mutation_rate": trial.suggest_float("mutation_rate", 0.01, 0.3),
        "selection_size": trial.suggest_int("selection_size", 2, 5),
        "elitism_count": trial.suggest_int("elitism_count", 1, 5),
        "stagnation_limit": 30,
    }
    score, status = _evaluate_config("ga", config, instances, seed, trial_timeout)
    trial.set_user_attr("eval_status", status)
    return score


def objective_sa(
    trial: optuna.Trial,
    instances,
    seed: int,
    trial_timeout: int,
) -> float:
    # Keep a valid probability simplex:
    # p_toggle + p_quantity <= 0.9 so p_both >= 0.1
    p_toggle = trial.suggest_float("p_toggle", 0.1, 0.5)
    p_quantity_max = min(0.6, 0.9 - p_toggle)
    p_quantity = trial.suggest_float("p_quantity", 0.1, p_quantity_max)

    t_initial = trial.suggest_float("T_initial", 1e3, 1e6, log=True)
    t_final = trial.suggest_float("T_final", 100.0, 1e4, log=True)

    config = {
        "T_initial": t_initial,
        "T_final": min(t_final, t_initial * 0.5),
        "cooling_rate": trial.suggest_float("cooling_rate", 0.5, 0.95),
        "max_iterations": trial.suggest_int("max_iterations", 10, 30),
        "p_toggle": p_toggle,
        "p_quantity": p_quantity,
        "delta": trial.suggest_float("delta", 0.05, 0.3),
        "reheat_factor": trial.suggest_float("reheat_factor", 1.1, 2.0),
        "reheat_threshold": trial.suggest_int("reheat_threshold", 20, 80),
    }
    score, status = _evaluate_config("sa", config, instances, seed, trial_timeout)
    trial.set_user_attr("eval_status", status)
    return score


def objective_de(
    trial: optuna.Trial,
    instances,
    seed: int,
    trial_timeout: int,
) -> float:
    config = {
        "pop_size": trial.suggest_int("pop_size", 20, 80),
        "max_generations": 50,
        "F": trial.suggest_float("F", 0.3, 1.5),
        "CR": trial.suggest_float("CR", 0.5, 1.0),
        "strategy": trial.suggest_categorical("strategy", ["rand/1/bin", "best/1/bin"]),
        "stagnation_limit": 30,
    }
    score, status = _evaluate_config("de", config, instances, seed, trial_timeout)
    trial.set_user_attr("eval_status", status)
    return score


def objective_gasa(
    trial: optuna.Trial,
    instances,
    seed: int,
    trial_timeout: int,
) -> float:
    config = {
        "pop_size": trial.suggest_int("pop_size", 20, 60),
        "n_generations": 50,
        "crossover_rate": trial.suggest_float("crossover_rate", 0.5, 0.95),
        "mutation_rate": trial.suggest_float("mutation_rate", 0.01, 0.3),
        "selection_size": trial.suggest_int("selection_size", 2, 5),
        "elitism_count": trial.suggest_int("elitism_count", 1, 5),
        "stagnation_limit": 30,
        "local_search_freq": trial.suggest_int("local_search_freq", 5, 20),
        "local_search_top_k": trial.suggest_int("local_search_top_k", 2, 10),
        "local_search_iters": trial.suggest_int("local_search_iters", 10, 50),
        "local_search_T": trial.suggest_float("local_search_T", 1e3, 1e6, log=True),
        "local_search_cooling": trial.suggest_float("local_search_cooling", 0.7, 0.99),
    }
    score, status = _evaluate_config("ga_sa", config, instances, seed, trial_timeout)
    trial.set_user_attr("eval_status", status)
    return score


OBJECTIVES = {
    "ga": objective_ga,
    "sa": objective_sa,
    "de": objective_de,
    "ga_sa": objective_gasa,
}


def _evaluate_worker(
    algo_key: str,
    config: dict,
    instances,
    seed: int,
    result_path: str,
) -> None:
    """Worker process for one Optuna trial evaluation."""
    payload: dict[str, Any]
    try:
        cls = ALGORITHM_CLASSES[algo_key]
        fitnesses = []
        for inst in instances:
            np.random.seed(seed)
            mh = cls(config)
            mh.solve(inst)
            fitnesses.append(float(mh.best_fitness))
        payload = {"ok": True, "fitness": float(np.mean(fitnesses))}
    except Exception as exc:
        payload = {"ok": False, "error": str(exc)}

    try:
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(payload, f)
    except Exception:
        # Parent treats missing/corrupted payload as trial error.
        pass


def _evaluate_config(
    algo_key: str,
    config: dict,
    instances,
    seed: int = 42,
    trial_timeout: int = 900,
) -> tuple[float, str]:
    """Evaluate one hyperparameter config with hard timeout guard.

    Returns:
        (score, status) where status in {"ok", "timeout", "error"}.
    """
    fd, result_path = tempfile.mkstemp(prefix="optuna_eval_", suffix=".json")
    os.close(fd)
    Path(result_path).unlink(missing_ok=True)
    proc = mp.Process(
        target=_evaluate_worker,
        args=(algo_key, config, instances, seed, result_path),
    )
    proc.start()
    proc.join(timeout=trial_timeout)

    if proc.is_alive():
        proc.terminate()
        proc.join(timeout=5)
        Path(result_path).unlink(missing_ok=True)
        return -1e12, "timeout"

    payload: dict[str, Any] | None = None
    try:
        with open(result_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except Exception:
        payload = None
    finally:
        Path(result_path).unlink(missing_ok=True)

    if payload is None:
        return -1e12, "error"

    if not payload.get("ok", False):
        return -1e12, "error"

    return float(payload["fitness"]), "ok"


def _build_trial_rows(study: optuna.Study) -> list[dict[str, Any]]:
    """Build serializable per-trial rows including best-so-far."""
    rows: list[dict[str, Any]] = []
    best_so_far = -np.inf

    for tr in study.trials:
        value = tr.value if tr.value is not None else float("nan")
        if tr.state == optuna.trial.TrialState.COMPLETE and tr.value is not None:
            best_so_far = max(best_so_far, tr.value)

        duration_s = (
            (tr.datetime_complete - tr.datetime_start).total_seconds()
            if tr.datetime_start is not None and tr.datetime_complete is not None
            else float("nan")
        )

        row: dict[str, Any] = {
            "trial": tr.number,
            "state": tr.state.name,
            "value": value,
            "best_so_far": best_so_far if np.isfinite(best_so_far) else float("nan"),
            "duration_seconds": duration_s,
        }
        for k, v in tr.params.items():
            row[f"param_{k}"] = v
        for k, v in tr.user_attrs.items():
            row[f"user_{k}"] = v
        rows.append(row)

    return rows


def _save_trials_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    all_keys = []
    for r in rows:
        for k in r.keys():
            if k not in all_keys:
                all_keys.append(k)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_keys)
        writer.writeheader()
        writer.writerows(rows)


def _save_history_json(
    path: Path, algo: str, rows: list[dict[str, Any]]
) -> dict[str, Any]:
    trial_numbers = [int(r["trial"]) for r in rows]
    values = [float(r["value"]) for r in rows]
    best = [float(r["best_so_far"]) for r in rows]
    states = [str(r["state"]) for r in rows]

    payload = {
        "algorithm": algo,
        "trial_numbers": trial_numbers,
        "values": values,
        "best_so_far": best,
        "states": states,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return payload


def _plot_single_history(path: Path, algo: str, history: dict[str, Any]) -> None:
    x = history["trial_numbers"]
    y = history["values"]
    y_best = history["best_so_far"]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(x, y, linewidth=1.0, alpha=0.4, label="Trial value")
    ax.plot(x, y_best, linewidth=2.0, label="Best so far")
    ax.set_title(f"Optuna Evolution - {algo.upper()}")
    ax.set_xlabel("Trial")
    ax.set_ylabel("Average fitness")
    ax.grid(alpha=0.25, linestyle="--")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _plot_comparison(path: Path, histories: dict[str, dict[str, Any]]) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))

    for algo, hist in histories.items():
        ax.plot(
            hist["trial_numbers"],
            hist["best_so_far"],
            linewidth=2.0,
            label=algo.upper(),
        )

    ax.set_title("Optuna Best-So-Far Evolution by Algorithm")
    ax.set_xlabel("Trial")
    ax.set_ylabel("Average fitness")
    ax.grid(alpha=0.25, linestyle="--")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Calibracion Optuna")
    parser.add_argument(
        "--algo",
        type=str,
        default="all",
        choices=["ga", "sa", "de", "ga_sa", "all"],
    )
    parser.add_argument("--n-trials", type=int, default=30)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--trial-timeout",
        type=int,
        default=900,
        help="Timeout duro por trial en segundos (default: 900)",
    )
    parser.add_argument(
        "--results-dir",
        type=str,
        default="experiments/results/tuning",
        help="Directorio para historial de trials y graficas",
    )
    args = parser.parse_args()

    instances = get_calibration_instances()
    print(f"Instancias de calibracion: {len(instances)}")
    for inst in instances:
        print(
            f"  {inst.name}: {inst.n_cut_forms}f, {inst.n_periods}t, {inst.n_scenarios}w"
        )

    config_dir = Path("experiments/config")
    config_dir.mkdir(parents=True, exist_ok=True)

    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    algos = list(OBJECTIVES.keys()) if args.algo == "all" else [args.algo]
    histories: dict[str, dict[str, Any]] = {}

    for algo in algos:
        print("\n" + "=" * 60)
        print(f"Calibrando: {algo.upper()} ({args.n_trials} trials)")
        print("=" * 60)
        print(f"Timeout por trial: {args.trial_timeout}s")

        obj_fn = OBJECTIVES[algo]
        study = optuna.create_study(
            direction="maximize",
            sampler=optuna.samplers.TPESampler(seed=args.seed),
            study_name=f"tuning_{algo}",
        )

        t0 = time.time()
        study.optimize(
            lambda trial: obj_fn(trial, instances, args.seed, args.trial_timeout),
            n_trials=args.n_trials,
            show_progress_bar=True,
        )
        elapsed = time.time() - t0

        best = study.best_trial
        print(f"\nMejor trial: #{best.number}")
        print(f"Fitness promedio: {best.value:,.0f}")
        print(f"Tiempo total: {elapsed:.1f}s")
        print("Hiperparametros:")
        for k, v in best.params.items():
            print(f"  {k}: {v}")

        n_timeout = sum(
            1 for tr in study.trials if tr.user_attrs.get("eval_status") == "timeout"
        )
        n_error = sum(
            1 for tr in study.trials if tr.user_attrs.get("eval_status") == "error"
        )
        print(f"Trials timeout: {n_timeout} | Trials error: {n_error}")

        # Save tuned config
        config_path = config_dir / f"tuning_{algo}.yaml"
        config_data = {
            "algorithm": algo,
            "best_params": best.params,
            "best_fitness": float(best.value),
            "n_trials": args.n_trials,
            "n_instances": len(instances),
            "instance_names": [i.name for i in instances],
            "elapsed_seconds": elapsed,
            "seed": args.seed,
            "trial_timeout_seconds": args.trial_timeout,
            "n_timeout_trials": n_timeout,
            "n_error_trials": n_error,
            "history_csv": str(results_dir / f"tuning_{algo}_trials.csv"),
            "history_json": str(results_dir / f"tuning_{algo}_history.json"),
            "history_plot": str(results_dir / f"tuning_{algo}_evolution.png"),
        }
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
        print(f"Config guardado en: {config_path}")

        # Save trial history artifacts
        rows = _build_trial_rows(study)
        csv_path = results_dir / f"tuning_{algo}_trials.csv"
        json_path = results_dir / f"tuning_{algo}_history.json"
        png_path = results_dir / f"tuning_{algo}_evolution.png"

        _save_trials_csv(csv_path, rows)
        history = _save_history_json(json_path, algo, rows)
        _plot_single_history(png_path, algo, history)

        histories[algo] = history
        print(f"Historial CSV: {csv_path}")
        print(f"Historial JSON: {json_path}")
        print(f"Grafica evolucion: {png_path}")

    if len(histories) >= 2:
        comparison_path = results_dir / "tuning_evolution_comparison.png"
        _plot_comparison(comparison_path, histories)
        print(f"\nGrafica comparativa: {comparison_path}")


if __name__ == "__main__":
    mp.freeze_support()
    main()
