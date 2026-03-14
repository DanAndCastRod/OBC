# Anexo G: Comparación con Benchmarks

## G.1. Introducción

Este anexo documenta la comparación de los algoritmos metaheurísticos implementados (GA, TS, Híbrido) contra soluciones óptimas obtenidas mediante programación lineal entera mixta (MILP).

## G.2. Metodología

### G.2.1. Solver Exacto

Se utilizó **PuLP** con el solver **CBC** (COIN-OR Branch and Cut) para obtener soluciones óptimas de referencia. El modelo MILP implementa:

- **Objetivo:** Minimizar número de estaciones
- **Variables:** Asignación binaria tarea-estación
- **Restricciones:** Precedencias, tiempo de ciclo

### G.2.2. Instancias de Prueba

| Instancia | n | Ciclo | Descripción |
|-----------|---|-------|-------------|
| demo_15t | 15 | 40s | Proceso avícola demo |
| lineal_10t | 10 | 25s | Cadena lineal simple |
| paralelo_12t | 12 | 30s | Tareas paralelas |

### G.2.3. Configuración Experimental

| Aspecto | Valor |
|---------|-------|
| Réplicas por algoritmo | 10 |
| Iteraciones máximas | 100 |
| Tiempo límite MILP | 30s |
| Semillas | 42, 142, 242, ... |

---

## G.3. Resultados

### G.3.1. Tabla Comparativa

| Instancia | Óptimo | GA | TS | Híbrido | Mejor Gap |
|-----------|--------|----|----|---------|-----------|
| demo_15t | 5 | 5.0 | 5.0 | 5.0 | **0.0%** |
| lineal_10t | 4 | 4.0 | 4.0 | 5.0 | **0.0%** |
| paralelo_12t | 4 | 4.0 | 4.0 | 4.0 | **0.0%** |

### G.3.2. Análisis por Instancia

#### demo_15t (Instancia Avícola Principal)

| Algoritmo | Est. Media | Std | Gap | Tiempo |
|-----------|------------|-----|-----|--------|
| MILP | 5 | — | 0% | 1.34s |
| GA | 5.0 | 0.0 | 0% | 0.48s |
| TS | 5.0 | 0.0 | 0% | 0.16s |
| Híbrido | 5.0 | 0.0 | 0% | 0.72s |

**Hallazgo:** Todos los algoritmos encuentran el óptimo en todas las réplicas. TS es el más rápido.

#### lineal_10t (Baseline Simple)

| Algoritmo | Est. Media | Std | Gap | Tiempo |
|-----------|------------|-----|-----|--------|
| MILP | 4 | — | 0% | 0.07s |
| GA | 4.0 | 0.0 | 0% | 0.39s |
| TS | 4.0 | 0.0 | 0% | 0.14s |
| Híbrido | 5.0 | 0.0 | 25% | 0.55s |

**Hallazgo:** GA y TS encuentran óptimo. Híbrido tiene gap del 25% debido a parámetros calibrados para instancias más complejas.

#### paralelo_12t (Tareas Paralelas)

| Algoritmo | Est. Media | Std | Gap | Tiempo |
|-----------|------------|-----|-----|--------|
| MILP | 4 | — | 0% | 0.10s |
| GA | 4.0 | 0.0 | 0% | 0.35s |
| TS | 4.0 | 0.0 | 0% | 0.12s |
| Híbrido | 4.0 | 0.0 | 0% | 0.52s |

**Hallazgo:** Todos encuentran óptimo. La ausencia de precedencias facilita la búsqueda.

---

## G.4. Comparación de Tiempos de Ejecución

| Algoritmo | demo_15t | lineal_10t | paralelo_12t | Promedio |
|-----------|----------|------------|--------------|----------|
| **MILP** | 1.34s | 0.07s | 0.10s | 0.50s |
| **GA** | 0.48s | 0.39s | 0.35s | 0.41s |
| **TS** | 0.16s | 0.14s | 0.12s | 0.14s |
| **Híbrido** | 0.72s | 0.55s | 0.52s | 0.60s |

**Observación:** TS es el más rápido con promedio de 0.14s, 3× más rápido que GA.

---

## G.5. Limitaciones

1. **Tamaño de instancias:** El solver MILP excede tiempos razonables para instancias >15 tareas
2. **Falta de benchmarks estándar:** DLBP no tiene repositorio de instancias tan desarrollado como ALBP/SALBP
3. **Parámetros del Híbrido:** Calibrado para instancias más grandes, subóptimo en pequeñas

---

## G.6. Visualizaciones

### Figura G.1: Comparación de Algoritmos por Instancia

\begin{figure}[H]
\centering
\includegraphics[width=0.9\textwidth]{figuras/benchmark_comparacion_instancias.png}
\caption{Comparación del número de estaciones obtenidas por cada algoritmo en las instancias de prueba.}
\label{fig:benchmark_comparacion}
\end{figure}

### Figura G.2: Gap vs Óptimo

\begin{figure}[H]
\centering
\includegraphics[width=0.7\textwidth]{figuras/benchmark_gap_optimo.png}
\caption{Gap promedio respecto al óptimo por algoritmo. GA y TS alcanzan gap=0%.}
\label{fig:benchmark_gap}
\end{figure}

### Figura G.3: Tiempos de Ejecución

\begin{figure}[H]
\centering
\includegraphics[width=0.9\textwidth]{figuras/benchmark_tiempos_ejecucion.png}
\caption{Comparación de tiempos de ejecución entre MILP y metaheurísticas.}
\label{fig:benchmark_tiempos}
\end{figure}

### Figura G.4: Performance Profile

\begin{figure}[H]
\centering
\includegraphics[width=0.8\textwidth]{figuras/benchmark_performance_profile.png}
\caption{Performance profile mostrando la fracción de instancias resueltas dentro del factor τ del mejor resultado.}
\label{fig:benchmark_profile}
\end{figure}

### Figura G.5: Resumen General

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{figuras/benchmark_resumen_general.png}
\caption{Resumen de métricas: gap promedio, tiempo promedio, y óptimos encontrados.}
\label{fig:benchmark_resumen}
\end{figure}

---

## G.7. Conclusiones

1. **GA y TS alcanzan óptimo** en todas las instancias pequeñas/medianas (≤15 tareas)
2. **Gap promedio = 0%** para GA y TS en las 3 instancias probadas
3. **TS es el más rápido** pero GA ofrece mejor balance calidad-diversidad
4. **MILP es exponencial:** Solo viable para instancias pequeñas
5. **Metaheurísticas validadas:** Resultados confirman correcta implementación

---

## G.8. Archivos Generados

| Archivo | Ubicación |
|---------|-----------|
| Script de comparación | `src/experiments/benchmark_comparison.py` |
| Script de gráficos | `src/experiments/generar_graficos_benchmark.py` |
| Resultados JSON | `results/benchmark_comparison.json` |
| Figura: Comparación | `docs/tesis/figuras/benchmark_comparacion_instancias.png` |
| Figura: Gap | `docs/tesis/figuras/benchmark_gap_optimo.png` |
| Figura: Tiempos | `docs/tesis/figuras/benchmark_tiempos_ejecucion.png` |
| Figura: Profile | `docs/tesis/figuras/benchmark_performance_profile.png` |
| Figura: Resumen | `docs/tesis/figuras/benchmark_resumen_general.png` |

---

*Análisis ejecutado: 22 de Enero de 2026*

