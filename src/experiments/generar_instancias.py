"""
DLBP Avícola - Generador de Instancias Sintéticas
==================================================
Genera instancias de prueba de diferentes tamaños para experimentación.

Autor: Daniel Castañeda
Fecha: Enero 2026
Fase: 4 - Experimentación
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


def generar_precedencias_aleatorias(
    n_tareas: int,
    n_areas: int,
    densidad: float,
    rng: np.random.Generator
) -> Dict[str, List[str]]:
    """
    Genera un grafo de precedencias aleatorio pero factible.
    
    Estrategia:
    1. Dividir tareas en áreas (grupos)
    2. Dentro de cada área, crear cadena secuencial
    3. Entre áreas, agregar precedencias según densidad
    
    Args:
        n_tareas: Número total de tareas
        n_areas: Número de áreas/grupos
        densidad: Probabilidad de agregar precedencia entre áreas
        rng: Generador aleatorio
        
    Returns:
        Dict {tarea: [lista_predecesoras]}
    """
    # Generar nombres de tareas
    tareas = [f"T{i:03d}" for i in range(n_tareas)]
    
    # Dividir en áreas
    tareas_por_area = n_tareas // n_areas
    areas = []
    for a in range(n_areas):
        inicio = a * tareas_por_area
        fin = inicio + tareas_por_area if a < n_areas - 1 else n_tareas
        areas.append(tareas[inicio:fin])
    
    precedencias = {t: [] for t in tareas}
    
    # Precedencias dentro de cada área (cadena)
    for area in areas:
        for i in range(1, len(area)):
            precedencias[area[i]].append(area[i-1])
    
    # Precedencias entre áreas (primera tarea de área i depende de última de área i-1)
    for i in range(1, len(areas)):
        if areas[i] and areas[i-1]:
            precedencias[areas[i][0]].append(areas[i-1][-1])
    
    # Agregar precedencias adicionales según densidad
    for i in range(n_tareas):
        for j in range(i+1, n_tareas):
            if rng.random() < densidad * 0.1:  # Factor bajo para no crear ciclos
                # Solo agregar si no crea ciclo (j depende de i)
                if tareas[i] not in precedencias[tareas[j]]:
                    precedencias[tareas[j]].append(tareas[i])
    
    return precedencias


def generar_tiempos_aleatorios(
    tareas: List[str],
    tiempo_min: int,
    tiempo_max: int,
    rng: np.random.Generator
) -> Dict[str, int]:
    """Genera tiempos de procesamiento aleatorios."""
    return {t: rng.integers(tiempo_min, tiempo_max + 1) for t in tareas}


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
    
    # Generar precedencias
    precedencias = generar_precedencias_aleatorias(
        n_tareas=spec.n_tareas,
        n_areas=spec.n_areas,
        densidad=spec.densidad_precedencias,
        rng=rng
    )
    
    # Generar tiempos
    tiempos = generar_tiempos_aleatorios(
        tareas=tareas,
        tiempo_min=spec.tiempo_min,
        tiempo_max=spec.tiempo_max,
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
            tiempo_max=12,
            densidad_precedencias=0.3
        ),
        InstanceSpec(
            nombre="mediana_40t",
            n_tareas=40,
            n_areas=6,
            tiempo_ciclo=40,
            tiempo_min=3,
            tiempo_max=15,
            densidad_precedencias=0.25
        ),
        InstanceSpec(
            nombre="grande_70t",
            n_tareas=70,
            n_areas=10,
            tiempo_ciclo=45,
            tiempo_min=3,
            tiempo_max=18,
            densidad_precedencias=0.2
        ),
        InstanceSpec(
            nombre="muy_grande_100t",
            n_tareas=100,
            n_areas=12,
            tiempo_ciclo=50,
            tiempo_min=3,
            tiempo_max=20,
            densidad_precedencias=0.15
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
    """Genera y exporta instancias sintéticas."""
    print("=" * 60)
    print("DLBP - GENERADOR DE INSTANCIAS SINTÉTICAS")
    print("=" * 60)
    
    # Generar instancias
    instancias = generar_conjunto_instancias()
    
    # Exportar
    carpeta_salida = os.path.join(os.path.dirname(__file__), "..", "..", "data", "instancias_sinteticas")
    
    print(f"\n📦 Generando {len(instancias)} instancias...")
    for nombre, inst in instancias.items():
        path = exportar_instancia(inst, nombre, carpeta_salida)
        print(f"   ✓ {nombre}: {inst.n_tareas} tareas, ciclo={inst.tiempo_ciclo}s")
        print(f"     Tiempo total: {inst.tiempo_total}s, Archivo: {os.path.basename(path)}")
    
    print(f"\n💾 Instancias exportadas a: {carpeta_salida}")
    print("=" * 60)


if __name__ == "__main__":
    main()
