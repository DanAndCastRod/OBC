"""
CLI de decisión de despiece: dado un lote de pollo (perfiles + cantidades) y un
mix comercial (pedidos + precios), calcula el plan de despiece óptimo.

Ejemplos:
    # Lote de 10.000 pollos estándar, catálogo y demanda por defecto
    python experiments/scripts/despiece_decision.py --carcasas 10000

    # Mezcla de parvada: 30% liviano, 50% estándar, 20% pesado
    python experiments/scripts/despiece_decision.py --carcasas 10000 \
        --mezcla liviano=0.3,estándar=0.5,pesado=0.2

    # Con pedidos (demanda en kg) por corte
    python experiments/scripts/despiece_decision.py --carcasas 10000 \
        --demanda "Pechuga=6000,Pernil completo=4000,Ala=1500"

Compara además, para el mismo lote, cada perfil puro para ilustrar cómo el
peso/rendimiento del ave cambia el balance óptimo de despresado.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Salida en UTF-8 para acentos y '×' en consolas Windows (cp1252)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.planning import (  # noqa: E402
    FlockMix,
    PERFILES_ESTANDAR,
    catalogo_despiece_default,
    optimizar_despiece,
)


def _parse_kv(texto: str) -> dict[str, float]:
    out: dict[str, float] = {}
    for par in texto.split(","):
        par = par.strip()
        if not par:
            continue
        clave, _, valor = par.partition("=")
        out[clave.strip()] = float(valor)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Decisión de despiece óptimo por lote")
    parser.add_argument("--carcasas", type=float, default=10000, help="número de carcasas del lote")
    parser.add_argument(
        "--mezcla",
        type=str,
        default=None,
        help="fracciones por perfil, p.ej. 'liviano=0.3,estándar=0.5,pesado=0.2'. "
        "Por defecto: 100%% estándar.",
    )
    parser.add_argument(
        "--demanda",
        type=str,
        default=None,
        help="demanda (kg) por corte, p.ej. 'Pechuga=6000,Ala=1500'. Sin tope si se omite.",
    )
    parser.add_argument("--solver", type=str, default="cbc", choices=["cbc", "highs", "gurobi"])
    args = parser.parse_args()

    if args.mezcla:
        flock = FlockMix.from_fractions(args.carcasas, _parse_kv(args.mezcla))
    else:
        flock = FlockMix.single(PERFILES_ESTANDAR["estándar"], args.carcasas)

    items = catalogo_despiece_default()
    if args.demanda:
        dem = _parse_kv(args.demanda)
        for it in items:
            if it.name in dem:
                it.demand_kg = dem[it.name]

    print("=" * 63)
    print("  DECISIÓN DE DESPIECE — plan óptimo del lote")
    print("=" * 63)
    perfiles = ", ".join(
        f"{n:.0f}× {p.name} ({p.weight_kg} kg)" for p, n in zip(flock.profiles, flock.counts)
    )
    print(f"  Lote: {flock.total_carcasses:,.0f} carcasas  [{perfiles}]")
    print(f"  Masa total: {flock.part_pool().sum():,.0f} kg\n")

    plan = optimizar_despiece(flock, items, solver=args.solver)
    print(plan.resumen())

    # Comparación por perfil puro (mismo número de carcasas)
    print("\n" + "=" * 63)
    print("  Sensibilidad al perfil del pollo (mismo nº de carcasas)")
    print("=" * 63)
    print(f"{'Perfil':<12}{'Masa(kg)':>12}{'Utilidad(COP)':>18}{'Corte estrella':>18}")
    print("-" * 60)
    for nombre, perfil in PERFILES_ESTANDAR.items():
        f1 = FlockMix.single(perfil, flock.total_carcasses)
        p1 = optimizar_despiece(f1, catalogo_despiece_default(), solver=args.solver)
        estrella = max(p1.sold_kg, key=p1.sold_kg.get)
        print(
            f"{nombre:<12}{f1.part_pool().sum():>12,.0f}"
            f"{p1.profit:>18,.0f}{estrella:>18}"
        )


if __name__ == "__main__":
    main()
