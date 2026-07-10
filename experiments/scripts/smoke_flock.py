"""
Smoke run de perfiles de pollo integrados al pipeline.

Genera una instancia 'small' con tres composiciones de parvada (liviano,
estándar, pesado) y ejecuta baseline + CBC exacto + GA-SA sobre cada una,
usando las MISMAS funciones del pipeline de comparación (`_run_single`) y su
ruta paralela (ProcessPoolExecutor). Reporta cómo cambian Z, gap vs CBC,
inventario y utilidad con el perfil del pollo.

No escribe en experiments/results/ — es una prueba de humo rápida.

Uso:
    python experiments/scripts/smoke_flock.py
    python experiments/scripts/smoke_flock.py --workers 3
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np  # noqa: E402

from experiments.scripts.run_comparison import _run_single  # noqa: E402
from src.instances.generator import InstanceGenerator  # noqa: E402

# GA-SA con presupuesto reducido para que el smoke sea rápido
GA_SA_PARAMS = {
    "pop_size": 30,
    "crossover_rate": 0.8589,
    "mutation_rate": 0.0505,
    "elitism_count": 1,
    "selection_size": 3,
    "local_search_T": 3226.60,
    "local_search_cooling": 0.7126,
    "local_search_freq": 9,
    "local_search_iters": 20,
    "n_generations": 60,
    "stagnation_limit": 25,
}

FLOCKS = {
    "liviano": {"liviano": 1.0},
    "estándar": {"estándar": 1.0},
    "pesado": {"pesado": 1.0},
    "mezcla-real": {"liviano": 0.3, "estándar": 0.5, "pesado": 0.2},
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke run de perfiles de pollo")
    parser.add_argument("--workers", type=int, default=1, help="procesos paralelos para GA-SA")
    parser.add_argument("--time-limit", type=int, default=60, help="límite CBC (s)")
    args = parser.parse_args()

    gen = InstanceGenerator()
    instances = {
        label: gen.generate("small", seed=42, flock_mix=mix, flock_label=label)
        for label, mix in FLOCKS.items()
    }

    print("=" * 78)
    print("  SMOKE RUN — perfiles de pollo en el pipeline (instancia small, seed 42)")
    print("=" * 78)
    print(f"{'Parvada':<14}{'Peso(kg)':>10}{'Pechuga α':>12}{'Masa/carc(kg)':>16}")
    print("-" * 52)
    for label, inst in instances.items():
        print(f"{label:<14}{inst.weight:>10.3f}{inst.alpha[0]:>12.4f}{inst.weight:>16.3f}")

    # --- Fase 1: CBC exacto por parvada (secuencial, llena el caché de gap) ---
    z_cbc: dict[str, float] = {}
    print("\n[1/3] CBC exacto por parvada...")
    for label, inst in instances.items():
        payload = _run_single("cbc_exact", {"params": {"time_limit": args.time_limit}},
                              inst, seed=42, time_limit=args.time_limit, z_cbc_cache=z_cbc)
        print(f"  {label:<14} Z_CBC = {payload.row['z_value']:>16,.0f}  "
              f"inv = {payload.row['avg_inventory']:>10,.1f}  t={payload.row['elapsed_seconds']:.1f}s")

    # --- Fase 2: baseline por parvada ---
    print("\n[2/3] Baseline (max-capacidad) por parvada...")
    base_rows = {}
    for label, inst in instances.items():
        payload = _run_single("baseline", {"params": {"strategy": "best"}},
                              inst, seed=42, time_limit=args.time_limit, z_cbc_cache=z_cbc)
        base_rows[label] = payload.row

    # --- Fase 3: GA-SA por parvada (en paralelo) ---
    print(f"\n[3/3] GA-SA por parvada (workers={args.workers})...")
    t0 = time.time()
    gasa_rows = {}
    algo_cfg = {"params": GA_SA_PARAMS}
    if args.workers > 1:
        cache_snap = dict(z_cbc)
        with cf.ProcessPoolExecutor(max_workers=args.workers) as pool:
            fut = {
                pool.submit(_run_single, "ga_sa", algo_cfg, inst, 42, args.time_limit, cache_snap): label
                for label, inst in instances.items()
            }
            for f in cf.as_completed(fut):
                gasa_rows[fut[f]] = f.result().row
    else:
        for label, inst in instances.items():
            gasa_rows[label] = _run_single(
                "ga_sa", algo_cfg, inst, 42, args.time_limit, z_cbc
            ).row
    print(f"  GA-SA completado en {time.time() - t0:.1f}s")

    # --- Comparación ---
    print("\n" + "=" * 78)
    print("  RESULTADOS POR PARVADA")
    print("=" * 78)
    print(f"{'Parvada':<14}{'Algoritmo':<10}{'Z':>16}{'gap%':>9}{'inv medio':>12}{'servicio%':>11}")
    print("-" * 72)
    for label in instances:
        c = base_rows[label]
        print(f"{label:<14}{'baseline':<10}{c['z_value']:>16,.0f}"
              f"{c['gap_percent']:>9.2f}{c['avg_inventory']:>12,.1f}{c['service_level']:>11.1f}")
        g = gasa_rows[label]
        print(f"{'':<14}{'ga_sa':<10}{g['z_value']:>16,.0f}"
              f"{g['gap_percent']:>9.2f}{g['avg_inventory']:>12,.1f}{g['service_level']:>11.1f}")

    print("\nLectura: al aumentar el peso del ave, la masa por carcasa y por tanto")
    print("Z crecen; el rendimiento de pechuga sube con el perfil pesado. El gap vs")
    print("CBC y el inventario permiten ver si el balance óptimo cambia con la parvada.")


if __name__ == "__main__":
    main()
