"""
Tests para GeneticAlgorithm.

Sprint: 2.2
"""

import numpy as np
import pytest

from src.metaheuristics.ga import GeneticAlgorithm
from src.model import constraints
from src.model.parameters import ProblemInstance

# ============================================================
# Fixture
# ============================================================


def make_trivial() -> ProblemInstance:
    return ProblemInstance(
        name="trivial_ga",
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


class TestGeneticAlgorithm:

    def test_convergence(self):
        """GA debe mejorar fitness a lo largo de las generaciones."""
        np.random.seed(42)
        inst = make_trivial()
        ga = GeneticAlgorithm(
            {
                "pop_size": 20,
                "n_generations": 30,
                "stagnation_limit": 100,
            }
        )
        sol = ga.solve(inst)

        assert sol is not None
        assert ga.best_fitness > -np.inf

        # Fitness debe mejorar: primera iteracion vs ultima
        iters, bests = ga.convergence_data()
        assert bests[-1] >= bests[0]

    def test_solution_is_feasible(self):
        """La solucion del GA debe cumplir todas las restricciones."""
        np.random.seed(42)
        inst = make_trivial()
        ga = GeneticAlgorithm(
            {
                "pop_size": 20,
                "n_generations": 20,
            }
        )
        sol = ga.solve(inst)

        results = constraints.check_all(sol, inst)
        for name, cr in results.items():
            assert cr.satisfied, f"{name}: {cr.violations[:3]}"

    def test_elitism_preserves_best(self):
        """El mejor fitness nunca debe empeorar entre generaciones."""
        np.random.seed(42)
        inst = make_trivial()
        ga = GeneticAlgorithm(
            {
                "pop_size": 20,
                "n_generations": 30,
            }
        )
        ga.solve(inst)

        _, bests = ga.convergence_data()
        # Best fitness es monotonamente creciente
        for i in range(1, len(bests)):
            assert (
                bests[i] >= bests[i - 1] - 1e-6
            ), f"Gen {i}: {bests[i]} < {bests[i-1]}"

    def test_stagnation_stops_early(self):
        """Con stagnation_limit bajo, GA debe parar antes de n_generations."""
        np.random.seed(42)
        inst = make_trivial()
        ga = GeneticAlgorithm(
            {
                "pop_size": 20,
                "n_generations": 500,
                "stagnation_limit": 5,  # parar rapido
            }
        )
        ga.solve(inst)

        # Debe haber terminado antes de 500 generaciones
        assert len(ga.history) < 500

    def test_custom_config(self):
        """Config personalizada se aplica correctamente."""
        ga = GeneticAlgorithm(
            {
                "pop_size": 100,
                "crossover_rate": 0.9,
            }
        )
        assert ga.config["pop_size"] == 100
        assert ga.config["crossover_rate"] == 0.9
        assert ga.config["mutation_rate"] == 0.1  # default

    def test_multiple_runs_different_results(self):
        """Distintas seeds producen distintos resultados."""
        inst = make_trivial()
        results = []
        for seed in [10, 20, 30]:
            np.random.seed(seed)
            ga = GeneticAlgorithm({"pop_size": 15, "n_generations": 10})
            ga.solve(inst)
            results.append(ga.best_fitness)

        # Al menos 2 de 3 deben ser diferentes
        unique = len(set(f"{r:.0f}" for r in results))
        assert unique >= 2

    def test_summary_output(self):
        """El summary contiene informacion relevante."""
        np.random.seed(42)
        inst = make_trivial()
        ga = GeneticAlgorithm({"pop_size": 10, "n_generations": 5})
        ga.solve(inst)
        s = ga.summary()
        assert "GeneticAlgorithm" in s
        assert "Best Z" in s


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
