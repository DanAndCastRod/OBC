"""
Re-tuning de SA para el régimen v2 (recomendación #15).

Los hiperparámetros de SA en comparison_v2.yaml se calibraron en v1 con el
decodificador viejo (sin demand_cap) y presupuesto dispar. Este script tunea
SOLO SA sobre 2 instancias v2 con demand_cap activo y presupuesto reducido
por corrida (max_evaluations), de modo que ~40 trials TPE sean viables.

Espacio de búsqueda:
    T_initial        fijo en None (auto-estimada)
    T_final          log-uniforme [100, 5e4]
    cooling_rate     [0.70, 0.98]
    max_iterations   int [20, 120]
    p_toggle         [0.1, 0.6]
    p_quantity       [0.1, min(0.5, 0.9 - p_toggle)]  (simplex válido, p_both >= 0.1)
    reheat_factor    [1.0, 2.0]
    reheat_threshold int [20, 120]
    delta            fijo en 0.0661 (valor calibrado vigente)

Objetivo: maximizar el Z medio sobre (instancia x seed) = 2 x 2 = 4 corridas.
Storage: journal de Optuna en experiments/results_v2/tuning_sa/ (reanudable).

Uso:
    python experiments/scripts/tune_sa_v2.py --n-trials 40 --max-evaluations 6000
"""

from __future__ import annotations

import argparse
import csv
import random
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
import optuna
import yaml
from optuna.storages import JournalStorage
from optuna.storages.journal import JournalFileBackend, JournalFileOpenLock

from src.metaheuristics.sa import SimulatedAnnealing
from src.model.parameters import ProblemInstance

optuna.logging.set_verbosity(optuna.logging.WARNING)

# Instancias de calibración v2 (una small, una medium; el régimen objetivo)
INSTANCE_PATHS = [
    "data/instances_v2/small_v2_seed201.yaml",
    "data/instances_v2/medium_v2_seed201.yaml",
]

# Fijos fuera del espacio de búsqueda
DELTA_FIXED = 0.0661
T_INITIAL_FIXED = None  # auto-estimada por el SA

# Presupuesto de la campaña v2 (para el bloque YAML final, NO para los trials)
CAMPAIGN_MAX_EVALUATIONS = 20000


def build_sa_config(params: dict[str, Any], max_evaluations: int) -> dict[str, Any]:
    """Config completa de SA a partir de los parámetros sugeridos."""
    return {
        "T_initial": T_INITIAL_FIXED,
        "T_final": params["T_final"],
        "cooling_rate": params["cooling_rate"],
        "max_iterations": params["max_iterations"],
        "p_toggle": params["p_toggle"],
        "p_quantity": params["p_quantity"],
        "delta": DELTA_FIXED,
        "reheat_factor": params["reheat_factor"],
        "reheat_threshold": params["reheat_threshold"],
        "max_evaluations": max_evaluations,
        "demand_cap": True,
    }


def make_objective(instances: list[ProblemInstance], run_seeds: list[int],
                   max_evaluations: int):
    """Objetivo Optuna: Z medio sobre (instancia x seed)."""

    def objective(trial: optuna.Trial) -> float:
        p_toggle = trial.suggest_float("p_toggle", 0.1, 0.6)
        # Simplex válido: p_toggle + p_quantity <= 0.9 para que p_both >= 0.1
        p_quantity_max = min(0.5, 0.9 - p_toggle)
        params = {
            "T_final": trial.suggest_float("T_final", 100.0, 5e4, log=True),
            "cooling_rate": trial.suggest_float("cooling_rate", 0.70, 0.98),
            "max_iterations": trial.suggest_int("max_iterations", 20, 120),
            "p_toggle": p_toggle,
            "p_quantity": trial.suggest_float("p_quantity", 0.1, p_quantity_max),
            "reheat_factor": trial.suggest_float("reheat_factor", 1.0, 2.0),
            "reheat_threshold": trial.suggest_int("reheat_threshold", 20, 120),
        }
        config = build_sa_config(params, max_evaluations)

        fitnesses: list[float] = []
        try:
            for inst in instances:
                for seed in run_seeds:
                    np.random.seed(seed)
                    random.seed(seed)
                    sa = SimulatedAnnealing(config)
                    sa.solve(inst)
                    fitnesses.append(float(sa.best_fitness))
                    trial.set_user_attr(
                        f"Z_{inst.name}_seed{seed}", float(sa.best_fitness)
                    )
        except Exception as exc:
            trial.set_user_attr("eval_status", "error")
            trial.set_user_attr("eval_error", str(exc))
            return -1e12

        trial.set_user_attr("eval_status", "ok")
        return float(np.mean(fitnesses))

    return objective


def save_trials_csv(path: Path, study: optuna.Study) -> None:
    """Historial de trials con best-so-far, en CSV."""
    rows: list[dict[str, Any]] = []
    best_so_far = -np.inf
    for tr in study.trials:
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
            "value": tr.value if tr.value is not None else float("nan"),
            "best_so_far": best_so_far if np.isfinite(best_so_far) else float("nan"),
            "duration_seconds": duration_s,
        }
        for k, v in tr.params.items():
            row[f"param_{k}"] = v
        for k, v in tr.user_attrs.items():
            row[f"user_{k}"] = v
        rows.append(row)

    fieldnames: list[str] = []
    for r in rows:
        for k in r:
            if k not in fieldnames:
                fieldnames.append(k)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def format_campaign_yaml(best_params: dict[str, Any]) -> str:
    """Bloque YAML de SA listo para pegar en comparison_v2.yaml."""
    lines = [
        "  sa:",
        '    class: "SimulatedAnnealing"',
        "    params:",
        "      T_initial: null        # auto-estimada",
        f"      T_final: {best_params['T_final']:.4f}",
        f"      cooling_rate: {best_params['cooling_rate']:.4f}",
        f"      delta: {DELTA_FIXED}",
        f"      max_iterations: {best_params['max_iterations']}",
        f"      p_quantity: {best_params['p_quantity']:.4f}",
        f"      p_toggle: {best_params['p_toggle']:.4f}",
        f"      reheat_factor: {best_params['reheat_factor']:.4f}",
        f"      reheat_threshold: {best_params['reheat_threshold']}",
        f"      max_evaluations: {CAMPAIGN_MAX_EVALUATIONS}  "
        "# con restarts encadenados hasta agotar",
        "      demand_cap: true",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Re-tuning de SA para el régimen v2")
    parser.add_argument("--n-trials", type=int, default=40)
    parser.add_argument(
        "--max-evaluations",
        type=int,
        default=6000,
        help="Presupuesto de evaluaciones por corrida de SA (default: 6000)",
    )
    parser.add_argument(
        "--sampler-seed",
        type=int,
        default=42,
        help="Seed del sampler TPE (default: 42)",
    )
    parser.add_argument(
        "--run-seeds",
        type=str,
        default="1,2",
        help="Seeds por trial, separadas por coma (default: 1,2)",
    )
    parser.add_argument(
        "--results-dir",
        type=str,
        default="experiments/results_v2/tuning_sa",
        help="Directorio para journal, historial y mejores parámetros",
    )
    parser.add_argument(
        "--study-name",
        type=str,
        default="tune_sa_v2",
        help="Nombre del estudio Optuna (reanudable vía journal)",
    )
    args = parser.parse_args()

    run_seeds = [int(s) for s in args.run_seeds.split(",") if s.strip()]

    instances = [ProblemInstance.from_yaml(p) for p in INSTANCE_PATHS]
    print(f"Instancias de calibración v2: {len(instances)}")
    for inst in instances:
        print(
            f"  {inst.name}: {inst.n_cut_forms}f, {inst.n_periods}t, "
            f"{inst.n_scenarios}w"
        )
    print(f"Seeds por trial: {run_seeds}")
    print(f"Presupuesto por corrida: {args.max_evaluations} evaluaciones")
    print(f"Corridas por trial: {len(instances) * len(run_seeds)}")

    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    # JournalFileOpenLock: el lock por symlink (default) requiere privilegios
    # en Windows; el lock por open exclusivo funciona sin ellos.
    journal_path = str(results_dir / "journal.log")
    storage = JournalStorage(
        JournalFileBackend(journal_path, lock_obj=JournalFileOpenLock(journal_path))
    )
    study = optuna.create_study(
        study_name=args.study_name,
        storage=storage,
        direction="maximize",
        sampler=optuna.samplers.TPESampler(seed=args.sampler_seed),
        load_if_exists=True,
    )
    n_done = len([t for t in study.trials if t.state.is_finished()])
    if n_done:
        print(f"Estudio existente con {n_done} trials terminados (se reanuda)")

    print("\n" + "=" * 60)
    print(f"Tuning SA v2: {args.n_trials} trials TPE")
    print("=" * 60)

    t0 = time.time()
    study.optimize(
        make_objective(instances, run_seeds, args.max_evaluations),
        n_trials=args.n_trials,
        show_progress_bar=True,
    )
    elapsed = time.time() - t0

    best = study.best_trial
    print(f"\nMejor trial: #{best.number}")
    print(f"Z medio: {best.value:,.0f}")
    print(f"Tiempo total: {elapsed:.1f}s")
    print("Hiperparámetros:")
    for k, v in best.params.items():
        print(f"  {k}: {v}")

    n_error = sum(
        1 for tr in study.trials if tr.user_attrs.get("eval_status") == "error"
    )
    print(f"Trials con error: {n_error}")

    # Artefactos
    csv_path = results_dir / "tuning_sa_v2_trials.csv"
    save_trials_csv(csv_path, study)
    print(f"Historial CSV: {csv_path}")

    summary_path = results_dir / "best_params_sa_v2.yaml"
    summary = {
        "algorithm": "sa",
        "regime": "v2 (demand_cap, presupuesto igualado)",
        "best_value_mean_Z": float(best.value),
        "best_trial": int(best.number),
        "best_params": {
            **best.params,
            "T_initial": T_INITIAL_FIXED,
            "delta": DELTA_FIXED,
        },
        "n_trials": len(study.trials),
        "instances": INSTANCE_PATHS,
        "run_seeds": run_seeds,
        "max_evaluations_per_run": args.max_evaluations,
        "sampler_seed": args.sampler_seed,
        "elapsed_seconds": elapsed,
    }
    with open(summary_path, "w", encoding="utf-8") as f:
        yaml.dump(summary, f, default_flow_style=False, allow_unicode=True)
    print(f"Mejores parámetros: {summary_path}")

    print("\nBloque listo para pegar en comparison_v2.yaml (algorithms.sa):")
    print("-" * 60)
    print(format_campaign_yaml(best.params))
    print("-" * 60)


if __name__ == "__main__":
    main()
