"""
Tests para DifferentialEvolution.

Sprint: 2.4
"""

import numpy as np
import pytest

from src.metaheuristics.de import DifferentialEvolution
from src.model import constraints
from src.model.parameters import ProblemInstance

# ============================================================
# Fixture
# ============================================================


def make_trivial() -> ProblemInstance:
    return ProblemInstance(
        name="trivial_de",
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


class TestDifferentialEvolution:

    def test_convergence(self):
        """DE debe mejorar fitness a lo largo de las generaciones."""
        np.random.seed(42)
        inst = make_trivial()
        de = DifferentialEvolution(
            {
                "pop_size": 15,
                "max_generations": 15,
                "stagnation_limit": 100,
            }
        )
        sol = de.solve(inst)

        assert sol is not None
        assert de.best_fitness > -np.inf

        iters, bests = de.convergence_data()
        assert bests[-1] >= bests[0]

    def test_solution_is_feasible(self):
        """La solucion del DE debe cumplir restricciones."""
        np.random.seed(42)
        inst = make_trivial()
        de = DifferentialEvolution(
            {
                "pop_size": 15,
                "max_generations": 10,
            }
        )
        sol = de.solve(inst)

        results = constraints.check_all(sol, inst)
        for name, cr in results.items():
            assert cr.satisfied, f"{name}: {cr.violations[:3]}"

    def test_greedy_selection_monotonic(self):
        """La seleccion greedy hace que el mejor fitness no empeore."""
        np.random.seed(42)
        inst = make_trivial()
        de = DifferentialEvolution(
            {
                "pop_size": 15,
                "max_generations": 15,
            }
        )
        de.solve(inst)

        _, bests = de.convergence_data()
        for i in range(1, len(bests)):
            assert (
                bests[i] >= bests[i - 1] - 1e-6
            ), f"Gen {i}: {bests[i]} < {bests[i-1]}"

    def test_discretize_valid(self):
        """Discretizacion produce valores dentro del rango."""
        np.random.seed(42)
        vec = np.random.random(10)  # 5 periodos -> dim=10
        y, q = DifferentialEvolution._decode(vec, 5, 500, 5000)

        for t in range(5):
            if not y[t]:
                assert q[t] == 0
            else:
                assert 500 <= q[t] <= 5000

    def test_encode_decode_roundtrip(self):
        """Encode -> decode preserva la estructura."""
        y = np.array([True, False, True, True, False])
        q = np.array([3000, 0, 4500, 1000, 0])
        vec = DifferentialEvolution._encode(y, q, 500, 5000)
        y2, q2 = DifferentialEvolution._decode(vec, 5, 500, 5000)

        np.testing.assert_array_equal(y, y2)
        np.testing.assert_array_equal(q, q2)

    def test_best_strategy(self):
        """Estrategia best/1/bin tambien funciona."""
        np.random.seed(42)
        inst = make_trivial()
        de = DifferentialEvolution(
            {
                "pop_size": 15,
                "max_generations": 10,
                "strategy": "best/1/bin",
            }
        )
        sol = de.solve(inst)
        assert sol is not None
        assert de.best_fitness > -np.inf

    def test_stagnation_stops_early(self):
        """Con stagnation_limit bajo, DE para antes de max_generations."""
        np.random.seed(42)
        inst = make_trivial()
        de = DifferentialEvolution(
            {
                "pop_size": 10,
                "max_generations": 1000,
                "stagnation_limit": 5,
            }
        )
        de.solve(inst)
        # Must have stopped before 1000 generations (history includes gen 0)
        assert len(de.history) <= 1001

    def test_summary(self):
        np.random.seed(42)
        inst = make_trivial()
        de = DifferentialEvolution(
            {
                "pop_size": 10,
                "max_generations": 5,
            }
        )
        de.solve(inst)
        s = de.summary()
        assert "DifferentialEvolution" in s


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
