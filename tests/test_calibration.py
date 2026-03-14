"""
Tests para el modulo de calibracion (Sprint 3.2).

Verifica:
- Coherencia interna de datos de calibracion
- Funcion calibrate_instance()
- Propiedades economicas (costos < precios)
- Capacidades (Q_min < Q_max)
- Correlacion entre coproductos

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 3.2
"""

import numpy as np
import pytest

from src.instances.calibration import (
    ANATOMICAL_PROPORTIONS,
    CAPACITY_REFERENCE,
    COST_REFERENCE,
    PRICE_RANGES_COP,
    SHELF_LIFE,
    WEIGHT_REFERENCE,
    calibrate_instance,
    get_default_correlation,
    validate_calibration_data,
)
from src.instances.generator import InstanceGenerator


@pytest.fixture
def gen():
    return InstanceGenerator()


# ============================================================
# Datos de calibracion
# ============================================================


class TestCalibrationData:
    """Tests para los diccionarios de referencia."""

    def test_anatomical_proportions_sum_one(self):
        """sum(alpha) == 1.0 exacto."""
        total = sum(ANATOMICAL_PROPORTIONS.values())
        assert abs(total - 1.0) < 1e-10

    def test_anatomical_proportions_all_positive(self):
        """Todas las proporciones > 0."""
        for name, val in ANATOMICAL_PROPORTIONS.items():
            assert val > 0, f"{name} = {val}"

    def test_prices_min_less_than_max(self):
        """min < max en todos los rangos de precios."""
        for name, pr in PRICE_RANGES_COP.items():
            assert pr["min"] < pr["max"], f"{name}: min={pr['min']} >= max={pr['max']}"

    def test_prices_default_in_range(self):
        """default esta entre min y max."""
        for name, pr in PRICE_RANGES_COP.items():
            assert (
                pr["min"] <= pr["default"] <= pr["max"]
            ), f"{name}: default {pr['default']} fuera de [{pr['min']}, {pr['max']}]"

    def test_costs_min_less_than_max(self):
        """min < max en costos."""
        for name, cr in COST_REFERENCE.items():
            assert cr["min"] < cr["max"], f"{name}: min >= max"

    def test_costs_default_in_range(self):
        """default entre min y max."""
        for name, cr in COST_REFERENCE.items():
            assert (
                cr["min"] <= cr["default"] <= cr["max"]
            ), f"{name}: default fuera de rango"

    def test_inv_cost_less_than_all_prices(self):
        """cost_inv < precio minimo de todos los productos."""
        cost_inv_max = COST_REFERENCE["cost_inv"]["max"]
        for name, pr in PRICE_RANGES_COP.items():
            assert (
                cost_inv_max < pr["min"]
            ), f"cost_inv max ({cost_inv_max}) >= {name} min ({pr['min']})"

    def test_capacity_q_min_less_than_q_max(self):
        """Q_min < Q_max en todas las capacidades."""
        for name, cap in CAPACITY_REFERENCE.items():
            assert (
                cap["Q_min"] < cap["Q_max"]
            ), f"{name}: Q_min ({cap['Q_min']}) >= Q_max ({cap['Q_max']})"

    def test_shelf_life_positive(self):
        """Vida util default > 0."""
        for name, sl in SHELF_LIFE.items():
            assert sl["default"] > 0, f"{name}: shelf_life <= 0"

    def test_shelf_life_min_less_than_max(self):
        """min <= max en vida util."""
        for name, sl in SHELF_LIFE.items():
            assert sl["min"] <= sl["max"], f"{name}: min > max"

    def test_weight_positive(self):
        """Peso default > 0."""
        assert WEIGHT_REFERENCE["default"] > 0

    def test_weight_range(self):
        """Peso en rango razonable (1-5 kg)."""
        assert 1.0 <= WEIGHT_REFERENCE["default"] <= 5.0

    def test_validate_calibration_data_passes(self):
        """validate_calibration_data() no reporta errores."""
        errors = validate_calibration_data()
        assert errors == [], f"Errores: {errors}"


# ============================================================
# calibrate_instance()
# ============================================================


class TestCalibrateInstance:
    """Tests para la funcion de calibracion."""

    def test_calibrated_instance_valid(self, gen):
        """Instancia calibrada pasa validate()."""
        inst = gen.generate(size_profile="small", seed=42)
        calibrated = calibrate_instance(inst)
        errors = calibrated.validate()
        assert errors == [], f"Errores: {errors}"

    def test_calibrate_preserves_demand(self, gen):
        """Calibracion no muta la demanda."""
        inst = gen.generate(size_profile="small", seed=42)
        calibrated = calibrate_instance(inst)
        assert np.array_equal(inst.demand, calibrated.demand)

    def test_calibrate_preserves_structure(self, gen):
        """Calibracion no muta estructura (formas, periodos, escenarios)."""
        inst = gen.generate(size_profile="medium", seed=42)
        calibrated = calibrate_instance(inst)
        assert calibrated.n_cut_forms == inst.n_cut_forms
        assert calibrated.n_periods == inst.n_periods
        assert calibrated.n_scenarios == inst.n_scenarios

    def test_calibrate_does_not_mutate_original(self, gen):
        """calibrate_instance() no muta la instancia original."""
        inst = gen.generate(size_profile="toy", seed=42)
        original_weight = inst.weight
        original_cost_prod = inst.cost_prod
        _ = calibrate_instance(inst, weight=3.0, cost_prod=9999)
        assert inst.weight == original_weight
        assert inst.cost_prod == original_cost_prod

    def test_calibrate_applies_overrides(self, gen):
        """Overrides se aplican correctamente."""
        inst = gen.generate(size_profile="toy", seed=42)
        calibrated = calibrate_instance(inst, weight=3.0, cost_prod=1800)
        assert calibrated.weight == 3.0
        assert calibrated.cost_prod == 1800

    def test_calibrate_applies_defaults(self, gen):
        """Sin overrides usa defaults de COST_REFERENCE."""
        inst = gen.generate(size_profile="toy", seed=42)
        calibrated = calibrate_instance(inst)
        assert calibrated.weight == WEIGHT_REFERENCE["default"]
        assert calibrated.cost_prod == COST_REFERENCE["cost_prod"]["default"]
        assert calibrated.cost_setup == COST_REFERENCE["cost_setup"]["default"]

    def test_calibrate_large_uses_large_capacity(self, gen):
        """Perfil large usa CAPACITY_REFERENCE['large']."""
        inst = gen.generate(size_profile="large", seed=42)
        calibrated = calibrate_instance(inst)
        assert calibrated.capacity_max == CAPACITY_REFERENCE["large"]["Q_max"]
        assert calibrated.capacity_min == CAPACITY_REFERENCE["large"]["Q_min"]

    def test_calibrate_invalid_source(self, gen):
        """Fuente invalida lanza ValueError."""
        inst = gen.generate(size_profile="toy", seed=42)
        with pytest.raises(ValueError, match="source"):
            calibrate_instance(inst, source="nonexistent")

    @pytest.mark.parametrize(
        "profile", ["toy", "small", "medium", "large", "industrial"]
    )
    def test_all_profiles_calibrate(self, gen, profile):
        """Todos los perfiles se calibran sin errores."""
        inst = gen.generate(size_profile=profile, seed=42)
        calibrated = calibrate_instance(inst)
        errors = calibrated.validate()
        assert errors == [], f"Errores calibrando {profile}: {errors}"

    def test_calibrated_costs_less_than_prices(self, gen):
        """cost_inv < prices despues de calibrar (sanity)."""
        inst = gen.generate(size_profile="small", seed=42)
        calibrated = calibrate_instance(inst)
        assert np.all(calibrated.cost_inv < calibrated.prices)


# ============================================================
# Correlacion
# ============================================================


class TestCorrelation:
    """Tests para la matriz de correlacion."""

    @pytest.mark.parametrize("n", [3, 6, 8, 10])
    def test_correlation_shape(self, n):
        """Forma correcta [n, n]."""
        corr = get_default_correlation(n)
        assert corr.shape == (n, n)

    @pytest.mark.parametrize("n", [3, 6, 8, 10])
    def test_correlation_diagonal_ones(self, n):
        """Diagonal = 1."""
        corr = get_default_correlation(n)
        assert np.allclose(np.diag(corr), 1.0)

    @pytest.mark.parametrize("n", [3, 6, 8, 10])
    def test_correlation_symmetric(self, n):
        """Matriz simetrica."""
        corr = get_default_correlation(n)
        assert np.allclose(corr, corr.T)

    @pytest.mark.parametrize("n", [3, 6, 8, 10])
    def test_correlation_positive_definite(self, n):
        """Definida positiva (Cholesky no falla)."""
        corr = get_default_correlation(n)
        np.linalg.cholesky(corr)  # throws if not PD

    def test_correlation_values_in_range(self):
        """Todos los valores entre -1 y 1."""
        corr = get_default_correlation(6)
        assert np.all(corr >= -1.0)
        assert np.all(corr <= 1.0)
