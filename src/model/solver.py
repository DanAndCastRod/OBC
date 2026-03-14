"""
Exact MILP solver for coproduct optimization.

Implemented with PuLP and supports CBC (default), HiGHS and Gurobi.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Optional

import numpy as np
import pulp

if TYPE_CHECKING:
    from src.model.parameters import ProblemInstance

from src.model.solution import Solution


class SolverStatus(Enum):
    """Solver status."""

    OPTIMAL = "optimal"
    FEASIBLE = "feasible"
    INFEASIBLE = "infeasible"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class SolverResult:
    """Complete solver result."""

    solution: Optional[Solution]
    status: SolverStatus
    objective_value: float
    gap: float
    elapsed_seconds: float
    solver_name: str
    n_variables: int = 0
    n_constraints: int = 0

    def __repr__(self) -> str:
        gap_repr = f"{self.gap:.4f}" if np.isfinite(self.gap) else "nan"
        return (
            f"SolverResult(status={self.status.value}, "
            f"Z={self.objective_value:,.0f}, gap={gap_repr}, "
            f"time={self.elapsed_seconds:.2f}s, solver={self.solver_name})"
        )


def solve_exact(
    instance: ProblemInstance,
    time_limit: int = 300,
    solver: str = "cbc",
    verbose: bool = False,
) -> SolverResult:
    """Solve a problem instance exactly with MILP."""
    start_time = time.time()

    validation_errors = instance.validate()
    if validation_errors:
        raise ValueError(
            "Invalid instance:\n" + "\n".join(f"  - {e}" for e in validation_errors)
        )

    f_count = instance.n_cut_forms
    t_count = instance.n_periods
    w_count = instance.n_scenarios
    a_count = instance.n_parts
    pi = instance.scenario_probs

    # Upper bound helper for production activation constraints
    alpha_f = instance.composition.astype(np.float64) @ instance.alpha

    model = pulp.LpProblem("Coproductos_MILP", pulp.LpMaximize)

    # --- First-stage variables ---
    y = pulp.LpVariable.dicts("y", range(t_count), cat=pulp.LpBinary)
    q = pulp.LpVariable.dicts("q", range(t_count), lowBound=0, cat=pulp.LpInteger)
    p = pulp.LpVariable.dicts(
        "p",
        ((f, t) for f in range(f_count) for t in range(t_count)),
        lowBound=0,
        cat=pulp.LpContinuous,
    )

    z_vars = None
    if instance.cut_config is None:
        z_vars = pulp.LpVariable.dicts(
            "z",
            ((f, t) for f in range(f_count) for t in range(t_count)),
            cat=pulp.LpBinary,
        )

    # --- Second-stage variables (scenario-dependent) ---
    v = pulp.LpVariable.dicts(
        "v",
        (
            (f, t, w)
            for f in range(f_count)
            for t in range(t_count)
            for w in range(w_count)
        ),
        lowBound=0,
        cat=pulp.LpContinuous,
    )
    I = pulp.LpVariable.dicts(
        "I",
        (
            (f, t, w)
            for f in range(f_count)
            for t in range(t_count)
            for w in range(w_count)
        ),
        lowBound=0,
        cat=pulp.LpContinuous,
    )
    u = pulp.LpVariable.dicts(
        "u",
        (
            (f, t, w)
            for f in range(f_count)
            for t in range(t_count)
            for w in range(w_count)
        ),
        lowBound=0,
        cat=pulp.LpContinuous,
    )

    # ================================================================
    # Objective (Eq. 1)
    # ================================================================
    model += (
        pulp.lpSum(
            pi[w]
            * (
                pulp.lpSum(
                    instance.prices[f] * v[(f, t, w)]
                    - instance.cost_inv[f] * I[(f, t, w)]
                    - instance.cost_pen[f] * u[(f, t, w)]
                    for f in range(f_count)
                )
                - instance.cost_prod * q[t]
                - instance.cost_setup * y[t]
            )
            for w in range(w_count)
            for t in range(t_count)
        ),
        "Objective",
    )

    # ================================================================
    # Core constraints (Eqs. 2-6)
    # ================================================================
    for w in range(w_count):
        for t in range(t_count):
            for f in range(f_count):
                i_prev = I[(f, t - 1, w)] if t > 0 else 0

                # Eq. 2: Material balance
                model += (
                    I[(f, t, w)] == i_prev + p[(f, t)] - v[(f, t, w)],
                    f"Balance_f{f}_t{t}_w{w}",
                )

                # Eq. 3: Demand satisfaction
                model += (
                    v[(f, t, w)] + u[(f, t, w)] == instance.demand[f, t, w],
                    f"Demand_f{f}_t{t}_w{w}",
                )

                # Eq. 6: Sales limit
                model += (
                    v[(f, t, w)] <= i_prev + p[(f, t)],
                    f"SalesLimit_f{f}_t{t}_w{w}",
                )

    for t in range(t_count):
        # Eq. 4: Maximum capacity
        model += (q[t] <= instance.capacity_max * y[t], f"CapMax_t{t}")
        # Eq. 5: Minimum lot
        model += (q[t] >= instance.capacity_min * y[t], f"CapMin_t{t}")

    # ================================================================
    # Structural controls: part allocation and cut activation
    # ================================================================
    # Anatomical part allocation:
    # sum_f composition[f,a] * p[f,t] <= alpha[a] * weight * q[t]
    for t in range(t_count):
        for a in range(a_count):
            model += (
                pulp.lpSum(
                    instance.composition[f, a] * p[(f, t)] for f in range(f_count)
                )
                <= instance.alpha[a] * instance.weight * q[t],
                f"PartAlloc_a{a}_t{t}",
            )

    # p[f,t] activation by z[f,t] (or fixed cut_config) and setup y[t]
    for f in range(f_count):
        m_f = float(max(0.0, alpha_f[f] * instance.weight * instance.capacity_max))
        for t in range(t_count):
            z_ft = z_vars[(f, t)] if z_vars is not None else int(instance.cut_config[f])
            model += (p[(f, t)] <= m_f * z_ft, f"ProdActivation_f{f}_t{t}")
            model += (p[(f, t)] <= m_f * y[t], f"ProdSetupLink_f{f}_t{t}")

    # Exclusivity groups: at most one active form in each group per period
    if z_vars is not None:
        for t in range(t_count):
            for g_idx, group in enumerate(instance.exclusivity_groups):
                if len(group.cut_form_indices) <= 1:
                    continue
                model += (
                    pulp.lpSum(z_vars[(f, t)] for f in group.cut_form_indices) <= 1,
                    f"Excl_g{g_idx}_t{t}",
                )

    # ================================================================
    # Eq. 7 Perishability (linear, no big-M)
    # ================================================================
    # Inventory at (f,t,w) cannot exceed cumulative production in last L[f] periods.
    for w in range(w_count):
        for f in range(f_count):
            l_f = int(instance.shelf_life[f])
            for t in range(t_count):
                start = max(0, t - l_f + 1)
                model += (
                    I[(f, t, w)] <= pulp.lpSum(p[(f, s)] for s in range(start, t + 1)),
                    f"Perish_f{f}_t{t}_w{w}",
                )

    n_vars = model.numVariables()
    n_cons = model.numConstraints()

    # ================================================================
    # Solve
    # ================================================================
    if solver.lower() == "highs":
        pulp_solver = pulp.HiGHS_CMD(msg=int(verbose), timeLimit=time_limit)
    elif solver.lower() == "gurobi":
        pulp_solver = pulp.GUROBI_CMD(msg=int(verbose), timeLimit=time_limit)
    else:
        pulp_solver = pulp.PULP_CBC_CMD(msg=int(verbose), timeLimit=time_limit)

    model.solve(pulp_solver)
    elapsed = time.time() - start_time

    # ================================================================
    # Extract solution and status
    # ================================================================
    pulp_status = pulp.LpStatus.get(model.status, "Unknown")
    obj_raw = pulp.value(model.objective)
    has_incumbent = obj_raw is not None and np.isfinite(float(obj_raw))

    if pulp_status == "Optimal":
        status = SolverStatus.OPTIMAL
    elif pulp_status == "Infeasible":
        status = SolverStatus.INFEASIBLE
    elif pulp_status == "Not Solved":
        status = SolverStatus.TIMEOUT
    elif has_incumbent:
        status = SolverStatus.FEASIBLE
    else:
        status = SolverStatus.ERROR

    sol: Optional[Solution]
    obj_val: float
    if has_incumbent and status in (
        SolverStatus.OPTIMAL,
        SolverStatus.FEASIBLE,
        SolverStatus.TIMEOUT,
    ):
        y_val = np.array(
            [bool(round(y[t].varValue or 0.0)) for t in range(t_count)], dtype=bool
        )
        q_val = np.array(
            [int(round(q[t].varValue or 0.0)) for t in range(t_count)], dtype=np.int64
        )
        p_val = np.zeros((f_count, t_count), dtype=np.float64)
        for f in range(f_count):
            for t in range(t_count):
                p_val[f, t] = float(p[(f, t)].varValue or 0.0)

        z_val = np.zeros((f_count, t_count), dtype=bool)
        if z_vars is None:
            z_val[:, :] = np.tile(
                instance.cut_config.astype(bool)[:, np.newaxis], (1, t_count)
            )
        else:
            for f in range(f_count):
                for t in range(t_count):
                    z_val[f, t] = bool(round(z_vars[(f, t)].varValue or 0.0))

        v_val = np.zeros((f_count, t_count, w_count), dtype=np.float64)
        i_val = np.zeros((f_count, t_count, w_count), dtype=np.float64)
        u_val = np.zeros((f_count, t_count, w_count), dtype=np.float64)
        for f in range(f_count):
            for t in range(t_count):
                for w in range(w_count):
                    v_val[f, t, w] = float(v[(f, t, w)].varValue or 0.0)
                    i_val[f, t, w] = float(I[(f, t, w)].varValue or 0.0)
                    u_val[f, t, w] = float(u[(f, t, w)].varValue or 0.0)

        obj_val = float(obj_raw)
        sol = Solution(
            y=y_val,
            q=q_val,
            p=p_val,
            z=z_val,
            v=v_val,
            I=i_val,
            u=u_val,
            objective_value=obj_val,
            algorithm=f"exact_{solver.lower()}",
            elapsed_seconds=elapsed,
            is_feasible=True,
        )
    else:
        sol = None
        obj_val = float(obj_raw) if has_incumbent else 0.0

    gap = 0.0 if status == SolverStatus.OPTIMAL else float("nan")

    return SolverResult(
        solution=sol,
        status=status,
        objective_value=obj_val,
        gap=gap,
        elapsed_seconds=elapsed,
        solver_name=solver.lower(),
        n_variables=n_vars,
        n_constraints=n_cons,
    )
