# Capítulo 5: Diseño Experimental

## 5.1. Introducción

Este capítulo describe el diseño experimental empleado para evaluar el desempeño de los algoritmos metaheurísticos propuestos (GA, TS, Híbrido) en la resolución del problema DLBP avícola. Se detallan las instancias de prueba, el proceso de calibración de parámetros, y las métricas de evaluación.

---

## 5.2. Generación de Instancias Sintéticas

Dado que los datos reales de plantas avícolas son frecuentemente confidenciales o incompletos, se desarrolló un generador de instancias sintéticas calibrado con parámetros de la literatura [@SolanoBlanco2022; @BeckerScholl2006].

### 5.2.1. Arquitectura del Generador

El generador crea instancias con las siguientes propiedades controladas:

```
Algoritmo: Generación de Instancia DLBP Sintética
─────────────────────────────────────────────────
Entrada: n_tareas, n_areas, tiempo_ciclo, densidad
Salida: Instancia (tareas, tiempos, precedencias)

1: Dividir n_tareas en n_areas grupos
2: Para cada área:
3:    Crear cadena de precedencia secuencial
4: Para cada par de áreas adyacentes:
5:    Conectar última tarea del área i con primera de área i+1
6: Agregar precedencias adicionales según densidad
7: Generar tiempos ~ Uniforme(t_min, t_max)
8: Retornar Instancia
─────────────────────────────────────────────────
```

### 5.2.2. Factores de Variación

Se construyó un conjunto de instancias variando sistemáticamente los siguientes factores:

| Factor | Niveles | Descripción |
|--------|---------|-------------|
| **Tamaño ($n$)** | 20, 40, 70, 100 | Número total de tareas |
| **Complejidad (áreas)** | 4, 6, 10, 12 | Número de subprocesos paralelos |
| **Tiempo de ciclo** | 30-50s | Restricción de capacidad por estación |
| **Densidad de precedencias** | 0.15-0.30 | Conectividad del grafo DAG |

### 5.2.3. Instancias de Prueba

| ID | Tareas | Áreas | Ciclo | Tiempo Total | Estaciones Mín. Teóricas |
|----|--------|-------|-------|--------------|-------------------------|
| `pequeña_20t` | 20 | 4 | 30s | 135s | ⌈135/30⌉ = 5 |
| `mediana_40t` | 40 | 6 | 40s | 362s | ⌈362/40⌉ = 10 |
| `grande_70t` | 70 | 10 | 45s | 740s | ⌈740/45⌉ = 17 |
| `muy_grande_100t` | 100 | 12 | 50s | 1076s | ⌈1076/50⌉ = 22 |

---

## 5.3. Calibración de Parámetros (Tuning)

### 5.3.1. Motivación

El desempeño de las metaheurísticas es altamente sensible a la configuración de sus parámetros [@EibenSmith2015]. Una calibración empírica rigurosa mejora la calidad de las soluciones y la comparabilidad de los resultados.

### 5.3.2. Metodología: Optuna

Se empleó el framework **Optuna** [@Akiba2019] para calibración automática de hiperparámetros mediante muestreo bayesiano (TPE - Tree-structured Parzen Estimator).

```python
# Esquema de calibración con Optuna
def objective(trial):
    params = {
        "poblacion_size": trial.suggest_int("pop", 30, 150),
        "prob_cruce": trial.suggest_float("cx", 0.6, 0.95),
        "prob_mutacion": trial.suggest_float("mut", 0.05, 0.25)
    }
    fitness = ejecutar_algoritmo(params)
    return fitness  # Minimizar
```

### 5.3.3. Espacio de Búsqueda

| Algoritmo | Parámetro | Tipo | Rango |
|-----------|-----------|------|-------|
| **GA** | `poblacion_size` | int | [30, 150] |
| | `prob_cruce` | float | [0.6, 0.95] |
| | `prob_mutacion` | float | [0.05, 0.25] |
| **TS** | `tamano_lista_tabu` | int | [7, 30] |
| | `tamano_vecindario` | int | [15, 50] |
| **Híbrido** | `aplicar_ts_cada` | int | [5, 30] |
| | `top_n_para_ts` | int | [3, 10] |

### 5.3.4. Protocolo de Calibración

1. **Instancia de entrenamiento:** `mediana_40t` (representativa del tamaño típico)
2. **Número de trials:** 50 por algoritmo
3. **Repeticiones:** 3 por evaluación (promedio robusto)
4. **Métrica objetivo:** Número de estaciones (minimizar)

---

## 5.4. Métricas de Evaluación

### 5.4.1. Métricas Primarias

| Métrica | Fórmula | Descripción |
|---------|---------|-------------|
| **Número de estaciones** ($n_s$) | - | Objetivo principal del DLBP |
| **Eficiencia de línea** ($\eta$) | $\eta = \frac{\sum t_i}{n_s \cdot C} \times 100\%$ | Utilización promedio |
| **Tiempo de cómputo** ($T$) | segundos | Eficiencia computacional |

### 5.4.2. Métricas de Robustez

| Métrica | Descripción |
|---------|-------------|
| **Desviación estándar** | Variabilidad entre repeticiones |
| **Tasa de factibilidad** | % de ejecuciones que producen solución válida |
| **Convergencia** | Iteración donde se alcanza el mejor valor |

---

## 5.5. Protocolo Experimental

### 5.5.1. Configuración de Ejecución

| Parámetro | Valor |
|-----------|-------|
| **Hardware** | CPU Intel i7, 16GB RAM |
| **Lenguaje** | Python 3.11 |
| **Repeticiones** | 30 por combinación (algoritmo × instancia) |
| **Semillas** | 42 + i×1000 para i ∈ [0, 29] |

### 5.5.2. Comparaciones Estadísticas

Se empleará el test de Friedman para comparar los rangos de los algoritmos sobre las instancias, seguido de comparaciones *post-hoc* con la corrección de Bonferroni si existen diferencias significativas (α = 0.05).

---

## Referencias del Capítulo

Las referencias citadas en este capítulo se encuentran en el archivo `referencias_dlbp.bib` del proyecto.
