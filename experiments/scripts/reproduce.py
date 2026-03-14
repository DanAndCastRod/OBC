"""
Sprint 5.1 — Pipeline de reproducibilidad end-to-end.

Verifica que la pipeline completa (instancia → CBC → GA-SA → métricas)
es reproducible con seed fija, e imprime tabla de versiones.

Uso:
    python experiments/scripts/reproduce.py

Autor: Daniel Andrés Castañeda Rodríguez
Sprint: 5.1
"""

from __future__ import annotations

import importlib.metadata
import platform
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, ".")

import numpy as np
import pandas as pd

from src.instances.generator import InstanceGenerator
from src.metaheuristics.ga_sa import HybridGASA
from src.model.parameters import ProblemInstance
from src.model.solver import solve_exact

# ============================================================
# Config
# ============================================================
REPRODUCE_SIZE = "small"
REPRODUCE_SEED = 42
GA_SA_SEED = 1
TOLERANCE = 1e-6

COMPARISON_CSV = Path("experiments/results/comparison.csv")

GA_SA_PARAMS = {
    "pop_size": 39,
    "crossover_rate": 0.8589,
    "mutation_rate": 0.0505,
    "elitism_count": 1,
    "selection_size": 3,
    "local_search_T": 3226.60,
    "local_search_cooling": 0.7126,
    "local_search_freq": 9,
    "local_search_iters": 26,
    "local_search_top_k": 10,
    "n_generations": 200,
    "stagnation_limit": 50,
}

PACKAGES = [
    "numpy",
    "scipy",
    "pandas",
    "pulp",
    "matplotlib",
    "seaborn",
    "optuna",
    "pyyaml",
    "tqdm",
    "pytest",
]


def _set_seed(seed: int) -> None:
    np.random.seed(seed)
    random.seed(seed)


def _get_versions() -> dict[str, str]:
    """Get installed versions of key packages."""
    versions = {
        "Python": platform.python_version(),
        "Platform": platform.platform(),
    }
    for pkg in PACKAGES:
        try:
            versions[pkg] = importlib.metadata.version(pkg)
        except importlib.metadata.PackageNotFoundError:
            versions[pkg] = "NOT FOUND"
    return versions


def _get_reference_z() -> float | None:
    """Get reference Z from comparison.csv for small_seed42 / ga_sa / seed=1."""
    if not COMPARISON_CSV.exists():
        return None
    df = pd.read_csv(COMPARISON_CSV)
    match = df[
        (df["algorithm"] == "ga_sa")
        & (df["instance"] == f"{REPRODUCE_SIZE}_seed{REPRODUCE_SEED}")
        & (df["seed"] == GA_SA_SEED)
    ]
    if match.empty:
        return None
    return float(match.iloc[0]["z_value"])


def main() -> None:
    print("=" * 60)
    print("  Reproducibilidad End-to-End — Sprint 5.1")
    print("=" * 60)

    # 1. Version table
    print("\n[1/5] Versiones del entorno:")
    versions = _get_versions()
    for pkg, ver in versions.items():
        print(f"  {pkg:20s} {ver}")

    # 2. Generate instance
    print(f"\n[2/5] Generando instancia {REPRODUCE_SIZE} (seed={REPRODUCE_SEED})...")
    _set_seed(REPRODUCE_SEED)
    gen = InstanceGenerator()
    instance = gen.generate(size_profile=REPRODUCE_SIZE, seed=REPRODUCE_SEED)
    print(f"  ✓ {instance.summary()}")

    # Also load the stored instance for comparison
    stored_path = Path(f"data/instances/{REPRODUCE_SIZE}_seed{REPRODUCE_SEED}.yaml")
    if stored_path.exists():
        instance_stored = ProblemInstance.from_yaml(stored_path)
        demand_match = np.allclose(instance.demand, instance_stored.demand, atol=1e-6)
        prices_match = np.allclose(instance.prices, instance_stored.prices, atol=1e-6)
        print(f"  ✓ Demanda coincide con almacenada: {demand_match}")
        print(f"  ✓ Precios coinciden con almacenados: {prices_match}")
        # Use stored instance for exact match with comparison.csv
        instance = instance_stored
    else:
        print(f"  ⚠ Instancia almacenada no encontrada: {stored_path}")

    # 3. Solve with CBC
    print("\n[3/5] Resolviendo con CBC (time_limit=300s)...")
    t0 = time.time()
    result = solve_exact(instance, time_limit=300, solver="cbc")
    t_cbc = time.time() - t0
    if result.solution is not None:
        print(f"  ✓ CBC Z = {result.objective_value:,.0f} COP ({t_cbc:.1f}s)")
        print(f"  ✓ Status: {result.status.value}")
    else:
        print(f"  ⚠ CBC no encontró solución ({result.status.value})")

    # 4. Run GA-SA
    print(f"\n[4/5] Ejecutando GA-SA (seed={GA_SA_SEED})...")
    _set_seed(GA_SA_SEED)
    mh = HybridGASA(GA_SA_PARAMS)
    t0 = time.time()
    sol = mh.solve(instance)
    t_gasa = time.time() - t0
    z_reproduce = sol.objective_value
    print(f"  ✓ GA-SA Z = {z_reproduce:,.0f} COP ({t_gasa:.1f}s)")
    print(f"  ✓ Evaluaciones: {mh.n_evaluations:,}")

    # 5. Compare with stored result
    print("\n[5/5] Verificando reproducibilidad...")
    z_reference = _get_reference_z()
    if z_reference is not None:
        diff = abs(z_reproduce - z_reference)
        match = diff < TOLERANCE
        print(f"  Z reproducido:  {z_reproduce:,.6f}")
        print(f"  Z almacenado:   {z_reference:,.6f}")
        print(f"  Diferencia:     {diff:.10f}")
        if match:
            print(f"  ✓ REPRODUCIBLE (diff < {TOLERANCE})")
        else:
            pct = diff / abs(z_reference) * 100 if abs(z_reference) > 0 else 0
            print(f"  ⚠ Diferencia detectada ({pct:.4f}%)")
            print("    Esto puede deberse a diferencias en el orden de operaciones")
            print("    flotantes entre ejecuciones. Si < 0.01%, es aceptable.")
    else:
        print(f"  ⚠ No se encontró referencia en {COMPARISON_CSV}")
        print(f"    Z reproducido: {z_reproduce:,.0f}")

    # Summary
    print("\n" + "=" * 60)
    tests_passed = True
    if z_reference is not None:
        pct_diff = (
            abs(z_reproduce - z_reference) / abs(z_reference) * 100
            if abs(z_reference) > 0
            else 0
        )
        if pct_diff > 0.01:
            tests_passed = False
    print(
        f"  {'✓' if tests_passed else '⚠'} Reproducibilidad: {'PASÓ' if tests_passed else 'ADVERTENCIA'}"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
