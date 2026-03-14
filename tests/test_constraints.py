"""
Tests para objective.py, constraints.py y decoder.py.

Sprint: 1.3
"""

import numpy as np
import pytest

from src.model import constraints, decoder, objective
from src.model.parameters import ProblemInstance
from src.model.solution import Solution

# ============================================================
# Fixture: instancia trivial determinista
# ============================================================


def make_trivial() -> ProblemInstance:
    """Instancia trivial: 3 piezas, 3 formas, 3 dias, 1 escenario.

    Formas: Pechuga (alpha=0.4), Muslo (0.3), Subprod (0.3)
    Sin exclusividad. Config fija: todas activas.
    """
    return ProblemInstance(
        name="trivial",
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


def make_overlap_instance() -> ProblemInstance:
    """Instance with overlapping forms on part A.

    Used to validate that part allocation avoids double counting.
    """
    return ProblemInstance(
        name="overlap",
        profile="test",
        seed=0,
        n_parts=2,
        part_names=["A", "B"],
        alpha=np.array([0.60, 0.40]),
        n_cut_forms=2,
        cut_form_names=["A_only", "AB_combo"],
        composition=np.array(
            [
                [1, 0],  # A_only consumes part A
                [1, 1],  # AB_combo consumes A and B
            ],
            dtype=np.int32,
        ),
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
# Tests: Decoder greedy
# ============================================================


class TestDecoder:

    def test_all_off_produces_zero(self):
        """y=0, q=0 para todos los periodos -> ventas=0, insatisfaccion=demanda."""
        inst = make_trivial()
        y = np.array([False, False, False])
        q = np.array([0, 0, 0])
        sol = decoder.decode(y, q, inst)

        assert sol.v is not None
        np.testing.assert_array_equal(sol.v, 0.0)
        np.testing.assert_array_equal(sol.I, 0.0)
        np.testing.assert_array_almost_equal(sol.u, inst.demand)

    def test_full_production(self):
        """Produccion maxima todos los dias -> ventas cubren demanda."""
        inst = make_trivial()
        y = np.array([True, True, True])
        q = np.array([5000, 5000, 5000])
        sol = decoder.decode(y, q, inst)

        assert sol.v is not None
        # Con 5000 carcasas * 2.5kg * alpha_f:
        # Pechuga: 5000*2.5*0.4 = 5000 kg/dia >> demanda 3000
        # Toda la demanda debe satisfacerse
        np.testing.assert_array_almost_equal(sol.u, 0.0)

    def test_decoder_produces_feasible_solution(self):
        """El decoder siempre debe producir una solucion factible."""
        inst = make_trivial()
        y = np.array([True, False, True])
        q = np.array([3000, 0, 4000])
        sol = decoder.decode(y, q, inst)

        results = constraints.check_all(sol, inst)
        for name, result in results.items():
            assert result.satisfied, f"{name}: {result.violations[:3]}"

    def test_partial_production_creates_unmet_demand(self):
        """Produccion insuficiente -> insatisfaccion > 0."""
        inst = make_trivial()
        y = np.array([True, False, False])
        q = np.array([500, 0, 0])  # lote minimo, solo dia 1
        sol = decoder.decode(y, q, inst)

        # Produccion: 500 * 2.5 * 0.4 = 500 kg pechuga
        # Demanda dia 1: 3000 -> insatisfaccion = 2500
        assert sol.u[0, 0, 0] > 0  # pechuga insatisfecha


# ============================================================
# Tests: Constraints
# ============================================================


class TestConstraints:

    def test_all_constraints_on_decoded_solution(self):
        """Una solucion decodificada cumple todas las restricciones."""
        inst = make_trivial()
        y = np.array([True, True, False])
        q = np.array([3000, 2000, 0])
        sol = decoder.decode(y, q, inst)

        results = constraints.check_all(sol, inst)
        for name, result in results.items():
            assert result.satisfied, f"{name}: {result.violations[:3]}"

    def test_capacity_max_violation(self):
        """q > Q_max se detecta."""
        inst = make_trivial()
        sol = Solution(
            y=np.array([True, False, False]),
            q=np.array([6000, 0, 0]),  # > 5000
            v=np.zeros((3, 3, 1)),
            I=np.zeros((3, 3, 1)),
            u=inst.demand.copy(),
        )
        result = constraints.check_capacity_max(sol, inst)
        assert not result.satisfied

    def test_capacity_min_violation(self):
        """q < Q_min cuando y=1 se detecta."""
        inst = make_trivial()
        sol = Solution(
            y=np.array([True, False, False]),
            q=np.array([100, 0, 0]),  # < 500
            v=np.zeros((3, 3, 1)),
            I=np.zeros((3, 3, 1)),
            u=inst.demand.copy(),
        )
        result = constraints.check_capacity_min(sol, inst)
        assert not result.satisfied

    def test_domains_negative_v(self):
        """Ventas negativas se detectan."""
        inst = make_trivial()
        v = np.zeros((3, 3, 1))
        v[0, 0, 0] = -100  # negativo
        sol = Solution(
            y=np.array([False, False, False]),
            q=np.array([0, 0, 0]),
            v=v,
            I=np.zeros((3, 3, 1)),
            u=inst.demand.copy(),
        )
        result = constraints.check_domains(sol, inst)
        assert not result.satisfied

    def test_demand_satisfaction_violation(self):
        """v + u != d se detecta."""
        inst = make_trivial()
        sol = Solution(
            y=np.array([False, False, False]),
            q=np.array([0, 0, 0]),
            v=np.zeros((3, 3, 1)),
            I=np.zeros((3, 3, 1)),
            u=np.zeros((3, 3, 1)),  # u=0 pero d>0 -> v+u != d
        )
        result = constraints.check_demand_satisfaction(sol, inst)
        assert not result.satisfied


# ============================================================
# Tests: Objective
# ============================================================


class TestObjective:

    def test_zero_solution_has_negative_z(self):
        """Sin produccion -> Z < 0 (solo penalizaciones)."""
        inst = make_trivial()
        y = np.array([False, False, False])
        q = np.array([0, 0, 0])
        sol = decoder.decode(y, q, inst)
        bd = objective.evaluate(sol, inst)

        assert bd.revenue == 0.0
        assert bd.prod_cost == 0.0
        assert bd.setup_cost == 0.0
        assert bd.pen_cost > 0.0
        assert bd.total < 0.0

    def test_full_production_positive_z(self):
        """Produccion maxima con demanda alcanzable -> Z > 0."""
        inst = make_trivial()
        y = np.array([True, True, True])
        q = np.array([5000, 5000, 5000])
        sol = decoder.decode(y, q, inst)
        bd = objective.evaluate(sol, inst)

        assert bd.revenue > 0.0
        assert bd.total > 0.0  # ingresos > costos

    def test_loop_vs_vectorized_equal(self):
        """Las dos versiones del evaluador deben dar el mismo resultado."""
        inst = make_trivial()
        y = np.array([True, False, True])
        q = np.array([3000, 0, 4000])
        sol = decoder.decode(y, q, inst)

        bd_loop = objective.evaluate(sol, inst)
        bd_vec = objective.evaluate_vectorized(sol, inst)

        assert abs(bd_loop.total - bd_vec.total) < 0.01
        assert abs(bd_loop.revenue - bd_vec.revenue) < 0.01
        assert abs(bd_loop.pen_cost - bd_vec.pen_cost) < 0.01

    def test_more_production_higher_revenue(self):
        """Mas produccion (dentro de capacidad) -> mas ingresos."""
        inst = make_trivial()

        y1 = np.array([True, False, False])
        q1 = np.array([1000, 0, 0])
        sol1 = decoder.decode(y1, q1, inst)
        bd1 = objective.evaluate(sol1, inst)

        y2 = np.array([True, True, True])
        q2 = np.array([3000, 3000, 3000])
        sol2 = decoder.decode(y2, q2, inst)
        bd2 = objective.evaluate(sol2, inst)

        assert bd2.revenue > bd1.revenue


# ============================================================
# Tests: Perecibilidad en decoder
# ============================================================


class TestPerishability:

    def test_short_shelf_life_forces_discard(self):
        """Producto con L=1 dia no puede acumular inventario."""
        inst = make_trivial()
        inst.shelf_life = np.array([1, 1, 30], dtype=np.int32)

        y = np.array([True, False, False])
        q = np.array([5000, 0, 0])
        sol = decoder.decode(y, q, inst)

        # Dia 1: produccion grande, dia 2: sin produccion
        # Con L=1, el inventario de dia 1 se descarta en dia 2
        # Pechuga: produccion = 5000*2.5*0.4 = 5000, demanda = 3000
        # Dia 1: I = 5000 - 3000 = 2000
        # Dia 2: I deberia ser 0 (perecido) porque L=1
        assert sol.I[0, 1, 0] == 0.0  # pechuga: inventario descartado

    def test_long_shelf_life_preserves_inventory(self):
        """Producto con L=30 dias acumula inventario."""
        inst = make_trivial()
        inst.shelf_life = np.array([30, 30, 30], dtype=np.int32)

        y = np.array([True, False, False])
        q = np.array([5000, 0, 0])
        sol = decoder.decode(y, q, inst)

        # Con L=30, el inventario sobrevive al dia 2
        # Pechuga: prod=5000, venta_d1=3000 -> I_d1 = 2000
        # Dia 2: disponible = 2000 (inventario), demanda = 3200
        # Ventas = 2000, I = 0 (se acabo)
        assert sol.I[0, 0, 0] > 0  # hay inventario dia 1


class TestPartAllocationCorrections:

    def test_decoder_respects_part_pool_with_overlap(self):
        """Decoder must not over-allocate shared anatomical mass."""
        inst = make_overlap_instance()
        y = np.array([True])
        q = np.array([100])
        sol = decoder.decode(y, q, inst)

        assert sol.p is not None
        used = np.dot(inst.composition[:, 0], sol.p[:, 0])  # part A
        available = inst.alpha[0] * inst.weight * q[0]
        assert used <= available + 1e-6
        assert sol.v[:, 0, 0].sum() <= inst.weight * q[0] + 1e-6

        part_check = constraints.check_part_allocation(sol, inst)
        assert part_check.satisfied, part_check.violations[:3]

    def test_part_allocation_detects_legacy_overcount(self):
        """Without explicit p, legacy implicit production can violate part mass."""
        inst = make_overlap_instance()
        sol = Solution(
            y=np.array([True]),
            q=np.array([100]),
            v=np.zeros((2, 1, 1)),
            I=np.zeros((2, 1, 1)),
            u=np.zeros((2, 1, 1)),
        )

        result = constraints.check_part_allocation(sol, inst)
        assert not result.satisfied


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
