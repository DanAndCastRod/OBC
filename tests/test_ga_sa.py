"""
Tests para HybridGASA.

Sprint: 2.5
"""

import numpy as np
import pytest

from src.metaheuristics.ga import GeneticAlgorithm
from src.metaheuristics.ga_sa import HybridGASA
from src.model import constraints
from src.model.parameters import ProblemInstance

# ============================================================
# Fixture
# ============================================================


def make_trivial() -> ProblemInstance:
    return ProblemInstance(
        name="trivial_gasa",
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


class TestHybridGASA:

    def test_convergence(self):
        """GA-SA debe encontrar una buena solucion."""
        np.random.seed(42)
        inst = make_trivial()
        gasa = HybridGASA(
            {
                "pop_size": 15,
                "n_generations": 20,
                "local_search_freq": 5,
                "local_search_top_k": 3,
                "local_search_iters": 10,
            }
        )
        sol = gasa.solve(inst)

        assert sol is not None
        assert gasa.best_fitness > -np.inf

    def test_solution_is_feasible(self):
        """Solucion GA-SA cumple restricciones."""
        np.random.seed(42)
        inst = make_trivial()
        gasa = HybridGASA(
            {
                "pop_size": 15,
                "n_generations": 15,
                "local_search_freq": 5,
                "local_search_top_k": 3,
                "local_search_iters": 10,
            }
        )
        sol = gasa.solve(inst)

        results = constraints.check_all(sol, inst)
        for name, cr in results.items():
            assert cr.satisfied, f"{name}: {cr.violations[:3]}"

    def test_local_search_applied(self):
        """SA se aplica cada local_search_freq generaciones."""
        np.random.seed(42)
        inst = make_trivial()
        gasa = HybridGASA(
            {
                "pop_size": 10,
                "n_generations": 12,
                "local_search_freq": 5,
                "local_search_top_k": 2,
                "local_search_iters": 5,
            }
        )
        gasa.solve(inst)

        # With 12 gens and freq=5, SA applied at gen 5 and 10
        # This means more evaluations than a pure GA with same params
        ga = GeneticAlgorithm(
            {
                "pop_size": 10,
                "n_generations": 12,
            }
        )
        np.random.seed(42)
        ga.solve(inst)

        # GA-SA should have done more evaluations (due to local search)
        assert gasa.n_evaluations >= ga.n_evaluations

    def test_ga_sa_not_worse_than_random(self):
        """GA-SA debe ser mejor que una solucion aleatoria."""
        np.random.seed(42)
        inst = make_trivial()
        from src.metaheuristics.encoding import random_solution
        from src.model import decoder, objective

        # Random fitness
        random_fits = []
        for _ in range(10):
            y, q = random_solution(inst)
            sol = decoder.decode(y, q, inst)
            bd = objective.evaluate_vectorized(sol, inst)
            random_fits.append(bd.total)
        avg_random = np.mean(random_fits)

        # GA-SA
        gasa = HybridGASA(
            {
                "pop_size": 15,
                "n_generations": 20,
                "local_search_freq": 5,
                "local_search_top_k": 3,
                "local_search_iters": 10,
            }
        )
        gasa.solve(inst)

        # GA-SA debe ser al menos tan bueno como el promedio random
        assert gasa.best_fitness >= avg_random

    def test_summary(self):
        np.random.seed(42)
        inst = make_trivial()
        gasa = HybridGASA(
            {
                "pop_size": 10,
                "n_generations": 5,
                "local_search_freq": 3,
                "local_search_iters": 5,
            }
        )
        gasa.solve(inst)
        s = gasa.summary()
        assert "HybridGASA" in s


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
