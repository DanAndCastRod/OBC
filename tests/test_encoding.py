"""
Tests para encoding.py y BaseMetaheuristic.

Sprint: 2.1
"""

import numpy as np
import pytest

from src.metaheuristics import encoding
from src.metaheuristics.base import BaseMetaheuristic
from src.model.parameters import ProblemInstance

# ============================================================
# Fixture
# ============================================================


def make_trivial() -> ProblemInstance:
    return ProblemInstance(
        name="trivial",
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
        n_periods=7,
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
                [[3000.0]] * 7,
                [[2000.0]] * 7,
                [[1000.0]] * 7,
            ]
        ),
    )


# ============================================================
# Tests: Encoding
# ============================================================


class TestEncoding:

    def test_random_binary_shape(self):
        y = encoding.generate_random_binary(10)
        assert len(y) == 10
        assert y.dtype == bool

    def test_random_integer_zero_when_inactive(self):
        y = np.array([True, False, True, False, True])
        q = encoding.generate_random_integer(5, 500, 5000, y)
        assert q[1] == 0
        assert q[3] == 0
        assert q[0] >= 500
        assert q[2] >= 500

    def test_random_solution_is_feasible(self):
        inst = make_trivial()
        np.random.seed(42)
        for _ in range(20):
            y, q = encoding.random_solution(inst)
            for t in range(inst.n_periods):
                if not y[t]:
                    assert q[t] == 0
                else:
                    assert inst.capacity_min <= q[t] <= inst.capacity_max

    def test_repair_zero_without_setup(self):
        y = np.array([False, False, True])
        q = np.array([1000, 500, 3000])  # q[0], q[1] should become 0
        y_r, q_r = encoding.repair_lot_sizing(y, q, 500, 5000)
        assert y_r[0] == True  # activated because q>0
        assert y_r[1] == True  # activated because q>0
        assert q_r[0] == 1000
        assert q_r[1] == 500

    def test_repair_clamps_quantity(self):
        y = np.array([True, True])
        q = np.array([100, 9000])  # below min, above max
        y_r, q_r = encoding.repair_lot_sizing(y, q, 500, 5000)
        assert q_r[0] == 500  # clamped to min
        assert q_r[1] == 5000  # clamped to max

    def test_neighborhood_toggle_changes_bits(self):
        np.random.seed(42)
        y = np.array([True, True, True, True, True])
        y_new = encoding.neighborhood_toggle(y, k=2)
        n_diff = np.sum(y != y_new)
        assert n_diff == 2

    def test_neighborhood_quantity_preserves_inactive(self):
        y = np.array([True, False, True])
        q = np.array([3000, 0, 4000])
        q_new = encoding.neighborhood_quantity(q, y, 500, 5000, delta=0.2)
        assert q_new[1] == 0  # inactive stays 0
        assert 500 <= q_new[0] <= 5000
        assert 500 <= q_new[2] <= 5000

    def test_crossover_uniform_produces_feasible(self):
        np.random.seed(42)
        y1 = np.array([True, False, True, True])
        q1 = np.array([3000, 0, 4000, 2000])
        y2 = np.array([False, True, True, False])
        q2 = np.array([0, 2500, 1500, 0])

        y_c1, q_c1, y_c2, q_c2 = encoding.crossover_uniform(y1, q1, y2, q2, 500, 5000)
        for t in range(4):
            if not y_c1[t]:
                assert q_c1[t] == 0
            if not y_c2[t]:
                assert q_c2[t] == 0

    def test_crossover_two_point_produces_feasible(self):
        np.random.seed(42)
        y1 = np.array([True, False, True, True, False])
        q1 = np.array([3000, 0, 4000, 2000, 0])
        y2 = np.array([False, True, True, False, True])
        q2 = np.array([0, 2500, 1500, 0, 3000])

        y_c1, q_c1, y_c2, q_c2 = encoding.crossover_two_point(y1, q1, y2, q2, 500, 5000)
        for t in range(5):
            if not y_c1[t]:
                assert q_c1[t] == 0
                assert q_c1[t] == 0
            if not y_c2[t]:
                assert q_c2[t] == 0

    def test_mutate_produces_feasible(self):
        np.random.seed(42)
        y = np.array([True, True, False, True])
        q = np.array([3000, 4000, 0, 2000])
        for _ in range(20):
            y_m, q_m = encoding.mutate(y, q, 500, 5000)
            for t in range(4):
                if not y_m[t]:
                    assert q_m[t] == 0
                else:
                    assert 500 <= q_m[t] <= 5000

    def test_mutate_zero_rates_no_change(self):
        """Sin tasas de mutacion, el individuo debe permanecer igual."""
        np.random.seed(42)
        y = np.array([True, True, False, True])
        q = np.array([3000, 4000, 0, 2000])
        y_m, q_m = encoding.mutate(
            y, q, 500, 5000, p_toggle=0.0, p_quantity=0.0, delta=0.2
        )
        np.testing.assert_array_equal(y_m, y)
        np.testing.assert_array_equal(q_m, q)

    def test_mutate_quantity_respects_probability(self):
        """Con p_toggle=0 y p_quantity=1, debe haber cambios en q activo."""
        np.random.seed(42)
        y = np.array([True, True, False, True])
        q = np.array([3000, 4000, 0, 2000])
        changed = 0
        for _ in range(30):
            y_m, q_m = encoding.mutate(
                y, q, 500, 5000, p_toggle=0.0, p_quantity=1.0, delta=0.2
            )
            if not np.array_equal(q_m, q):
                changed += 1
            np.testing.assert_array_equal(y_m, y)
        assert changed > 0


# ============================================================
# Tests: BaseMetaheuristic
# ============================================================


class DummyMH(BaseMetaheuristic):
    """Metaheuristica dummy para tests."""

    def solve(self, instance, **kwargs):
        self.reset()
        y, q = self.generate_random(instance)
        fitness, sol = self.evaluate_and_get_solution(y, q, instance)
        self.update_best(fitness, sol, instance)
        self.log_iteration(0, self.best_fitness, fitness)
        return self.best_solution


class TestBaseMetaheuristic:

    def test_evaluate_fitness_returns_float(self):
        mh = DummyMH()
        inst = make_trivial()
        np.random.seed(42)
        y, q = encoding.random_solution(inst)
        fitness = mh.evaluate_fitness(y, q, inst)
        assert isinstance(fitness, float)
        assert mh.n_evaluations == 1

    def test_solve_returns_solution(self):
        mh = DummyMH()
        inst = make_trivial()
        np.random.seed(42)
        sol = mh.solve(inst)
        assert sol is not None
        assert mh.best_fitness > -np.inf
        assert len(mh.history) == 1

    def test_convergence_data(self):
        mh = DummyMH()
        inst = make_trivial()
        np.random.seed(42)
        mh.solve(inst)
        iters, best = mh.convergence_data()
        assert len(iters) == 1
        assert len(best) == 1

    def test_reset_clears_state(self):
        mh = DummyMH()
        inst = make_trivial()
        np.random.seed(42)
        mh.solve(inst)
        mh.reset()
        assert mh.best_fitness == -np.inf
        assert len(mh.history) == 0
        assert mh.n_evaluations == 0

    def test_summary(self):
        mh = DummyMH()
        inst = make_trivial()
        np.random.seed(42)
        mh.solve(inst)
        s = mh.summary()
        assert "DummyMH" in s


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
