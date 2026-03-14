# Fase 1: Re-ejecución Experimental Robusta

## Objetivo
Regenerar todos los datos experimentales con rigor estadístico, cubriendo las 4 instancias estándar (20, 40, 70, 100 tareas) con los 4 métodos (MILP, GA, TS, Híbrido).

---

## 1.1 Análisis de Sensibilidad (Corregido)

### Problema Actual
La sensibilidad se ejecutó sobre una instancia trivial (~15 tareas) donde cualquier configuración encuentra el óptimo. Resultado: variación 0% en todos los parámetros.

### Plan de Corrección

**Instancia para sensibilidad:** `mediana_40t.json` (40 tareas) — suficiente complejidad para que los parámetros impacten.

**Parámetros a evaluar:**

| Algoritmo | Parámetro | Rango de Exploración | Puntos |
|-----------|-----------|---------------------|--------|
| **GA** | `poblacion_size` | 30, 50, 75, 100, 150 | 5 |
| **GA** | `prob_cruce` | 0.60, 0.70, 0.80, 0.90, 0.95 | 5 |
| **GA** | `prob_mutacion` | 0.05, 0.10, 0.15, 0.20, 0.25 | 5 |
| **TS** | `tamano_lista_tabu` | 7, 10, 15, 20, 30 | 5 |
| **TS** | `tamano_vecindario` | 15, 25, 35, 49, 60 | 5 |
| **Hybrid** | `aplicar_ts_cada` | 5, 10, 15, 24, 30 | 5 |
| **Hybrid** | `iter_ts_por_individuo` | 10, 20, 28, 35, 40 | 5 |

**Protocolo:**
- 30 réplicas por configuración
- Semillas: 42 + i×1000 (i ∈ [0,29])
- Métrica: estaciones_media, estaciones_std, tiempo_medio
- Al variar un parámetro, fijar los demás en su valor calibrado

### Script a Modificar
`src/experiments/analisis_sensibilidad.py` — cambiar la instancia de `demo_15t` a `mediana_40t.json`.

### Resultado Esperado
- `results/sensibilidad_parametros_v2.json` con variación visible
- Gráficas tipo tornado o spider mostrando impacto relativo

---

## 1.2 Experimento Comparativo Completo

### Problema Actual
`resultados_comparacion.json` tiene solo 1 instancia (`avicola_45t`) con 5 réplicas. El cap6 documenta 4 instancias pero los JSON no los respaldan.

### Plan de Corrección

**Ejecutar `experimento_final.py` con:**
- `n_replicas = 30` (actualmente en 10 en el código, cap6 dice 30)
- Instancias: `pequeña_20t`, `mediana_40t`, `grande_70t`, `muy_grande_100t`
- Algoritmos: GA, TS, Hybrid
- Guardar en: `results/resultados_experimento_final.json` y `.csv`

**Comando:**
```bash
cd c:\Users\facem\OneDrive\Documentos\Maestría\OBC
python src/experiments/experimento_final.py
```

> ⚠️ **IMPORTANTE:** Antes de ejecutar, verificar que `generar_conjunto_instancias()` produce las 4 instancias estándar (20, 40, 70, 100 tareas). Si solo genera 1, hay que corregir el generador.

---

## 1.3 Benchmark MILP Expandido

### Problema Actual
Solo 3 instancias diminutas (10, 12, 15 tareas). No incluye las instancias reales.

### Plan de Corrección

Ejecutar MILP (PuLP/CBC) sobre las 4 instancias estándar con timeout progresivo:

| Instancia | Tareas | Timeout MILP (s) | Resultado Esperado |
|-----------|--------|-------------------|-------------------|
| pequeña_20t | 20 | 120 | Probablemente resuelve |
| mediana_40t | 40 | 300 | Probablemente timeout |
| grande_70t | 70 | 300 | Timeout seguro |
| muy_grande_100t | 100 | 300 | Timeout seguro |

**Métricas a registrar:**
- Mejor solución encontrada (bound superior)
- Mejor cota inferior (lower bound)
- Gap de optimalidad
- Tiempo hasta timeout
- Estado: Optimal / Feasible / Infeasible / Timeout

**Script:** Crear `src/experiments/benchmark_milp_completo.py`

**Resultado:** `results/benchmark_milp_completo.json` con tabla comparativa:
```
| Instancia | Tareas | MILP Best | MILP LB | Gap MILP | GA μ | TS μ | Hybrid μ | Tiempo MILP | Tiempo GA | ...
```

---

## 1.4 Corrección del Fitness = 0.0

### Problema
En `resultados_comparacion.json`, `fitness: 0.0` en todas las ejecuciones. La función `Solution.fitness` probablemente retorna 0 cuando no se ha calculado correctamente.

### Plan
1. Revisar `src/algorithms/base.py` → clase `Solution` → propiedad `fitness`
2. Verificar que el fitness se calcula como función de `n_estaciones` y `eficiencia`
3. Asegurar que el historial de fitness registra valores reales

---

## 1.5 Validación Estadística Real

### Problema
Test de Friedman y Nemenyi documentados en cap6 pero sin datos JSON de soporte.

### Plan
Crear script `src/experiments/tests_estadisticos.py`:
1. Cargar resultados de `resultados_experimento_final.json`
2. Ejecutar test de Friedman (`scipy.stats.friedmanchisquare`)
3. Ejecutar post-hoc Nemenyi (`scikit-posthocs`)
4. Guardar resultados en `results/tests_estadisticos.json`
5. Generar tabla de rangos y diagrama de diferencias críticas

---

## Entregables de Fase 1

| Archivo | Descripción |
|---------|-------------|
| `results/sensibilidad_parametros_v2.json` | Sensibilidad sobre instancia mediana |
| `results/resultados_experimento_final.json` | Experimento completo, 4 instancias, 30 réplicas |
| `results/resultados_experimento_final.csv` | Mismo en CSV para análisis externo |
| `results/benchmark_milp_completo.json` | MILP en las 4 instancias con timeout |
| `results/tests_estadisticos.json` | Friedman + Nemenyi |
| `src/experiments/benchmark_milp_completo.py` | Script nuevo para MILP expandido |
| `src/experiments/tests_estadisticos.py` | Script nuevo para análisis estadístico |

## Estimación de Tiempo
- Sensibilidad (con 30 réplicas × 7 params × 5 valores): ~20a 40 min
- Experimento final (4 instancias × 3 algos × 30 réplicas): ~15 min
- Benchmark MILP: ~25 min (mayormente timeouts)
- Tests estadísticos: ~1 min
- **Total estimado: 1-2 horas**
