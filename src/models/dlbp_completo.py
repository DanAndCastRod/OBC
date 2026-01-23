"""
DLBP Avícola - Modelo Expandido (12 Áreas Operativas)
======================================================
Este script implementa el modelo DLBP completo para una planta
de procesamiento avícola con las 12 áreas operativas reales.

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: 1 - Modelado Matemático (Versión Expandida)
"""

from pulp import LpProblem, LpVariable, LpMinimize, LpBinary, lpSum, LpStatus, value
from typing import Dict, List, Tuple


def crear_instancia_completa() -> Dict:
    """
    Crea una instancia completa del proceso avícola con las 12 áreas operativas.
    
    Áreas:
    1. Sacrificio (A01-A06)
    2. Eviscerado (B01-B05)
    3. Chiller (C01-C03)
    4. Empaque Víscera (V01-V03)
    5. Selección (SEL)
    6. Pollo Entero (E01-E02)
    7. Despresado (D01-D25)
    8. Deshuesado (H01-H04)
    9. Adobo (AD01-AD03)
    10. Sellado (S01-S04)
    11. Golpe de Frío (GF01-GF02)
    12. Almacenamiento (ALMAC)
    """
    
    # ======================== DEFINICIÓN DE TAREAS ========================
    tareas = [
        # Área 1: Sacrificio
        "A01_Recepcion", "A02_Colgado", "A03_Aturdido", 
        "A04_Sangrado", "A05_Escaldado", "A06_Desplumado",
        
        # Área 2: Eviscerado
        "B01_CorteAbdominal", "B02_ExtraccionVisceras", "B03_SepararCabeza",
        "B04_CortarPatas", "B05_LavadoInterno",
        
        # Área 3: Chiller
        "C01_InmersionFria", "C02_ControlTemp", "C03_Escurrido",
        
        # Área 4: Empaque Víscera (paralelo)
        "V01_RecepcionMenudencias", "V02_ClasificacionVisc", "V03_EmpaqueViscera",
        
        # Área 5: Selección
        "SEL_Seleccion",
        
        # Área 6: Pollo Entero
        "E01_ClasificacionPeso", "E02_EmpaqueEntero",
        
        # Área 7: Despresado
        "D00_EntradaDespresado",
        "D01_CortarAlas", "D02_AlasSolas", "D03_AlasConCostillar",
        "D10_CortarPechuga",
        "D20_SepararPernil", "D21_PernilSinRab", "D22_PernilConRab",
        "D24_Contramuslo", "D25_Muslo",
        
        # Área 8: Deshuesado
        "H01_DeshuesarPechuga", "H02_FiletearPechuga",
        "H03_DeshuesarMuslo", "H04_FiletearMuslo",
        
        # Área 9: Adobo
        "AD01_PrepararMarinada", "AD02_AplicarAdobo", "AD03_Reposo",
        
        # Área 10: Sellado
        "S01_BolsaGranel", "S02_Embandejado", "S03_SelladoVacio", "S04_Etiquetado",
        
        # Área 11: Golpe de Frío
        "GF01_TunelEnfriamiento", "GF02_ControlCadenaFrio",
        
        # Área 12: Almacenamiento
        "ALMAC_CuartoFrio"
    ]
    
    # ======================== ESTACIONES DISPONIBLES ========================
    # Más estaciones para el modelo expandido
    estaciones = [f"S{i:02d}" for i in range(1, 16)]  # S01 a S15
    
    # ======================== TIEMPOS DE PROCESAMIENTO ========================
    tiempos = {
        # Área 1: Sacrificio (tiempos en segundos)
        "A01_Recepcion": 3, "A02_Colgado": 4, "A03_Aturdido": 2,
        "A04_Sangrado": 5, "A05_Escaldado": 8, "A06_Desplumado": 10,
        
        # Área 2: Eviscerado
        "B01_CorteAbdominal": 6, "B02_ExtraccionVisceras": 15,
        "B03_SepararCabeza": 5, "B04_CortarPatas": 6, "B05_LavadoInterno": 8,
        
        # Área 3: Chiller
        "C01_InmersionFria": 4, "C02_ControlTemp": 3, "C03_Escurrido": 5,
        
        # Área 4: Empaque Víscera
        "V01_RecepcionMenudencias": 5, "V02_ClasificacionVisc": 8, "V03_EmpaqueViscera": 10,
        
        # Área 5: Selección
        "SEL_Seleccion": 4,
        
        # Área 6: Pollo Entero
        "E01_ClasificacionPeso": 6, "E02_EmpaqueEntero": 12,
        
        # Área 7: Despresado
        "D00_EntradaDespresado": 3,
        "D01_CortarAlas": 8, "D02_AlasSolas": 5, "D03_AlasConCostillar": 7,
        "D10_CortarPechuga": 12,
        "D20_SepararPernil": 10, "D21_PernilSinRab": 6, "D22_PernilConRab": 4,
        "D24_Contramuslo": 8, "D25_Muslo": 8,
        
        # Área 8: Deshuesado
        "H01_DeshuesarPechuga": 18, "H02_FiletearPechuga": 12,
        "H03_DeshuesarMuslo": 15, "H04_FiletearMuslo": 10,
        
        # Área 9: Adobo
        "AD01_PrepararMarinada": 10, "AD02_AplicarAdobo": 8, "AD03_Reposo": 5,
        
        # Área 10: Sellado
        "S01_BolsaGranel": 6, "S02_Embandejado": 10, "S03_SelladoVacio": 8, "S04_Etiquetado": 4,
        
        # Área 11: Golpe de Frío
        "GF01_TunelEnfriamiento": 5, "GF02_ControlCadenaFrio": 3,
        
        # Área 12: Almacenamiento
        "ALMAC_CuartoFrio": 4
    }
    
    # ======================== PRECEDENCIAS ========================
    precedencias = {
        # Área 1: Sacrificio (secuencial estricto)
        "A01_Recepcion": [],
        "A02_Colgado": ["A01_Recepcion"],
        "A03_Aturdido": ["A02_Colgado"],
        "A04_Sangrado": ["A03_Aturdido"],
        "A05_Escaldado": ["A04_Sangrado"],
        "A06_Desplumado": ["A05_Escaldado"],
        
        # Área 2: Eviscerado
        "B01_CorteAbdominal": ["A06_Desplumado"],
        "B02_ExtraccionVisceras": ["B01_CorteAbdominal"],
        "B03_SepararCabeza": ["B02_ExtraccionVisceras"],
        "B04_CortarPatas": ["B03_SepararCabeza"],
        "B05_LavadoInterno": ["B04_CortarPatas"],
        
        # Área 3: Chiller
        "C01_InmersionFria": ["B05_LavadoInterno"],
        "C02_ControlTemp": ["C01_InmersionFria"],
        "C03_Escurrido": ["C02_ControlTemp"],
        
        # Área 4: Empaque Víscera (paralelo desde B02)
        "V01_RecepcionMenudencias": ["B02_ExtraccionVisceras"],
        "V02_ClasificacionVisc": ["V01_RecepcionMenudencias"],
        "V03_EmpaqueViscera": ["V02_ClasificacionVisc"],
        
        # Área 5: Selección
        "SEL_Seleccion": ["C03_Escurrido"],
        
        # Área 6: Pollo Entero (una ruta desde Selección)
        "E01_ClasificacionPeso": ["SEL_Seleccion"],
        "E02_EmpaqueEntero": ["E01_ClasificacionPeso"],
        
        # Área 7: Despresado (otra ruta desde Selección)
        "D00_EntradaDespresado": ["SEL_Seleccion"],
        "D01_CortarAlas": ["D00_EntradaDespresado"],
        "D02_AlasSolas": ["D01_CortarAlas"],
        "D03_AlasConCostillar": ["D01_CortarAlas"],
        "D10_CortarPechuga": ["D00_EntradaDespresado"],
        "D20_SepararPernil": ["D00_EntradaDespresado"],
        "D21_PernilSinRab": ["D20_SepararPernil"],
        "D22_PernilConRab": ["D20_SepararPernil"],
        "D24_Contramuslo": ["D21_PernilSinRab", "D22_PernilConRab"],
        "D25_Muslo": ["D21_PernilSinRab", "D22_PernilConRab"],
        
        # Área 8: Deshuesado
        "H01_DeshuesarPechuga": ["D10_CortarPechuga"],
        "H02_FiletearPechuga": ["H01_DeshuesarPechuga"],
        "H03_DeshuesarMuslo": ["D25_Muslo"],
        "H04_FiletearMuslo": ["H03_DeshuesarMuslo"],
        
        # Área 9: Adobo (desde Pollo Entero)
        "AD01_PrepararMarinada": ["E02_EmpaqueEntero"],
        "AD02_AplicarAdobo": ["AD01_PrepararMarinada"],
        "AD03_Reposo": ["AD02_AplicarAdobo"],
        
        # Área 10: Sellado (recibe de múltiples fuentes)
        "S01_BolsaGranel": ["D02_AlasSolas", "D03_AlasConCostillar", "D24_Contramuslo"],
        "S02_Embandejado": ["H02_FiletearPechuga", "H04_FiletearMuslo", "AD03_Reposo"],
        "S03_SelladoVacio": ["S02_Embandejado"],
        "S04_Etiquetado": ["S01_BolsaGranel", "S03_SelladoVacio"],
        
        # Área 11: Golpe de Frío
        "GF01_TunelEnfriamiento": ["S04_Etiquetado", "V03_EmpaqueViscera"],
        "GF02_ControlCadenaFrio": ["GF01_TunelEnfriamiento"],
        
        # Área 12: Almacenamiento
        "ALMAC_CuartoFrio": ["GF02_ControlCadenaFrio"]
    }
    
    return {
        "tareas": tareas,
        "estaciones": estaciones,
        "tiempos": tiempos,
        "precedencias": precedencias,
        "tiempo_ciclo": 45  # segundos
    }


def resolver_dlbp(instancia: Dict, verbose: bool = True) -> Dict:
    """
    Resuelve el problema DLBP usando programación lineal entera mixta.
    
    Objetivo: Minimizar el número de estaciones utilizadas
    sujeto a restricciones de precedencia y tiempo de ciclo.
    """
    tareas = instancia["tareas"]
    estaciones = instancia["estaciones"]
    tiempos = instancia["tiempos"]
    precedencias = instancia["precedencias"]
    C = instancia["tiempo_ciclo"]
    
    if verbose:
        print(f"Resolviendo DLBP con {len(tareas)} tareas y {len(estaciones)} estaciones...")
        print(f"Tiempo de ciclo: {C} segundos")
    
    # Crear el problema
    prob = LpProblem("DLBP_Avicola_Completo", LpMinimize)
    
    # Variables de decisión
    x = {
        i: {s: LpVariable(f"x_{i}_{s}", cat=LpBinary) for s in estaciones}
        for i in tareas
    }
    y = {s: LpVariable(f"y_{s}", cat=LpBinary) for s in estaciones}
    
    # Función objetivo: Minimizar número de estaciones
    prob += lpSum(y[s] for s in estaciones), "Minimizar_Estaciones"
    
    # Restricción 1: Cada tarea debe asignarse exactamente a una estación
    for i in tareas:
        prob += lpSum(x[i][s] for s in estaciones) == 1, f"Asig_{i[:15]}"
    
    # Restricción 2: Precedencias
    for i in tareas:
        for j in precedencias.get(i, []):
            if j in tareas:
                prob += (
                    lpSum(int(s[1:]) * x[j][s] for s in estaciones) <= 
                    lpSum(int(s[1:]) * x[i][s] for s in estaciones),
                    f"Prec_{j[:10]}_{i[:10]}"
                )
    
    # Restricción 3: Tiempo de ciclo
    for s in estaciones:
        prob += (
            lpSum(tiempos[i] * x[i][s] for i in tareas) <= C * y[s],
            f"Ciclo_{s}"
        )
    
    # Restricción 4: Activación de estación
    for i in tareas:
        for s in estaciones:
            prob += x[i][s] <= y[s], f"Act_{i[:10]}_{s}"
    
    # Resolver
    prob.solve()
    
    # Resultados
    if verbose:
        print("\n" + "=" * 60)
        print("RESULTADO DEL MODELO DLBP - 12 ÁREAS OPERATIVAS")
        print("=" * 60)
        print(f"Estado: {LpStatus[prob.status]}")
        print(f"Estaciones utilizadas: {int(value(prob.objective))}")
        print("-" * 60)
        
        print("\nAsignación por Estación:")
        total_tiempo = 0
        for s in estaciones:
            if value(y[s]) > 0.5:
                tareas_en_estacion = [i for i in tareas if value(x[i][s]) > 0.5]
                tiempo_estacion = sum(tiempos[i] for i in tareas_en_estacion)
                total_tiempo += tiempo_estacion
                utilizacion = (tiempo_estacion / C) * 100
                print(f"\n  {s} ({tiempo_estacion}s / {C}s = {utilizacion:.0f}%):")
                for t in tareas_en_estacion:
                    print(f"      - {t} ({tiempos[t]}s)")
        
        print("\n" + "-" * 60)
        print(f"Tiempo total de procesamiento: {total_tiempo}s")
        print(f"Eficiencia promedio: {(total_tiempo / (int(value(prob.objective)) * C)) * 100:.1f}%")
    
    return {
        "status": LpStatus[prob.status],
        "estaciones_usadas": int(value(prob.objective)),
        "asignacion": {
            s: [i for i in tareas if value(x[i][s]) > 0.5] 
            for s in estaciones if value(y[s]) > 0.5
        }
    }


def main():
    """Función principal."""
    print("=" * 60)
    print("DLBP AVÍCOLA - MODELO EXPANDIDO (12 ÁREAS)")
    print("Fase 1: Fundamentación y Modelado Matemático")
    print("=" * 60)
    print()
    
    # Crear instancia completa
    instancia = crear_instancia_completa()
    
    print(f"Instancia creada:")
    print(f"  - Tareas: {len(instancia['tareas'])}")
    print(f"  - Estaciones disponibles: {len(instancia['estaciones'])}")
    print(f"  - Tiempo de ciclo: {instancia['tiempo_ciclo']}s")
    print()
    
    # Resolver
    resultado = resolver_dlbp(instancia)
    
    if resultado["status"] == "Optimal":
        print("\n" + "=" * 60)
        print("✓ MODELO VALIDADO EXITOSAMENTE")
        print("=" * 60)


if __name__ == "__main__":
    main()
