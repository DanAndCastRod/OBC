"""Tests de la decisión de despiece de un solo periodo (src/planning)."""

import numpy as np
import pytest

from src.planning import (
    BirdProfile,
    CommercialItem,
    FlockMix,
    PERFILES_ESTANDAR,
    catalogo_despiece_default,
    optimizar_despiece,
)


class TestBirdProfile:

    def test_alpha_debe_sumar_uno(self):
        with pytest.raises(ValueError):
            BirdProfile("malo", 2.5, ("a", "b"), (0.3, 0.3))

    def test_masa_por_carcasa(self):
        p = PERFILES_ESTANDAR["estándar"]
        masa = p.part_mass_per_carcass()
        assert masa.sum() == pytest.approx(p.weight_kg, rel=1e-9)
        # pechuga = 0.30 * 2.5 = 0.75 kg
        assert masa[0] == pytest.approx(0.75, rel=1e-9)


class TestFlockMix:

    def test_part_pool_perfil_unico(self):
        flock = FlockMix.single(PERFILES_ESTANDAR["estándar"], 1000)
        pool = flock.part_pool()
        assert pool.sum() == pytest.approx(1000 * 2.5, rel=1e-9)

    def test_mezcla_por_fracciones(self):
        flock = FlockMix.from_fractions(
            1000, {"liviano": 0.3, "estándar": 0.5, "pesado": 0.2}
        )
        assert flock.total_carcasses == pytest.approx(1000)
        # masa = 300*2.0 + 500*2.5 + 200*3.0 = 600 + 1250 + 600 = 2450 kg
        assert flock.part_pool().sum() == pytest.approx(2450, rel=1e-9)

    def test_fracciones_deben_sumar_uno(self):
        with pytest.raises(ValueError):
            FlockMix.from_fractions(1000, {"liviano": 0.3, "estándar": 0.3})


class TestOptimizarDespiece:

    def test_respeta_disponibilidad_anatomica(self):
        flock = FlockMix.single(PERFILES_ESTANDAR["estándar"], 1000)
        plan = optimizar_despiece(flock, catalogo_despiece_default())
        assert plan.status == "Optimal"
        # No se puede usar más masa de una pieza que la disponible
        for part in plan.part_pool_kg:
            assert plan.part_used_kg[part] <= plan.part_pool_kg[part] + 1e-6

    def test_competencia_por_masa_sin_doble_conteo(self):
        """Pernil y cortes individuales comparten piezas: el uso de muslo y
        contramuslo no puede exceder su disponibilidad aunque haya varios
        cortes que los usen (la restricción de part_pool evita doble conteo)."""
        flock = FlockMix.single(PERFILES_ESTANDAR["estándar"], 1000)
        plan = optimizar_despiece(flock, catalogo_despiece_default())
        assert plan.part_used_kg["muslo"] <= plan.part_pool_kg["muslo"] + 1e-6
        assert plan.part_used_kg["contramuslo"] <= plan.part_pool_kg["contramuslo"] + 1e-6
        # Con los precios por defecto conviene deshuesar (no producir pernil)
        assert plan.produced_kg["Pernil completo"] <= 1e-6

    def test_exclusividad_comercial_opcional(self):
        """Si se asigna el mismo grupo de exclusividad, a lo sumo un corte del
        grupo puede activarse."""
        flock = FlockMix.single(PERFILES_ESTANDAR["estándar"], 1000)
        items = catalogo_despiece_default()
        for it in items:
            if it.name in ("Pernil completo", "Muslo", "Contramuslo"):
                it.exclusivity_group = "pierna"
        plan = optimizar_despiece(flock, items)
        activos = sum(
            plan.produced_kg[n] > 1e-6 for n in ("Pernil completo", "Muslo", "Contramuslo")
        )
        assert activos <= 1

    def test_perfil_pesado_da_mas_pechuga(self):
        """Un ave más pesada rinde proporcionalmente más pechuga."""
        n = 1000
        liviano = optimizar_despiece(
            FlockMix.single(PERFILES_ESTANDAR["liviano"], n), catalogo_despiece_default()
        )
        pesado = optimizar_despiece(
            FlockMix.single(PERFILES_ESTANDAR["pesado"], n), catalogo_despiece_default()
        )
        assert pesado.sold_kg["Pechuga"] > liviano.sold_kg["Pechuga"]
        # y mayor masa total => mayor utilidad
        assert pesado.profit > liviano.profit

    def test_demanda_limita_ventas(self):
        flock = FlockMix.single(PERFILES_ESTANDAR["estándar"], 1000)
        items = catalogo_despiece_default()
        for it in items:
            if it.name == "Pechuga":
                it.demand_kg = 100.0
        plan = optimizar_despiece(flock, items)
        assert plan.sold_kg["Pechuga"] <= 100.0 + 1e-6

    def test_composition_longitud_invalida(self):
        flock = FlockMix.single(PERFILES_ESTANDAR["estándar"], 1000)
        malo = [CommercialItem("X", (1, 0, 0), 1000.0)]  # 3 piezas, se esperan 6
        with pytest.raises(ValueError):
            optimizar_despiece(flock, malo)
