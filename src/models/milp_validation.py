"""
DLBP Avícola - Script de Validación MILP
=========================================
Este script implementa una versión simplificada del modelo DLBP
para validar la lógica de precedencia y tiempos de ciclo.

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: 1 - Modelado Matemático
"""

from pulp import LpProblem, LpVariable, LpMinimize, LpBinary, lpSum, LpStatus, value


def crear_instancia_juguete():
    """
    Crea una instancia de prueba basada en el proceso REAL de desensamble avícola.
    Incluye: Línea principal + Selección + Módulo Pernil (subconjunto representativo).
    """
    instancia = {
        # Tareas del proceso real (subconjunto: Línea principal + Pernil)
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
        
        # Estaciones disponibles
        "estaciones": ["S1", "S2", "S3", "S4", "S5"],
        
        # Tiempos de procesamiento (segundos) - Estimados
        "tiempos": {
            "T01_Colgado": 5,
            "T02_Evisceracion": 20,
            "T03_SepararCabezaPatas": 12,
            "T04_Chiller": 8,  # Tiempo de manipulación (no enfriamiento real)
            "T05_Seleccion": 6,
            "T06_AreaDespresado": 4,
            "T07_CortarPernil": 15,
            "T08_Contramuslo": 10,
            "T09_Muslo": 10,
            "T10_DeshuesarMuslo": 18,
            "T11_FiletearMuslo": 12
        },
        
        # Precedencias basadas en el flujo real
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
        
        # Zonificación: Tareas sucias vs limpias (normas sanitarias)
        "zonas": {
            "T01_Colgado": "sucia",
            "T02_Evisceracion": "sucia",
            "T03_SepararCabezaPatas": "sucia",
            "T04_Chiller": "transicion",  # Zona de transición (enfriamiento)
            "T05_Seleccion": "limpia",
            "T06_AreaDespresado": "limpia",
            "T07_CortarPernil": "limpia",
            "T08_Contramuslo": "limpia",
            "T09_Muslo": "limpia",
            "T10_DeshuesarMuslo": "limpia",
            "T11_FiletearMuslo": "limpia"
        },
        
        # Tiempo de ciclo máximo (segundos)
        "tiempo_ciclo": 40
    }
    return instancia


def resolver_dlbp(instancia, verbose=True):
    """
    Resuelve el problema DLBP usando programación lineal entera mixta.
    
    Objetivo: Minimizar el número de estaciones utilizadas
    sujeto a restricciones de precedencia y tiempo de ciclo.
    """
    tareas = instancia["tareas"]
    estaciones = instancia["estaciones"]
    tiempos = instancia["tiempos"]
    precedencias = instancia["precedencias"]
    zonas = instancia.get("zonas", {})  # Zonificación opcional
    C = instancia["tiempo_ciclo"]
    
    # Crear el problema
    prob = LpProblem("DLBP_Avicola", LpMinimize)
    
    # Variables de decisión
    # x[i][s] = 1 si tarea i se asigna a estación s
    x = {
        i: {s: LpVariable(f"x_{i}_{s}", cat=LpBinary) for s in estaciones}
        for i in tareas
    }
    
    # y[s] = 1 si estación s está activa
    y = {s: LpVariable(f"y_{s}", cat=LpBinary) for s in estaciones}
    
    # Función objetivo: Minimizar número de estaciones
    prob += lpSum(y[s] for s in estaciones), "Minimizar_Estaciones"
    
    # Restricción 1: Cada tarea debe asignarse exactamente a una estación
    for i in tareas:
        prob += lpSum(x[i][s] for s in estaciones) == 1, f"Asignacion_Unica_{i}"
    
    # Restricción 2: Precedencias
    # Si j es predecesora de i, entonces station(j) <= station(i)
    for i in tareas:
        for j in precedencias[i]:
            # Suma ponderada: estación de j <= estación de i
            prob += (
                lpSum(int(s[1:]) * x[j][s] for s in estaciones) <= 
                lpSum(int(s[1:]) * x[i][s] for s in estaciones),
                f"Precedencia_{j}_antes_{i}"
            )
    
    # Restricción 3: Tiempo de ciclo
    for s in estaciones:
        prob += (
            lpSum(tiempos[i] * x[i][s] for i in tareas) <= C * y[s],
            f"Tiempo_Ciclo_{s}"
        )
    
    # Restricción 4: Activación de estación
    for i in tareas:
        for s in estaciones:
            prob += x[i][s] <= y[s], f"Activacion_{i}_{s}"
    
    # Restricción 5: Zonificación (tareas sucias NO pueden compartir estación con limpias)
    if zonas:
        tareas_sucias = [t for t in tareas if zonas.get(t) == "sucia"]
        tareas_limpias = [t for t in tareas if zonas.get(t) == "limpia"]
        for s in estaciones:
            for i in tareas_sucias:
                for j in tareas_limpias:
                    prob += x[i][s] + x[j][s] <= 1, f"Zonificacion_{i}_{j}_{s}"
    
    # Resolver
    prob.solve()
    
    # Resultados
    if verbose:
        print("=" * 50)
        print("RESULTADO DEL MODELO DLBP")
        print("=" * 50)
        print(f"Estado: {LpStatus[prob.status]}")
        print(f"Número de estaciones utilizadas: {int(value(prob.objective))}")
        print()
        
        print("Asignación de tareas:")
        for s in estaciones:
            if value(y[s]) > 0.5:
                tareas_en_estacion = [i for i in tareas if value(x[i][s]) > 0.5]
                tiempo_total = sum(tiempos[i] for i in tareas_en_estacion)
                print(f"  {s}: {tareas_en_estacion} (Tiempo: {tiempo_total}s / {C}s)")
        
        print()
        print("Validación de precedencias:")
        for i in tareas:
            for j in precedencias[i]:
                est_j = [s for s in estaciones if value(x[j][s]) > 0.5][0]
                est_i = [s for s in estaciones if value(x[i][s]) > 0.5][0]
                valido = "✓" if int(est_j[1:]) <= int(est_i[1:]) else "✗"
                print(f"  {j} ({est_j}) -> {i} ({est_i}): {valido}")
    
    return {
        "status": LpStatus[prob.status],
        "estaciones_usadas": int(value(prob.objective)),
        "asignacion": {
            s: [i for i in tareas if value(x[i][s]) > 0.5] 
            for s in estaciones if value(y[s]) > 0.5
        }
    }


def main():
    """Función principal para ejecutar la validación."""
    print("DLBP Avícola - Validación de Modelo MILP")
    print("Fase 1: Fundamentación y Modelado Matemático")
    print()
    
    # Crear y resolver instancia de prueba
    instancia = crear_instancia_juguete()
    
    print(f"Instancia: {len(instancia['tareas'])} tareas, {len(instancia['estaciones'])} estaciones")
    print(f"Tiempo de ciclo: {instancia['tiempo_ciclo']} segundos")
    print()
    
    resultado = resolver_dlbp(instancia)
    
    if resultado["status"] == "Optimal":
        print("\n✓ Modelo validado exitosamente!")
        print("  - Restricciones de precedencia: OK")
        print("  - Restricciones de tiempo de ciclo: OK")
        print("  - Restricciones de zonificación: OK")
    else:
        print(f"\n✗ Error en el modelo: {resultado['status']}")


if __name__ == "__main__":
    main()
