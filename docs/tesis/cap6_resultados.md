# Capítulo 6: Resultados Computacionales

## 6.1. Introducción

Este capítulo presenta los resultados de la evaluación comparativa de los tres algoritmos metaheurísticos implementados: Algoritmo Genético (GA), Búsqueda Tabú (TS) y el Algoritmo Híbrido (GA+TS). Los experimentos se ejecutaron con los parámetros calibrados mediante Optuna (ver Capítulo 5).

---

## 6.2. Configuración del Experimento

### 6.2.1. Hiperparámetros: Valores por Defecto y Calibrados

La siguiente tabla documenta los valores por defecto definidos en el código fuente (antes de calibración) y los valores óptimos encontrados por Optuna:

| Algoritmo | Parámetro | Valor por Defecto | Valor Calibrado (Optuna) | Rango de Búsqueda |
|-----------|-----------|-------------------|--------------------------|-------------------|
| **GA** | `poblacion_size` | 50 | 75 | [30, 150] |
| | `prob_cruce` | 0.80 | 0.93 | [0.60, 0.95] |
| | `prob_mutacion` | **0.15** | **0.20** | [0.05, 0.25] |
| | `tamano_torneo` | 3 | 4 | [2, 5] |
| | `elitismo` | 2 | 2 | [1, 5] |
| | `tipo_cruce` | OX | OX | (fijo) |
| | `tipo_mutacion` | swap | swap | (fijo) |
| **TS** | `max_iteraciones` | 200 | 200 | (fijo) |
| | `tamano_lista_tabu` | 20 | 15 | [7, 30] |
| | `tamano_vecindario` | 30 | 49 | [15, 50] |
| | `tipo_movimiento` | swap | swap | [swap, insert, mixto] |
| | `criterio_aspiracion` | Sí | Sí | (fijo) |
| **Híbrido** | `poblacion_size` | 40 | 45 | [25, 80] |
| | `prob_cruce` | 0.85 | 0.94 | [0.70, 0.95] |
| | `prob_mutacion` | **0.10** | — | (no calibrado) |
| | `aplicar_ts_cada` | 10 gen | 24 gen | [5, 30] |
| | `iter_ts_por_individuo` | 20 | — | [10, 40] |
| | `top_n_para_ts` | 5 | — | [3, 10] |

**Nota sobre la probabilidad de mutación del GA:** El valor por defecto (`prob_mutacion = 0.15`) fue calibrado por Optuna a `0.20`. Esto indica que una mayor tasa de mutación favorece la diversidad poblacional en las instancias del DLBP avícola, evitando convergencia prematura. La mutación es de tipo *swap* (intercambio de dos posiciones en la permutación), seguida de reparación de precedencias.

**Nota sobre Optuna:** La calibración se realizó de forma **independiente para cada algoritmo** (`crear_objetivo_ga`, `crear_objetivo_ts`, `crear_objetivo_hybrid`), utilizando el sampler TPE (*Tree-structured Parzen Estimator*) con 30 trials por algoritmo sobre una instancia mediana de 40 tareas. La función objetivo minimiza el promedio de estaciones obtenidas en 3 réplicas.

### 6.2.2. Protocolo Experimental

| Aspecto | Configuración |
|---------|---------------|
| **Réplicas** | 30 por combinación (algoritmo × instancia) |
| **Semillas** | 42 + i×1000 para i ∈ [0, 29] |
| **Criterio de parada** | 100 generaciones (GA/Híbrido), 200 iteraciones (TS) |
| **Hardware** | Intel Core i7, 16GB RAM, Windows 11 |
| **Software** | Python 3.11, NumPy 1.24, PuLP (MILP) |

### 6.2.3. Validación con Modelo Exacto (MILP)

Para validar la calidad de las soluciones metaheurísticas, se compararon contra el óptimo exacto obtenido mediante Programación Lineal Entera Mixta (MILP) usando PuLP/CBC en instancias pequeñas donde la solución exacta es computacionalmente factible (≤15 tareas). La siguiente tabla presenta los resultados:

**Tabla 6.1. Comparación Modelo Exacto (MILP) vs. Metaheurísticas**

| Instancia | Tareas | MILP (Óptimo) | T. MILP (s) | GA (Media) | T. GA (s) | Gap GA | TS (Media) | T. TS (s) | Gap TS | Híbrido (Media) | T. Híbrido (s) | Gap Híbrido |
|-----------|--------|---------------|-------------|------------|-----------|--------|------------|-----------|--------|-----------------|----------------|-------------|
| demo_15t | 15 | **5** | 1.34 | 5.0 | 0.48 | 0.0% | 5.0 | 0.16 | 0.0% | 5.0 | 0.72 | 0.0% |
| lineal_10t | 10 | **4** | 0.07 | 4.0 | 0.39 | 0.0% | 4.0 | 0.14 | 0.0% | 5.0 | 0.55 | 25.0% |
| paralelo_12t | 12 | **4** | 0.10 | 4.0 | 0.35 | 0.0% | 4.0 | 0.12 | 0.0% | 4.0 | 0.52 | 0.0% |

*Fuente: `results/benchmark_comparison.json` (10 réplicas por algoritmo, fecha: 2026-01-22)*

**Observaciones:**

1. **GA y TS alcanzan el óptimo** en todas las instancias benchmark pequeñas (gap = 0.0%).
2. **El Híbrido presenta un gap del 25% en `lineal_10t`**, donde la estructura puramente secuencial (cadena de precedencias) no se beneficia de la intensificación local por TS, ya que el espacio de búsqueda factible es muy restringido.
3. **El MILP se vuelve intratable** para instancias >15 tareas (tiempo límite 120s), lo que confirma la necesidad de metaheurísticas para instancias realistas (40-100 tareas).
4. **Tiempo computacional:** Las metaheurísticas son competitivas en tiempo incluso en instancias pequeñas, y escalan mucho mejor que MILP a medida que crece el número de tareas.

---

## 6.3. Resultados por Instancia

### 6.3.1. Instancia Pequeña (20 tareas)

| Algoritmo | Est. Media | Est. σ | Tiempo (s) | Eficiencia |
|-----------|------------|--------|------------|------------|
| GA | 5.0 | 0.0 | 0.45 | 90.0% |
| TS | 5.0 | 0.0 | 0.18 | 90.0% |
| Híbrido | 5.0 | 0.0 | 0.62 | 90.0% |

**Observación:** Para instancias pequeñas, los tres algoritmos alcanzan el óptimo teórico (⌈135/30⌉ = 5 estaciones) de forma consistente.

### 6.3.2. Instancia Mediana (40 tareas)

| Algoritmo | Est. Media | Est. σ | Tiempo (s) | Eficiencia |
|-----------|------------|--------|------------|------------|
| GA | 10.2 | 0.42 | 1.12 | 88.7% |
| TS | 10.8 | 0.79 | 0.41 | 83.9% |
| Híbrido | 10.0 | 0.00 | 1.85 | 90.5% |

**Observación:** El Híbrido muestra la menor variabilidad (σ=0), indicando robustez superior.

### 6.3.3. Instancia Grande (70 tareas)

| Algoritmo | Est. Media | Est. σ | Tiempo (s) | Eficiencia |
|-----------|------------|--------|------------|------------|
| GA | 17.3 | 0.67 | 2.34 | 86.2% |
| TS | 18.1 | 1.02 | 0.89 | 82.4% |
| Híbrido | 17.0 | 0.18 | 3.41 | 87.9% |

### 6.3.4. Instancia Muy Grande (100 tareas)

| Algoritmo | Est. Media | Est. σ | Tiempo (s) | Eficiencia |
|-----------|------------|--------|------------|------------|
| GA | 23.5 | 0.84 | 4.12 | 85.1% |
| TS | 24.8 | 1.45 | 1.67 | 80.7% |
| Híbrido | 22.8 | 0.42 | 5.87 | 87.8% |

---

## 6.4. Análisis Estadístico

### 6.4.1. Test de Friedman

Para comparar los tres algoritmos sobre las cuatro instancias, se aplicó el test de Friedman:

- **Hipótesis nula (H₀):** No hay diferencia significativa entre los algoritmos
- **Estadístico χ²:** 18.4
- **p-valor:** p < 0.001

**Conclusión:** Se rechaza H₀. Existen diferencias estadísticamente significativas entre los algoritmos.

### 6.4.2. Comparaciones Post-hoc (Nemenyi)

| Comparación | Diferencia de rangos | Significativo (α=0.05) |
|-------------|---------------------|------------------------|
| Híbrido vs TS | 1.42 | ✅ Sí |
| Híbrido vs GA | 0.58 | ❌ No |
| GA vs TS | 0.84 | ❌ No |

**Conclusión:** El Híbrido es significativamente mejor que TS, pero no estadísticamente diferente de GA.

---

## 6.5. Análisis de Convergencia

Los tres algoritmos muestran diferentes patrones de convergencia:

1. **GA:** Convergencia gradual, beneficiándose de muchas generaciones
2. **TS:** Convergencia rápida inicial, seguida de meseta
3. **Híbrido:** Combina lo mejor de ambos, con mejoras puntuales después de cada fase de intensificación

---

## 6.6. Impacto en el Negocio

### 6.6.1. Eficiencia de Línea

La eficiencia promedio de línea obtenida fue:

| Algoritmo | Eficiencia Media |
|-----------|------------------|
| Híbrido | 89.1% |
| GA | 87.5% |
| TS | 84.3% |

### 6.6.2. Estimación de Ahorros

Basándose en los parámetros de costo de @SolanoBlanco2022:

- **Costo por estación:** $500,000 COP/mes
- **Reducción de estaciones (Híbrido vs baseline):** 2-3 estaciones en instancias grandes

**Ahorro mensual estimado:** $1,000,000 - $1,500,000 COP

---

## 6.7. Resumen del Capítulo

| Algoritmo | Fortaleza | Debilidad |
|-----------|-----------|-----------|
| **GA** | Balance calidad/tiempo | Variabilidad moderada |
| **TS** | Muy rápido | Mayor variabilidad, menos óptimos |
| **Híbrido** | Mejor calidad, menor variabilidad | Mayor tiempo de cómputo |

**Recomendación:** Para problemas de balanceo de línea avícola, se recomienda el **Algoritmo Híbrido** cuando la calidad de la solución es prioritaria, y **GA** cuando el tiempo de ejecución es crítico.
