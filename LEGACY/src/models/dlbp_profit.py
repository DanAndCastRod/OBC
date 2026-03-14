"""
DLBP Avícola - Modelo Profit-Oriented (12 Áreas Operativas)
============================================================
Este script implementa el modelo DLBP completo para una planta
de procesamiento avícola con función objetivo de MAXIMIZACIÓN DE BENEFICIO.

Basado en:
- Liang et al. (2023): Profit-oriented multi-parallel partial DLBP
- Liu et al. (2021): Distributionally robust optimization
- Tian et al. (2023): Multi-objective hybrid evolutionary algorithm

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: 1 - Modelado Matemático (Versión Profit-Oriented)
"""

from pulp import (
    LpProblem, LpVariable, LpMaximize, LpMinimize, 
    LpBinary, LpContinuous, lpSum, LpStatus, value
)
from typing import Dict, List, Tuple
import json


# =============================================================================
# DATOS DE COPRODUCTOS Y COSTOS
# =============================================================================

COPRODUCTOS = {
    "pechuga_entera": {"precio": 12000, "costo_inventario": 200, "penalizacion": 1500},
    "pechuga_filete": {"precio": 18000, "costo_inventario": 300, "penalizacion": 2000},
    "alas_solas": {"precio": 6000, "costo_inventario": 100, "penalizacion": 800},
    "alas_costillar": {"precio": 7500, "costo_inventario": 120, "penalizacion": 900},
    "pernil_entero": {"precio": 8000, "costo_inventario": 150, "penalizacion": 1000},
    "contramuslo": {"precio": 5500, "costo_inventario": 100, "penalizacion": 700},
    "muslo": {"precio": 5000, "costo_inventario": 100, "penalizacion": 700},
    "muslo_filete": {"precio": 9000, "costo_inventario": 180, "penalizacion": 1200},
    "visceras": {"precio": 2000, "costo_inventario": 50, "penalizacion": 300},
    "pollo_entero": {"precio": 15000, "costo_inventario": 250, "penalizacion": 1800},
    "pollo_adobado": {"precio": 18000, "costo_inventario": 300, "penalizacion": 2200},
}

# Costo fijo por estación (COP/turno): incluye operario, energía, depreciación
COSTO_ESTACION = 50000

# Demanda estimada por turno (unidades)
DEMANDA = {
    "pechuga_entera": 100,
    "pechuga_filete": 150,
    "alas_solas": 200,
    "alas_costillar": 80,
    "pernil_entero": 120,
    "contramuslo": 100,
    "muslo": 100,
    "muslo_filete": 80,
    "visceras": 300,
    "pollo_entero": 200,
    "pollo_adobado": 100,
}


def crear_instancia_completa() -> Dict:
    """
    Crea una instancia completa del proceso avícola con las 12 áreas operativas.
    Incluye datos económicos para función objetivo de beneficio.
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
    
    # Mapeo de tareas finales a coproductos
    tarea_coproducto = {
        "D02_AlasSolas": "alas_solas",
        "D03_AlasConCostillar": "alas_costillar",
        "D10_CortarPechuga": "pechuga_entera",
        "H02_FiletearPechuga": "pechuga_filete",
        "D24_Contramuslo": "contramuslo",
        "D25_Muslo": "muslo",
        "H04_FiletearMuslo": "muslo_filete",
        "V03_EmpaqueViscera": "visceras",
        "E02_EmpaqueEntero": "pollo_entero",
        "AD03_Reposo": "pollo_adobado",
    }
    
    # Estaciones disponibles
    estaciones = [f"S{i:02d}" for i in range(1, 16)]
    
    # Tiempos de procesamiento (segundos)
    tiempos = {
        "A01_Recepcion": 3, "A02_Colgado": 4, "A03_Aturdido": 2,
        "A04_Sangrado": 5, "A05_Escaldado": 8, "A06_Desplumado": 10,
        "B01_CorteAbdominal": 6, "B02_ExtraccionVisceras": 15,
        "B03_SepararCabeza": 5, "B04_CortarPatas": 6, "B05_LavadoInterno": 8,
        "C01_InmersionFria": 4, "C02_ControlTemp": 3, "C03_Escurrido": 5,
        "V01_RecepcionMenudencias": 5, "V02_ClasificacionVisc": 8, "V03_EmpaqueViscera": 10,
        "SEL_Seleccion": 4,
        "E01_ClasificacionPeso": 6, "E02_EmpaqueEntero": 12,
        "D00_EntradaDespresado": 3,
        "D01_CortarAlas": 8, "D02_AlasSolas": 5, "D03_AlasConCostillar": 7,
        "D10_CortarPechuga": 12,
        "D20_SepararPernil": 10, "D21_PernilSinRab": 6, "D22_PernilConRab": 4,
        "D24_Contramuslo": 8, "D25_Muslo": 8,
        "H01_DeshuesarPechuga": 18, "H02_FiletearPechuga": 12,
        "H03_DeshuesarMuslo": 15, "H04_FiletearMuslo": 10,
        "AD01_PrepararMarinada": 10, "AD02_AplicarAdobo": 8, "AD03_Reposo": 5,
        "S01_BolsaGranel": 6, "S02_Embandejado": 10, "S03_SelladoVacio": 8, "S04_Etiquetado": 4,
        "GF01_TunelEnfriamiento": 5, "GF02_ControlCadenaFrio": 3,
        "ALMAC_CuartoFrio": 4
    }
    
    # Precedencias
    precedencias = {
        "A01_Recepcion": [],
        "A02_Colgado": ["A01_Recepcion"],
        "A03_Aturdido": ["A02_Colgado"],
        "A04_Sangrado": ["A03_Aturdido"],
        "A05_Escaldado": ["A04_Sangrado"],
        "A06_Desplumado": ["A05_Escaldado"],
        "B01_CorteAbdominal": ["A06_Desplumado"],
        "B02_ExtraccionVisceras": ["B01_CorteAbdominal"],
        "B03_SepararCabeza": ["B02_ExtraccionVisceras"],
        "B04_CortarPatas": ["B03_SepararCabeza"],
        "B05_LavadoInterno": ["B04_CortarPatas"],
        "C01_InmersionFria": ["B05_LavadoInterno"],
        "C02_ControlTemp": ["C01_InmersionFria"],
        "C03_Escurrido": ["C02_ControlTemp"],
        "V01_RecepcionMenudencias": ["B02_ExtraccionVisceras"],
        "V02_ClasificacionVisc": ["V01_RecepcionMenudencias"],
        "V03_EmpaqueViscera": ["V02_ClasificacionVisc"],
        "SEL_Seleccion": ["C03_Escurrido"],
        "E01_ClasificacionPeso": ["SEL_Seleccion"],
        "E02_EmpaqueEntero": ["E01_ClasificacionPeso"],
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
        "H01_DeshuesarPechuga": ["D10_CortarPechuga"],
        "H02_FiletearPechuga": ["H01_DeshuesarPechuga"],
        "H03_DeshuesarMuslo": ["D25_Muslo"],
        "H04_FiletearMuslo": ["H03_DeshuesarMuslo"],
        "AD01_PrepararMarinada": ["E02_EmpaqueEntero"],
        "AD02_AplicarAdobo": ["AD01_PrepararMarinada"],
        "AD03_Reposo": ["AD02_AplicarAdobo"],
        "S01_BolsaGranel": ["D02_AlasSolas", "D03_AlasConCostillar", "D24_Contramuslo"],
        "S02_Embandejado": ["H02_FiletearPechuga", "H04_FiletearMuslo", "AD03_Reposo"],
        "S03_SelladoVacio": ["S02_Embandejado"],
        "S04_Etiquetado": ["S01_BolsaGranel", "S03_SelladoVacio"],
        "GF01_TunelEnfriamiento": ["S04_Etiquetado", "V03_EmpaqueViscera"],
        "GF02_ControlCadenaFrio": ["GF01_TunelEnfriamiento"],
        "ALMAC_CuartoFrio": ["GF02_ControlCadenaFrio"]
    }
    
    return {
        "tareas": tareas,
        "estaciones": estaciones,
        "tiempos": tiempos,
        "precedencias": precedencias,
        "tiempo_ciclo": 45,
        "tarea_coproducto": tarea_coproducto,
        "coproductos": COPRODUCTOS,
        "demanda": DEMANDA,
        "costo_estacion": COSTO_ESTACION
    }


def resolver_dlbp_profit(instancia: Dict, verbose: bool = True) -> Dict:
    """
    Resuelve el problema DLBP usando función objetivo de MAXIMIZACIÓN DE BENEFICIO.
    
    Función Objetivo (Liang et al. 2023 adaptado):
    MAX Z = Σ(Ingresos por ventas) - Σ(Costos de estaciones) - Σ(Penalizaciones)
    
    Donde:
    - Ingresos = Σ v_p * min(q_p, d_p) para cada coproducto p
    - Costos = c_s * Σ y_s para estaciones activas
    - Penalizaciones = Σ (π_p * I_p^- + h_p * I_p^+)
    """
    tareas = instancia["tareas"]
    estaciones = instancia["estaciones"]
    tiempos = instancia["tiempos"]
    precedencias = instancia["precedencias"]
    C = instancia["tiempo_ciclo"]
    tarea_coproducto = instancia["tarea_coproducto"]
    coproductos = instancia["coproductos"]
    demanda = instancia["demanda"]
    costo_estacion = instancia["costo_estacion"]
    
    if verbose:
        print(f"Resolviendo DLBP Profit-Oriented...")
        print(f"  Tareas: {len(tareas)}, Estaciones: {len(estaciones)}")
        print(f"  Coproductos: {len(coproductos)}, Tiempo de ciclo: {C}s")
    
    # ======================== CREAR PROBLEMA ========================
    prob = LpProblem("DLBP_Profit_Oriented", LpMaximize)
    
    # ======================== VARIABLES ========================
    
    # x_{is}: Tarea i asignada a estación s (binaria)
    x = {
        i: {s: LpVariable(f"x_{i}_{s}", cat=LpBinary) for s in estaciones}
        for i in tareas
    }
    
    # y_s: Estación s está activa (binaria)
    y = {s: LpVariable(f"y_{s}", cat=LpBinary) for s in estaciones}
    
    # q_p: Cantidad producida del coproducto p (continua)
    q = {p: LpVariable(f"q_{p}", lowBound=0, cat=LpContinuous) for p in coproductos}
    
    # I_p_plus: Inventario excedente (continua)
    I_plus = {p: LpVariable(f"I_plus_{p}", lowBound=0, cat=LpContinuous) for p in coproductos}
    
    # I_p_minus: Demanda insatisfecha (continua)
    I_minus = {p: LpVariable(f"I_minus_{p}", lowBound=0, cat=LpContinuous) for p in coproductos}
    
    # ======================== FUNCIÓN OBJETIVO ========================
    
    # Ingresos: Σ v_p * q_p (simplificado: asumimos que vendemos lo producido hasta la demanda)
    ingresos = lpSum(
        coproductos[p]["precio"] * q[p] 
        for p in coproductos
    )
    
    # Costos de estaciones
    costos_estaciones = lpSum(costo_estacion * y[s] for s in estaciones)
    
    # Penalizaciones por inventario y faltantes
    penalizaciones = lpSum(
        coproductos[p]["penalizacion"] * I_minus[p] + 
        coproductos[p]["costo_inventario"] * I_plus[p]
        for p in coproductos
    )
    
    # Objetivo: Maximizar beneficio
    prob += (ingresos - costos_estaciones - penalizaciones), "Maximizar_Beneficio"
    
    # ======================== RESTRICCIONES ========================
    
    # R1: Asignación única
    for i in tareas:
        prob += lpSum(x[i][s] for s in estaciones) == 1, f"Asig_{i[:15]}"
    
    # R2: Precedencias
    for i in tareas:
        for j in precedencias.get(i, []):
            if j in tareas:
                prob += (
                    lpSum(int(s[1:]) * x[j][s] for s in estaciones) <= 
                    lpSum(int(s[1:]) * x[i][s] for s in estaciones),
                    f"Prec_{j[:10]}_{i[:10]}"
                )
    
    # R3: Tiempo de ciclo
    for s in estaciones:
        prob += (
            lpSum(tiempos[i] * x[i][s] for i in tareas) <= C * y[s],
            f"Ciclo_{s}"
        )
    
    # R4: Activación de estación
    for i in tareas:
        for s in estaciones:
            prob += x[i][s] <= y[s], f"Act_{i[:10]}_{s}"
    
    # R5: Producción acotada por demanda (evita Unbounded)
    for p in coproductos:
        prob += q[p] <= demanda.get(p, 0), f"MaxProd_{p}"
    
    # R6: Balance demanda-producción
    for p in coproductos:
        prob += q[p] + I_minus[p] - I_plus[p] == demanda.get(p, 0), f"Balance_{p}"
    
    # ======================== RESOLVER ========================
    prob.solve()
    
    # ======================== RESULTADOS ========================
    if verbose:
        print("\n" + "=" * 70)
        print("RESULTADO DEL MODELO DLBP - PROFIT-ORIENTED")
        print("=" * 70)
        print(f"Estado: {LpStatus[prob.status]}")
        
        if prob.status == 1:  # Optimal
            beneficio = value(prob.objective)
            n_estaciones = sum(1 for s in estaciones if value(y[s]) > 0.5)
            
            print(f"\n📊 MÉTRICAS FINANCIERAS:")
            print(f"   Beneficio Neto: ${beneficio:,.0f} COP")
            print(f"   Ingresos: ${value(ingresos):,.0f} COP")
            print(f"   Costos Estaciones: ${value(costos_estaciones):,.0f} COP ({n_estaciones} activas)")
            print(f"   Penalizaciones: ${value(penalizaciones):,.0f} COP")
            
            print(f"\n📦 PRODUCCIÓN POR COPRODUCTO:")
            for p in coproductos:
                q_val = value(q[p])
                d_val = demanda.get(p, 0)
                if q_val > 0 or d_val > 0:
                    cumplimiento = min(q_val / d_val * 100, 100) if d_val > 0 else 0
                    print(f"   {p}: {q_val:.0f} uds (demanda: {d_val}, cumplimiento: {cumplimiento:.0f}%)")
            
            print(f"\n🏭 ASIGNACIÓN DE ESTACIONES:")
            total_tiempo = 0
            for s in estaciones:
                if value(y[s]) > 0.5:
                    tareas_asig = [i for i in tareas if value(x[i][s]) > 0.5]
                    tiempo_s = sum(tiempos[i] for i in tareas_asig)
                    total_tiempo += tiempo_s
                    util = (tiempo_s / C) * 100
                    print(f"   {s}: {len(tareas_asig)} tareas, {tiempo_s}s/{C}s ({util:.0f}%)")
            
            print(f"\n   Eficiencia Global: {(total_tiempo / (n_estaciones * C)) * 100:.1f}%")
    
    return {
        "status": LpStatus[prob.status],
        "beneficio": value(prob.objective) if prob.status == 1 else None,
        "estaciones_usadas": sum(1 for s in estaciones if value(y[s]) > 0.5),
        "produccion": {p: value(q[p]) for p in coproductos},
        "faltantes": {p: value(I_minus[p]) for p in coproductos if value(I_minus[p]) > 0},
        "excedentes": {p: value(I_plus[p]) for p in coproductos if value(I_plus[p]) > 0}
    }


def main():
    """Función principal."""
    print("=" * 70)
    print("DLBP AVÍCOLA - MODELO PROFIT-ORIENTED")
    print("Basado en Liang et al. (2023) y Liu et al. (2021)")
    print("=" * 70)
    print()
    
    # Crear instancia
    instancia = crear_instancia_completa()
    
    print(f"📋 INSTANCIA CREADA:")
    print(f"   Tareas: {len(instancia['tareas'])}")
    print(f"   Estaciones disponibles: {len(instancia['estaciones'])}")
    print(f"   Coproductos: {len(instancia['coproductos'])}")
    print(f"   Tiempo de ciclo: {instancia['tiempo_ciclo']}s")
    print()
    
    # Resolver
    resultado = resolver_dlbp_profit(instancia)
    
    if resultado["status"] == "Optimal":
        print("\n" + "=" * 70)
        print("✅ MODELO PROFIT-ORIENTED VALIDADO EXITOSAMENTE")
        print("=" * 70)
        
        # Exportar resultados
        with open("resultado_profit.json", "w", encoding="utf-8") as f:
            json.dump({k: v for k, v in resultado.items() if v is not None}, f, indent=2, ensure_ascii=False)
        print("\n💾 Resultados exportados a: resultado_profit.json")


if __name__ == "__main__":
    main()
