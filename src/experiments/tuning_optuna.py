"""
DLBP Avícola - Calibración de Hiperparámetros con Optuna
=========================================================
Calibra automáticamente los parámetros de GA, TS e Híbrido
usando optimización bayesiana (TPE).

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: 3 - Generación de Datos y Calibración
"""

import sys
import os
import yaml
from dataclasses import asdict
from typing import Dict, Callable
import numpy as np

# Agregar paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "algorithms"))
from base import ProblemInstance
from genetic_algorithm import GeneticAlgorithm, GAConfig
from tabu_search import TabuSearch, TSConfig
from hybrid import HybridAlgorithm, HybridConfig

# Importar Optuna solo si está disponible
try:
    import optuna
    from optuna.samplers import TPESampler
    OPTUNA_AVAILABLE = True
except ImportError:
    OPTUNA_AVAILABLE = False
    print("⚠️ Optuna no disponible. Instalar con: pip install optuna")


def cargar_instancia_tuning() -> ProblemInstance:
    """Carga la instancia de mediana para tuning."""
    # Usar instancia mediana como representativa
    return ProblemInstance(
        tareas=[f"T{i:03d}" for i in range(40)],
        tiempos={f"T{i:03d}": np.random.randint(5, 15) for i in range(40)},
        precedencias={
            f"T{i:03d}": [f"T{i-1:03d}"] if i > 0 and i % 7 != 0 else [] 
            for i in range(40)
        },
        tiempo_ciclo=40,
        n_estaciones_max=20
    )


def evaluar_configuracion(
    instancia: ProblemInstance,
    algoritmo: str,
    params: Dict,
    n_repeticiones: int = 3,
    semilla_base: int = 42
) -> float:
    """
    Evalúa una configuración ejecutando el algoritmo múltiples veces.
    
    Returns:
        Promedio del número de estaciones (menor es mejor)
    """
    resultados = []
    
    for rep in range(n_repeticiones):
        semilla = semilla_base + rep * 100
        
        if algoritmo == "GA":
            config = GAConfig(**params)
            optimizer = GeneticAlgorithm(instancia, config, seed=semilla)
            mejor = optimizer.optimizar(max_iter=50, verbose=False)
        elif algoritmo == "TS":
            config = TSConfig(**params)
            optimizer = TabuSearch(instancia, config, seed=semilla)
            mejor = optimizer.optimizar(max_iter=100, verbose=False)
        elif algoritmo == "Hybrid":
            config = HybridConfig(**params)
            optimizer = HybridAlgorithm(instancia, config, seed=semilla)
            mejor = optimizer.optimizar(max_iter=50, verbose=False)
        else:
            raise ValueError(f"Algoritmo desconocido: {algoritmo}")
        
        if mejor.es_factible:
            resultados.append(mejor.n_estaciones)
        else:
            resultados.append(float('inf'))
    
    return np.mean(resultados) if resultados else float('inf')


def crear_objetivo_ga(instancia: ProblemInstance) -> Callable:
    """Crea la función objetivo para calibrar GA."""
    def objective(trial):
        params = {
            "poblacion_size": trial.suggest_int("poblacion_size", 30, 150),
            "prob_cruce": trial.suggest_float("prob_cruce", 0.6, 0.95),
            "prob_mutacion": trial.suggest_float("prob_mutacion", 0.05, 0.25),
            "tamano_torneo": trial.suggest_int("tamano_torneo", 2, 5),
            "elitismo": trial.suggest_int("elitismo", 1, 5)
        }
        return evaluar_configuracion(instancia, "GA", params)
    return objective


def crear_objetivo_ts(instancia: ProblemInstance) -> Callable:
    """Crea la función objetivo para calibrar TS."""
    def objective(trial):
        params = {
            "tamano_lista_tabu": trial.suggest_int("tamano_lista_tabu", 7, 30),
            "tamano_vecindario": trial.suggest_int("tamano_vecindario", 15, 50),
            "tipo_movimiento": trial.suggest_categorical("tipo_movimiento", ["swap", "insert", "mixto"])
        }
        return evaluar_configuracion(instancia, "TS", params)
    return objective


def crear_objetivo_hybrid(instancia: ProblemInstance) -> Callable:
    """Crea la función objetivo para calibrar Híbrido."""
    def objective(trial):
        params = {
            "poblacion_size": trial.suggest_int("poblacion_size", 25, 80),
            "prob_cruce": trial.suggest_float("prob_cruce", 0.7, 0.95),
            "aplicar_ts_cada": trial.suggest_int("aplicar_ts_cada", 5, 30),
            "iter_ts_por_individuo": trial.suggest_int("iter_ts_por_individuo", 10, 40),
            "top_n_para_ts": trial.suggest_int("top_n_para_ts", 3, 10)
        }
        return evaluar_configuracion(instancia, "Hybrid", params)
    return objective


def calibrar_algoritmo(
    algoritmo: str,
    instancia: ProblemInstance,
    n_trials: int = 30,
    verbose: bool = True
) -> Dict:
    """
    Ejecuta la calibración para un algoritmo.
    
    Returns:
        Diccionario con mejores parámetros encontrados
    """
    if not OPTUNA_AVAILABLE:
        print("❌ Optuna no disponible")
        return {}
    
    if verbose:
        print(f"\n🔧 Calibrando {algoritmo}...")
        print(f"   Trials: {n_trials}")
    
    # Silenciar logs de Optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    
    # Crear estudio
    sampler = TPESampler(seed=42)
    study = optuna.create_study(
        direction="minimize",
        sampler=sampler,
        study_name=f"DLBP_{algoritmo}"
    )
    
    # Seleccionar función objetivo
    if algoritmo == "GA":
        objective = crear_objetivo_ga(instancia)
    elif algoritmo == "TS":
        objective = crear_objetivo_ts(instancia)
    elif algoritmo == "Hybrid":
        objective = crear_objetivo_hybrid(instancia)
    else:
        raise ValueError(f"Algoritmo desconocido: {algoritmo}")
    
    # Optimizar
    study.optimize(objective, n_trials=n_trials, show_progress_bar=verbose)
    
    if verbose:
        print(f"   ✅ Mejor fitness: {study.best_value:.2f} estaciones")
        print(f"   Mejores parámetros:")
        for k, v in study.best_params.items():
            print(f"      {k}: {v}")
    
    return {
        "algoritmo": algoritmo,
        "mejor_fitness": float(study.best_value),
        "mejores_params": study.best_params
    }


def exportar_configuracion(resultados: Dict, carpeta: str = "config"):
    """Exporta los parámetros calibrados a YAML."""
    os.makedirs(carpeta, exist_ok=True)
    path = os.path.join(carpeta, "algorithm_params.yaml")
    
    config = {"calibracion": {}}
    for alg, data in resultados.items():
        config["calibracion"][alg] = {
            "fitness_obtenido": data["mejor_fitness"],
            "parametros": data["mejores_params"]
        }
    
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    return path


def main():
    """Ejecuta la calibración completa."""
    print("=" * 60)
    print("DLBP AVÍCOLA - CALIBRACIÓN DE HIPERPARÁMETROS")
    print("=" * 60)
    
    if not OPTUNA_AVAILABLE:
        print("\n❌ Error: Optuna no está instalado.")
        print("   Instalar con: pip install optuna")
        return
    
    # Cargar instancia de tuning
    instancia = cargar_instancia_tuning()
    print(f"\n📋 Instancia de tuning: {instancia.n_tareas} tareas")
    
    # Calibrar cada algoritmo
    n_trials = 30  # Ajustar según tiempo disponible
    resultados = {}
    
    for alg in ["GA", "TS", "Hybrid"]:
        resultados[alg] = calibrar_algoritmo(
            algoritmo=alg,
            instancia=instancia,
            n_trials=n_trials,
            verbose=True
        )
    
    # Exportar configuración
    config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config")
    path = exportar_configuracion(resultados, config_path)
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE CALIBRACIÓN")
    print("=" * 60)
    for alg, data in resultados.items():
        print(f"\n{alg}:")
        print(f"   Fitness: {data['mejor_fitness']:.2f}")
        print(f"   Params: {data['mejores_params']}")
    
    print(f"\n💾 Configuración exportada a: {path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
