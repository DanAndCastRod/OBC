"""Herramientas de planeación operativa basadas en el modelo de coproductos.

Este paquete ofrece capacidades de *decisión de despiece* de un solo periodo,
pensadas para uso práctico en planta: dado un perfil (o mezcla) de pollo y un
mix comercial (pedidos y precios), calcula el plan de despiece que maximiza la
utilidad respetando la disponibilidad anatómica y las exclusividades de corte.

A diferencia del pipeline experimental de la tesis (multi-periodo, estocástico,
resuelto con metaheurísticas), aquí el problema de un día con pedidos conocidos
es pequeño y se resuelve de forma exacta.
"""

from src.planning.despiece import (
    BirdProfile,
    CommercialItem,
    DespiecePlan,
    FlockMix,
    PERFILES_ESTANDAR,
    catalogo_despiece_default,
    optimizar_despiece,
)

__all__ = [
    "BirdProfile",
    "FlockMix",
    "CommercialItem",
    "DespiecePlan",
    "PERFILES_ESTANDAR",
    "catalogo_despiece_default",
    "optimizar_despiece",
]
