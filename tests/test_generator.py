"""
Tests para el generador de instancias (Sprint 3.1).

Verifica:
- Validez de instancias generadas (pasa validate())
- Propiedades matematicas (sum alpha=1, demanda>=0)
- Reproducibilidad con seed
- Todos los perfiles de tamano
- Perfiles de demanda
- Overrides de parametros
- Distribuciones de demanda

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 3.1
"""

import numpy as np
import pytest

from src.instances.distributions import (
    add_seasonality,
    generate_demand_lognormal,
    generate_demand_normal,
    generate_scenarios,
)
from src.instances.generator import (
    DEMAND_PROFILES,
    SIZE_PROFILES,
    InstanceGenerator,
    ProductCatalog,
)

# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def gen():
    """InstanceGenerator fresh."""
    return InstanceGenerator()


# ============================================================
# Distributions tests
# ============================================================


class TestDistributions:
    """Tests para funciones de distribucion de demanda."""

    def test_normal_non_negative(self):
        """Demanda Normal truncada siempre >= 0."""
        rng = np.random.RandomState(42)
        d = generate_demand_normal(1000, 0.5, 1000, rng)
        assert np.all(d >= 0)

    def test_normal_shape(self):
        """Forma correcta de la salida."""
        rng = np.random.RandomState(42)
        d = generate_demand_normal(1000, 0.2, 50, rng)
        assert d.shape == (50,)

    def test_normal_mean_approximation(self):
        """Media muestral cercana a la poblacional (tol=10%)."""
        rng = np.random.RandomState(42)
        d = generate_demand_normal(5000, 0.1, 10000, rng)
        assert abs(d.mean() - 5000) / 5000 < 0.10

    def test_lognormal_positive(self):
        """LogNormal siempre > 0."""
        rng = np.random.RandomState(42)
        d = generate_demand_lognormal(1000, 0.5, 1000, rng)
        assert np.all(d > 0)

    def test_lognormal_shape(self):
        """Forma correcta."""
        rng = np.random.RandomState(42)
        d = generate_demand_lognormal(1000, 0.2, 50, rng)
        assert d.shape == (50,)

    def test_lognormal_mean_approximation(self):
        """Media muestral cercana (LogNormal converge mas lento)."""
        rng = np.random.RandomState(42)
        d = generate_demand_lognormal(5000, 0.2, 50000, rng)
        assert abs(d.mean() - 5000) / 5000 < 0.10

    def test_lognormal_cv_zero(self):
        """CV=0 produce demanda constante."""
        rng = np.random.RandomState(42)
        d = generate_demand_lognormal(3000, 0.0, 20, rng)
        assert np.allclose(d, 3000)

    def test_seasonality_shape(self):
        """add_seasonality preserva forma."""
        base = np.ones(52) * 1000
        mod = add_seasonality(base, 0.3, 52)
        assert mod.shape == base.shape

    def test_seasonality_amplitude(self):
        """Estacionalidad crea variacion dentro de +/- amplitude."""
        base = np.ones(52) * 1000
        mod = add_seasonality(base, 0.3, 52)
        assert mod.max() <= 1300.01
        assert mod.min() >= 699.99

    def test_seasonality_zero_amplitude(self):
        """Amplitud 0 no cambia la demanda."""
        base = np.ones(52) * 1000
        mod = add_seasonality(base, 0.0, 52)
        assert np.allclose(mod, base)

    def test_seasonality_2d(self):
        """Estacionalidad funciona con array 2D [T, W]."""
        base = np.ones((12, 50)) * 1000
        mod = add_seasonality(base, 0.2, 12)
        assert mod.shape == (12, 50)

    def test_generate_scenarios_shape(self):
        """Pipeline completo genera forma correcta."""
        d = generate_scenarios(
            n_products=3,
            n_periods=4,
            n_scenarios=5,
            base_demands=np.array([1000, 800, 500]),
            cvs=np.array([0.1, 0.2, 0.3]),
        )
        assert d.shape == (3, 4, 5)

    def test_generate_scenarios_non_negative(self):
        """Pipeline produce demanda >= 0."""
        d = generate_scenarios(
            n_products=6,
            n_periods=12,
            n_scenarios=50,
            base_demands=np.array([4000, 3000, 1500, 1200, 2000, 1000]),
            cvs=np.array([0.1, 0.2, 0.25, 0.25, 0.3, 0.4]),
        )
        assert np.all(d >= 0)

    def test_generate_scenarios_with_seasonality(self):
        """Pipeline con estacionalidad genera forma correcta."""
        d = generate_scenarios(
            n_products=3,
            n_periods=52,
            n_scenarios=20,
            base_demands=np.array([1000, 800, 500]),
            cvs=np.array([0.1, 0.2, 0.3]),
            seasonality={"amplitude": 0.3, "period": 52, "phase_shift": 0.0},
        )
        assert d.shape == (3, 52, 20)
        assert np.all(d >= 0)

    def test_generate_scenarios_reproducible(self):
        """Misma seed produce mismos resultados."""
        args = dict(
            n_products=3,
            n_periods=4,
            n_scenarios=5,
            base_demands=np.array([1000, 800, 500]),
            cvs=np.array([0.1, 0.2, 0.3]),
        )
        d1 = generate_scenarios(seed=42, **args)
        d2 = generate_scenarios(seed=42, **args)
        assert np.array_equal(d1, d2)


# ============================================================
# ProductCatalog tests
# ============================================================


class TestProductCatalog:
    """Verificar integridad del catalogo de productos."""

    @pytest.mark.parametrize(
        "profile_fn",
        [
            ProductCatalog.toy,
            ProductCatalog.small,
            ProductCatalog.medium,
            ProductCatalog.large,
            ProductCatalog.industrial,
        ],
    )
    def test_alpha_sums_to_one(self, profile_fn):
        """sum(alpha) = 1 en todo catalogo."""
        cat = profile_fn()
        assert np.isclose(cat["alpha"].sum(), 1.0), f"sum(alpha) = {cat['alpha'].sum()}"

    @pytest.mark.parametrize(
        "profile_fn",
        [
            ProductCatalog.toy,
            ProductCatalog.small,
            ProductCatalog.large,
            ProductCatalog.industrial,
        ],
    )
    def test_composition_shape(self, profile_fn):
        """composition es [n_cut_forms, n_parts]."""
        cat = profile_fn()
        assert cat["composition"].shape == (cat["n_cut_forms"], cat["n_parts"])

    @pytest.mark.parametrize(
        "profile_fn",
        [
            ProductCatalog.toy,
            ProductCatalog.small,
            ProductCatalog.large,
            ProductCatalog.industrial,
        ],
    )
    def test_prices_positive(self, profile_fn):
        """Todos los precios > 0."""
        cat = profile_fn()
        assert np.all(cat["prices"] > 0)

    @pytest.mark.parametrize(
        "profile_fn",
        [
            ProductCatalog.toy,
            ProductCatalog.small,
            ProductCatalog.large,
            ProductCatalog.industrial,
        ],
    )
    def test_arrays_lengths(self, profile_fn):
        """Arrays economicos tienen longitud == n_cut_forms."""
        cat = profile_fn()
        n_f = cat["n_cut_forms"]
        assert len(cat["prices"]) == n_f
        assert len(cat["cost_inv"]) == n_f
        assert len(cat["cost_pen"]) == n_f
        assert len(cat["shelf_life"]) == n_f
        assert len(cat["base_demands"]) == n_f
        assert len(cat["cvs"]) == n_f


# ============================================================
# InstanceGenerator tests
# ============================================================


class TestInstanceGenerator:
    """Tests de generacion de instancias."""

    @pytest.mark.parametrize("profile", list(SIZE_PROFILES.keys()))
    def test_generates_valid_instance(self, gen, profile):
        """Instancia generada pasa validate() para cada perfil."""
        inst = gen.generate(size_profile=profile, seed=42)
        errors = inst.validate()
        assert errors == [], f"Errores en {profile}: {errors}"

    @pytest.mark.parametrize("profile", list(SIZE_PROFILES.keys()))
    def test_alpha_sums_to_one(self, gen, profile):
        """sum(alpha) == 1 en toda instancia generada."""
        inst = gen.generate(size_profile=profile, seed=42)
        assert np.isclose(inst.alpha.sum(), 1.0)

    @pytest.mark.parametrize("profile", list(SIZE_PROFILES.keys()))
    def test_demand_non_negative(self, gen, profile):
        """Demanda >= 0 en toda instancia generada."""
        inst = gen.generate(size_profile=profile, seed=42)
        assert np.all(inst.demand >= 0)

    @pytest.mark.parametrize("profile", list(SIZE_PROFILES.keys()))
    def test_demand_shape(self, gen, profile):
        """Demanda tiene forma [n_cut_forms, n_periods, n_scenarios]."""
        inst = gen.generate(size_profile=profile, seed=42)
        expected = (inst.n_cut_forms, inst.n_periods, inst.n_scenarios)
        assert inst.demand.shape == expected

    @pytest.mark.parametrize("profile", list(SIZE_PROFILES.keys()))
    def test_profile_dimensions(self, gen, profile):
        """Dimensiones coinciden con el perfil definido."""
        sp = SIZE_PROFILES[profile]
        cat = sp["catalog_fn"]()
        inst = gen.generate(size_profile=profile, seed=42)
        assert inst.n_cut_forms == cat["n_cut_forms"]
        assert inst.n_periods == sp["n_periods"]
        assert inst.n_scenarios == sp["n_scenarios"]

    def test_reproducibility_with_seed(self, gen):
        """Misma seed produce instancia identica."""
        i1 = gen.generate(size_profile="small", seed=42)
        i2 = gen.generate(size_profile="small", seed=42)
        assert np.array_equal(i1.demand, i2.demand)
        assert np.array_equal(i1.alpha, i2.alpha)
        assert np.array_equal(i1.prices, i2.prices)
        assert i1.name == i2.name

    def test_different_seeds_differ(self, gen):
        """Seeds distintas producen demanda diferente."""
        i1 = gen.generate(size_profile="small", seed=42)
        i2 = gen.generate(size_profile="small", seed=99)
        assert not np.array_equal(i1.demand, i2.demand)

    def test_name_format(self, gen):
        """Nombre sigue formato {profile}_seed{N}."""
        inst = gen.generate(size_profile="medium", seed=123)
        assert inst.name == "medium_seed123"

    def test_profile_attribute(self, gen):
        """Atributo profile se setea correctamente."""
        inst = gen.generate(size_profile="large", seed=42)
        assert inst.profile == "large"

    def test_seed_attribute(self, gen):
        """Atributo seed se preserva."""
        inst = gen.generate(size_profile="toy", seed=99)
        assert inst.seed == 99

    def test_capacity_constraints(self, gen):
        """capacity_min < capacity_max siempre."""
        for profile in SIZE_PROFILES:
            inst = gen.generate(size_profile=profile, seed=42)
            assert inst.capacity_min < inst.capacity_max

    def test_costs_less_than_prices(self, gen):
        """cost_inv < prices (sanity check economico)."""
        for profile in SIZE_PROFILES:
            inst = gen.generate(size_profile=profile, seed=42)
            assert np.all(inst.cost_inv < inst.prices)

    def test_scenario_probs_sum_one(self, gen):
        """sum(scenario_probs) == 1."""
        inst = gen.generate(size_profile="small", seed=42)
        assert np.isclose(inst.scenario_probs.sum(), 1.0)

    @pytest.mark.parametrize("dp", list(DEMAND_PROFILES.keys()))
    def test_demand_profiles(self, gen, dp):
        """Todos los perfiles de demanda generan instancias validas."""
        inst = gen.generate(
            size_profile="small",
            demand_profile=dp,
            seed=42,
        )
        errors = inst.validate()
        assert errors == [], f"Errores con demand_profile={dp}: {errors}"
        assert np.all(inst.demand >= 0)

    def test_override_n_periods(self, gen):
        """Override de n_periods funciona."""
        inst = gen.generate(size_profile="toy", n_periods=10, seed=42)
        assert inst.n_periods == 10
        assert inst.demand.shape[1] == 10

    def test_override_n_scenarios(self, gen):
        """Override de n_scenarios funciona."""
        inst = gen.generate(size_profile="toy", n_scenarios=30, seed=42)
        assert inst.n_scenarios == 30
        assert inst.demand.shape[2] == 30

    def test_override_capacity(self, gen):
        """Override de capacidad funciona."""
        inst = gen.generate(
            size_profile="toy",
            capacity_max=8000,
            capacity_min=200,
            seed=42,
        )
        assert inst.capacity_max == 8000
        assert inst.capacity_min == 200

    def test_normal_distribution(self, gen):
        """Distribucion Normal funciona."""
        inst = gen.generate(
            size_profile="toy",
            distribution="normal",
            seed=42,
        )
        errors = inst.validate()
        assert errors == []
        assert np.all(inst.demand >= 0)

    def test_invalid_size_profile(self, gen):
        """Perfil inexistente lanza ValueError."""
        with pytest.raises(ValueError, match="size_profile"):
            gen.generate(size_profile="nonexistent")

    def test_invalid_demand_profile(self, gen):
        """Perfil de demanda inexistente lanza ValueError."""
        with pytest.raises(ValueError, match="demand_profile"):
            gen.generate(demand_profile="nonexistent")

    def test_generate_set(self, gen):
        """generate_set() produce multiples instancias con seeds distintas."""
        instances = gen.generate_set(
            size_profile="toy",
            n_seeds=3,
            base_seed=100,
        )
        assert len(instances) == 3
        assert instances[0].seed == 100
        assert instances[1].seed == 101
        assert instances[2].seed == 102
        # Todas validas
        for inst in instances:
            assert inst.validate() == []
        # Demanda diferente
        assert not np.array_equal(instances[0].demand, instances[1].demand)

    def test_available_profiles(self):
        """available_profiles() retorna info correcta."""
        profiles = InstanceGenerator.available_profiles()
        assert "toy" in profiles
        assert "industrial" in profiles
        assert profiles["toy"]["n_cut_forms"] == 3
        assert profiles["industrial"]["n_cut_forms"] == 10

    def test_exclusivity_groups_valid(self, gen):
        """Grupos de exclusividad son coherentes con cut_config."""
        for profile in ["small", "medium", "large", "industrial"]:
            inst = gen.generate(size_profile=profile, seed=42)
            for group in inst.exclusivity_groups:
                if inst.cut_config is not None:
                    active = sum(
                        int(inst.cut_config[i]) for i in group.cut_form_indices
                    )
                    assert active <= 1, (
                        f"Grupo '{group.name}' en {profile}: "
                        f"{active} formas activas (max 1)"
                    )

    def test_shelf_life_positive(self, gen):
        """Vida util siempre > 0."""
        for profile in SIZE_PROFILES:
            inst = gen.generate(size_profile=profile, seed=42)
            assert np.all(inst.shelf_life > 0)

    def test_yaml_roundtrip(self, gen, tmp_path):
        """Instancia se serializa/deserializa correctamente."""
        inst = gen.generate(size_profile="small", seed=42)
        yaml_path = tmp_path / "test_instance.yaml"
        inst.to_yaml(yaml_path)

        loaded = ProblemInstance.from_yaml(yaml_path)
        assert loaded.name == inst.name
        assert loaded.n_cut_forms == inst.n_cut_forms
        assert loaded.n_periods == inst.n_periods
        assert loaded.n_scenarios == inst.n_scenarios
        assert np.allclose(loaded.demand, inst.demand)
        assert np.allclose(loaded.alpha, inst.alpha)


# Necesario para import de ProblemInstance en roundtrip test
from src.model.parameters import ProblemInstance
