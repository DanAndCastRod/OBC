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

    def test_low_demand_forces_spoilage_discard(self):
        """Inventario perecedero se descarta al vencer la vida util aunque
        la demanda no lo consuma.

        Este caso falla con un decoder que solo arrastra capas FIFO sin
        caducarlas: con L=2 y produccion unica en el dia 0, el stock debe
        seguir disponible en el dia 1 (aun fresco) pero desaparecer en el
        dia 2 (vencido), independientemente de la demanda.
        """
        inst = make_trivial()
        inst.n_periods = 4
        inst.shelf_life = np.array([2, 2, 30], dtype=np.int32)
        # Demanda baja y constante: no alcanza a consumir la produccion
        inst.demand = np.full((3, 4, 1), 100.0, dtype=np.float64)

        y = np.array([True, False, False, False])
        q = np.array([5000, 0, 0, 0])
        sol = decoder.decode(y, q, inst)

        # Pechuga: prod dia 0 = 0.40 * 2.5 * 5000 = 5000
        assert sol.p[0, 0] == 5000.0
        assert sol.I[0, 0, 0] > 0  # dia 0: hay stock fresco
        assert sol.I[0, 1, 0] > 0  # dia 1: aun fresco (edad 1 < L=2)
        assert sol.I[0, 2, 0] == 0  # dia 2: vencido (edad 2 >= L), descartado
        assert sol.I[0, 3, 0] == 0

        # La factibilidad ahora refleja la cota real de perecibilidad del MILP
        perish = constraints.check_perishability(sol, inst)
        assert perish.satisfied, perish.violations[:3]


class TestDemandCapDecoder:

    def test_cap_limits_production_to_demand_window(self):
        """Con demand_cap, la produccion no excede la demanda esperada de la
        ventana de vida util (mas el factor de seguridad)."""
        inst = make_trivial()
        inst.n_periods = 4
        inst.shelf_life = np.array([2, 2, 30], dtype=np.int32)
        inst.demand = np.full((3, 4, 1), 100.0, dtype=np.float64)

        y = np.array([True, False, False, False])
        q = np.array([5000, 0, 0, 0])

        sol_free = decoder.decode(y, q, inst)
        sol_cap = decoder.decode(y, q, inst, demand_cap=True)

        # Sin tope: agota el pool (pechuga = 0.4*2.5*5000 = 5000)
        assert sol_free.p[0, 0] == 5000.0
        # Con tope: ventana L=2 con demanda esperada 100/dia -> 200
        assert sol_cap.p[0, 0] == pytest.approx(200.0, abs=1e-6)

    def test_cap_improves_or_matches_objective(self):
        """El tope evita inventario invendible: Z no puede empeorar en un
        escenario de demanda baja y constante."""
        from src.model import objective

        inst = make_trivial()
        inst.n_periods = 4
        inst.shelf_life = np.array([2, 2, 30], dtype=np.int32)
        inst.demand = np.full((3, 4, 1), 100.0, dtype=np.float64)

        y = np.array([True, True, True, True])
        q = np.array([5000, 5000, 5000, 5000])

        z_free = objective.evaluate(decoder.decode(y, q, inst), inst).total
        z_cap = objective.evaluate(
            decoder.decode(y, q, inst, demand_cap=True), inst
        ).total

        assert z_cap >= z_free
        # y el inventario cae
        inv_free = float(np.mean(decoder.decode(y, q, inst).I))
        inv_cap = float(np.mean(decoder.decode(y, q, inst, demand_cap=True).I))
        assert inv_cap < inv_free

    def test_cap_default_off_preserves_behavior(self):
        """Sin el flag, el decoder se comporta exactamente igual que antes."""
        inst = make_trivial()
        y = np.array([True, False, False])
        q = np.array([5000, 0, 0])
        a = decoder.decode(y, q, inst)
        b = decoder.decode(y, q, inst, demand_cap=False)
        assert np.allclose(a.p, b.p)
        assert np.allclose(a.v, b.v)


class TestMaterialBalanceWithSpoilage:

    def test_spoilage_is_not_a_violation(self):
        """El inventario que cae por caducidad NO viola el balance (Eq.2):
        el balance real es I[t] = I[t-1] + p - v - merma."""
        inst = make_trivial()
        inst.n_periods = 4
        inst.shelf_life = np.array([2, 2, 30], dtype=np.int32)
        inst.demand = np.full((3, 4, 1), 100.0, dtype=np.float64)

        y = np.array([True, False, False, False])
        q = np.array([5000, 0, 0, 0])
        sol = decoder.decode(y, q, inst)

        # Hay merma real (pechuga vence en t=2) pero el balance debe pasar
        assert sol.I[0, 2, 0] == 0.0
        res = constraints.check_material_balance(sol, inst)
        assert res.satisfied, res.violations[:3]

    def test_phantom_inventory_is_caught(self):
        """Inventario POR ENCIMA del balance sin merma sí es violación."""
        inst = make_trivial()
        y = np.array([True, False, False])
        q = np.array([5000, 0, 0])
        sol = decoder.decode(y, q, inst)
        # Inyectar inventario fantasma en t=1
        sol.I[0, 1, 0] += 1000.0
        res = constraints.check_material_balance(sol, inst)
        assert not res.satisfied

    def test_no_spoilage_still_exact(self):
        """Sin merma (vida util larga) el balance sigue siendo exacto."""
        inst = make_trivial()
        inst.shelf_life = np.array([30, 30, 30], dtype=np.int32)
        y = np.array([True, True, False])
        q = np.array([3000, 4000, 0])
        sol = decoder.decode(y, q, inst)
        res = constraints.check_material_balance(sol, inst)
        assert res.satisfied, res.violations[:3]


class TestSecondStageEquivalence:
    """La simulacion vectorizada debe ser identica a la de bucles."""

    def _assert_equivalent(self, p, inst):
        v1, i1, u1 = decoder._second_stage_loop(p, inst)
        v2, i2, u2 = decoder._second_stage_vectorized(p, inst)
        np.testing.assert_allclose(v1, v2, atol=1e-9)
        np.testing.assert_allclose(i1, i2, atol=1e-9)
        np.testing.assert_allclose(u1, u2, atol=1e-9)

    def test_equivalence_trivial(self):
        inst = make_trivial()
        y = np.array([True, True, False])
        q = np.array([3000, 4000, 0])
        sol = decoder.decode(y, q, inst)
        self._assert_equivalent(sol.p, inst)

    def test_equivalence_short_shelf_life(self):
        inst = make_trivial()
        inst.n_periods = 5
        inst.shelf_life = np.array([1, 2, 3], dtype=np.int32)
        inst.demand = np.random.RandomState(7).uniform(
            50, 4000, size=(3, 5, 4)
        )
        inst.n_scenarios = 4
        inst.scenario_probs = np.ones(4) / 4
        p = np.random.RandomState(11).uniform(0, 3000, size=(3, 5))
        self._assert_equivalent(p, inst)

    def test_equivalence_real_instance(self):
        from pathlib import Path

        path = Path("data/instances/small_seed42.yaml")
        if not path.exists():
            pytest.skip("instancia no encontrada")
        inst = ProblemInstance.from_yaml(path)
        rng = np.random.RandomState(3)
        q = rng.randint(
            inst.capacity_min, inst.capacity_max + 1, size=inst.n_periods
        )
        y = rng.random(inst.n_periods) > 0.3
        sol = decoder.decode(y, q, inst, demand_cap=True)
        self._assert_equivalent(sol.p, inst)


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
