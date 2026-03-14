"""
Tests para ProblemInstance y Solution.

Sprint: 1.2
"""

import tempfile
from pathlib import Path

import numpy as np
import pytest

from src.model.parameters import ExclusivityGroup, ProblemInstance
from src.model.solution import Solution, SolutionBreakdown

# ============================================================
# Fixtures
# ============================================================

INSTANCE_YAML = Path("data/instances/toy_seed42.yaml")


def make_trivial_instance() -> ProblemInstance:
    """Crear instancia trivial (nivel 0) para tests rapidos."""
    return ProblemInstance(
        name="trivial_test",
        profile="trivial",
        seed=0,
        # Capa 1: 3 piezas
        n_parts=3,
        part_names=["Pechuga", "Muslo", "Otros"],
        alpha=np.array([0.40, 0.30, 0.30]),
        # Capa 2: 3 formas
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
        # Periodos
        n_periods=3,
        # Economicos
        weight=2.5,
        prices=np.array([14000.0, 9000.0, 1500.0]),
        cost_prod=2000.0,
        cost_setup=500000.0,
        cost_inv=np.array([300.0, 250.0, 100.0]),
        cost_pen=np.array([5000.0, 3500.0, 500.0]),
        # Capacidad
        capacity_max=5000,
        capacity_min=500,
        # Perecibilidad
        shelf_life=np.array([5, 5, 30], dtype=np.int32),
        # Escenarios: 1 determinista
        n_scenarios=1,
        scenario_probs=np.array([1.0]),
        demand=np.array(
            [
                [[3000.0], [3200.0], [2800.0]],  # Pechuga
                [[2000.0], [2100.0], [1900.0]],  # Muslo
                [[1000.0], [1100.0], [900.0]],  # Subproducto
            ]
        ),
    )


# ============================================================
# Tests ProblemInstance
# ============================================================


class TestProblemInstance:

    def test_trivial_validates(self):
        instance = make_trivial_instance()
        errors = instance.validate()
        assert errors == [], f"Errores inesperados: {errors}"

    def test_alpha_sum_validation(self):
        instance = make_trivial_instance()
        instance.alpha = np.array([0.40, 0.30, 0.20])  # sum = 0.90
        errors = instance.validate()
        assert any("sum(alpha)" in e for e in errors)

    def test_scenario_probs_sum_validation(self):
        instance = make_trivial_instance()
        instance.scenario_probs = np.array([0.5])  # sum != 1
        errors = instance.validate()
        assert any("sum(scenario_probs)" in e for e in errors)

    def test_demand_shape_validation(self):
        instance = make_trivial_instance()
        instance.demand = np.zeros((2, 3, 1))  # wrong n_cut_forms
        errors = instance.validate()
        assert any("demand shape" in e for e in errors)

    def test_capacity_validation(self):
        instance = make_trivial_instance()
        instance.capacity_min = 6000  # > capacity_max
        errors = instance.validate()
        assert any("capacity_min" in e for e in errors)

    def test_exclusivity_group_validation(self):
        instance = make_trivial_instance()
        instance.exclusivity_groups = [
            ExclusivityGroup("bad", [0, 99], 0)  # index 99 out of range
        ]
        errors = instance.validate()
        assert any("indice 99" in e for e in errors)

    def test_yaml_round_trip(self):
        """Exportar a YAML y re-importar debe dar la misma instancia."""
        instance = make_trivial_instance()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test_instance.yaml"
            instance.to_yaml(path)
            loaded = ProblemInstance.from_yaml(path)

        assert loaded.name == instance.name
        assert loaded.n_parts == instance.n_parts
        assert loaded.n_cut_forms == instance.n_cut_forms
        assert loaded.n_periods == instance.n_periods
        assert loaded.n_scenarios == instance.n_scenarios
        np.testing.assert_array_almost_equal(loaded.alpha, instance.alpha)
        np.testing.assert_array_almost_equal(loaded.demand, instance.demand)
        np.testing.assert_array_equal(loaded.composition, instance.composition)

    def test_load_toy_yaml(self):
        """Cargar la instancia toy real del proyecto."""
        if not INSTANCE_YAML.exists():
            pytest.skip(f"{INSTANCE_YAML} no encontrada")
        instance = ProblemInstance.from_yaml(INSTANCE_YAML)
        assert instance.n_parts == 3
        assert instance.n_cut_forms == 3
        assert instance.n_periods == 4
        assert instance.n_scenarios == 5
        assert instance.demand.shape == (3, 4, 5)

    def test_summary(self):
        instance = make_trivial_instance()
        s = instance.summary()
        assert "trivial_test" in s
        assert "3 dias" in s

    def test_repr(self):
        instance = make_trivial_instance()
        r = repr(instance)
        assert "ProblemInstance" in r


# ============================================================
# Tests Solution
# ============================================================


class TestSolution:

    def test_feasible_solution(self):
        instance = make_trivial_instance()
        sol = Solution(
            y=np.array([True, True, False]),
            q=np.array([3000, 4000, 0]),
            algorithm="test",
        )
        violations = sol.check_feasibility(instance)
        assert violations == []
        assert sol.is_feasible

    def test_infeasible_quantity_without_setup(self):
        instance = make_trivial_instance()
        sol = Solution(
            y=np.array([True, False, False]),
            q=np.array([3000, 4000, 0]),  # t=1: y=0 but q=4000
        )
        violations = sol.check_feasibility(instance)
        assert len(violations) > 0
        assert not sol.is_feasible

    def test_infeasible_below_min_lot(self):
        instance = make_trivial_instance()
        sol = Solution(
            y=np.array([True, True, False]),
            q=np.array([3000, 100, 0]),  # t=1: q=100 < Q_min=500
        )
        violations = sol.check_feasibility(instance)
        assert any("Q_min" in v for v in violations)

    def test_infeasible_above_max_capacity(self):
        instance = make_trivial_instance()
        sol = Solution(
            y=np.array([True, False, False]),
            q=np.array([6000, 0, 0]),  # q=6000 > Q_max=5000
        )
        violations = sol.check_feasibility(instance)
        assert any("Q_max" in v for v in violations)

    def test_properties(self):
        sol = Solution(
            y=np.array([True, True, False]),
            q=np.array([3000, 4000, 0]),
        )
        assert sol.n_periods == 3
        assert sol.total_production == 7000
        assert sol.n_setups == 2

    def test_breakdown_total(self):
        bd = SolutionBreakdown(
            revenue=100000.0,
            prod_cost=20000.0,
            setup_cost=5000.0,
            inv_cost=3000.0,
            pen_cost=2000.0,
        )
        assert bd.total == 70000.0


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
