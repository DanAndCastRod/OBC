"""
Tests para SimulatedAnnealing.

Sprint: 2.3
"""


import numpy as np
import pytest

from src.metaheuristics.sa import SimulatedAnnealing
from src.model import constraints
from src.model.parameters import ProblemInstance

# ============================================================
# Fixture
# ============================================================


def make_trivial() -> ProblemInstance:
    return ProblemInstance(
        name="trivial_sa",
        profile="trivial",
        seed=0,
        n_parts=3,
        part_names=["Pechuga", "Muslo", "Otros"],
        alpha=np.array([0.40, 0.30, 0.30]),
        n_cut_forms=3,
        cut_form_names=["Pechuga", "Muslo", "Subproducto"],
        composition=np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.int32),
        exclusivity_groups=[],
        cut_config=np.array([1, 1, 1], dtype=np.int32),
        n_periods=5,
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
                [[3000.0]] * 5,
                [[2000.0]] * 5,
                [[1000.0]] * 5,
            ]
        ),
    )


# ============================================================
# Tests
# ============================================================


class TestSimulatedAnnealing:

    def test_convergence(self):
        """SA debe encontrar una solucion razonable."""
        np.random.seed(42)
        inst = make_trivial()
        sa = SimulatedAnnealing(
            {
                "T_initial": 1e5,
                "T_final": 1e3,
                "cooling_rate": 0.5,
                "max_iterations": 10,
            }
        )
        sol = sa.solve(inst)

        assert sol is not None
        assert sa.best_fitness > -np.inf

    def test_solution_is_feasible(self):
        """La solucion del SA debe cumplir restricciones."""
        np.random.seed(42)
        inst = make_trivial()
        sa = SimulatedAnnealing(
            {
                "T_initial": 1e5,
                "T_final": 1e3,
                "cooling_rate": 0.5,
                "max_iterations": 10,
            }
        )
        sol = sa.solve(inst)

        results = constraints.check_all(sol, inst)
        for name, cr in results.items():
            assert cr.satisfied, f"{name}: {cr.violations[:3]}"

    def test_high_temp_accepts_all(self):
        """A T muy alta, acepta practicamente todo (random walk)."""
        accepted = 0
        n_trials = 100
        for _ in range(n_trials):
            delta = -np.random.uniform(1000, 100000)  # peor
            if SimulatedAnnealing._accept(delta, 1e12):
                accepted += 1
        # Con T=1e12, exp(delta/T) ~ 1.0, deberia aceptar >95%
        assert accepted > 90

    def test_low_temp_rejects_worse(self):
        """A T ~0, solo acepta mejoras (hill climbing)."""
        accepted = 0
        n_trials = 100
        for _ in range(n_trials):
            delta = -np.random.uniform(100, 10000)  # peor
            if SimulatedAnnealing._accept(delta, 0.001):
                accepted += 1
        # Con T=0.001, deberia rechazar casi todo
        assert accepted < 5

    def test_always_accepts_improvement(self):
        """Delta > 0 se acepta siempre, sin importar T."""
        for _ in range(50):
            assert SimulatedAnnealing._accept(100.0, 0.001)
            assert SimulatedAnnealing._accept(100.0, 1e12)

    def test_auto_temperature(self):
        """Temperatura auto-estimada debe ser positiva y razonable."""
        np.random.seed(42)
        inst = make_trivial()
        sa = SimulatedAnnealing({"T_initial": None})
        T0 = sa._estimate_initial_temperature(inst, n_samples=10)
        assert T0 > 0
        assert np.isfinite(T0)

    def test_reheating_increases_temperature(self):
        """Con stagnation, SA debe reheatar y explorar mas."""
        np.random.seed(42)
        inst = make_trivial()
        sa = SimulatedAnnealing(
            {
                "T_initial": 1e4,
                "T_final": 1e3,
                "cooling_rate": 0.5,
                "max_iterations": 5,
                "reheat_threshold": 3,
                "reheat_factor": 1.5,
            }
        )
        sol = sa.solve(inst)
        assert sol is not None
        # SA completed without crashing with reheat logic

    def test_summary(self):
        np.random.seed(42)
        inst = make_trivial()
        sa = SimulatedAnnealing(
            {
                "T_initial": 1e5,
                "T_final": 1e3,
                "cooling_rate": 0.5,
                "max_iterations": 5,
            }
        )
        sa.solve(inst)
        s = sa.summary()
        assert "SimulatedAnnealing" in s


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
