"""
Constraint checker for the MILP model (Eqs. 2-8 + structural controls).

This module validates:
- Core equations (balance, demand, capacity, sales, perishability, domains)
- Part-allocation consistency (no double counting of anatomical mass)
- Exclusivity consistency for cut-form groups
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from src.model.parameters import ProblemInstance
    from src.model.solution import Solution


# CBC returns floating values with small residuals after extraction.
# 1e-3 keeps checks strict at business scale while avoiding false infeasibility.
TOL = 1e-3


@dataclass
class ConstraintResult:
    """Result of a single constraint check."""

    name: str
    satisfied: bool
    violations: list[str] = field(default_factory=list)

    def __repr__(self) -> str:
        status = "OK" if self.satisfied else f"FAIL ({len(self.violations)} violations)"
        return f"{self.name}: {status}"


def check_material_balance(sol: Solution, inst: ProblemInstance) -> ConstraintResult:
    """Eq. 2: Material balance per form, period and scenario.

    I[f,t,w] = I[f,t-1,w] + p[f,t] - v[f,t,w]
    """
    violations = []
    p = _get_production(sol, inst)

    for w in range(inst.n_scenarios):
        for t in range(inst.n_periods):
            for f in range(inst.n_cut_forms):
                i_prev = 0.0 if t == 0 else sol.I[f, t - 1, w]
                expected_i = i_prev + p[f, t] - sol.v[f, t, w]
                actual_i = sol.I[f, t, w]
                if abs(expected_i - actual_i) > TOL:
                    violations.append(
                        f"f={f},t={t},w={w}: I={actual_i:.4f}, expected={expected_i:.4f}"
                    )

    return ConstraintResult("Eq.2 Material balance", len(violations) == 0, violations)


def check_demand_satisfaction(sol: Solution, inst: ProblemInstance) -> ConstraintResult:
    """Eq. 3: Demand satisfaction.

    v[f,t,w] + u[f,t,w] = d[f,t,w]
    """
    violations = []
    for w in range(inst.n_scenarios):
        for t in range(inst.n_periods):
            for f in range(inst.n_cut_forms):
                lhs = sol.v[f, t, w] + sol.u[f, t, w]
                rhs = inst.demand[f, t, w]
                if abs(lhs - rhs) > TOL:
                    violations.append(f"f={f},t={t},w={w}: v+u={lhs:.4f}, d={rhs:.4f}")

    return ConstraintResult(
        "Eq.3 Demand satisfaction", len(violations) == 0, violations
    )


def check_capacity_max(sol: Solution, inst: ProblemInstance) -> ConstraintResult:
    """Eq. 4: Maximum capacity.

    q[t] <= Q_max * y[t]
    """
    violations = []
    for t in range(inst.n_periods):
        limit = inst.capacity_max * int(sol.y[t])
        if sol.q[t] > limit + TOL:
            violations.append(f"t={t}: q={sol.q[t]}, limit={limit} (y={sol.y[t]})")

    return ConstraintResult("Eq.4 Capacity max", len(violations) == 0, violations)


def check_capacity_min(sol: Solution, inst: ProblemInstance) -> ConstraintResult:
    """Eq. 5: Minimum lot.

    q[t] >= Q_min * y[t]
    """
    violations = []
    for t in range(inst.n_periods):
        if sol.y[t] and sol.q[t] < inst.capacity_min - TOL:
            violations.append(f"t={t}: q={sol.q[t]} < Q_min={inst.capacity_min}")

    return ConstraintResult("Eq.5 Capacity min", len(violations) == 0, violations)


def check_sales_limit(sol: Solution, inst: ProblemInstance) -> ConstraintResult:
    """Eq. 6: Sales cannot exceed available stock.

    v[f,t,w] <= I[f,t-1,w] + p[f,t]
    """
    violations = []
    p = _get_production(sol, inst)

    for w in range(inst.n_scenarios):
        for t in range(inst.n_periods):
            for f in range(inst.n_cut_forms):
                i_prev = 0.0 if t == 0 else sol.I[f, t - 1, w]
                available = i_prev + p[f, t]
                if sol.v[f, t, w] > available + TOL:
                    violations.append(
                        f"f={f},t={t},w={w}: v={sol.v[f,t,w]:.4f} > avail={available:.4f}"
                    )

    return ConstraintResult("Eq.6 Sales limit", len(violations) == 0, violations)


def check_perishability(sol: Solution, inst: ProblemInstance) -> ConstraintResult:
    """Eq. 7: Perishability.

    Inventory must be zero after L[f] consecutive periods with no production
    for that specific form.
    """
    violations = []
    p = _get_production(sol, inst)

    for w in range(inst.n_scenarios):
        for f in range(inst.n_cut_forms):
            l_f = int(inst.shelf_life[f])
            consecutive_no_prod = 0
            for t in range(inst.n_periods):
                if p[f, t] > TOL:
                    consecutive_no_prod = 0
                else:
                    consecutive_no_prod += 1

                if consecutive_no_prod >= l_f and sol.I[f, t, w] > TOL:
                    violations.append(
                        f"f={f},t={t},w={w}: I={sol.I[f,t,w]:.4f} > 0 "
                        f"with no production for {l_f} periods"
                    )

    return ConstraintResult("Eq.7 Perishability", len(violations) == 0, violations)


def check_domains(sol: Solution, inst: ProblemInstance) -> ConstraintResult:
    """Eq. 8: Variable domains."""
    violations = []

    for t in range(len(sol.y)):
        if sol.y[t] not in (True, False, 0, 1):
            violations.append(f"y[{t}]={sol.y[t]} is not binary")

    if np.any(sol.q < -TOL):
        violations.append("q has negative values")

    if sol.p is not None and np.any(sol.p < -TOL):
        violations.append("p has negative values")
    if sol.v is not None and np.any(sol.v < -TOL):
        violations.append("v has negative values")
    if sol.I is not None and np.any(sol.I < -TOL):
        violations.append("I has negative values")
    if sol.u is not None and np.any(sol.u < -TOL):
        violations.append("u has negative values")

    return ConstraintResult("Eq.8 Domains", len(violations) == 0, violations)


def check_part_allocation(sol: Solution, inst: ProblemInstance) -> ConstraintResult:
    """Structural check: no anatomical part can be over-allocated.

    For each part a and period t:
    sum_f composition[f,a] * p[f,t] <= alpha[a] * weight * q[t]
    """
    violations = []
    p = _get_production(sol, inst)

    for t in range(inst.n_periods):
        for a in range(inst.n_parts):
            used = float(np.dot(inst.composition[:, a], p[:, t]))
            available = float(inst.alpha[a] * inst.weight * sol.q[t])
            if used > available + TOL:
                violations.append(
                    f"a={a},t={t}: used={used:.4f} > available={available:.4f}"
                )

    return ConstraintResult("Part allocation", len(violations) == 0, violations)


def check_exclusivity(sol: Solution, inst: ProblemInstance) -> ConstraintResult:
    """Structural check: exclusivity groups and fixed cut configuration."""
    violations = []
    p = _get_production(sol, inst)
    z = _get_cut_activation(sol, inst, p)

    if inst.cut_config is not None:
        for f in range(inst.n_cut_forms):
            if int(inst.cut_config[f]) == 0 and np.any(p[f, :] > TOL):
                violations.append(f"f={f}: production > 0 with cut_config=0")

    for t in range(inst.n_periods):
        for group in inst.exclusivity_groups:
            active_count = sum(int(z[f, t]) for f in group.cut_form_indices)
            if active_count > 1:
                violations.append(
                    f"group={group.name}, t={t}: {active_count} active forms "
                    f"{group.cut_form_indices}"
                )

    return ConstraintResult("Exclusivity", len(violations) == 0, violations)


def check_all(sol: Solution, inst: ProblemInstance) -> dict[str, ConstraintResult]:
    """Run all checks."""
    results = {}
    checks = [
        check_material_balance,
        check_demand_satisfaction,
        check_capacity_max,
        check_capacity_min,
        check_sales_limit,
        check_perishability,
        check_domains,
        check_part_allocation,
        check_exclusivity,
    ]
    for check_fn in checks:
        result = check_fn(sol, inst)
        results[result.name] = result
    return results


def all_satisfied(sol: Solution, inst: ProblemInstance) -> bool:
    """Return True if all checks are satisfied."""
    results = check_all(sol, inst)
    return all(r.satisfied for r in results.values())


def _get_effective_alpha(inst: ProblemInstance) -> np.ndarray:
    """Legacy production factor by cut form."""
    alpha_f = inst.composition.astype(np.float64) @ inst.alpha
    if inst.cut_config is not None:
        alpha_f = alpha_f * inst.cut_config
    return alpha_f


def _get_production(sol: Solution, inst: ProblemInstance) -> np.ndarray:
    """Get production matrix p[f,t]. Fallback to legacy deterministic production."""
    if sol.p is not None:
        if sol.p.ndim != 2:
            raise ValueError("sol.p must be a 2D array with shape [F, T]")
        return sol.p

    alpha_f = _get_effective_alpha(inst)
    # Legacy behavior: deterministic production by form from q[t]
    return np.outer(alpha_f * inst.weight, sol.q.astype(np.float64))


def _get_cut_activation(
    sol: Solution, inst: ProblemInstance, p: np.ndarray
) -> np.ndarray:
    """Get binary activation z[f,t] from solution, fixed config, or production."""
    if sol.z is not None:
        if sol.z.ndim != 2:
            raise ValueError("sol.z must be a 2D array with shape [F, T]")
        return sol.z.astype(bool)

    if inst.cut_config is not None:
        return np.tile(inst.cut_config.astype(bool)[:, np.newaxis], (1, inst.n_periods))

    return p > TOL
