# Fase 4: Diseño Experimental y Análisis de Resultados

> **Estado:** ✅ Completada  
> **Semanas:** 23-27  
> **Carpeta de código:** `experiments/`  
> **Objetivo:** Ejecutar comparación rigurosa de GA vs SA vs DE vs GA-SA, y validar hipótesis H1/H2/H3 con significancia estadística.

---

## Contexto

La Fase 4 responde tres preguntas de investigación:

1. ¿Las metaheurísticas reducen costos >= 5% vs baseline? -> **H1**
2. ¿GA-SA domina a las individuales con gap <= 2%? -> **H2**
3. ¿Se reduce inventario de baja rotación >= 15%? -> **H3**

Las corridas se almacenan en CSV y se analizan con scripts reproducibles.

---

## Sprint 4.1: Diseño Experimental (Semana 23)

**Objetivo:** Definir diseño experimental, métricas y baseline.

### Checklist

- [x] Definir factores y niveles:
  - [x] Factor A: Algoritmo -> {GA, SA, DE, GA-SA, CBC-exact, Baseline}
  - [x] Factor B: Tamaño -> {Small, Medium, Large}
  - [x] Instancias: 9 (3 por tamaño)
  - [x] Réplicas metaheurísticas: 30 seeds por combinación
  - [x] Réplicas deterministas: 1 seed por instancia para `baseline` y `cbc_exact`
  - [x] Total bruto: 6 x 9 x 30 = 1620 corridas
  - [x] Total efectivo con deterministas: 1098 corridas
- [x] Definir métricas de respuesta:
  - [x] `z_value`
  - [x] `gap_percent`
  - [x] `service_level`
  - [x] `avg_inventory`
  - [x] `low_rotation_inventory`
  - [x] `elapsed_seconds`
  - [x] `n_evaluations`
- [x] Implementar baseline en `experiments/scripts/baseline.py`
- [x] Configuración:
  - [x] `experiments/config/comparison.yaml`
  - [x] `experiments/config/sensitivity.yaml`

---

## Sprint 4.2: Ejecución de Experimentos (Semanas 24-25)

**Objetivo:** Ejecutar combinaciones experimentales y almacenar resultados de forma robusta.

### Checklist

- [x] `experiments/scripts/run_comparison.py`:
  - [x] Respeta `n_replicas` y seeds efectivos
  - [x] Soporta algoritmos deterministas con una semilla
  - [x] Guarda resultados incrementales en `comparison.csv`
  - [x] Guarda trazas de convergencia/diversidad en `comparison_traces.csv`
  - [x] Checkpoint periódico y reanudación robusta
  - [x] `--dry-run` no borra resultados existentes
  - [x] Contadores y resumen final corregidos
  - [x] Estimación de tiempo por algoritmo (no constante)
- [x] `experiments/scripts/run_sensitivity.py`:
  - [x] Gap calculado contra control `delta=0` por seed y parámetro
  - [x] Soporte consistente de `n_replicas`
  - [x] Guardado incremental en `experiments/results/sensitivity.csv`
  - [x] Export de resumen en `experiments/results/sensitivity.json`

---

## Sprint 4.3: Análisis Estadístico (Semanas 25-26)

**Objetivo:** Validar/rechazar H1/H2/H3 con pruebas estadísticas.

### Checklist

- [x] `experiments/scripts/run_statistical_tests.py`:
  - [x] H1, H2, H3 implementadas
  - [x] H2 validada con prueba one-sided contra umbral de gap (`<= 2%`)
  - [x] H3 robusta cuando baseline de inventario es cero (usa solo casos con `baseline > 0`)
  - [x] ANOVA + Tukey HSD
  - [x] Fallback con Bonferroni
  - [x] Robustez ante datasets parciales (evita crash de Tukey por n<=1)
- [x] `experiments/scripts/generate_results_tables.py`:
  - [x] Tabla principal
  - [x] Tabla por instancia
  - [x] Boxplot fitness
  - [x] Pareto calidad-tiempo
  - [x] Comparación nivel de servicio

---

## Sprint 4.4: Interpretación y Documentación (Semana 27)

**Objetivo:** Consolidar resultados para reporte y sustentación.

### Checklist

- [x] Reporte base de fase: `documentacion/reportes/reporte_fase4.md`
- [x] Tablas y figuras exportadas desde scripts reproducibles

---

## Sprint 4.5: Análisis de Complejidad Computacional (Semana 27)

**Objetivo:** Caracterizar formalmente la complejidad empírica y la escalabilidad de las metaheurísticas.

### Implementación técnica

- [x] Script principal: `experiments/scripts/run_complexity_analysis.py`
- [x] Notebook de análisis: `notebooks/04_complexity_analysis.ipynb`
- [x] Instrumentación de convergencia/diversidad en metaheurísticas:
  - [x] `src/metaheuristics/base.py`
  - [x] `src/metaheuristics/ga.py`
  - [x] `src/metaheuristics/de.py`
  - [x] `src/metaheuristics/ga_sa.py`

### Entregables automáticos de 4.5

- [x] Escalabilidad empírica:
  - [x] `complexity_scaling_by_size.csv`
  - [x] `complexity_exponent_fit.csv`
  - [x] `complexity_loglog_scaling.png`
- [x] Performance profiles (Dolan-More):
  - [x] `performance_profile.csv`
  - [x] `performance_profile.png`
- [x] Convergence profiles:
  - [x] `convergence_profiles.csv`
  - [x] `convergence_profiles.png`
- [x] Diversidad poblacional:
  - [x] `diversity_profiles.csv`
  - [x] `diversity_profiles.png`
  - [x] `diversity_premature_summary.csv`
- [x] Complejidad por componente:
  - [x] `cprofile_component_breakdown.csv` (con `--run-cprofile`)
  - [x] `cprofile_component_breakdown.png` (con `--run-cprofile`)
  - [x] perfiles `.txt` por algoritmo en `experiments/results/complexity/cprofile/`
- [x] Reporte consolidado:
  - [x] `experiments/results/complexity/complexity_report.md`

### Estado de ejecución experimental de 4.5

- [x] Ejecutar corrida completa de comparación con trazas (`run_comparison.py`)
- [x] Ejecutar análisis de complejidad (`run_complexity_analysis.py`)
- [x] Validar resultados para incluir en documento final/presentación

---

## Criterios de salida de la Fase 4

La fase se considera completa cuando:

1. Se ejecuta la comparación completa y queda almacenada en CSV.
2. Se ejecutan y documentan H1, H2 y H3.
3. Se generan tablas y gráficos de fase 4.4.
4. Se generan performance/convergence/diversity profiles de 4.5.
5. Se estima complejidad empírica con ajuste log-log.
6. Se documenta el reporte final de fase para tesis/presentación.
