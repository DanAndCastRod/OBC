"""
Generador del set de instancias v2 (diseño experimental revisado).

Diferencias deliberadas frente al set v1 (data/instances/):

1. **Las decisiones de setup importan.** En v1 la demanda excedía la oferta
   (nivel de servicio ~56%) y el costo de setup (500k COP/día) era ~1% del
   margen diario: producir a tope todos los días era casi óptimo y el baseline
   trivial empataba con el óptimo. En v2 la capacidad tiene holgura
   (cap_max 10,000–12,000), el setup cuesta 50M COP/día y la demanda es
   volátil (amplitud 0.35): el óptimo apaga la línea algunos días y el
   baseline queda 10–11% por debajo (validado con CBC en la exploración del
   2026-07-10: mejora GA-SA vs baseline +5.2% a +7.6%).
2. **Medium se diferencia estructuralmente de small** (en v1 `medium()`
   retornaba el mismo catálogo que small): aquí medium usa 18 periodos
   (vs 12) además de 50 escenarios.
3. **Más instancias, menos seeds.** La unidad estadística es la instancia:
   v2 trae 10 instancias por tamaño (30 en total) pensadas para ~6 réplicas,
   en lugar de 3 instancias × 30 réplicas.
4. **Parvada mixta realista**: 30% liviano / 50% estándar / 20% pesado.

Uso:
    python experiments/scripts/generate_instances_v2.py [--validate]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, ".")

import numpy as np

from src.instances.generator import InstanceGenerator

OUTPUT_DIR = Path("data/instances_v2")
SEEDS = list(range(201, 211))  # 10 instancias por tamano
MEZCLA = {"liviano": 0.3, "estándar": 0.5, "pesado": 0.2}

# Economia v2 validada (exploracion 2026-07-10)
SETUP_COST = 50_000_000.0  # COP/dia

SIZE_SPECS = {
    "small": dict(capacity_max=10_000, capacity_min=2_000),
    "medium": dict(capacity_max=10_000, capacity_min=2_000, n_periods=18),
    "large": dict(capacity_max=12_000, capacity_min=2_400),
}


def generate_all() -> list[Path]:
    gen = InstanceGenerator()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    for size, spec in SIZE_SPECS.items():
        for seed in SEEDS:
            inst = gen.generate(
                size_profile=size,
                demand_profile="volatile",
                seed=seed,
                cost_setup=SETUP_COST,
                flock_mix=MEZCLA,
                flock_label="v2",
                **spec,
            )
            path = OUTPUT_DIR / f"{inst.name}.yaml"
            inst.to_yaml(path)
            paths.append(path)
            print(f"  {path}  (T={inst.n_periods}, W={inst.n_scenarios}, "
                  f"cap={inst.capacity_max}, setup={inst.cost_setup:,.0f})")
    return paths


def validate_sample() -> None:
    """Validar con CBC que el diseño logra lo que promete (1 por tamaño)."""
    from experiments.scripts.baseline import solve_baseline
    from src.model.parameters import ProblemInstance
    from src.model.solver import solve_exact

    print("\nValidación con CBC (1 instancia por tamaño):")
    for size in SIZE_SPECS:
        path = OUTPUT_DIR / f"{size}_v2_seed201.yaml"
        inst = ProblemInstance.from_yaml(path)
        res = solve_exact(inst, time_limit=300)
        z_base = solve_baseline(inst, "best", demand_cap=True).objective_value
        gap_base = (
            (res.objective_value - z_base) / abs(res.objective_value) * 100
            if res.objective_value
            else float("nan")
        )
        days_off = (
            int(np.sum(~res.solution.y)) if res.solution is not None else -1
        )
        print(
            f"  {size:<8} CBC={res.status.value:<8} t={res.elapsed_seconds:>6.1f}s "
            f"Z={res.objective_value:>16,.0f} dias_off={days_off} "
            f"gap_baseline={gap_base:.2f}%"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generar instancias v2")
    parser.add_argument("--validate", action="store_true",
                        help="resolver 1 instancia por tamaño con CBC y "
                             "verificar que el setup importa")
    args = parser.parse_args()

    print(f"Generando {len(SEEDS) * len(SIZE_SPECS)} instancias en {OUTPUT_DIR}/")
    generate_all()
    if args.validate:
        validate_sample()


if __name__ == "__main__":
    main()
