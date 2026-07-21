"""
Re-tuning de GA/DE/GA-SA para el régimen v2 (generalización de tune_sa_v2.py).

Los hiperparámetros de GA, DE y GA-SA en comparison_v2.yaml se calibraron en
v1 con el decodificador viejo (sin demand_cap) y presupuesto dispar. Este
script tunea UN algoritmo (elegido vía --algo) sobre 2 instancias v2 con
demand_cap activo y presupuesto reducido por corrida (max_evaluations), de
modo que ~40 trials TPE sean viables.

Espacios de búsqueda (los cortes de generaciones quedan altos: el presupuesto
lo da max_evaluations):

    ga:
        pop_size        int [30, 120]
        crossover_rate  [0.60, 0.95]
        mutation_rate   [0.01, 0.20]
        elitism_count   int [1, 5]
        selection_size  int [2, 5]
        (fijos: n_generations 100000, stagnation_limit 100000)

    de:
        pop_size        int [20, 80]
        CR              [0.30, 0.90]
        F               [0.20, 0.90]
        (fijos: strategy "best/1/bin", max_generations 100000,
                stagnation_limit 100000)

    ga_sa:
        pop_size             int [20, 60]
        crossover_rate       [0.60, 0.95]
        mutation_rate        [0.01, 0.15]
        elitism_count        int [1, 3]
        selection_size       int [2, 5]
        local_search_T       log-uniforme [500, 10000]
        local_search_cooling [0.60, 0.90]
        local_search_freq    int [3, 15]
        local_search_iters   int [10, 50]
        local_search_top_k   int [3, 15]
        (fijos: n_generations 100000, stagnation_limit 100000)

Objetivo: maximizar el Z medio sobre (instancia x seed) = 2 x 2 = 4 corridas.
Storage: journal de Optuna en experiments/results_v2/tuning_<algo>/ (reanudable).

Uso:
    python experiments/scripts/tune_mh_v2.py --algo ga --n-trials 40 --max-evaluations 6000
    python experiments/scripts/tune_mh_v2.py --algo de --n-trials 40 --max-evaluations 6000
    python experiments/scripts/tune_mh_v2.py --algo ga_sa --n-trials 40 --max-evaluations 6000
"""

from __future__ import annotations

import argparse
import csv
import random
import sys
import time
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
import optuna
import yaml
from optuna.storages import JournalStorage
from optuna.storages.journal import JournalFileBackend, JournalFileOpenLock

from src.metaheuristics.de import DifferentialEvolution
from src.metaheuristics.ga import GeneticAlgorithm
from src.metaheuristics.ga_sa import HybridGASA
from src.model.parameters import ProblemInstance

optuna.logging.set_verbosity(optuna.logging.WARNING)

# Instancias de calibración v2 (una small, una medium; el régimen objetivo)
INSTANCE_PATHS = [
    "data/instances_v2/small_v2_seed201.yaml",
    "data/instances_v2/medium_v2_seed201.yaml",
]

# Presupuesto de la campaña v2 (para el bloque YAML final, NO para los trials)
CAMPAIGN_MAX_EVALUATIONS = 20000


# ============================================================
# Espacios de búsqueda por algoritmo
# ============================================================
def suggest_ga(trial: optuna.Trial) -> dict[str, Any]:
    return {
        "pop_size": trial.suggest_int("pop_size", 30, 120),
        "crossover_rate": trial.suggest_float("crossover_rate", 0.60, 0.95),
        "mutation_rate": trial.suggest_float("mutation_rate", 0.01, 0.20),
        "elitism_count": trial.suggest_int("elitism_count", 1, 5),
        "selection_size": trial.suggest_int("selection_size", 2, 5),
    }


def suggest_de(trial: optuna.Trial) -> dict[str, Any]:
    return {
        "pop_size": trial.suggest_int("pop_size", 20, 80),
        "CR": trial.suggest_float("CR", 0.30, 0.90),
        "F": trial.suggest_float("F", 0.20, 0.90),
    }


def suggest_ga_sa(trial: optuna.Trial) -> dict[str, Any]:
    return {
        "pop_size": trial.suggest_int("pop_size", 20, 60),
        "crossover_rate": trial.suggest_float("crossover_rate", 0.60, 0.95),
        "mutation_rate": trial.suggest_float("mutation_rate", 0.01, 0.15),
        "elitism_count": trial.suggest_int("elitism_count", 1, 3),
        "selection_size": trial.suggest_int("selection_size", 2, 5),
        "local_search_T": trial.suggest_float(
            "local_search_T", 500.0, 10000.0, log=True
        ),
        "local_search_cooling": trial.suggest_float(
            "local_search_cooling", 0.60, 0.90
        ),
        "local_search_freq": trial.suggest_int("local_search_freq", 3, 15),
        "local_search_iters": trial.suggest_int("local_search_iters", 10, 50),
        "local_search_top_k": trial.suggest_int("local_search_top_k", 3, 15),
    }


# ============================================================
# Especificación por algoritmo: clase, fijos y formato del YAML final.
# yaml_order: (clave, formato) en el orden del bloque de comparison_v2.yaml;
# formato None = valor tal cual (ints y strings), "x.4f"/"x.2f" = float.
# ============================================================
ALGO_SPECS: dict[str, dict[str, Any]] = {
    "ga": {
        "cls": GeneticAlgorithm,
        "class_name": "GeneticAlgorithm",
        "suggest": suggest_ga,
        "fixed": {"n_generations": 100000, "stagnation_limit": 100000},
        "yaml_order": [
            ("pop_size", None),
            ("crossover_rate", ".4f"),
            ("mutation_rate", ".4f"),
            ("elitism_count", None),
            ("selection_size", None),
            ("n_generations", None),
            ("stagnation_limit", None),
        ],
    },
    "de": {
        "cls": DifferentialEvolution,
        "class_name": "DifferentialEvolution",
        "suggest": suggest_de,
        "fixed": {
            "strategy": "best/1/bin",
            "max_generations": 100000,
            "stagnation_limit": 100000,
        },
        "yaml_order": [
            ("pop_size", None),
            ("CR", ".4f"),
            ("F", ".4f"),
            ("strategy", None),
            ("max_generations", None),
            ("stagnation_limit", None),
        ],
    },
    "ga_sa": {
        "cls": HybridGASA,
        "class_name": "HybridGASA",
        "suggest": suggest_ga_sa,
        "fixed": {"n_generations": 100000, "stagnation_limit": 100000},
        "yaml_order": [
            ("pop_size", None),
            ("crossover_rate", ".4f"),
            ("mutation_rate", ".4f"),
            ("elitism_count", None),
            ("selection_size", None),
            ("local_search_T", ".2f"),
            ("local_search_cooling", ".4f"),
            ("local_search_freq", None),
            ("local_search_iters", None),
            ("local_search_top_k", None),
            ("n_generations", None),
            ("stagnation_limit", None),
        ],
    },
}


def build_config(
    algo: str, params: dict[str, Any], max_evaluations: int
) -> dict[str, Any]:
    """Config completa del algoritmo a partir de los parámetros sugeridos."""
    spec = ALGO_SPECS[algo]
    return {
        **params,
        **spec["fixed"],
        "max_evaluations": max_evaluations,
        "demand_cap": True,
    }


def make_objective(
    algo: str,
    instances: list[ProblemInstance],
    run_seeds: list[int],
    max_evaluations: int,
) -> Callable[[optuna.Trial], float]:
    """Objetivo Optuna: Z medio sobre (instancia x seed)."""
    spec = ALGO_SPECS[algo]

    def objective(trial: optuna.Trial) -> float:
        params = spec["suggest"](trial)
        config = build_config(algo, params, max_evaluations)

        fitnesses: list[float] = []
        try:
            for inst in instances:
                for seed in run_seeds:
                    np.random.seed(seed)
                    random.seed(seed)
                    mh = spec["cls"](config)
                    mh.solve(inst)
                    fitnesses.append(float(mh.best_fitness))
                    trial.set_user_attr(
                        f"Z_{inst.name}_seed{seed}", float(mh.best_fitness)
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


def format_campaign_yaml(algo: str, best_params: dict[str, Any]) -> str:
    """Bloque YAML del algoritmo listo para pegar en comparison_v2.yaml."""
    spec = ALGO_SPECS[algo]
    merged = {**best_params, **spec["fixed"]}
    lines = [
        f"  {algo}:",
        f'    class: "{spec["class_name"]}"',
        "    params:",
    ]
    for key, fmt in spec["yaml_order"]:
        value = merged[key]
        if fmt is not None:
            rendered = f"{value:{fmt}}"
        elif isinstance(value, str):
            rendered = f'"{value}"'
        else:
            rendered = str(value)
        lines.append(f"      {key}: {rendered}")
    lines.append(f"      max_evaluations: {CAMPAIGN_MAX_EVALUATIONS}")
    lines.append("      demand_cap: true")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Re-tuning de GA/DE/GA-SA para el régimen v2"
    )
    parser.add_argument(
        "--algo",
        type=str,
        required=True,
        choices=sorted(ALGO_SPECS),
        help="Algoritmo a tunear (ga, de o ga_sa)",
    )
    parser.add_argument("--n-trials", type=int, default=40)
    parser.add_argument(
        "--max-evaluations",
        type=int,
        default=6000,
        help="Presupuesto de evaluaciones por corrida del algoritmo (default: 6000)",
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
        default=None,
        help=(
            "Directorio para journal, historial y mejores parámetros "
            "(default: experiments/results_v2/tuning_<algo>)"
        ),
    )
    parser.add_argument(
        "--study-name",
        type=str,
        default=None,
        help="Nombre del estudio Optuna (default: tune_<algo>_v2; reanudable vía journal)",
    )
    args = parser.parse_args()

    algo = args.algo
    results_dir = Path(
        args.results_dir
        if args.results_dir is not None
        else f"experiments/results_v2/tuning_{algo}"
    )
    study_name = args.study_name if args.study_name is not None else f"tune_{algo}_v2"
    run_seeds = [int(s) for s in args.run_seeds.split(",") if s.strip()]

    instances = [ProblemInstance.from_yaml(p) for p in INSTANCE_PATHS]
    print(f"Algoritmo a tunear: {algo} ({ALGO_SPECS[algo]['class_name']})")
    print(f"Instancias de calibración v2: {len(instances)}")
    for inst in instances:
        print(
            f"  {inst.name}: {inst.n_cut_forms}f, {inst.n_periods}t, "
            f"{inst.n_scenarios}w"
        )
    print(f"Seeds por trial: {run_seeds}")
    print(f"Presupuesto por corrida: {args.max_evaluations} evaluaciones")
    print(f"Corridas por trial: {len(instances) * len(run_seeds)}")

    results_dir.mkdir(parents=True, exist_ok=True)

    # JournalFileOpenLock: el lock por symlink (default) requiere privilegios
    # en Windows; el lock por open exclusivo funciona sin ellos.
    journal_path = str(results_dir / "journal.log")
    storage = JournalStorage(
        JournalFileBackend(journal_path, lock_obj=JournalFileOpenLock(journal_path))
    )
    study = optuna.create_study(
        study_name=study_name,
        storage=storage,
        direction="maximize",
        sampler=optuna.samplers.TPESampler(seed=args.sampler_seed),
        load_if_exists=True,
    )
    n_done = len([t for t in study.trials if t.state.is_finished()])
    if n_done:
        print(f"Estudio existente con {n_done} trials terminados (se reanuda)")

    print("\n" + "=" * 60)
    print(f"Tuning {algo} v2: {args.n_trials} trials TPE")
    print("=" * 60)

    t0 = time.time()
    study.optimize(
        make_objective(algo, instances, run_seeds, args.max_evaluations),
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
    csv_path = results_dir / f"tuning_{algo}_v2_trials.csv"
    save_trials_csv(csv_path, study)
    print(f"Historial CSV: {csv_path}")

    summary_path = results_dir / f"best_params_{algo}_v2.yaml"
    summary = {
        "algorithm": algo,
        "regime": "v2 (demand_cap, presupuesto igualado)",
        "best_value_mean_Z": float(best.value),
        "best_trial": int(best.number),
        "best_params": {
            **best.params,
            **ALGO_SPECS[algo]["fixed"],
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

    print(f"\nBloque listo para pegar en comparison_v2.yaml (algorithms.{algo}):")
    print("-" * 60)
    print(format_campaign_yaml(algo, best.params))
    print("-" * 60)


if __name__ == "__main__":
    main()
