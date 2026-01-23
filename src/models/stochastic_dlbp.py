"""
DLBP Avícola - Modelo con Tiempos Estocásticos
===============================================
Este script extiende el modelo MILP básico para considerar
variabilidad en los tiempos de procesamiento mediante simulación
Monte Carlo.

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: 1 - Modelado Matemático (Extensión Estocástica)
"""

import random
import statistics
from typing import Dict, List, Tuple
from pulp import LpProblem, LpVariable, LpMinimize, LpBinary, lpSum, LpStatus, value, PULP_CBC_CMD


def crear_instancia_base() -> Dict:
    """
    Crea la instancia base del proceso avícola con tiempos nominales.
    Los tiempos serán perturbados en cada simulación.
    """
    return {
        "tareas": [
            "T01_Colgado",
            "T02_Evisceracion", 
            "T03_SepararCabezaPatas",
            "T04_Chiller",
            "T05_Seleccion",
            "T06_AreaDespresado",
            "T07_CortarPernil",
            "T08_Contramuslo",
            "T09_Muslo",
            "T10_DeshuesarMuslo",
            "T11_FiletearMuslo"
        ],
        "estaciones": ["S1", "S2", "S3", "S4", "S5"],
        
        # Tiempos NOMINALES (base para perturbación)
        "tiempos_base": {
            "T01_Colgado": 5,
            "T02_Evisceracion": 20,
            "T03_SepararCabezaPatas": 12,
            "T04_Chiller": 8,
            "T05_Seleccion": 6,
            "T06_AreaDespresado": 4,
            "T07_CortarPernil": 15,
            "T08_Contramuslo": 10,
            "T09_Muslo": 10,
            "T10_DeshuesarMuslo": 18,
            "T11_FiletearMuslo": 12
        },
        
        "precedencias": {
            "T01_Colgado": [],
            "T02_Evisceracion": ["T01_Colgado"],
            "T03_SepararCabezaPatas": ["T02_Evisceracion"],
            "T04_Chiller": ["T03_SepararCabezaPatas"],
            "T05_Seleccion": ["T04_Chiller"],
            "T06_AreaDespresado": ["T05_Seleccion"],
            "T07_CortarPernil": ["T06_AreaDespresado"],
            "T08_Contramuslo": ["T07_CortarPernil"],
            "T09_Muslo": ["T07_CortarPernil"],
            "T10_DeshuesarMuslo": ["T09_Muslo"],
            "T11_FiletearMuslo": ["T10_DeshuesarMuslo"]
        },
        
        "zonas": {
            "T01_Colgado": "sucia",
            "T02_Evisceracion": "sucia",
            "T03_SepararCabezaPatas": "sucia",
            "T04_Chiller": "transicion",
            "T05_Seleccion": "limpia",
            "T06_AreaDespresado": "limpia",
            "T07_CortarPernil": "limpia",
            "T08_Contramuslo": "limpia",
            "T09_Muslo": "limpia",
            "T10_DeshuesarMuslo": "limpia",
            "T11_FiletearMuslo": "limpia"
        },
        
        "tiempo_ciclo": 40
    }


def generar_tiempos_estocasticos(
    tiempos_base: Dict[str, float], 
    varianza_pct: float = 0.20,
    distribucion: str = "triangular"
) -> Dict[str, float]:
    """
    Genera un conjunto de tiempos perturbados según una distribución.
    
    Args:
        tiempos_base: Diccionario de tiempos nominales
        varianza_pct: Porcentaje de variación (0.20 = ±20%)
        distribucion: Tipo de distribución ("triangular", "normal", "uniforme")
    
    Returns:
        Diccionario con tiempos perturbados
    """
    tiempos_perturbados = {}
    
    for tarea, tiempo_nominal in tiempos_base.items():
        min_t = tiempo_nominal * (1 - varianza_pct)
        max_t = tiempo_nominal * (1 + varianza_pct)
        
        if distribucion == "triangular":
            # Distribución triangular (más probable en el centro)
            tiempo = random.triangular(min_t, max_t, tiempo_nominal)
        elif distribucion == "uniforme":
            # Distribución uniforme
            tiempo = random.uniform(min_t, max_t)
        elif distribucion == "normal":
            # Distribución normal truncada
            sigma = tiempo_nominal * varianza_pct / 2
            tiempo = random.gauss(tiempo_nominal, sigma)
            tiempo = max(min_t, min(max_t, tiempo))  # Truncar
        else:
            tiempo = tiempo_nominal
        
        tiempos_perturbados[tarea] = round(tiempo, 2)
    
    return tiempos_perturbados


def resolver_dlbp_silencioso(instancia: Dict) -> Dict:
    """
    Versión silenciosa del solver DLBP (sin output a consola).
    """
    tareas = instancia["tareas"]
    estaciones = instancia["estaciones"]
    tiempos = instancia["tiempos"]
    precedencias = instancia["precedencias"]
    zonas = instancia.get("zonas", {})
    C = instancia["tiempo_ciclo"]
    
    prob = LpProblem("DLBP_Stochastic", LpMinimize)
    
    x = {i: {s: LpVariable(f"x_{i}_{s}", cat=LpBinary) for s in estaciones} for i in tareas}
    y = {s: LpVariable(f"y_{s}", cat=LpBinary) for s in estaciones}
    
    prob += lpSum(y[s] for s in estaciones), "Minimizar_Estaciones"
    
    for i in tareas:
        prob += lpSum(x[i][s] for s in estaciones) == 1
    
    for i in tareas:
        for j in precedencias[i]:
            prob += lpSum(int(s[1:]) * x[j][s] for s in estaciones) <= lpSum(int(s[1:]) * x[i][s] for s in estaciones)
    
    for s in estaciones:
        prob += lpSum(tiempos[i] * x[i][s] for i in tareas) <= C * y[s]
    
    for i in tareas:
        for s in estaciones:
            prob += x[i][s] <= y[s]
    
    if zonas:
        tareas_sucias = [t for t in tareas if zonas.get(t) == "sucia"]
        tareas_limpias = [t for t in tareas if zonas.get(t) == "limpia"]
        for s in estaciones:
            for i in tareas_sucias:
                for j in tareas_limpias:
                    prob += x[i][s] + x[j][s] <= 1
    
    prob.solve(PULP_CBC_CMD(msg=0))  # Silencioso
    
    if LpStatus[prob.status] == "Optimal":
        return {
            "status": "Optimal",
            "estaciones_usadas": int(value(prob.objective)),
            "factible": True
        }
    else:
        return {
            "status": LpStatus[prob.status],
            "estaciones_usadas": None,
            "factible": False
        }


def simulacion_montecarlo(
    n_simulaciones: int = 100,
    varianza_pct: float = 0.20,
    distribucion: str = "triangular",
    verbose: bool = True
) -> Dict:
    """
    Ejecuta N simulaciones del modelo DLBP con tiempos estocásticos.
    
    Args:
        n_simulaciones: Número de repeticiones
        varianza_pct: Variabilidad en tiempos de procesamiento
        distribucion: Tipo de distribución para los tiempos
        verbose: Mostrar progreso
    
    Returns:
        Diccionario con estadísticas de la simulación
    """
    instancia_base = crear_instancia_base()
    resultados = []
    infactibles = 0
    
    if verbose:
        print(f"Ejecutando {n_simulaciones} simulaciones Monte Carlo...")
        print(f"Varianza: ±{int(varianza_pct*100)}% | Distribución: {distribucion}")
        print()
    
    for i in range(n_simulaciones):
        # Generar tiempos perturbados
        tiempos_sim = generar_tiempos_estocasticos(
            instancia_base["tiempos_base"],
            varianza_pct,
            distribucion
        )
        
        # Crear instancia con tiempos perturbados
        instancia_sim = instancia_base.copy()
        instancia_sim["tiempos"] = tiempos_sim
        
        # Resolver
        resultado = resolver_dlbp_silencioso(instancia_sim)
        
        if resultado["factible"]:
            resultados.append(resultado["estaciones_usadas"])
        else:
            infactibles += 1
        
        # Progreso
        if verbose and (i + 1) % 20 == 0:
            print(f"  Simulación {i+1}/{n_simulaciones} completada...")
    
    # Estadísticas
    if resultados:
        stats = {
            "n_simulaciones": n_simulaciones,
            "n_factibles": len(resultados),
            "n_infactibles": infactibles,
            "media_estaciones": round(statistics.mean(resultados), 2),
            "desv_std_estaciones": round(statistics.stdev(resultados), 2) if len(resultados) > 1 else 0,
            "min_estaciones": min(resultados),
            "max_estaciones": max(resultados),
            "distribucion_resultados": {k: resultados.count(k) for k in sorted(set(resultados))}
        }
    else:
        stats = {
            "n_simulaciones": n_simulaciones,
            "n_factibles": 0,
            "n_infactibles": infactibles,
            "error": "Todas las simulaciones fueron infactibles"
        }
    
    return stats


def imprimir_histograma(stats: Dict) -> None:
    """Imprime un histograma ASCII simple de los resultados."""
    if "distribucion_resultados" not in stats:
        return
    
    dist = stats["distribucion_resultados"]
    max_count = max(dist.values())
    scale = 40 / max_count  # Escala para 40 caracteres
    
    print("\n📊 Histograma de Estaciones Usadas:")
    print("-" * 50)
    for estaciones, count in sorted(dist.items()):
        bar = "█" * int(count * scale)
        pct = count / stats["n_factibles"] * 100
        print(f"  {estaciones} estaciones: {bar} ({count} | {pct:.1f}%)")


def main():
    """Función principal para ejecutar la simulación estocástica."""
    print("=" * 60)
    print("DLBP Avícola - Simulación con Tiempos Estocásticos")
    print("Fase 1: Modelado Matemático (Extensión Monte Carlo)")
    print("=" * 60)
    print()
    
    # Ejecutar simulación
    stats = simulacion_montecarlo(
        n_simulaciones=100,
        varianza_pct=0.20,
        distribucion="triangular"
    )
    
    # Mostrar resultados
    print()
    print("=" * 60)
    print("RESULTADOS DE LA SIMULACIÓN")
    print("=" * 60)
    print(f"Simulaciones ejecutadas: {stats['n_simulaciones']}")
    print(f"Soluciones factibles:    {stats['n_factibles']}")
    print(f"Soluciones infactibles:  {stats['n_infactibles']}")
    print()
    
    if stats['n_factibles'] > 0:
        print(f"📈 Estadísticas de Estaciones Usadas:")
        print(f"   Media:     {stats['media_estaciones']:.2f}")
        print(f"   Desv. Std: {stats['desv_std_estaciones']:.2f}")
        print(f"   Mínimo:    {stats['min_estaciones']}")
        print(f"   Máximo:    {stats['max_estaciones']}")
        
        imprimir_histograma(stats)
        
        print()
        print("✓ Simulación completada exitosamente!")
    else:
        print("✗ Error: Todas las simulaciones fueron infactibles.")
        print("  Considere aumentar el tiempo de ciclo o reducir la varianza.")


if __name__ == "__main__":
    main()
