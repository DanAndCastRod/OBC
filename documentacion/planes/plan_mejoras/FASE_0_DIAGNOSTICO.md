# Fase 0: Diagnóstico Integral del Proyecto

## Resumen Ejecutivo

Este diagnóstico identifica las debilidades críticas encontradas al auditar los datos experimentales, el código fuente y la presentación de sustentación.

---

## 🔴 Problemas Críticos Identificados

### 1. Análisis de Sensibilidad: Resultados Planos (No Informativo)

**Archivo:** `results/sensibilidad_parametros.json`

| Algoritmo | Parámetro | Valores Probados | Resultado | Variación |
|-----------|-----------|------------------|-----------|-----------|
| GA | poblacion_size | 50, 75, 100, 125 | **5.0 estaciones en TODOS** | 0% |
| GA | prob_cruce | 0.80, 0.85, 0.90, 0.95 | **5.0 estaciones en TODOS** | 0% |
| GA | prob_mutacion | 0.10, 0.15, 0.20, 0.25 | **5.0 estaciones en TODOS** | 0% |
| TS | tamano_lista_tabu | 10, 15, 20, 25 | **5.1 estaciones en TODOS** | 0% |
| TS | tamano_vecindario | 30, 40, 50, 60 | **5.1 estaciones en TODOS** | 0% |
| Hybrid | aplicar_ts_cada | 15, 20, 25, 30 | **5.0 estaciones en TODOS** | 0% |

**Diagnóstico:** La instancia usada es trivialmente pequeña (~15 tareas). Con tan pocas tareas, cualquier configuración encuentra el óptimo, haciendo el análisis de sensibilidad inútil.

**Solución:** Ejecutar sensibilidad sobre instancias mediana (40t) y grande (70t), donde los parámetros SÍ impactan la calidad.

---

### 2. Benchmark MILP: Escala Insuficiente

**Archivo:** `results/benchmark_comparison.json`

- Solo 3 instancias: `lineal_10t`, `paralelo_12t`, `demo_15t`
- MILP resuelve todo en <1.4 segundos
- Con instancias tan pequeñas, no se demuestra la ventaja de las metaheurísticas
- **No se incluyen las 4 instancias reales (20, 40, 70, 100 tareas)**

**Solución:** Ejecutar MILP con timeout en las 4 instancias principales, documentar intratabilidad.

---

### 3. Resultados Comparativos: Solo 1 Instancia, 5 Réplicas

**Archivo:** `src/experiments/resultados_comparacion.json`

- Solo la instancia `avicola_45t` (no existe en las 4 instancias estándar)
- Solo 5 semillas (42, 1042, 2042, 3042, 4042) — no las 30 del protocolo
- Todos los algoritmos encuentan exactamente 8 estaciones
- **Fitness = 0.0 en todas las ejecuciones** (valor sospechoso)

**Diagnóstico:** `cap6_resultados.md` tiene tablas con datos para 20/40/70/100 tareas que sí diferencian, pero NO hay JSON que respalde esos números. Posible datos hardcodeados en el documento.

---

### 4. Calibración Incompleta del Híbrido

**Archivo:** `config/algorithm_params.yaml`

El algoritmo Híbrido tiene **5 parámetros calibrados por Optuna**, pero la tabla en `cap6_resultados.md` marca `prob_mutacion` como "no calibrado" y `iter_ts_por_individuo` y `top_n_para_ts` como "—".

Sin embargo, `algorithm_params.yaml` muestra:
```yaml
Hybrid:
  fitness_obtenido: 10.0
  parametros:
    aplicar_ts_cada: 24
    iter_ts_por_individuo: 28
    poblacion_size: 45
    prob_cruce: 0.937678576602479
    top_n_para_ts: 4
```

**Paradoja:** Los valores están calibrados pero marcados como "—" en la documentación. Además, `prob_mutacion` no aparece en el YAML ni en Optuna, pero sí en el código del Híbrido.

---

### 5. Presentación: Contenido Faltante

La presentación (`sustentacion_dlbp.html`) NO muestra:

| Elemento | Estado |
|----------|--------|
| Metodología de búsqueda bibliográfica (SLR) | ❌ No existe |
| Resultados de búsqueda (queries, resultados, filtros) | ❌ No existe |
| Tabla de calibración de TS e Híbrido | ❌ Solo muestra GA |
| Tabla comparativa 4 instancias × 4 algoritmos | ❌ No existe |
| Test de Friedman y post-hoc | ❌ No existe |
| Gráficas de convergencia reales | ❓ Charts estáticos sin datos del JSON |

---

## 🟡 Problemas Moderados

1. **Gráficos de sensibilidad**: Parecen "planos" porque los datos son idénticos — no es un error visual, es que los datos son planos
2. **Métricas del Proyecto**: El slide "Resumen del Proyecto" referencia una imagen (`resumen_proyecto.png`) que puede no existir o ser genérica
3. **Historial de fitness = 0.0**: En `resultados_comparacion.json`, todos los valores de fitness son 0.0 — indica que la función de fitness probablemente no se está registrando correctamente (el `n_estaciones` sí se registra)

---

## 🟢 Datos Existentes Válidos

1. **`cap6_resultados.md`** tiene tablas por instancia que SÍ muestran diferenciación
2. **Calibración con Optuna** funciona para los 3 algoritmos
3. **El código del experimento final** está estructurado correctamente para 30 réplicas
4. **Test de Friedman y Nemenyi** documentados en cap6 (aunque falta verificar datos de soporte)
5. **Instancias sintéticas** bien definidas (20, 40, 70, 100 tareas)

---

## Siguiente Paso

→ Ver **FASE_1** para el plan de re-ejecución experimental y **FASE_2** para actualización de la presentación.
