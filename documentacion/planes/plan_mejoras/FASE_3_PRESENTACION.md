# Fase 3: Actualización de la Presentación de Sustentación

## Objetivo
Integrar en `docs/presentacion/sustentacion_dlbp.html` todos los datos experimentales reales, con visualizaciones robustas y tablas completas.

---

## 3.1 Slides a Agregar/Modificar

### 3.1.1 [NUEVO] Metodología de Revisión Bibliográfica
- Diagrama PRISMA simplificado
- Estadísticas de búsqueda (queries, resultados, filtros)
- Insertar **después del slide de Tendencias Emergentes**

### 3.1.2 [MODIFICAR] Calibración de Parámetros (actualmente solo GA)

**Estado actual:** Solo muestra la tabla de GA con el gráfico de Optuna.

**Después del cambio:** Mostrar los 3 algoritmos:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Calibración con Optuna (TPE)                      │
├──────────────┬──────────────────────┬────────────────┬───────────────┤
│  Parámetro   │ GA (Calibrado)       │ TS (Calibrado) │ Híbrido (Cal) │
├──────────────┼──────────────────────┼────────────────┼───────────────┤
│ poblacion    │ 75                   │ —              │ 45            │
│ prob_cruce   │ 0.93                 │ —              │ 0.94          │
│ prob_mutacion│ 0.20                 │ —              │ 0.10 (defecto)│
│ tamano_torneo│ 4                    │ —              │ —             │
│ elitismo     │ 1                    │ —              │ —             │
│ lista_tabu   │ —                    │ 15             │ —             │
│ vecindario   │ —                    │ 49             │ —             │
│ movimiento   │ —                    │ swap           │ —             │
│ aplicar_ts   │ —                    │ —              │ cada 24 gen   │
│ iter_ts_ind  │ —                    │ —              │ 28            │
│ top_n_ts     │ —                    │ —              │ 4             │
└──────────────┴──────────────────────┴────────────────┴───────────────┘
```

### 3.1.3 [NUEVO] Tabla Comparativa: 4 Instancias × 4 Algoritmos

**Este es el slide más importante:**

```
┌──────────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ Instancia    │ Tareas   │ MILP     │ GA (μ±σ) │ TS (μ±σ) │ Híb(μ±σ) │
├──────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ pequeña_20t  │ 20       │ 5*       │ 5.0±0.0  │ 5.0±0.0  │ 5.0±0.0  │
│ mediana_40t  │ 40       │ Timeout  │ 10.2±0.42│ 10.8±0.79│ 10.0±0.0 │
│ grande_70t   │ 70       │ Timeout  │ 17.3±0.67│ 18.1±1.02│ 17.0±0.18│
│ muy_grande   │ 100      │ Timeout  │ 23.5±0.84│ 24.8±1.45│ 22.8±0.42│
└──────────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
* Valores reales a completar tras re-ejecución (Fase 1)
```

### 3.1.4 [MODIFICAR] Análisis de Sensibilidad

**Reemplazar** los gráficos planos actuales con datos de la instancia mediana (40t).

- Chart.js con barras agrupadas mostrando variación real
- Tornado chart si es posible
- Destacar parámetros críticos vs. no-críticos

### 3.1.5 [MODIFICAR] Benchmark / Validación MILP

**Expandir** de 3 instancias a las 4 instancias principales:
- Mostrar MILP status (Optimal / Timeout)  
- Mostrar gap de optimalidad cuando existe
- Demostrar visualmente la intratabilidad creciente

### 3.1.6 [MODIFICAR] Gráfica "Resultados en Números" (Chart.js)

**Actualizar datos** del Chart.js para reflejar los resultados reales:
- Bar chart: estaciones por instancia por algoritmo
- Radar chart: eficiencia, tiempo, variabilidad

### 3.1.7 [NUEVO] Test Estadístico (Friedman + Nemenyi)

Nuevo slide con:
- Hipótesis nula/alternativa
- Valor χ² y p-valor
- Tabla de comparaciones post-hoc
- Diagrama de diferencias críticas (opcional)

### 3.1.8 [ELIMINAR/REFORMULAR] Métricas del Proyecto y Resumen

Los slides "Métricas del Proyecto" (50 tests, 6 params calibrados, etc.) y "Resumen del Proyecto" (imagen estática) deben:
- Reemplazar con métricas basadas en datos reales
- Eliminar imagen estática si no existe
- Mostrar métricas del proceso experimental real

---

## 3.2 Corrección de Datos en Charts Existentes

### Gráfico de Convergencia (Chart.js existente)
Actualmente muestra datos hardcodeados. Cambiar a:
- Cargar datos reales del historial de fitness
- Mostrar convergencia diferenciada entre algoritmos

### Gráfico de Comparación Visual
Actualmente los datos del `datasets` son estáticos. Actualizarlos con:
- Datos de `results/resultados_experimento_final.json`
- O al menos datos coherentes con cap6

---

## 3.3 Verificación de Parámetros Específicos

### Probabilidad de Mutación del GA
- **Valor por defecto:** 0.15 (en `genetic_algorithm.py`)
- **Valor calibrado:** 0.20 (en `algorithm_params.yaml`, valor real: 0.1964)
- **En la presentación:** Verificar que coincida con YAML → **0.20**
- **Validez:** ✅ Correcto. 0.20 es aceptable para DLBP (rango típico 0.05-0.30)

### Parámetros del Híbrido
Todos calibrados en YAML:
```yaml
Hybrid:
  aplicar_ts_cada: 24        # Cada 24 generaciones de GA, aplicar fase TS
  iter_ts_por_individuo: 28  # 28 iteraciones de TS por individuo seleccionado
  poblacion_size: 45          # Población más pequeña que GA solo
  prob_cruce: 0.94            # Probabilidad de cruce alta
  top_n_para_ts: 4            # Aplicar TS a los 4 mejores individuos
```

---

## Entregables de Fase 3

| Archivo | Acción |
|---------|--------|
| `docs/presentacion/sustentacion_dlbp.html` | Modificaciones masivas según 3.1 |
| `docs/presentacion/figuras/` | Nuevas figuras si se generan |

## Dependencias
- **Requiere Fase 1 completada** para tener datos reales
- Puede comenzar en paralelo el diseño de slides (estructura HTML/CSS) sin datos
