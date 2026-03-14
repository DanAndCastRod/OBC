"""
Generador del banco completo de instancias para el proyecto.

Genera 15 instancias (3 seeds x 5 perfiles) usando InstanceGenerator,
resuelve instancias toy y small con CBC, y documenta el banco.

Sprint: 3.3
Uso: python experiments/scripts/generate_instances.py [--output-dir data/instances]

Nota: las funciones create_small_instance y create_medium_instance
se mantienen para compatibilidad con run_tuning.py (calibracion Fase 2).
"""

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, ".")

import numpy as np

from src.instances.generator import InstanceGenerator
from src.model.parameters import ProblemInstance

# ============================================================
# Funciones legacy (compatibilidad con run_tuning.py)
# ============================================================


def create_small_instance(seed: int = 100) -> ProblemInstance:
    """Small: 3 formas, 5 dias, 3 escenarios (legacy para tuning)."""
    rng = np.random.RandomState(seed)
    n_f, n_t, n_w = 3, 5, 3

    base_demand = np.array([3000.0, 2000.0, 1000.0])
    demand = np.zeros((n_f, n_t, n_w))
    for f in range(n_f):
        for t in range(n_t):
            for w in range(n_w):
                demand[f, t, w] = max(100, base_demand[f] * (1 + 0.15 * rng.randn()))

    return ProblemInstance(
        name=f"small_seed{seed}",
        profile="small",
        seed=seed,
        n_parts=3,
        part_names=["Pechuga", "Muslo", "Otros"],
        alpha=np.array([0.40, 0.30, 0.30]),
        n_cut_forms=3,
        cut_form_names=["Pechuga", "Muslo", "Subproducto"],
        composition=np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.int32),
        exclusivity_groups=[],
        cut_config=np.array([1, 1, 1], dtype=np.int32),
        n_periods=n_t,
        weight=2.5,
        prices=np.array([14000.0, 9000.0, 1500.0]),
        cost_prod=2000.0,
        cost_setup=500000.0,
        cost_inv=np.array([300.0, 250.0, 100.0]),
        cost_pen=np.array([5000.0, 3500.0, 500.0]),
        capacity_max=5000,
        capacity_min=500,
        shelf_life=np.array([5, 5, 30], dtype=np.int32),
        n_scenarios=n_w,
        scenario_probs=np.array([1 / n_w] * n_w),
        demand=demand,
    )


def create_medium_instance(seed: int = 200) -> ProblemInstance:
    """Medium: 6 formas, 10 dias, 10 escenarios (legacy para tuning)."""
    rng = np.random.RandomState(seed)
    n_f, n_t, n_w = 6, 10, 10

    from src.model.parameters import ExclusivityGroup

    base_demand = np.array([4000.0, 2500.0, 2000.0, 1500.0, 1000.0, 800.0])
    demand = np.zeros((n_f, n_t, n_w))
    for f in range(n_f):
        for t in range(n_t):
            for w in range(n_w):
                demand[f, t, w] = max(100, base_demand[f] * (1 + 0.20 * rng.randn()))

    return ProblemInstance(
        name=f"medium_seed{seed}",
        profile="medium",
        seed=seed,
        n_parts=5,
        part_names=["Pechuga", "Muslo", "Contramuslo", "Ala", "Otros"],
        alpha=np.array([0.35, 0.15, 0.12, 0.08, 0.30]),
        n_cut_forms=6,
        cut_form_names=[
            "Pechuga",
            "Pernil (muslo+contra)",
            "Muslo solo",
            "Ala",
            "Subproducto",
            "Medio pollo",
        ],
        composition=np.array(
            [
                [1, 0, 0, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1],
                [1, 1, 1, 1, 0],
            ],
            dtype=np.int32,
        ),
        exclusivity_groups=[
            ExclusivityGroup(
                name="Muslo vs Pernil",
                cut_form_indices=[1, 2],
                shared_part_index=1,
            ),
        ],
        cut_config=np.array([1, 1, 0, 1, 1, 0], dtype=np.int32),
        n_periods=n_t,
        weight=2.5,
        prices=np.array([14000.0, 11000.0, 9000.0, 6000.0, 1500.0, 12000.0]),
        cost_prod=2000.0,
        cost_setup=500000.0,
        cost_inv=np.array([300.0, 250.0, 250.0, 200.0, 100.0, 280.0]),
        cost_pen=np.array([5000.0, 3500.0, 3500.0, 2500.0, 500.0, 4000.0]),
        capacity_max=8000,
        capacity_min=1000,
        shelf_life=np.array([5, 5, 5, 5, 30, 3], dtype=np.int32),
        n_scenarios=n_w,
        scenario_probs=np.array([1 / n_w] * n_w),
        demand=demand,
    )


def generate_calibration_set(n_seeds: int = 5) -> list[ProblemInstance]:
    """Generar conjunto legacy para calibracion (compatibilidad)."""
    instances = []
    for i in range(n_seeds):
        instances.append(create_small_instance(seed=100 + i))
        instances.append(create_medium_instance(seed=200 + i))
    return instances


# ============================================================
# Generacion del banco completo (Sprint 3.3)
# ============================================================

PROFILES = ["toy", "small", "medium", "large", "industrial"]
SEEDS = [42, 123, 456]
SOLVABLE_PROFILES = {"toy", "small"}  # solver rapido


def generate_instance_bank(
    output_dir: Path,
    seeds: list[int] | None = None,
    solve_small: bool = True,
    solver_time_limit: int = 120,
) -> list[dict]:
    """Generar banco completo de instancias.

    Args:
        output_dir: Directorio de salida.
        seeds: Lista de semillas (default: [42, 123, 456]).
        solve_small: Resolver toy/small con CBC.
        solver_time_limit: Timeout del solver en segundos.

    Returns:
        Lista de dicts con info de cada instancia generada.
    """
    if seeds is None:
        seeds = SEEDS

    output_dir.mkdir(parents=True, exist_ok=True)
    gen = InstanceGenerator()
    catalog = []

    print(
        f"Generando banco de instancias: {len(PROFILES)} perfiles x {len(seeds)} seeds"
    )
    print(f"Directorio: {output_dir}")
    print(f"Solver para toy/small: {'Si' if solve_small else 'No'}")
    print("=" * 70)

    for profile in PROFILES:
        for seed in seeds:
            inst = gen.generate(size_profile=profile, seed=seed)

            # Guardar YAML
            yaml_path = output_dir / f"{inst.name}.yaml"
            inst.to_yaml(yaml_path)

            # Estadisticas de demanda
            demand_mean = float(inst.demand.mean())
            demand_std = float(inst.demand.std())
            demand_cv = demand_std / demand_mean if demand_mean > 0 else 0

            entry = {
                "name": inst.name,
                "profile": profile,
                "seed": seed,
                "n_cut_forms": inst.n_cut_forms,
                "n_periods": inst.n_periods,
                "n_scenarios": inst.n_scenarios,
                "n_exclusivity_groups": len(inst.exclusivity_groups),
                "demand_mean": round(demand_mean, 1),
                "demand_std": round(demand_std, 1),
                "demand_cv": round(demand_cv, 3),
                "yaml_path": str(yaml_path),
                "optimal_z": None,
                "solver_time": None,
                "solver_status": None,
            }

            # Resolver con CBC (solo toy y small)
            if solve_small and profile in SOLVABLE_PROFILES:
                try:
                    from src.model.solver import SolverStatus, solve_exact

                    print(f"  Resolviendo {inst.name} con CBC...", end=" ", flush=True)
                    t0 = time.time()
                    result = solve_exact(inst, time_limit=solver_time_limit)
                    elapsed = time.time() - t0

                    entry["solver_time"] = round(elapsed, 2)
                    entry["solver_status"] = result.status.name

                    if result.status == SolverStatus.OPTIMAL:
                        entry["optimal_z"] = round(float(result.objective_value), 2)
                        print(f"Z={entry['optimal_z']:,.0f}  ({elapsed:.1f}s)")
                    else:
                        print(f"{result.status.name}  ({elapsed:.1f}s)")
                except Exception as e:
                    print(f"ERROR: {e}")
                    entry["solver_status"] = f"error: {e}"
            else:
                print(
                    f"  {inst.name}: {inst.n_cut_forms}f, {inst.n_periods}t, {inst.n_scenarios}w"
                )

            catalog.append(entry)

    # Guardar catalogo JSON
    catalog_path = output_dir / "instance_catalog.json"
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"\nCatalogo guardado en: {catalog_path}")

    # Imprimir resumen
    print(f"\n{'='*70}")
    print(f"Resumen: {len(catalog)} instancias generadas")
    print(
        f"{'Nombre':<25} {'F':>2} {'T':>3} {'W':>4} {'Demand mu':>10} {'CV':>5} {'Solver':>10} {'Z*':>15}"
    )
    print("-" * 80)
    for e in catalog:
        z_str = f"{e['optimal_z']:,.0f}" if e["optimal_z"] else "-"
        sv_str = e["solver_status"] or "-"
        print(
            f"{e['name']:<25} {e['n_cut_forms']:>2} {e['n_periods']:>3} "
            f"{e['n_scenarios']:>4} {e['demand_mean']:>10,.1f} {e['demand_cv']:>5.3f} "
            f"{sv_str:>10} {z_str:>15}"
        )

    return catalog


# ============================================================
# Main
# ============================================================


def main():
    parser = argparse.ArgumentParser(
        description="Generar banco de instancias del problema de coproductos."
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/instances",
        help="Directorio de salida (default: data/instances)",
    )
    parser.add_argument(
        "--no-solve",
        action="store_true",
        help="No resolver con CBC (mas rapido)",
    )
    parser.add_argument(
        "--solver-timeout",
        type=int,
        default=120,
        help="Timeout del solver en segundos (default: 120)",
    )
    args = parser.parse_args()

    generate_instance_bank(
        output_dir=Path(args.output_dir),
        solve_small=not args.no_solve,
        solver_time_limit=args.solver_timeout,
    )


if __name__ == "__main__":
    main()
