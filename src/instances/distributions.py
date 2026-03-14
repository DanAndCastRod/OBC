"""
Distribuciones de demanda para generacion de instancias.

Funciones para generar demanda estocastica con:
- Distribuciones Normal y LogNormal
- Estacionalidad (modulacion senoidal)
- Correlacion entre coproductos (Cholesky)

Referencia: La demanda avicola sigue patrones estacionales
(diciembre alto, enero-febrero bajo) con variabilidad dependiente
del producto (pechuga estable, alas/subproducto volatiles).

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 3.1
"""

from __future__ import annotations

import numpy as np


def generate_demand_normal(
    mean: float,
    cv: float,
    n_scenarios: int,
    rng: np.random.RandomState,
) -> np.ndarray:
    """Generar demanda con distribucion Normal truncada (>= 0).

    Args:
        mean: Demanda media (kg/periodo).
        cv: Coeficiente de variacion (std/mean).
        n_scenarios: Numero de escenarios.
        rng: Generador aleatorio con seed.

    Returns:
        Array [n_scenarios] con demanda >= 0.
    """
    std = cv * mean
    samples = rng.normal(mean, std, size=n_scenarios)
    return np.maximum(samples, 0.0)


def generate_demand_lognormal(
    mean: float,
    cv: float,
    n_scenarios: int,
    rng: np.random.RandomState,
) -> np.ndarray:
    """Generar demanda con distribucion LogNormal.

    La LogNormal es mas apropiada para demanda: siempre positiva,
    sesgada a la derecha, y el CV controla la cola pesada.

    Args:
        mean: Demanda media esperada (kg/periodo).
        cv: Coeficiente de variacion.
        n_scenarios: Numero de escenarios.
        rng: Generador aleatorio con seed.

    Returns:
        Array [n_scenarios] con demanda > 0.

    Nota:
        Si X ~ LogNormal(mu, sigma), entonces E[X] = exp(mu + sigma^2/2)
        y CV[X] = sqrt(exp(sigma^2) - 1).
        Dado mean y cv, se despeja: sigma^2 = log(1 + cv^2),
        mu = log(mean) - sigma^2/2.
    """
    if cv <= 0:
        return np.full(n_scenarios, mean)

    sigma2 = np.log(1 + cv**2)
    mu = np.log(max(mean, 1.0)) - sigma2 / 2
    sigma = np.sqrt(sigma2)
    return rng.lognormal(mu, sigma, size=n_scenarios)


def add_seasonality(
    base_demand: np.ndarray,
    amplitude: float,
    period: int,
    phase_shift: float = 0.0,
) -> np.ndarray:
    """Modular demanda con estacionalidad senoidal.

    demand[t] = base[t] * (1 + amplitude * sin(2*pi*t/period + phase))

    Args:
        base_demand: Array [n_periods] o [n_periods, ...] con demanda base.
        amplitude: Amplitud relativa (0.0 = sin estacionalidad, 0.3 = ±30%).
        period: Periodo de la estacionalidad (ej: 52 para semanal anual).
        phase_shift: Desfase en radianes (0 = pico en t=period/4).

    Returns:
        Array con misma forma que base_demand, modulado.
    """
    n_t = base_demand.shape[0]
    t = np.arange(n_t, dtype=np.float64)
    factor = 1.0 + amplitude * np.sin(2 * np.pi * t / period + phase_shift)

    # Broadcast: si base es [T] o [T, W], factor es [T]
    if base_demand.ndim == 1:
        return base_demand * factor
    else:
        return base_demand * factor[:, np.newaxis]


def add_correlation(
    demands: np.ndarray,
    corr_matrix: np.ndarray,
    rng: np.random.RandomState,
) -> np.ndarray:
    """Introducir correlacion entre coproductos via Cholesky.

    Transforma escenarios independientes en correlacionados.

    Args:
        demands: Array [n_products, n_periods, n_scenarios] independiente.
        corr_matrix: Matriz de correlacion [n_products, n_products].
            Debe ser simetrica, definida positiva, con 1's en diagonal.
        rng: Generador (no usado, para consistencia de interfaz).

    Returns:
        Array correlacionado con misma forma.
    """
    n_f, n_t, n_w = demands.shape
    L = np.linalg.cholesky(corr_matrix)  # [F, F]

    result = demands.copy()
    for t in range(n_t):
        # Estandarizar por producto
        means = demands[:, t, :].mean(axis=1, keepdims=True)  # [F, 1]
        stds = demands[:, t, :].std(axis=1, keepdims=True)  # [F, 1]
        stds = np.where(stds < 1e-10, 1.0, stds)

        z = (demands[:, t, :] - means) / stds  # [F, W]
        z_corr = L @ z  # [F, W]
        result[:, t, :] = means + stds * z_corr

    return np.maximum(result, 0.0)


def generate_scenarios(
    n_products: int,
    n_periods: int,
    n_scenarios: int,
    base_demands: np.ndarray,
    cvs: np.ndarray,
    distribution: str = "lognormal",
    seasonality: dict | None = None,
    corr_matrix: np.ndarray | None = None,
    seed: int = 42,
) -> np.ndarray:
    """Pipeline completo de generacion de escenarios de demanda.

    Args:
        n_products: Numero de formas de corte.
        n_periods: Horizonte de planificacion.
        n_scenarios: Numero de escenarios estocasticos.
        base_demands: Array [n_products] con demanda media por producto.
        cvs: Array [n_products] con coeficiente de variacion por producto.
        distribution: 'normal' o 'lognormal' (default).
        seasonality: Dict con 'amplitude', 'period', 'phase_shift' (optional).
        corr_matrix: Matriz [F, F] de correlacion (optional).
        seed: Semilla aleatoria.

    Returns:
        Array [n_products, n_periods, n_scenarios] de demanda.
    """
    rng = np.random.RandomState(seed)

    gen_fn = (
        generate_demand_lognormal
        if distribution == "lognormal"
        else generate_demand_normal
    )

    # 1. Generar demanda base: [F, T, W]
    demand = np.zeros((n_products, n_periods, n_scenarios))
    for f in range(n_products):
        for t in range(n_periods):
            demand[f, t, :] = gen_fn(base_demands[f], cvs[f], n_scenarios, rng)

    # 2. Estacionalidad (por producto)
    if seasonality is not None:
        amp = seasonality.get("amplitude", 0.0)
        period = seasonality.get("period", n_periods)
        phase = seasonality.get("phase_shift", 0.0)

        if amp > 0:
            for f in range(n_products):
                demand[f] = add_seasonality(demand[f], amp, period, phase)

    # 3. Correlacion entre productos
    if corr_matrix is not None:
        demand = add_correlation(demand, corr_matrix, rng)

    return np.maximum(demand, 0.0)
