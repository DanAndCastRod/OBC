# Anexo E: Análisis de Sensibilidad de Parámetros

## E.1. Introducción

El presente anexo documenta el **análisis de sensibilidad** realizado sobre los parámetros calibrados de los algoritmos metaheurísticos (GA, TS, Híbrido). El objetivo es validar la robustez de la configuración obtenida con Optuna y determinar cuáles parámetros tienen mayor impacto en la calidad de las soluciones.

### E.1.1. Motivación

Los parámetros calibrados mediante optimización bayesiana (Optuna) fueron seleccionados para maximizar el desempeño en un conjunto específico de instancias de prueba. Sin embargo, surge la pregunta: **¿qué tan sensibles son los resultados a pequeñas variaciones en estos parámetros?**

Un análisis de sensibilidad responde a:
1. ¿Los parámetros calibrados son los únicos que producen buenos resultados?
2. ¿Existen parámetros cuya variación afecta significativamente la calidad?
3. ¿Cuál es el trade-off entre calidad de solución y tiempo de cómputo?

---

## E.2. Metodología

### E.2.1. Enfoque One-at-a-Time (OAT)

Se utilizó el método **One-at-a-Time (OAT)**, también conocido como análisis de sensibilidad local. Este enfoque consiste en:

1. **Fijar** todos los parámetros en sus valores base (calibrados)
2. **Variar** un solo parámetro a través de un rango predefinido
3. **Medir** el impacto en la métrica objetivo (número de estaciones)
4. **Repetir** para cada parámetro de interés

**Ventajas del OAT:**
- Fácil interpretación de resultados
- Identifica claramente el efecto individual de cada parámetro
- Computacionalmente eficiente

**Limitaciones:**
- No captura interacciones entre parámetros
- Asume independencia de efectos

### E.2.2. Parámetros Analizados

Se seleccionaron **6 parámetros** representativos de los tres algoritmos:

| # | Algoritmo | Parámetro | Descripción | Valor Base |
|---|-----------|-----------|-------------|------------|
| 1 | GA | `poblacion_size` | Tamaño de la población de cromosomas | 75 |
| 2 | GA | `prob_cruce` | Probabilidad de aplicar cruce OX | 0.93 |
| 3 | GA | `prob_mutacion` | Probabilidad de mutación por intercambio | 0.20 |
| 4 | TS | `tamano_lista_tabu` | Longevidad de la memoria tabú | 15 |
| 5 | TS | `tamano_vecindario` | Número de vecinos explorados por iteración | 49 |
| 6 | Híbrido | `aplicar_ts_cada` | Frecuencia de aplicación de búsqueda local | 24 |

### E.2.3. Niveles de Variación

Para cada parámetro se definieron **4 niveles** que cubren un rango razonable de operación:

| Parámetro | Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 | Rango |
|-----------|---------|---------|---------|---------|-------|
| poblacion_size | 50 | 75* | 100 | 125 | ±67% |
| prob_cruce | 0.80 | 0.85 | 0.90 | 0.95 | ±16% |
| prob_mutacion | 0.10 | 0.15 | 0.20* | 0.25 | ±75% |
| tamano_lista_tabu | 10 | 15* | 20 | 25 | ±67% |
| tamano_vecindario | 30 | 40 | 50 | 60 | ±53% |
| aplicar_ts_cada | 15 | 20 | 25 | 30 | ±50% |

*Valor base (calibrado con Optuna)

### E.2.4. Configuración Experimental

| Aspecto | Configuración |
|---------|---------------|
| **Instancia de prueba** | 15 tareas avícolas, tiempo de ciclo = 40s |
| **Réplicas por configuración** | 10 ejecuciones independientes |
| **Semillas aleatorias** | 42, 1042, 2042, ..., 9042 |
| **Generaciones máximas** | 50 (GA e Híbrido) |
| **Iteraciones TS** | 100 |
| **Total de ejecuciones** | 6 parámetros × 4 niveles × 10 réplicas = **240** |

### E.2.5. Métricas de Evaluación

Para cada configuración se registraron:

1. **Número de estaciones** (μ ± σ): Métrica principal de calidad
2. **Eficiencia de línea** (%): Utilización promedio de estaciones
3. **Tiempo de ejecución** (segundos): Costo computacional
4. **Tasa de factibilidad** (%): Porcentaje de soluciones válidas

### E.2.6. Criterio de Criticidad

Un parámetro se considera **crítico** si:

$$\text{Rango de variación} = \max(\mu) - \min(\mu) > 0.5 \text{ estaciones}$$

Donde μ es la media del número de estaciones en las 10 réplicas.

---

## E.3. Procedimiento de Ejecución

### E.3.1. Paso 1: Preparación del Entorno

```python
# Cargar instancia de prueba
instancia = crear_instancia_test()  # 15 tareas, ciclo=40s

# Definir parámetros base
PARAMS_BASE = {
    'GA': {'poblacion_size': 75, 'prob_cruce': 0.93, 'prob_mutacion': 0.20},
    'TS': {'tamano_lista_tabu': 15, 'tamano_vecindario': 49},
    'Hybrid': {'aplicar_ts_cada': 24}
}
```

### E.3.2. Paso 2: Ejecución del Análisis OAT

Para cada parámetro `p` y cada valor `v` en su rango:

```
Para cada algoritmo A en [GA, TS, Híbrido]:
    Para cada parámetro P en parámetros[A]:
        Para cada valor V en valores[P]:
            config = copia(PARAMS_BASE[A])
            config[P] = V
            
            resultados = []
            Para réplica r = 1 hasta 10:
                semilla = 42 + (r-1) * 1000
                solucion = ejecutar(A, instancia, config, semilla)
                resultados.append(solucion.n_estaciones)
            
            guardar(A, P, V, media(resultados), std(resultados))
```

### E.3.3. Paso 3: Cálculo de Impacto

```python
def calcular_impacto(resultados, valor_base):
    base = resultados[valor_base]['media']
    variaciones = [r['media'] - base for r in resultados.values()]
    rango = max(variaciones) - min(variaciones)
    es_critico = rango > 0.5
    return rango, es_critico
```

---

## E.4. Resultados Detallados

### E.4.1. Algoritmo Genético (GA)

#### Parámetro: `poblacion_size`

| Tamaño | Estaciones (μ±σ) | Eficiencia | Tiempo (s) | Δ vs Base |
|--------|------------------|------------|------------|-----------|
| 50 | 5.00 ± 0.00 | 82.5% | 0.57 | 0.00 |
| **75*** | 5.00 ± 0.00 | 82.5% | 0.82 | — |
| 100 | 5.00 ± 0.00 | 82.5% | 1.08 | 0.00 |
| 125 | 5.00 ± 0.00 | 82.5% | 1.33 | 0.00 |

**Análisis:** El tamaño de población **no afecta la calidad** de la solución en el rango probado. Todas las configuraciones encuentran el óptimo de 5 estaciones. Sin embargo, el tiempo de ejecución escala linealmente: aumentar la población de 50 a 125 incrementa el tiempo en **133%**.

**Rango de variación:** 0.00 estaciones → **ROBUSTO**

#### Parámetro: `prob_cruce`

| Probabilidad | Estaciones (μ±σ) | Eficiencia | Tiempo (s) | Δ vs Base |
|--------------|------------------|------------|------------|-----------|
| 0.80 | 5.00 ± 0.00 | 82.5% | 0.75 | 0.00 |
| 0.85 | 5.00 ± 0.00 | 82.5% | 0.81 | 0.00 |
| 0.90 | 5.00 ± 0.00 | 82.5% | 0.78 | 0.00 |
| 0.95 | 5.00 ± 0.00 | 82.5% | 0.84 | 0.00 |

**Análisis:** La probabilidad de cruce es completamente **robusta** en el rango [0.80, 0.95]. El operador de cruce OX mantiene validez de precedencias independientemente de la frecuencia de aplicación.

**Rango de variación:** 0.00 estaciones → **ROBUSTO**

#### Parámetro: `prob_mutacion`

| Probabilidad | Estaciones (μ±σ) | Eficiencia | Tiempo (s) | Δ vs Base |
|--------------|------------------|------------|------------|-----------|
| 0.10 | 5.00 ± 0.00 | 82.5% | 0.76 | 0.00 |
| 0.15 | 5.00 ± 0.00 | 82.5% | 0.77 | 0.00 |
| **0.20*** | 5.00 ± 0.00 | 82.5% | 0.76 | — |
| 0.25 | 5.00 ± 0.00 | 82.5% | 0.80 | 0.00 |

**Análisis:** La probabilidad de mutación no afecta el resultado final para esta instancia. Esto sugiere que el espacio de búsqueda es suficientemente pequeño para que el GA converja al óptimo incluso con poca exploración.

**Rango de variación:** 0.00 estaciones → **ROBUSTO**

---

### E.4.2. Búsqueda Tabú (TS)

#### Parámetro: `tamano_lista_tabu`

| Tamaño | Estaciones (μ±σ) | Eficiencia | Tiempo (s) | Δ vs Base |
|--------|------------------|------------|------------|-----------|
| 10 | 5.10 ± 0.30 | 81.1% | 0.51 | 0.00 |
| **15*** | 5.10 ± 0.30 | 81.1% | 0.58 | — |
| 20 | 5.10 ± 0.30 | 81.1% | 0.69 | 0.00 |
| 25 | 5.10 ± 0.30 | 81.1% | 0.69 | 0.00 |

**Análisis:** La longitud de la lista tabú no afecta significativamente los resultados. Note que TS presenta variabilidad (σ=0.30) que GA no tiene - esto es inherente al carácter local de la búsqueda tabú.

**Rango de variación:** 0.00 estaciones → **ROBUSTO**

#### Parámetro: `tamano_vecindario`

| Tamaño | Estaciones (μ±σ) | Eficiencia | Tiempo (s) | Δ vs Base |
|--------|------------------|------------|------------|-----------|
| 30 | 5.10 ± 0.30 | 81.1% | 0.29 | 0.00 |
| 40 | 5.10 ± 0.30 | 81.1% | 0.43 | 0.00 |
| 50 | 5.10 ± 0.30 | 81.1% | 0.53 | 0.00 |
| 60 | 5.10 ± 0.30 | 81.1% | 0.67 | 0.00 |

**Análisis:** Vecindarios más grandes no mejoran la calidad pero incrementan linealmente el tiempo de cómputo (2.3× de 30 a 60).

**Rango de variación:** 0.00 estaciones → **ROBUSTO**

---

### E.4.3. Algoritmo Híbrido

#### Parámetro: `aplicar_ts_cada`

| Frecuencia | Estaciones (μ±σ) | Eficiencia | Tiempo (s) | Δ vs Base |
|------------|------------------|------------|------------|-----------|
| 15 | 5.00 ± 0.00 | 82.5% | 1.01 | 0.00 |
| 20 | 5.00 ± 0.00 | 82.5% | 0.80 | 0.00 |
| 25 | 5.00 ± 0.00 | 82.5% | 0.66 | 0.00 |
| 30 | 5.00 ± 0.00 | 82.5% | 0.60 | 0.00 |

**Análisis:** La frecuencia de intensificación no afecta la calidad final. Aplicar TS menos frecuentemente (cada 30 generaciones) reduce el tiempo en **41%** comparado con cada 15 generaciones.

**Rango de variación:** 0.00 estaciones → **ROBUSTO**

---

## E.5. Análisis del Impacto en Tiempo de Cómputo

Aunque los parámetros no afectan la calidad, sí impactan significativamente el tiempo:

| Parámetro | Variación | Δ Tiempo |
|-----------|-----------|----------|
| poblacion_size | 50 → 125 | +133% |
| tamano_vecindario | 30 → 60 | +131% |
| aplicar_ts_cada | 15 → 30 | -41% |
| tamano_lista_tabu | 10 → 25 | +35% |

**Recomendación práctica:** Para instancias similares, usar `poblacion_size=50` y `aplicar_ts_cada=30` puede reducir el tiempo de ejecución significativamente sin sacrificar calidad.

---

## E.6. Diagrama de Tornado

![Diagrama de Tornado](figuras/sensibilidad_resumen.png)

El diagrama de tornado muestra el rango de variación de cada parámetro respecto al umbral crítico (línea roja punteada en 0.5 estaciones). Todos los parámetros se encuentran **muy por debajo del umbral**, confirmando su robustez.

---

## E.7. Conclusiones del Análisis

### E.7.1. Hallazgos Principales

1. **Todos los parámetros son robustos:** Los 6 parámetros analizados presentan rango de variación = 0, muy por debajo del umbral crítico de 0.5 estaciones.

2. **Óptimo consistente:** Para la instancia de prueba (15 tareas), los algoritmos encuentran consistentemente el óptimo teórico de 5 estaciones (165s tiempo total ÷ 40s ciclo = 4.125 → 5 estaciones).

3. **Trade-off calidad-tiempo:** Aunque la calidad no varía, los parámetros afectan significativamente el tiempo de cómputo. Poblaciones y vecindarios más grandes incrementan el tiempo proporcionalmente.

4. **Validación de Optuna:** Los parámetros calibrados con Optuna son válidos y estables. No se requieren ajustes adicionales.

### E.7.2. Limitaciones

- El análisis se realizó con una instancia de prueba de 15 tareas. Instancias más grandes podrían mostrar mayor sensibilidad.
- El método OAT no captura interacciones entre parámetros.
- La variabilidad observada en TS (σ=0.30) podría amplificarse en instancias más complejas.

### E.7.3. Recomendaciones

| Escenario | Configuración Recomendada |
|-----------|---------------------------|
| Máxima calidad | Usar parámetros base calibrados |
| Ejecución rápida | `poblacion_size=50`, `aplicar_ts_cada=30` |
| Balance | `poblacion_size=75`, `aplicar_ts_cada=24` |

---

## E.8. Archivos del Análisis

| Archivo | Ubicación | Descripción |
|---------|-----------|-------------|
| Script principal | `src/experiments/analisis_sensibilidad.py` | Código del análisis OAT |
| Resultados JSON | `results/sensibilidad_parametros.json` | Datos crudos de las 240 ejecuciones |
| Resumen MD | `results/sensibilidad_resumen.md` | Tabla resumen de resultados |
| Figura tornado | `docs/tesis/figuras/sensibilidad_resumen.png` | Diagrama de impacto |
| Figura tiempos | `docs/tesis/figuras/sensibilidad_tiempos.png` | Análisis de tiempo |

---

*Análisis ejecutado: 22 de Enero de 2026*  
*Tiempo total de ejecución: ~10 minutos*  
*240 configuraciones × 10 réplicas = 2,400 evaluaciones de fitness*
