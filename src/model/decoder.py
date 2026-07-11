"""
Greedy decoder:
given first-stage decisions (y, q), compute second-stage variables (v, I, u).

This decoder includes explicit part allocation per period to avoid double
counting when cut forms share anatomical parts.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from src.model.parameters import ProblemInstance

from src.model.solution import Solution

TOL = 1e-9


def decode(
    y: np.ndarray,
    q: np.ndarray,
    instance: ProblemInstance,
    demand_cap: bool = False,
    demand_cap_factor: float = 1.0,
) -> Solution:
    """Decode first-stage vectors into a complete solution with greedy logic.

    Production is assigned by part-pool feasibility:
    - Available anatomical mass at t: alpha[a] * weight * q[t]
    - Form production p[f,t] consumes required parts from that pool
    - Sales and inventory are then simulated per scenario with FIFO layers

    Args:
        demand_cap: If True, production of each form is additionally capped by
            the expected residual demand within its shelf-life window
            (newsvendor-style). Without the cap, the greedy exhausts the part
            pool in price order and stockpiles product the market cannot
            absorb, paying inventory (and spoilage) for nothing.
        demand_cap_factor: Safety multiplier on the demand window (>1 keeps a
            buffer against demand scenarios above the mean).
    """
    f_count = instance.n_cut_forms
    t_count = instance.n_periods
    w_count = instance.n_scenarios

    y_vec = np.array(y, dtype=bool)
    q_vec = np.array(q, dtype=np.int64)

    # Cut-form activation z[f,t] (fixed config or exclusivity-aware selection)
    z = _build_cut_activation(instance)

    # Expected demand per form-period (used only when demand_cap is enabled)
    if demand_cap:
        expected_demand = instance.demand.mean(axis=2)  # [F, T]
        # Expected carried inventory per form, tracked deterministically on
        # the mean-demand path. Expiry is ignored here on purpose: it only
        # lowers real inventory, so the cap stays slightly conservative.
        exp_inv = np.zeros(f_count, dtype=np.float64)
        shelf = instance.shelf_life.astype(np.int64)

    # Production by form-period (scenario independent): p[f,t]
    p = np.zeros((f_count, t_count), dtype=np.float64)
    priority_order = np.argsort(-instance.prices)

    for t in range(t_count):
        carcasses = int(q_vec[t]) if y_vec[t] else 0
        if carcasses > 0:
            # Available anatomical mass by part at period t
            part_pool = (
                instance.alpha.astype(np.float64) * instance.weight * carcasses
            )

            for f in priority_order:
                if not z[f, t]:
                    continue

                required_parts = np.where(instance.composition[f] > 0)[0]
                if required_parts.size == 0:
                    continue

                max_prod = float(np.min(part_pool[required_parts]))
                if demand_cap:
                    window_end = min(t + int(shelf[f]), t_count)
                    window_demand = float(
                        expected_demand[f, t:window_end].sum()
                    )
                    cap = max(
                        0.0, demand_cap_factor * window_demand - exp_inv[f]
                    )
                    max_prod = min(max_prod, cap)
                if max_prod <= TOL:
                    continue

                p[f, t] = max_prod
                part_pool[required_parts] -= max_prod
                part_pool = np.maximum(part_pool, 0.0)

        if demand_cap:
            # Avanzar el inventario esperado sobre la trayectoria media
            exp_inv = np.maximum(
                0.0, exp_inv + p[:, t] - expected_demand[:, t]
            )

    # Second stage: simulacion FIFO con caducidad, vectorizada sobre los
    # escenarios (la version por bucles se conserva como referencia para el
    # test de equivalencia).
    v, I, u = _second_stage_vectorized(p, instance)

    return Solution(
        y=y_vec,
        q=q_vec,
        p=p,
        z=z,
        v=v,
        I=I,
        u=u,
        algorithm="greedy_decoder",
    )


def _second_stage_vectorized(
    p: np.ndarray, instance: ProblemInstance
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Simular ventas/inventario/insatisfaccion para TODOS los escenarios.

    Equivalente exacto de la simulacion por capas FIFO con caducidad
    (_second_stage_loop), pero con las capas representadas como cubetas por
    periodo de produccion en un arreglo [W, F, T]: bucket[w, f, s] = cantidad
    remanente producida en el periodo s. La caducidad descarta cubetas con
    s <= t - L[f] y el consumo FIFO vacia primero las cubetas mas viejas via
    suma acumulada. Todo el trabajo por escenario se hace en NumPy, lo que
    acelera la evaluacion de fitness ~un orden de magnitud en instancias con
    muchos escenarios.
    """
    f_count = instance.n_cut_forms
    t_count = instance.n_periods
    w_count = instance.n_scenarios

    v = np.zeros((f_count, t_count, w_count), dtype=np.float64)
    I = np.zeros((f_count, t_count, w_count), dtype=np.float64)
    u = np.zeros((f_count, t_count, w_count), dtype=np.float64)

    shelf_life = instance.shelf_life.astype(np.int64)
    periods = np.arange(t_count)

    # bucket[w, f, s]: remanente de la produccion del periodo s
    buckets = np.zeros((w_count, f_count, t_count), dtype=np.float64)

    for t in range(t_count):
        # 0) Caducidad: descartar cubetas con s <= t - L[f]
        expired = periods[np.newaxis, :] <= (t - shelf_life[:, np.newaxis])
        buckets[:, expired] = 0.0

        # 1) Produccion del periodo (identica en todos los escenarios)
        buckets[:, :, t] = p[:, t][np.newaxis, :]

        # 2-3) Ventas greedy: el orden por precio no altera el resultado
        # porque cada forma tiene su propio pool de inventario
        demand_t = instance.demand[:, t, :].T  # [W, F]
        available = buckets.sum(axis=2)  # [W, F]
        sell = np.minimum(available, demand_t)  # [W, F]
        v[:, t, :] = sell.T
        u[:, t, :] = (demand_t - sell).T

        # Consumo FIFO: las cubetas mas viejas (s menor) se vacian primero.
        # cum_before[w,f,s] = inventario en cubetas mas viejas que s
        cum = np.cumsum(buckets, axis=2)
        cum_before = cum - buckets
        consumed = np.clip(sell[:, :, np.newaxis] - cum_before, 0.0, buckets)
        buckets -= consumed

        # 4) Inventario de fin de periodo
        I[:, t, :] = buckets.sum(axis=2).T

    return v, I, u


def _second_stage_loop(
    p: np.ndarray, instance: ProblemInstance
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Version de referencia por bucles de la simulacion de segunda etapa.

    Conservada para el test de equivalencia con _second_stage_vectorized.
    """
    f_count = instance.n_cut_forms
    t_count = instance.n_periods
    w_count = instance.n_scenarios

    v = np.zeros((f_count, t_count, w_count), dtype=np.float64)
    I = np.zeros((f_count, t_count, w_count), dtype=np.float64)
    u = np.zeros((f_count, t_count, w_count), dtype=np.float64)

    shelf_life = instance.shelf_life.astype(np.int64)
    priority_order = np.argsort(-instance.prices)

    for w in range(w_count):
        # Capas [periodo_produccion, cantidad] FIFO; las capas mas viejas que
        # la vida util se descartan (misma cota Eq.7 que impone el MILP).
        inv_layers: list[list[list[float]]] = [[] for _ in range(f_count)]

        for t in range(t_count):
            for f in range(f_count):
                l_f = int(shelf_life[f])
                oldest_valid = t - l_f + 1
                if inv_layers[f]:
                    inv_layers[f] = [
                        layer for layer in inv_layers[f] if layer[0] >= oldest_valid
                    ]

            for f in range(f_count):
                prod_ft = p[f, t]
                if prod_ft > TOL:
                    inv_layers[f].append([float(t), float(prod_ft)])

            available = np.zeros(f_count, dtype=np.float64)
            for f in range(f_count):
                available[f] = float(sum(layer[1] for layer in inv_layers[f]))

            for f in priority_order:
                demand_ftw = float(instance.demand[f, t, w])
                sell = min(available[f], demand_ftw)
                v[f, t, w] = sell
                u[f, t, w] = demand_ftw - sell

                remaining_to_sell = sell
                new_layers: list[list[float]] = []
                for layer in inv_layers[f]:
                    s_period, qty = layer
                    if remaining_to_sell <= TOL:
                        new_layers.append(layer)
                    elif qty <= remaining_to_sell + TOL:
                        remaining_to_sell -= qty
                    else:
                        new_layers.append([s_period, qty - remaining_to_sell])
                        remaining_to_sell = 0.0
                inv_layers[f] = new_layers

            for f in range(f_count):
                I[f, t, w] = float(sum(layer[1] for layer in inv_layers[f]))

    return v, I, u


def _build_cut_activation(instance: ProblemInstance) -> np.ndarray:
    """Build cut-form activation matrix z[f,t].

    - Fixed cut_config: constant across all periods
    - Variable cut_config: all forms active by default, and each exclusivity
      group selects one form per period using expected revenue potential.
    """
    f_count = instance.n_cut_forms
    t_count = instance.n_periods

    if instance.cut_config is not None:
        return np.tile(instance.cut_config.astype(bool)[:, np.newaxis], (1, t_count))

    z = np.ones((f_count, t_count), dtype=bool)
    if not instance.exclusivity_groups:
        return z

    expected_demand = np.einsum("ftw,w->ft", instance.demand, instance.scenario_probs)

    for t in range(t_count):
        for group in instance.exclusivity_groups:
            forms = list(group.cut_form_indices)
            if len(forms) <= 1:
                continue

            scores = instance.prices[forms] * expected_demand[forms, t]
            selected = forms[int(np.argmax(scores))]

            z[forms, t] = False
            z[selected, t] = True

    return z
