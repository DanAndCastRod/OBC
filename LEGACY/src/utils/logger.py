"""
DLBP Avícola - Módulo de Logging Estructurado
==============================================
Proporciona configuración de logging consistente para todo el proyecto.

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: Mejoras - Documentación Técnica
"""

import logging
import sys
from datetime import datetime
from typing import Optional


def configurar_logger(
    nombre: str,
    nivel: int = logging.INFO,
    archivo: Optional[str] = None
) -> logging.Logger:
    """
    Configura un logger con formato estándar.
    
    Args:
        nombre: Nombre del logger (ej: 'GA', 'TS', 'Hybrid')
        nivel: Nivel de logging (default: INFO)
        archivo: Ruta opcional para guardar logs a archivo
        
    Returns:
        Logger configurado
        
    Ejemplo:
        >>> from utils.logger import configurar_logger
        >>> logger = configurar_logger('GA')
        >>> logger.info("Generación 1: fitness = 5")
    """
    logger = logging.getLogger(nombre)
    logger.setLevel(nivel)
    
    # Evitar duplicación de handlers
    if logger.handlers:
        return logger
    
    # Formato estándar
    formato = logging.Formatter(
        '%(asctime)s | %(name)-10s | %(levelname)-7s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Handler para consola
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(nivel)
    ch.setFormatter(formato)
    logger.addHandler(ch)
    
    # Handler para archivo (opcional)
    if archivo:
        fh = logging.FileHandler(archivo, encoding='utf-8')
        fh.setLevel(nivel)
        fh.setFormatter(formato)
        logger.addHandler(fh)
    
    return logger


def log_experimento(
    logger: logging.Logger,
    algoritmo: str,
    iteracion: int,
    fitness: float,
    tiempo: float,
    extra: Optional[dict] = None
):
    """
    Registra una iteración de experimento con formato estándar.
    
    Args:
        logger: Logger configurado
        algoritmo: Nombre del algoritmo
        iteracion: Número de iteración/generación
        fitness: Valor de fitness actual
        tiempo: Tiempo transcurrido
        extra: Datos adicionales opcionales
    """
    msg = f"Iter {iteracion:4d} | Fitness: {fitness:.2f} | Tiempo: {tiempo:.3f}s"
    if extra:
        extras = " | ".join(f"{k}={v}" for k, v in extra.items())
        msg += f" | {extras}"
    logger.info(msg)


def log_resumen(
    logger: logging.Logger,
    algoritmo: str,
    mejor_fitness: float,
    tiempo_total: float,
    iteraciones: int
):
    """
    Registra resumen final de una ejecución.
    """
    logger.info("=" * 50)
    logger.info(f"RESUMEN {algoritmo}")
    logger.info(f"  Mejor fitness: {mejor_fitness:.2f}")
    logger.info(f"  Tiempo total:  {tiempo_total:.2f}s")
    logger.info(f"  Iteraciones:   {iteraciones}")
    logger.info("=" * 50)


# Logger global del proyecto
_logger_proyecto = None

def get_logger() -> logging.Logger:
    """Obtiene el logger global del proyecto."""
    global _logger_proyecto
    if _logger_proyecto is None:
        _logger_proyecto = configurar_logger('DLBP')
    return _logger_proyecto


if __name__ == "__main__":
    # Demo del módulo
    logger = configurar_logger('Demo', nivel=logging.DEBUG)
    
    logger.debug("Mensaje de depuración")
    logger.info("Iniciando algoritmo...")
    
    log_experimento(logger, "GA", 1, 10.5, 0.234, {"poblacion": 50})
    log_experimento(logger, "GA", 2, 9.2, 0.456, {"poblacion": 50})
    log_experimento(logger, "GA", 3, 8.0, 0.678)
    
    log_resumen(logger, "GA", 8.0, 1.368, 3)
    
    logger.warning("Advertencia de prueba")
    logger.error("Error de prueba (esto es solo demo)")
    
    print("\n[OK] Módulo de logging funcionando correctamente")
