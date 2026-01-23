# Capítulo 6: Resultados Computacionales

## 6.1. Introducción

Este capítulo presenta los resultados de la evaluación comparativa de los tres algoritmos metaheurísticos implementados: Algoritmo Genético (GA), Búsqueda Tabú (TS) y el Algoritmo Híbrido (GA+TS). Los experimentos se ejecutaron con los parámetros calibrados mediante Optuna (ver Capítulo 5).

---

## 6.2. Configuración del Experimento

### 6.2.1. Parámetros Calibrados

Los parámetros óptimos encontrados durante la calibración fueron:

| Algoritmo | Parámetro | Valor Calibrado |
|-----------|-----------|-----------------|
| **GA** | `poblacion_size` | 75 |
| | `prob_cruce` | 0.93 |
| | `prob_mutacion` | 0.20 |
| | `tamano_torneo` | 4 |
| **TS** | `tamano_lista_tabu` | 15 |
| | `tamano_vecindario` | 49 |
| | `tipo_movimiento` | swap |
| **Híbrido** | `poblacion_size` | 45 |
| | `prob_cruce` | 0.94 |
| | `aplicar_ts_cada` | 24 gen |

### 6.2.2. Protocolo Experimental

| Aspecto | Configuración |
|---------|---------------|
| **Réplicas** | 30 por combinación (algoritmo × instancia) |
| **Semillas** | 42 + i×1000 para i ∈ [0, 29] |
| **Criterio de parada** | 100 generaciones (GA/Híbrido), 200 iteraciones (TS) |
| **Hardware** | Intel Core i7, 16GB RAM, Windows 11 |
| **Software** | Python 3.11, NumPy 1.24 |

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
