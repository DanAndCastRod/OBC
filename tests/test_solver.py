"""
Tests de integracion para el solver exacto.

Sprint: 1.4
"""

import numpy as np
import pytest

from src.model import constraints, decoder, objective
from src.model.parameters import ProblemInstance
from src.model.solver import SolverStatus, solve_exact

# ============================================================
# Fixtures
# ============================================================


def make_trivial_deterministic() -> ProblemInstance:
    """Instancia trivial determinista para validacion manual.

    3 formas, 3 dias, 1 escenario. Solucion verificable a mano.
    """
    return ProblemInstance(
        name="trivial_det",
        profile="trivial",
        seed=0,
        n_parts=3,
        part_names=["Pechuga", "Muslo", "Otros"],
        alpha=np.array([0.40, 0.30, 0.30]),
        n_cut_forms=3,
        cut_form_names=["Pechuga", "Muslo", "Subproducto"],
        composition=np.array(
            [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1],
            ],
            dtype=np.int32,
        ),
        exclusivity_groups=[],
        cut_config=np.array([1, 1, 1], dtype=np.int32),
        n_periods=3,
        weight=2.5,
        prices=np.array([14000.0, 9000.0, 1500.0]),
        cost_prod=2000.0,
        cost_setup=500000.0,
        cost_inv=np.array([300.0, 250.0, 100.0]),
        cost_pen=np.array([5000.0, 3500.0, 500.0]),
        capacity_max=5000,
        capacity_min=500,
        shelf_life=np.array([5, 5, 30], dtype=np.int32),
        n_scenarios=1,
        scenario_probs=np.array([1.0]),
        demand=np.array(
            [
                [[3000.0], [3200.0], [2800.0]],
                [[2000.0], [2100.0], [1900.0]],
                [[1000.0], [1100.0], [900.0]],
            ]
        ),
    )


def make_infeasible_instance() -> ProblemInstance:
    """Instancia donde la demanda es imposible de satisfacer."""
    return ProblemInstance(
        name="infeasible",
        profile="trivial",
        seed=0,
        n_parts=2,
        part_names=["A", "B"],
        alpha=np.array([0.50, 0.50]),
        n_cut_forms=2,
        cut_form_names=["ProdA", "ProdB"],
        composition=np.array([[1, 0], [0, 1]], dtype=np.int32),
        exclusivity_groups=[],
        cut_config=np.array([1, 1], dtype=np.int32),
        n_periods=2,
        weight=2.0,
        prices=np.array([10000.0, 5000.0]),
        cost_prod=1000.0,
        cost_setup=100000.0,
        cost_inv=np.array([100.0, 100.0]),
        cost_pen=np.array([0.0, 0.0]),  # sin penalizacion = debe satisfacer todo
        capacity_max=100,
        capacity_min=10,
        shelf_life=np.array([30, 30], dtype=np.int32),
        n_scenarios=1,
        scenario_probs=np.array([1.0]),
        # Demand mucho mayor que capacidad
        demand=np.array(
            [
                [[999999.0], [999999.0]],
                [[999999.0], [999999.0]],
            ]
        ),
    )


def make_overlap_instance() -> ProblemInstance:
    """Instance with overlapping forms to test part-allocation in MILP."""
    return ProblemInstance(
        name="overlap",
        profile="test",
        seed=0,
        n_parts=2,
        part_names=["A", "B"],
        alpha=np.array([0.60, 0.40]),
        n_cut_forms=2,
        cut_form_names=["A_only", "AB_combo"],
        composition=np.array([[1, 0], [1, 1]], dtype=np.int32),
        exclusivity_groups=[],
        cut_config=None,
        n_periods=1,
        weight=1.0,
        prices=np.array([10.0, 12.0]),
        cost_prod=0.0,
        cost_setup=0.0,
        cost_inv=np.array([0.0, 0.0]),
        cost_pen=np.array([1000.0, 1000.0]),
        capacity_max=1000,
        capacity_min=0,
        shelf_life=np.array([10, 10], dtype=np.int32),
        n_scenarios=1,
        scenario_probs=np.array([1.0]),
        demand=np.array(
            [
                [[1000.0]],
                [[1000.0]],
            ]
        ),
    )


# ============================================================
# Tests
# ============================================================


class TestSolverExact:

    def test_trivial_finds_optimal(self):
        """Solver encuentra solucion optima para instancia trivial."""
        inst = make_trivial_deterministic()
        result = solve_exact(inst, time_limit=30, solver="cbc")

        assert result.status == SolverStatus.OPTIMAL
        assert result.solution is not None
        assert result.objective_value > 0
        assert result.gap == 0.0

    def test_solution_is_feasible(self):
        """La solucion del solver cumple todas las restricciones."""
        inst = make_trivial_deterministic()
        result = solve_exact(inst, time_limit=30)

        assert result.solution is not None
        results = constraints.check_all(result.solution, inst)
        for name, cr in results.items():
            assert cr.satisfied, f"{name}: {cr.violations[:3]}"

    def test_solver_vs_evaluate_agree(self):
        """El Z del solver y el evaluador deben coincidir."""
        inst = make_trivial_deterministic()
        result = solve_exact(inst, time_limit=30)

        assert result.solution is not None
        bd = objective.evaluate_vectorized(result.solution, inst)

        # Tolerancia: PuLP puede redondear enteros
        assert (
            abs(bd.total - result.objective_value) < 1.0
        ), f"evaluate={bd.total:.2f}, solver={result.objective_value:.2f}"

    def test_solver_beats_greedy(self):
        """El solver optimo debe dar Z >= greedy decoder."""
        inst = make_trivial_deterministic()

        # Solver exacto
        result = solve_exact(inst, time_limit=30)
        assert result.solution is not None

        # Greedy: produccion maxima todos los dias
        y_greedy = np.array([True, True, True])
        q_greedy = np.array([5000, 5000, 5000])
        sol_greedy = decoder.decode(y_greedy, q_greedy, inst)
        bd_greedy = objective.evaluate_vectorized(sol_greedy, inst)

        assert (
            result.objective_value >= bd_greedy.total - 1.0
        ), f"Solver={result.objective_value:.0f} < Greedy={bd_greedy.total:.0f}"

    def test_timeout_short(self):
        """Con time_limit=1, debe terminar rapidamente."""
        inst = make_trivial_deterministic()
        result = solve_exact(inst, time_limit=1)

        # Deberia resolver antes del timeout (instancia trivial)
        assert result.status in (SolverStatus.OPTIMAL, SolverStatus.FEASIBLE)

    def test_result_metrics(self):
        """SolverResult contiene metricas utiles."""
        inst = make_trivial_deterministic()
        result = solve_exact(inst, time_limit=30)

        assert result.n_variables > 0
        assert result.n_constraints > 0
        assert result.elapsed_seconds >= 0

    def test_load_toy_and_solve(self):
        """Cargar instancia toy YAML y resolver."""
        from pathlib import Path

        toy_path = Path("data/instances/toy_seed42.yaml")
        if not toy_path.exists():
            pytest.skip("toy_seed42.yaml no encontrada")

        inst = ProblemInstance.from_yaml(toy_path)
        result = solve_exact(inst, time_limit=60)

        assert result.status in (SolverStatus.OPTIMAL, SolverStatus.FEASIBLE)
        assert result.solution is not None
        assert result.objective_value > 0

    def test_solver_respects_part_allocation_overlap(self):
        """Solver must respect anatomical mass with overlapping forms."""
        inst = make_overlap_instance()
        result = solve_exact(inst, time_limit=30, solver="cbc")

        assert result.status in (SolverStatus.OPTIMAL, SolverStatus.FEASIBLE)
        assert result.solution is not None
        assert result.solution.p is not None

        # Sanity: total sold cannot exceed total carcass kg in this setup.
        total_sales = float(result.solution.v[:, 0, 0].sum())
        total_kg = float(inst.weight * result.solution.q[0])
        assert total_sales <= total_kg + 1e-6

        part_check = constraints.check_part_allocation(result.solution, inst)
        assert part_check.satisfied, part_check.violations[:3]


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
