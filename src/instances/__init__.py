"""Paquete de generacion de instancias para el problema de coproductos."""

from src.instances.distributions import (
    add_seasonality,
    generate_demand_lognormal,
    generate_demand_normal,
    generate_scenarios,
)
from src.instances.generator import InstanceGenerator

__all__ = [
    "InstanceGenerator",
    "generate_demand_normal",
    "generate_demand_lognormal",
    "generate_scenarios",
    "add_seasonality",
]
