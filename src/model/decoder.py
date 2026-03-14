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
) -> Solution:
    """Decode first-stage vectors into a complete solution with greedy logic.

    Production is assigned by part-pool feasibility:
    - Available anatomical mass at t: alpha[a] * weight * q[t]
    - Form production p[f,t] consumes required parts from that pool
    - Sales and inventory are then simulated per scenario with FIFO layers
    """
    f_count = instance.n_cut_forms
    t_count = instance.n_periods
    w_count = instance.n_scenarios

    y_vec = np.array(y, dtype=bool)
    q_vec = np.array(q, dtype=np.int64)

    # Cut-form activation z[f,t] (fixed config or exclusivity-aware selection)
    z = _build_cut_activation(instance)

    # Production by form-period (scenario independent): p[f,t]
    p = np.zeros((f_count, t_count), dtype=np.float64)
    priority_order = np.argsort(-instance.prices)

    for t in range(t_count):
        carcasses = int(q_vec[t]) if y_vec[t] else 0
        if carcasses <= 0:
            continue

        # Available anatomical mass by part at period t
        part_pool = instance.alpha.astype(np.float64) * instance.weight * carcasses

        for f in priority_order:
            if not z[f, t]:
                continue

            required_parts = np.where(instance.composition[f] > 0)[0]
            if required_parts.size == 0:
                continue

            max_prod = float(np.min(part_pool[required_parts]))
            if max_prod <= TOL:
                continue

            p[f, t] = max_prod
            part_pool[required_parts] -= max_prod
            part_pool = np.maximum(part_pool, 0.0)

    # Second-stage arrays
    v = np.zeros((f_count, t_count, w_count), dtype=np.float64)
    I = np.zeros((f_count, t_count, w_count), dtype=np.float64)
    u = np.zeros((f_count, t_count, w_count), dtype=np.float64)

    for w in range(w_count):
        # Inventory layers per form (FIFO by production period).
        # Keep quantities only: explicit spoilage is not modeled in Eq.2.
        inv_layers: list[list[float]] = [[] for _ in range(f_count)]

        for t in range(t_count):
            # 1) Add current-period production
            for f in range(f_count):
                prod_ft = p[f, t]
                if prod_ft > TOL:
                    inv_layers[f].append(float(prod_ft))

            # 2) Available inventory by form
            available = np.zeros(f_count, dtype=np.float64)
            for f in range(f_count):
                available[f] = float(sum(inv_layers[f]))

            # 3) Greedy sales by descending price
            for f in priority_order:
                demand_ftw = float(instance.demand[f, t, w])
                sell = min(available[f], demand_ftw)
                v[f, t, w] = sell
                u[f, t, w] = demand_ftw - sell

                # FIFO consumption: oldest layers are at the front
                remaining_to_sell = sell
                new_layers: list[float] = []
                for layer in inv_layers[f]:
                    if remaining_to_sell <= TOL:
                        new_layers.append(layer)
                    elif layer <= remaining_to_sell + TOL:
                        remaining_to_sell -= layer
                    else:
                        layer -= remaining_to_sell
                        remaining_to_sell = 0.0
                        new_layers.append(layer)
                inv_layers[f] = new_layers

            # 4) End-of-period inventory
            for f in range(f_count):
                I[f, t, w] = float(sum(inv_layers[f]))

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
