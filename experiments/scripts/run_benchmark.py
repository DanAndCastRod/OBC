"""
Benchmark comparativo: solver exacto + metaheuristicas.

Genera:
- salida en consola
- CSV/JSON con resultados
- graficas por instancia (gap y tiempo)

Uso:
    python experiments/scripts/run_benchmark.py --output-dir experiments/results/benchmark
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, ".")

import matplotlib
import numpy as np
import yaml

from experiments.scripts.generate_instances import (
    create_medium_instance,
    create_small_instance,
)
from src.metaheuristics.de import DifferentialEvolution
from src.metaheuristics.ga import GeneticAlgorithm
from src.metaheuristics.ga_sa import HybridGASA
from src.metaheuristics.sa import SimulatedAnnealing
from src.model import constraints
from src.model.solver import SolverStatus, solve_exact

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_tuned_config(algo: str, config_dir: str = "experiments/config") -> dict:
    """Load tuned config if available."""
    path = Path(config_dir) / f"tuning_{algo}.yaml"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("best_params", {})


def _save_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    keys = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def _save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def _plot_instance_summary(
    output_dir: Path, instance_name: str, rows: list[dict]
) -> None:
    alg_order = ["Exact (CBC)", "GA", "SA", "DE", "GA-SA"]
    subset = [r for r in rows if r["instance"] == instance_name]
    subset_map = {r["algorithm"]: r for r in subset}
    algs = [a for a in alg_order if a in subset_map]
    if not algs:
        return

    gaps = [float(subset_map[a]["gap_percent"]) for a in algs]
    times = [float(subset_map[a]["time_seconds"]) for a in algs]

    x = np.arange(len(algs))
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

    axes[0].bar(x, gaps, color="#2E86AB")
    axes[0].set_title(f"{instance_name} - Gap vs Exact")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(algs, rotation=30, ha="right")
    axes[0].set_ylabel("Gap %")
    axes[0].grid(axis="y", alpha=0.25, linestyle="--")

    axes[1].bar(x, times, color="#F18F01")
    axes[1].set_title(f"{instance_name} - Runtime")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(algs, rotation=30, ha="right")
    axes[1].set_ylabel("Seconds")
    axes[1].grid(axis="y", alpha=0.25, linestyle="--")

    fig.tight_layout()
    fig.savefig(output_dir / f"benchmark_{instance_name}_summary.png", dpi=160)
    plt.close(fig)


def run_benchmark(output_dir: str, exact_time_limit: int = 120, seed: int = 42) -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    instances = {
        "small_seed100": create_small_instance(seed=100),
        "medium_seed200": create_medium_instance(seed=200),
    }

    print("=" * 72)
    print("BENCHMARK: Solver Exacto + GA/SA/DE/GA-SA")
    print("=" * 72)

    all_rows: list[dict] = []

    for inst_name, inst in instances.items():
        print("\n" + "*" * 72)
        print(f"Instancia: {inst_name}")
        print(
            f"  Formas={inst.n_cut_forms}  Periodos={inst.n_periods}  Escenarios={inst.n_scenarios}"
        )
        print(
            f"  Q_min={inst.capacity_min}  Q_max={inst.capacity_max}  Exclusividad={len(inst.exclusivity_groups)}"
        )
        print("*" * 72)

        results: dict[str, dict] = {}
        z_baseline: float | None = None

        # 1) Exact
        print("\n[1/5] Solver exacto (CBC)...")
        try:
            exact = solve_exact(inst, time_limit=exact_time_limit)
            feasible = exact.solution is not None and constraints.all_satisfied(
                exact.solution, inst
            )
            is_optimal = exact.status == SolverStatus.OPTIMAL
            if feasible and is_optimal:
                z_baseline = exact.objective_value

            results["Exact (CBC)"] = {
                "Z": exact.objective_value,
                "time": exact.elapsed_seconds,
                "gap": 0.0 if is_optimal else float("nan"),
                "feasible": feasible,
                "evals": "-",
                "status": exact.status.value,
            }
            print(
                f"  Z={exact.objective_value:,.0f}  t={exact.elapsed_seconds:.2f}s  status={exact.status.value}"
            )
            if z_baseline is None:
                print(
                    "  [WARN] Baseline exacto no-optimo; gaps de metaheuristicas se reportaran como NaN."
                )
        except Exception as exc:
            print(f"  ERROR: {exc}")
            results["Exact (CBC)"] = {
                "Z": float("nan"),
                "time": float("nan"),
                "gap": float("nan"),
                "feasible": False,
                "evals": "-",
                "status": "error",
            }

        mh_map = {
            "ga": (
                "GA",
                GeneticAlgorithm,
                {"pop_size": 30, "n_generations": 50, "stagnation_limit": 30},
            ),
            "sa": (
                "SA",
                SimulatedAnnealing,
                {
                    "T_initial": 1e5,
                    "T_final": 1e3,
                    "cooling_rate": 0.5,
                    "max_iterations": 30,
                },
            ),
            "de": (
                "DE",
                DifferentialEvolution,
                {"pop_size": 30, "max_generations": 50, "stagnation_limit": 30},
            ),
            "ga_sa": (
                "GA-SA",
                HybridGASA,
                {
                    "pop_size": 30,
                    "n_generations": 50,
                    "stagnation_limit": 30,
                    "local_search_freq": 10,
                    "local_search_top_k": 3,
                    "local_search_iters": 15,
                },
            ),
        }

        for i, (key, (label, cls, defaults)) in enumerate(mh_map.items(), start=2):
            print(f"\n[{i}/5] {label}...")
            tuned = load_tuned_config(key)
            config = {**defaults, **tuned}
            if tuned:
                print(f"  usando tuned config: experiments/config/tuning_{key}.yaml")

            np.random.seed(seed)
            mh = cls(config)
            t0 = time.time()
            sol = mh.solve(inst)
            elapsed = time.time() - t0

            feasible = constraints.all_satisfied(sol, inst)
            if z_baseline is not None and abs(z_baseline) > 1e-9:
                gap = (z_baseline - mh.best_fitness) / abs(z_baseline) * 100.0
            else:
                gap = float("nan")

            results[label] = {
                "Z": mh.best_fitness,
                "time": elapsed,
                "gap": gap,
                "feasible": feasible,
                "evals": mh.n_evaluations,
                "status": "n/a",
            }
            print(
                f"  Z={mh.best_fitness:,.0f}  t={elapsed:.2f}s  gap={gap:.2f}%  feasible={feasible}  evals={mh.n_evaluations}"
            )

        print("\n" + "-" * 90)
        print(
            f"{'Algoritmo':<15} {'Z':>15} {'Tiempo':>10} {'Gap%':>10} {'Evals':>10} {'OK':>6} {'Status':>12}"
        )
        print("-" * 90)
        for algo_name, res in results.items():
            ok = "OK" if res["feasible"] else "FAIL"
            print(
                f"{algo_name:<15} {res['Z']:>15,.0f} {res['time']:>9.2f}s {res['gap']:>9.2f}% "
                f"{str(res['evals']):>10} {ok:>6} {res['status']:>12}"
            )

            all_rows.append(
                {
                    "instance": inst_name,
                    "algorithm": algo_name,
                    "z_value": float(res["Z"]),
                    "time_seconds": float(res["time"]),
                    "gap_percent": float(res["gap"]),
                    "feasible": bool(res["feasible"]),
                    "evaluations": str(res["evals"]),
                    "status": str(res["status"]),
                }
            )

        _plot_instance_summary(output_path, inst_name, all_rows)

    csv_path = output_path / "benchmark_results.csv"
    json_path = output_path / "benchmark_results.json"
    _save_csv(csv_path, all_rows)
    _save_json(
        json_path,
        {
            "generated_at_epoch": time.time(),
            "rows": all_rows,
        },
    )

    print("\n" + "=" * 72)
    print("Benchmark completado.")
    print(f"CSV:   {csv_path}")
    print(f"JSON:  {json_path}")
    print(f"PNGs:  {output_path}\\benchmark_<instancia>_summary.png")


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark metaheuristicas")
    parser.add_argument(
        "--output-dir",
        type=str,
        default="experiments/results/benchmark",
    )
    parser.add_argument("--time-limit", type=int, default=120)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    run_benchmark(
        output_dir=args.output_dir,
        exact_time_limit=args.time_limit,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
