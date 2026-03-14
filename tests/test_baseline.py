"""
Tests para baseline y metricas experimentales (Sprint 4.1).

Verifica:
- Baseline proporcional genera soluciones factibles
- Baseline max-capacity genera soluciones factibles
- Z > 0 para ambas heuristicas
- Metricas se calculan correctamente
- Configs YAML se cargan sin errores
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

sys.path.insert(0, ".")

from experiments.scripts.baseline import (
    _compute_max_capacity_q,
    _compute_proportional_q,
    solve_baseline,
)
from experiments.scripts.metrics import (
    ExperimentMetrics,
    compute_all_metrics,
    compute_avg_inventory,
    compute_gap,
    compute_low_rotation_inventory,
    compute_service_level,
)
from src.model import constraints
from src.model.parameters import ProblemInstance

# ============================================================
# Fixtures
# ============================================================

INSTANCE_DIR = Path("data/instances")


@pytest.fixture
def toy_instance():
    """Cargar instancia toy para tests rapidos."""
    path = INSTANCE_DIR / "toy_seed42.yaml"
    if not path.exists():
        pytest.skip(f"Instancia {path} no encontrada")
    return ProblemInstance.from_yaml(path)


@pytest.fixture
def small_instance():
    """Cargar instancia small para tests."""
    path = INSTANCE_DIR / "small_seed42.yaml"
    if not path.exists():
        pytest.skip(f"Instancia {path} no encontrada")
    return ProblemInstance.from_yaml(path)


# ============================================================
# Tests de Baseline
# ============================================================


class TestBaselineProportional:
    """Tests para la heuristica baseline proporcional."""

    def test_generates_valid_q(self, toy_instance):
        """q_t debe estar dentro de [Q_min, Q_max]."""
        q = _compute_proportional_q(toy_instance)
        assert len(q) == toy_instance.n_periods
        for t in range(toy_instance.n_periods):
            assert q[t] >= toy_instance.capacity_min
            assert q[t] <= toy_instance.capacity_max

    def test_solution_is_feasible(self, toy_instance):
        """Solucion proporcional debe ser factible."""
        sol = solve_baseline(toy_instance, strategy="proportional")
        assert sol.is_feasible, f"Violaciones: {sol.check_feasibility(toy_instance)}"

    def test_passes_all_constraints(self, toy_instance):
        """Solucion proporcional debe pasar check_all."""
        sol = solve_baseline(toy_instance, strategy="proportional")
        assert constraints.all_satisfied(sol, toy_instance)

    def test_positive_z(self, toy_instance):
        """Z debe ser positivo (hay ingresos)."""
        sol = solve_baseline(toy_instance, strategy="proportional")
        assert sol.objective_value > 0, f"Z={sol.objective_value}"

    def test_algorithm_name(self, toy_instance):
        """Nombre del algoritmo debe ser 'baseline-proportional'."""
        sol = solve_baseline(toy_instance, strategy="proportional")
        assert sol.algorithm == "baseline-proportional"


class TestBaselineMaxCapacity:
    """Tests para la heuristica baseline max-capacity."""

    def test_generates_max_q(self, toy_instance):
        """q_t debe ser Q_max para todos los periodos."""
        q = _compute_max_capacity_q(toy_instance)
        assert len(q) == toy_instance.n_periods
        assert np.all(q == toy_instance.capacity_max)

    def test_solution_is_feasible(self, toy_instance):
        """Solucion max-capacity debe ser factible."""
        sol = solve_baseline(toy_instance, strategy="max_capacity")
        assert sol.is_feasible, f"Violaciones: {sol.check_feasibility(toy_instance)}"

    def test_passes_all_constraints(self, toy_instance):
        """Solucion max-capacity debe pasar check_all."""
        sol = solve_baseline(toy_instance, strategy="max_capacity")
        assert constraints.all_satisfied(sol, toy_instance)

    def test_positive_z(self, toy_instance):
        """Z debe ser positivo."""
        sol = solve_baseline(toy_instance, strategy="max_capacity")
        assert sol.objective_value > 0, f"Z={sol.objective_value}"

    def test_algorithm_name(self, toy_instance):
        """Nombre del algoritmo debe ser 'baseline-max'."""
        sol = solve_baseline(toy_instance, strategy="max_capacity")
        assert sol.algorithm == "baseline-max"


class TestBaselineBest:
    """Tests para la seleccion automatica del mejor baseline."""

    def test_selects_best(self, toy_instance):
        """'best' debe retornar la solucion con mayor Z."""
        sol_prop = solve_baseline(toy_instance, strategy="proportional")
        sol_max = solve_baseline(toy_instance, strategy="max_capacity")
        sol_best = solve_baseline(toy_instance, strategy="best")

        expected_z = max(sol_prop.objective_value, sol_max.objective_value)
        assert abs(sol_best.objective_value - expected_z) < 1e-6

    def test_is_feasible(self, toy_instance):
        """Mejor baseline debe ser factible."""
        sol = solve_baseline(toy_instance, strategy="best")
        assert sol.is_feasible


# ============================================================
# Tests de Metricas
# ============================================================


class TestMetrics:
    """Tests para el modulo de metricas."""

    def test_gap_normal(self):
        """Gap con valores normales."""
        assert abs(compute_gap(95.0, 100.0) - 5.0) < 1e-9
        assert abs(compute_gap(100.0, 100.0) - 0.0) < 1e-9

    def test_gap_zero_reference(self):
        """Gap con referencia 0 retorna NaN."""
        assert math.isnan(compute_gap(50.0, 0.0))

    def test_gap_nan_reference(self):
        """Gap con referencia NaN retorna NaN."""
        assert math.isnan(compute_gap(50.0, float("nan")))

    def test_service_level_range(self, toy_instance):
        """Nivel de servicio debe estar entre 0 y 100."""
        sol = solve_baseline(toy_instance, strategy="best")
        sl = compute_service_level(sol, toy_instance)
        assert 0.0 <= sl <= 100.0, f"service_level={sl}"

    def test_avg_inventory_non_negative(self, toy_instance):
        """Inventario promedio no debe ser negativo."""
        sol = solve_baseline(toy_instance, strategy="best")
        avg_inv = compute_avg_inventory(sol, toy_instance)
        assert avg_inv >= 0.0

    def test_low_rotation_non_negative(self, toy_instance):
        """Inventario baja rotacion no debe ser negativo."""
        sol = solve_baseline(toy_instance, strategy="best")
        low_rot = compute_low_rotation_inventory(sol, toy_instance)
        assert low_rot >= 0.0

    def test_compute_all_metrics(self, toy_instance):
        """compute_all_metrics retorna ExperimentMetrics valido."""
        sol = solve_baseline(toy_instance, strategy="best")
        m = compute_all_metrics(
            sol,
            toy_instance,
            z_reference=sol.objective_value * 1.1,
            elapsed_seconds=1.5,
            n_evaluations=100,
        )
        assert isinstance(m, ExperimentMetrics)
        assert m.z_value > 0
        assert 0 <= m.service_level <= 100
        assert m.avg_inventory >= 0
        assert m.elapsed_seconds == 1.5
        assert m.n_evaluations == 100
        assert m.is_feasible

    def test_metrics_to_dict(self, toy_instance):
        """to_dict retorna diccionario completo."""
        sol = solve_baseline(toy_instance, strategy="best")
        m = compute_all_metrics(sol, toy_instance)
        d = m.to_dict()
        required_keys = {
            "z_value",
            "gap_percent",
            "service_level",
            "avg_inventory",
            "low_rotation_inventory",
            "elapsed_seconds",
            "n_evaluations",
            "is_feasible",
        }
        assert required_keys == set(d.keys())


# ============================================================
# Tests de Configs YAML
# ============================================================


class TestConfigs:
    """Tests para los archivos de configuracion."""

    def test_comparison_yaml_loads(self):
        """comparison.yaml se carga sin errores."""
        path = Path("experiments/config/comparison.yaml")
        assert path.exists(), f"{path} no encontrado"
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        assert "experiment" in config
        assert "algorithms" in config
        assert "instances" in config
        assert config["experiment"]["n_replicas"] == 30
        assert len(config["experiment"]["seeds"]) == 30

    def test_comparison_has_all_algorithms(self):
        """comparison.yaml debe incluir los 6 algoritmos."""
        path = Path("experiments/config/comparison.yaml")
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        expected = {"ga", "sa", "de", "ga_sa", "cbc_exact", "baseline"}
        actual = set(config["algorithms"].keys())
        assert expected == actual, f"Faltan: {expected - actual}"

    def test_comparison_instances_exist(self):
        """Todas las instancias en comparison.yaml deben existir."""
        path = Path("experiments/config/comparison.yaml")
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        for size, paths in config["instances"].items():
            for inst_path in paths:
                assert Path(inst_path).exists(), f"Instancia {inst_path} no existe"

    def test_sensitivity_yaml_loads(self):
        """sensitivity.yaml se carga sin errores."""
        path = Path("experiments/config/sensitivity.yaml")
        assert path.exists(), f"{path} no encontrado"
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        assert "parameters" in config
        assert "algorithm" in config
        assert config["algorithm"] == "ga_sa"

    def test_sensitivity_base_instance_exists(self):
        """Instancia base de sensitivity.yaml debe existir."""
        path = Path("experiments/config/sensitivity.yaml")
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        inst_path = config["base_instance"]
        assert Path(inst_path).exists(), f"Instancia {inst_path} no existe"
