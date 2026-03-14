"""
DLBP Avícola - Generador de Instancias Sintéticas (v2)
=======================================================
Genera instancias con precedencias REALISTAS para experimentación.

Mejoras v2:
- Precedencias con bifurcaciones y convergencias (diamond patterns)
- Distribución de tiempos heterogénea (bimodal: tareas pesadas + ligeras)
- Estructura de grafo DAG variada, no solo cadenas
- Instancias que crean diferenciación entre algoritmos

Autor: Daniel Castañeda
Fecha: Febrero 2026
Fase: Mejora Experimental
"""

import sys
import os
import json
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "algorithms"))
from base import ProblemInstance


@dataclass
class InstanceSpec:
    """Especificación para generar una instancia."""
    nombre: str
    n_tareas: int
    n_areas: int
    tiempo_ciclo: int
    tiempo_min: int
    tiempo_max: int
    densidad_precedencias: float  # 0.0 a 1.0
    tipo_estructura: str = "mixta"  # "cadena", "arbol", "diamante", "mixta"


def generar_precedencias_v2(
    n_tareas: int,
    n_areas: int,
    densidad: float,
    tipo_estructura: str,
    rng: np.random.Generator
) -> Dict[str, List[str]]:
    """
    Genera un grafo de precedencias con estructura variada.
    
    Tipos de estructura:
    - "cadena": secuencial (original, para baseline)
    - "arbol": bifurcaciones (1→N)
    - "diamante": bifurcación + convergencia (diamond patterns)
    - "mixta": combinación de todas (más realista)
    
    Args:
        n_tareas: Número total de tareas
        n_areas: Número de áreas/grupos  
        densidad: Controla cuántas precedencias inter-área se agregan
        tipo_estructura: Tipo de grafo a generar
        rng: Generador aleatorio
        
    Returns:
        Dict {tarea: [lista_predecesoras]}
    """
    tareas = [f"T{i:03d}" for i in range(n_tareas)]
    precedencias = {t: [] for t in tareas}
    
    # Dividir en áreas
    tareas_por_area = n_tareas // n_areas
    areas = []
    for a in range(n_areas):
        inicio = a * tareas_por_area
        fin = inicio + tareas_por_area if a < n_areas - 1 else n_tareas
        areas.append(tareas[inicio:fin])
    
    if tipo_estructura == "cadena":
        _generar_cadenas(areas, precedencias, rng)
    elif tipo_estructura == "arbol":
        _generar_arboles(areas, precedencias, rng)
    elif tipo_estructura == "diamante":
        _generar_diamantes(areas, precedencias, rng)
    elif tipo_estructura == "mixta":
        _generar_mixta(areas, precedencias, rng)
    else:
        _generar_mixta(areas, precedencias, rng)
    
    # Agregar algunas precedencias inter-área (controladas)
    _agregar_precedencias_inter_area(areas, precedencias, densidad, rng)
    
    return precedencias


def _generar_cadenas(areas, precedencias, rng):
    """Precedencias de cadena simple dentro de cada área."""
    for area in areas:
        for i in range(1, len(area)):
            precedencias[area[i]].append(area[i-1])


def _generar_arboles(areas, precedencias, rng):
    """
    Precedencias tipo árbol: la primera tarea del área es raíz,
    las demás se conectan con bifurcaciones (1→2 o 1→3).
    """
    for area in areas:
        if len(area) <= 1:
            continue
        
        # Raíz del árbol
        raiz = area[0]
        pending = [raiz]
        assigned = {raiz}
        idx = 1
        
        while idx < len(area):
            if not pending:
                break
            parent = pending.pop(0)
            # Cada nodo padre tiene 2-3 hijos
            n_hijos = min(rng.integers(2, 4), len(area) - idx)
            for _ in range(n_hijos):
                if idx >= len(area):
                    break
                hijo = area[idx]
                precedencias[hijo].append(parent)
                pending.append(hijo)
                assigned.add(hijo)
                idx += 1


def _generar_diamantes(areas, precedencias, rng):
    """
    Precedencias con patrón diamante: bifurcación + convergencia.
    
    Ejemplo (4 tareas):
        T0 → T1
        T0 → T2  
        T1 → T3
        T2 → T3  (convergencia)
    """
    for area in areas:
        n = len(area)
        if n <= 2:
            for i in range(1, n):
                precedencias[area[i]].append(area[i-1])
            continue
        
        # Crear patrón diamante
        i = 0
        while i < n:
            remaining = n - i
            
            if remaining >= 4:
                # Diamond: 1 raíz → 2 paralelas → 1 convergente
                raiz = area[i]
                par1 = area[i+1]
                par2 = area[i+2]
                conv = area[i+3]
                
                precedencias[par1].append(raiz)
                precedencias[par2].append(raiz)
                precedencias[conv].append(par1)
                precedencias[conv].append(par2)
                
                i += 4
            elif remaining >= 3:
                # Fork: 1 → 2 paralelas
                raiz = area[i]
                precedencias[area[i+1]].append(raiz)
                precedencias[area[i+2]].append(raiz)
                i += 3
            elif remaining == 2:
                precedencias[area[i+1]].append(area[i])
                i += 2
            else:
                i += 1
        
        # Conectar diamantes consecutivos
        # El convergente de un diamante es predecesor de la raíz del siguiente
        for j in range(4, n, 4):
            if j < n and j-1 >= 0:
                # Solo conectar si no están ya conectados
                if area[j-1] not in precedencias[area[j]]:
                    # El último del bloque anterior → primero del siguiente
                    min_j = min(j, n-1)
                    if area[min_j] != area[j-1]:
                        precedencias[area[min_j]].append(area[j-1])


def _generar_mixta(areas, precedencias, rng):
    """
    Combinación de cadenas, árboles y diamantes.
    Cada área usa un patrón diferente para máxima diversidad.
    """
    patrones = ["cadena", "arbol", "diamante"]
    
    for i, area in enumerate(areas):
        patron = patrones[i % 3]
        
        if patron == "cadena":
            # Cadena simple
            for j in range(1, len(area)):
                precedencias[area[j]].append(area[j-1])
        
        elif patron == "arbol":
            _generar_arboles([area], precedencias, rng)
        
        elif patron == "diamante":
            _generar_diamantes([area], precedencias, rng)


def _agregar_precedencias_inter_area(areas, precedencias, densidad, rng):
    """
    Agrega precedencias CONTROLADAS entre áreas.
    
    Estrategia: solo conectar últimas tareas de un área con primeras del siguiente,
    con probabilidad controlada. NO conectar todas las áreas en serie.
    """
    for i in range(1, len(areas)):
        # Conectar con probabilidad proporcional a densidad
        if rng.random() < densidad:
            # Escoger una tarea del último tercio del área anterior
            area_prev = areas[i-1]
            area_curr = areas[i]
            
            if not area_prev or not area_curr:
                continue
            
            # Tarea fuente: del tercio final del área anterior
            tercio = max(1, len(area_prev) // 3)
            idx_fuente = rng.integers(len(area_prev) - tercio, len(area_prev))
            fuente = area_prev[idx_fuente]
            
            # Tarea destino: del primer tercio del área actual
            tercio_dest = max(1, len(area_curr) // 3)
            idx_dest = rng.integers(0, tercio_dest)
            destino = area_curr[idx_dest]
            
            # Verificar que no cree ciclo (fuente index < destino index)
            if fuente not in precedencias[destino]:
                precedencias[destino].append(fuente)


def generar_tiempos_v2(
    tareas: List[str],
    tiempo_min: int,
    tiempo_max: int,
    tiempo_ciclo: int,
    rng: np.random.Generator
) -> Dict[str, int]:
    """
    Genera tiempos con distribución BIMODAL para crear instancias desafiantes.
    
    Mezcla de:
    - Tareas pesadas (cercanas al ciclo): difíciles de empaquetar
    - Tareas ligeras: relleno flexible
    
    Esto crea situaciones donde el orden de asignación importa mucho.
    """
    tiempos = {}
    umbral_pesada = tiempo_ciclo * 0.6  # Tareas que usan >60% del ciclo
    
    for t in tareas:
        if rng.random() < 0.25:  # 25% tareas pesadas
            # Tarea pesada: entre 50% y 90% del ciclo
            t_min_pesada = max(tiempo_min, int(tiempo_ciclo * 0.5))
            t_max_pesada = min(tiempo_max, int(tiempo_ciclo * 0.9))
            if t_min_pesada <= t_max_pesada:
                tiempos[t] = int(rng.integers(t_min_pesada, t_max_pesada + 1))
            else:
                tiempos[t] = int(rng.integers(tiempo_min, tiempo_max + 1))
        else:  # 75% tareas ligeras/medianas
            tiempos[t] = int(rng.integers(tiempo_min, max(tiempo_min + 1, int(tiempo_max * 0.7)) + 1))
    
    return tiempos


def generar_instancia(spec: InstanceSpec, semilla: int = 42) -> ProblemInstance:
    """
    Genera una instancia sintética según la especificación.
    
    Args:
        spec: Especificación de la instancia
        semilla: Semilla para reproducibilidad
        
    Returns:
        ProblemInstance generada
    """
    rng = np.random.default_rng(semilla)
    
    # Generar tareas
    tareas = [f"T{i:03d}" for i in range(spec.n_tareas)]
    
    # Generar precedencias v2
    precedencias = generar_precedencias_v2(
        n_tareas=spec.n_tareas,
        n_areas=spec.n_areas,
        densidad=spec.densidad_precedencias,
        tipo_estructura=spec.tipo_estructura,
        rng=rng
    )
    
    # Generar tiempos v2 (bimodal)
    tiempos = generar_tiempos_v2(
        tareas=tareas,
        tiempo_min=spec.tiempo_min,
        tiempo_max=spec.tiempo_max,
        tiempo_ciclo=spec.tiempo_ciclo,
        rng=rng
    )
    
    return ProblemInstance(
        tareas=tareas,
        tiempos=tiempos,
        precedencias=precedencias,
        tiempo_ciclo=spec.tiempo_ciclo,
        n_estaciones_max=spec.n_tareas  # Máximo teórico
    )


def generar_conjunto_instancias() -> Dict[str, ProblemInstance]:
    """
    Genera un conjunto estándar de instancias para experimentación.
    
    Usa estructura "mixta" para crear instancias con diversidad de 
    precedencias (cadenas + árboles + diamantes), tiempos bimodales,
    y conexiones inter-área controladas.
    
    Returns:
        Dict {nombre: instancia}
    """
    especificaciones = [
        InstanceSpec(
            nombre="pequeña_20t",
            n_tareas=20,
            n_areas=4,
            tiempo_ciclo=30,
            tiempo_min=3,
            tiempo_max=18,       # Mayor rango para tiempos pesados
            densidad_precedencias=0.3,
            tipo_estructura="mixta"
        ),
        InstanceSpec(
            nombre="mediana_40t",
            n_tareas=40,
            n_areas=6,
            tiempo_ciclo=40,
            tiempo_min=3,
            tiempo_max=25,       # Hasta 62% del ciclo como máximo
            densidad_precedencias=0.4,
            tipo_estructura="mixta"
        ),
        InstanceSpec(
            nombre="grande_70t",
            n_tareas=70,
            n_areas=10,
            tiempo_ciclo=45,
            tiempo_min=3,
            tiempo_max=30,       # Hasta 67% del ciclo
            densidad_precedencias=0.35,
            tipo_estructura="mixta"
        ),
        InstanceSpec(
            nombre="muy_grande_100t",
            n_tareas=100,
            n_areas=12,
            tiempo_ciclo=50,
            tiempo_min=3,
            tiempo_max=35,       # Hasta 70% del ciclo
            densidad_precedencias=0.3,
            tipo_estructura="mixta"
        )
    ]
    
    instancias = {}
    for spec in especificaciones:
        instancias[spec.nombre] = generar_instancia(spec, semilla=42)
    
    return instancias


def exportar_instancia(instancia: ProblemInstance, nombre: str, carpeta: str):
    """Exporta una instancia a archivo JSON."""
    os.makedirs(carpeta, exist_ok=True)
    path = os.path.join(carpeta, f"{nombre}.json")
    
    # Convertir numpy types a tipos nativos de Python
    tiempos_nativos = {k: int(v) for k, v in instancia.tiempos.items()}
    
    data = {
        "nombre": nombre,
        "n_tareas": int(instancia.n_tareas),
        "tiempo_ciclo": int(instancia.tiempo_ciclo),
        "tiempo_total": int(instancia.tiempo_total),
        "tareas": instancia.tareas,
        "tiempos": tiempos_nativos,
        "precedencias": instancia.precedencias
    }
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return path


def main():
    """Genera y exporta instancias sintéticas v2."""
    print("=" * 60)
    print("DLBP - GENERADOR DE INSTANCIAS SINTÉTICAS v2")
    print("=" * 60)
    
    # Generar instancias
    instancias = generar_conjunto_instancias()
    
    # Exportar
    carpeta_salida = os.path.join(os.path.dirname(__file__), "..", "..", "data", "instancias_sinteticas")
    
    print(f"\n📦 Generando {len(instancias)} instancias...")
    for nombre, inst in instancias.items():
        path = exportar_instancia(inst, nombre, carpeta_salida)
        
        # Contar precedencias no vacías
        n_prec = sum(1 for p in inst.precedencias.values() if p)
        n_edges = sum(len(p) for p in inst.precedencias.values())
        
        print(f"   ✓ {nombre}: {inst.n_tareas} tareas, ciclo={inst.tiempo_ciclo}s")
        print(f"     Tiempo total: {inst.tiempo_total}s, Precedencias: {n_edges} arcos")
        print(f"     LB estaciones: ⌈{inst.tiempo_total}/{inst.tiempo_ciclo}⌉ = "
              f"{-(-inst.tiempo_total // inst.tiempo_ciclo)}")
    
    print(f"\n💾 Instancias exportadas a: {carpeta_salida}")
    print("=" * 60)


if __name__ == "__main__":
    main()
