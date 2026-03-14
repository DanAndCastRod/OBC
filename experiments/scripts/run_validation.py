"""
Sprint 5.1 — Validación operativa, robustez y visualizaciones.

Genera:
  - experiments/results/validation/fig_qt_per_period.png
  - experiments/results/validation/fig_sales_stacked.png
  - experiments/results/validation/fig_inventory_shelf_life.png
  - documentacion/reportes/reporte_validacion.md

Uso:
    python experiments/scripts/run_validation.py
    python experiments/scripts/run_validation.py --instance medium_seed42 --seed 1

Autor: Daniel Andrés Castañeda Rodríguez
Sprint: 5.1
"""

from __future__ import annotations

import argparse
import copy
import random
import sys
import textwrap
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, ".")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import yaml

from src.metaheuristics.ga_sa import HybridGASA
from src.model import decoder, objective
from src.model.parameters import ProblemInstance
from src.model.solution import Solution

# ============================================================
# Paths
# ============================================================
OUT_DIR = Path("experiments/results/validation")
REPORT_PATH = Path("documentacion/reportes/reporte_validacion.md")
COMPARISON_CFG = Path("experiments/config/comparison.yaml")

# ============================================================
# Style
# ============================================================
COLORS = [
    "#008B8B",
    "#EB8A3E",
    "#365660",
    "#2196F3",
    "#9C27B0",
    "#4CAF50",
    "#FF5722",
    "#795548",
]


def _load_ga_sa_config() -> dict:
    """Load calibrated GA-SA params from comparison.yaml."""
    with open(COMPARISON_CFG, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return dict(cfg["algorithms"]["ga_sa"]["params"])


def _load_instance(name: str) -> ProblemInstance:
    """Load a named instance from data/instances/."""
    p = Path(f"data/instances/{name}.yaml")
    if not p.exists():
        raise FileNotFoundError(f"Instancia no encontrada: {p}")
    return ProblemInstance.from_yaml(p)


def _run_ga_sa(instance: ProblemInstance, seed: int) -> Solution:
    """Execute GA-SA with calibrated params and fixed seed."""
    np.random.seed(seed)
    random.seed(seed)
    params = _load_ga_sa_config()
    mh = HybridGASA(params)
    sol = mh.solve(instance)
    return sol


# ============================================================
# 1. Operational Validation
# ============================================================
def validate_operational(sol: Solution, instance: ProblemInstance) -> dict:
    """Check that the production plan is realistic."""
    diag: dict = {}

    # --- q_t variation ---
    q = sol.q.astype(float)
    mean_q = q.mean()
    std_q = q.std()
    cv_q = std_q / mean_q if mean_q > 0 else 0.0
    diag["q_mean"] = float(mean_q)
    diag["q_std"] = float(std_q)
    diag["q_cv"] = float(cv_q)
    diag["q_reasonable"] = cv_q > 0.05  # not constant

    # --- Inventory accumulation ---
    # Average inventory over scenarios per period: I_avg[t] = mean over w,f of I[f,t,w]
    I_per_period = sol.I.sum(axis=(0, 2)) / instance.n_scenarios  # [T]
    first_half = I_per_period[: len(I_per_period) // 2].mean()
    second_half = I_per_period[len(I_per_period) // 2 :].mean()
    diag["inv_first_half_avg"] = float(first_half)
    diag["inv_second_half_avg"] = float(second_half)
    diag["inv_accumulates"] = second_half > first_half * 2.0  # flag if doubles

    # --- Setup economics ---
    bd = sol.breakdown
    n_setups = int(sol.y.sum())
    revenue_per_setup = bd.revenue / max(n_setups, 1)
    diag["n_setups"] = n_setups
    diag["cost_setup_per_day"] = float(instance.cost_setup)
    diag["revenue_per_setup"] = float(revenue_per_setup)
    diag["setup_economically_rational"] = revenue_per_setup > instance.cost_setup

    # --- Feasibility ---
    violations = sol.check_feasibility(instance)
    diag["n_violations"] = len(violations)
    diag["violations"] = violations
    diag["is_feasible"] = len(violations) == 0

    return diag


# ============================================================
# 2. Visualizations
# ============================================================
def plot_qt_per_period(sol: Solution, instance: ProblemInstance, out: Path) -> None:
    """Figura X1: Bar chart of q_t by period."""
    T = sol.n_periods
    fig, ax = plt.subplots(figsize=(10, 4))

    colors = [COLORS[0] if sol.y[t] else "#cccccc" for t in range(T)]
    ax.bar(range(T), sol.q, color=colors, edgecolor="white", linewidth=0.5)

    # Reference lines
    ax.axhline(
        instance.capacity_max,
        color="#e74c3c",
        ls="--",
        lw=1,
        label=f"Q_max={instance.capacity_max:,}",
    )
    ax.axhline(
        instance.capacity_min,
        color="#f39c12",
        ls="--",
        lw=1,
        label=f"Q_min={instance.capacity_min:,}",
    )
    ax.axhline(
        sol.q.mean(),
        color=COLORS[1],
        ls=":",
        lw=1.5,
        label=f"Promedio={sol.q.mean():,.0f}",
    )

    ax.set_xlabel("Periodo (t)", fontsize=11)
    ax.set_ylabel("Carcasas producidas (q_t)", fontsize=11)
    ax.set_title(
        f"Producción por periodo — {instance.name}", fontsize=13, fontweight="bold"
    )
    ax.legend(fontsize=9)
    ax.set_xlim(-0.5, T - 0.5)
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out}")


def plot_sales_stacked(sol: Solution, instance: ProblemInstance, out: Path) -> None:
    """Figura X2: Stacked bar chart of sales per coproduct per period."""
    T = instance.n_periods
    F = instance.n_cut_forms

    # Average sales over scenarios: v_avg[f, t]
    v_avg = sol.v.mean(axis=2)  # [F, T]

    fig, ax = plt.subplots(figsize=(10, 5))
    bottom = np.zeros(T)
    for f in range(F):
        ax.bar(
            range(T),
            v_avg[f],
            bottom=bottom,
            color=COLORS[f % len(COLORS)],
            label=instance.cut_form_names[f],
            edgecolor="white",
            linewidth=0.3,
        )
        bottom += v_avg[f]

    ax.set_xlabel("Periodo (t)", fontsize=11)
    ax.set_ylabel("Ventas promedio (kg)", fontsize=11)
    ax.set_title(
        f"Ventas por coproducto — {instance.name}", fontsize=13, fontweight="bold"
    )
    ax.legend(fontsize=8, bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0)
    ax.set_xlim(-0.5, T - 0.5)
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out}")


def plot_inventory_shelf_life(
    sol: Solution, instance: ProblemInstance, out: Path
) -> None:
    """Figura X3: Inventory per coproduct with shelf-life reference."""
    T = instance.n_periods
    F = instance.n_cut_forms

    # Average inventory over scenarios: I_avg[f, t]
    I_avg = sol.I.mean(axis=2)  # [F, T]

    fig, ax = plt.subplots(figsize=(10, 5))
    for f in range(F):
        ax.plot(
            range(T),
            I_avg[f],
            color=COLORS[f % len(COLORS)],
            linewidth=1.5,
            marker="o",
            markersize=3,
            label=f"{instance.cut_form_names[f]} (L={int(instance.shelf_life[f])}d)",
        )

    # Add shelf-life annotations: vertical dashed lines per product
    for f in range(F):
        L = int(instance.shelf_life[f])
        if L < T:
            ax.axvline(L, color=COLORS[f % len(COLORS)], ls=":", alpha=0.4, lw=1)

    ax.set_xlabel("Periodo (t)", fontsize=11)
    ax.set_ylabel("Inventario promedio (kg)", fontsize=11)
    ax.set_title(
        f"Inventario vs vida útil — {instance.name}", fontsize=13, fontweight="bold"
    )
    ax.legend(fontsize=8, bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0)
    ax.set_xlim(-0.5, T - 0.5)
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out}")


# ============================================================
# 3. Robustness Analysis
# ============================================================
def analyze_robustness(
    sol: Solution, instance: ProblemInstance, perturbations: list[float] | None = None
) -> list[dict]:
    """Perturb demand ±delta%, re-evaluate solution (without re-optimization)."""
    if perturbations is None:
        perturbations = [-0.10, 0.0, +0.10]

    # Original Z
    bd_orig = objective.evaluate_vectorized(sol, instance)
    z_orig = bd_orig.total

    results = []
    for delta in perturbations:
        # Deep-copy instance and perturb demand
        inst_p = copy.deepcopy(instance)
        rng = np.random.RandomState(42)
        noise = 1.0 + delta * (2 * rng.random(inst_p.demand.shape) - 1)
        inst_p.demand = np.maximum(inst_p.demand * noise, 0.0)

        # Re-decode with same y, q
        sol_p = decoder.decode(sol.y.copy(), sol.q.copy(), inst_p)
        bd_p = objective.evaluate_vectorized(sol_p, inst_p)

        violations = sol_p.check_feasibility(inst_p)

        z_new = bd_p.total
        pct_change = (
            ((z_new - z_orig) / abs(z_orig) * 100) if abs(z_orig) > 1e-9 else 0.0
        )

        results.append(
            {
                "delta_pct": delta * 100,
                "z_original": z_orig,
                "z_perturbed": z_new,
                "z_change_pct": pct_change,
                "is_feasible": len(violations) == 0,
                "n_violations": len(violations),
            }
        )

    return results


# ============================================================
# 4. Report Generation
# ============================================================
def generate_report(
    instance: ProblemInstance,
    sol: Solution,
    diag: dict,
    robustness: list[dict],
    seed: int,
    elapsed: float,
    out_dir: Path,
) -> str:
    """Generate Markdown validation report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Robustness table rows
    rob_rows = ""
    for r in robustness:
        status = "✅ Sí" if r["is_feasible"] else "❌ No"
        z_chg = f"{r['z_change_pct']:+.2f}%"
        rob_rows += (
            f"| {r['delta_pct']:+.0f}% | {r['z_original']:,.0f} | "
            f"{r['z_perturbed']:,.0f} | {z_chg} | {status} |\n"
        )

    # Max deterioration
    max_deterioration = max(
        abs(r["z_change_pct"]) for r in robustness if r["delta_pct"] != 0
    )
    robust_verdict = "✅ Sí" if max_deterioration < 5.0 else "⚠️ No"

    md = textwrap.dedent(f"""\
    # Reporte de Validación — Sprint 5.1

    > **Generado:** {now}
    > **Instancia:** `{instance.name}` | **Seed:** {seed}
    > **Algoritmo:** GA-SA (híbrido) | **Tiempo:** {elapsed:.1f}s

    ---

    ## 1. Resumen de la Solución

    | Métrica | Valor |
    |---|---|
    | Z (objetivo) | {sol.objective_value:,.0f} COP |
    | Ingresos | {sol.breakdown.revenue:,.0f} COP |
    | Costo producción | {sol.breakdown.prod_cost:,.0f} COP |
    | Costo setup | {sol.breakdown.setup_cost:,.0f} COP |
    | Costo inventario | {sol.breakdown.inv_cost:,.0f} COP |
    | Penalización | {sol.breakdown.pen_cost:,.0f} COP |
    | Periodos | {sol.n_periods} |
    | Setups | {diag["n_setups"]} / {sol.n_periods} |
    | Producción total | {sol.total_production:,} carcasas |
    | Factible | {"✅ Sí" if diag["is_feasible"] else "❌ No"} |

    ---

    ## 2. Diagnósticos Operativos

    ### 2.1. Variación de Producción

    | Indicador | Valor | Veredicto |
    |---|---|---|
    | q promedio | {diag["q_mean"]:,.0f} carcasas/día | — |
    | q desv. estándar | {diag["q_std"]:,.0f} | — |
    | Coef. variación (CV) | {diag["q_cv"]:.3f} | {"✅ Razonable" if diag["q_reasonable"] else "⚠️ Muy constante"} |

    ### 2.2. Acumulación de Inventario

    | Indicador | Valor |
    |---|---|
    | Inv. promedio (primera mitad) | {diag["inv_first_half_avg"]:,.1f} |
    | Inv. promedio (segunda mitad) | {diag["inv_second_half_avg"]:,.1f} |
    | ¿Se acumula indefinidamente? | {"⚠️ Sí" if diag["inv_accumulates"] else "✅ No"} |

    ### 2.3. Racionalidad Económica de Setups

    | Indicador | Valor |
    |---|---|
    | Costo de setup (F) | {diag["cost_setup_per_day"]:,.0f} COP/día |
    | Ingreso por setup | {diag["revenue_per_setup"]:,.0f} COP |
    | ¿Setup económicamente racional? | {"✅ Sí" if diag["setup_economically_rational"] else "⚠️ No"} |

    ### 2.4. Factibilidad

    - Violaciones encontradas: **{diag["n_violations"]}**
    {chr(10).join(f"  - {v}" for v in diag["violations"]) if diag["violations"] else "  - Ninguna"}

    ---

    ## 3. Análisis de Robustez

    Se perturba la demanda uniformemente en ±δ% y se re-evalúa la solución **sin re-optimizar**.

    | Perturbación | Z Original | Z Perturbado | Δ Z | ¿Factible? |
    |---|---|---|---|---|
    {rob_rows}
    - **Máximo deterioro:** {max_deterioration:.2f}%
    - **¿Deterioro < 5%?** {robust_verdict}

    ---

    ## 4. Figuras

    ### Figura X1 — Producción por periodo ($q_t$)
    ![Producción por periodo](../../experiments/results/validation/fig_qt_per_period.png)

    ### Figura X2 — Ventas por coproducto (apilado)
    ![Ventas por coproducto](../../experiments/results/validation/fig_sales_stacked.png)

    ### Figura X3 — Inventario vs vida útil
    ![Inventario vs vida útil](../../experiments/results/validation/fig_inventory_shelf_life.png)

    ---

    ## 5. Conclusión

    La solución GA-SA para `{instance.name}`:
    - {"✅" if diag["is_feasible"] else "❌"} Cumple todas las restricciones del modelo
    - {"✅" if diag["q_reasonable"] else "⚠️"} Producción varía razonablemente entre periodos
    - {"✅" if not diag["inv_accumulates"] else "⚠️"} Inventario no se acumula indefinidamente
    - {"✅" if diag["setup_economically_rational"] else "⚠️"} Setups son económicamente racionales
    - {robust_verdict} Solución es robusta ante perturbaciones de ±10% en demanda
    """)

    return md


# ============================================================
# Main
# ============================================================
def main() -> None:
    parser = argparse.ArgumentParser(description="Sprint 5.1 — Validación operativa")
    parser.add_argument(
        "--instance", default="medium_seed42", help="Nombre de instancia (sin .yaml)"
    )
    parser.add_argument("--seed", type=int, default=1, help="Seed para GA-SA")
    args = parser.parse_args()

    print("=" * 60)
    print("  Sprint 5.1 — Validación Final y Reproducibilidad")
    print("=" * 60)

    # Load instance
    print(f"\n[1/5] Cargando instancia {args.instance}...")
    instance = _load_instance(args.instance)
    print(f"  ✓ {instance.summary()}")

    # Run GA-SA
    print(f"\n[2/5] Ejecutando GA-SA (seed={args.seed})...")
    t0 = time.time()
    sol = _run_ga_sa(instance, args.seed)
    elapsed = time.time() - t0
    print(f"  ✓ Z = {sol.objective_value:,.0f} COP en {elapsed:.1f}s")
    print(f"  {sol.breakdown}")

    # Operational validation
    print("\n[3/5] Validación operativa...")
    diag = validate_operational(sol, instance)
    print(
        f"  q: mean={diag['q_mean']:,.0f}, std={diag['q_std']:,.0f}, CV={diag['q_cv']:.3f}"
    )
    print(
        f"  Setups: {diag['n_setups']}/{sol.n_periods}, rev/setup={diag['revenue_per_setup']:,.0f}"
    )
    print(f"  Inventario acumula: {diag['inv_accumulates']}")
    print(f"  Factible: {diag['is_feasible']} ({diag['n_violations']} violaciones)")

    # Visualizations
    print("\n[4/5] Generando visualizaciones...")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    plot_qt_per_period(sol, instance, OUT_DIR / "fig_qt_per_period.png")
    plot_sales_stacked(sol, instance, OUT_DIR / "fig_sales_stacked.png")
    plot_inventory_shelf_life(sol, instance, OUT_DIR / "fig_inventory_shelf_life.png")

    # Robustness
    print("\n[5/5] Análisis de robustez...")
    robustness = analyze_robustness(sol, instance, perturbations=[-0.10, 0.0, +0.10])
    for r in robustness:
        status = "✓" if r["is_feasible"] else "✗"
        print(
            f"  δ={r['delta_pct']:+.0f}%: Z={r['z_perturbed']:,.0f} "
            f"(Δ={r['z_change_pct']:+.2f}%) [{status}]"
        )

    # Generate report
    report = generate_report(
        instance, sol, diag, robustness, args.seed, elapsed, OUT_DIR
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"\n  ✓ Reporte: {REPORT_PATH}")

    print("\n" + "=" * 60)
    print("  ✓ Validación completada exitosamente")
    print("=" * 60)


if __name__ == "__main__":
    main()
