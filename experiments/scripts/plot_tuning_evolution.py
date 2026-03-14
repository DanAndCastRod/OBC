"""
Genera grafica comparativa de evolucion de tuning a partir de historiales JSON.

Uso:
    python experiments/scripts/plot_tuning_evolution.py \
        --results-dir experiments/results/tuning
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_histories(results_dir: Path) -> dict[str, dict]:
    histories = {}
    for path in sorted(results_dir.glob("tuning_*_history.json")):
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        algo = payload.get("algorithm")
        if algo:
            histories[algo] = payload
    return histories


def plot_comparison(histories: dict[str, dict], output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    for algo, hist in histories.items():
        ax.plot(
            hist.get("trial_numbers", []),
            hist.get("best_so_far", []),
            linewidth=2.0,
            label=algo.upper(),
        )
    ax.set_title("Optuna Best-So-Far Evolution by Algorithm")
    ax.set_xlabel("Trial")
    ax.set_ylabel("Average fitness")
    ax.grid(alpha=0.25, linestyle="--")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot tuning evolution comparison")
    parser.add_argument(
        "--results-dir",
        type=str,
        default="experiments/results/tuning",
    )
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    histories = load_histories(results_dir)
    if not histories:
        raise FileNotFoundError(
            f"No se encontraron archivos tuning_*_history.json en {results_dir}"
        )

    output_path = results_dir / "tuning_evolution_comparison.png"
    plot_comparison(histories, output_path)
    print(f"Grafica guardada en: {output_path}")


if __name__ == "__main__":
    main()
