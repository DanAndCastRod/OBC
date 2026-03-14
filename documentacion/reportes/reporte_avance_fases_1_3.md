# Informe Parcial de Avance de Investigación

**Título:** Modelo de Optimización para la Planificación de la Producción de Coproductos Avícolas Perecibles bajo Demanda Estocástica: Un Enfoque con Metaheurísticas Híbridas  
**Autor:** Daniel Andrés Castañeda Rodríguez  
**Directora:** Ing. Eliana Mirledy Ocampo Toro, PhD.  
**Programa:** Maestría en Investigación Operativa y Estadística — Universidad Tecnológica de Pereira  
**Fecha:** 3 de marzo de 2026  
**Periodo reportado:** Fases 1–3 (Semanas 1–22)

---

## 1. Introducción

El presente informe documenta el avance del proyecto de investigación correspondiente a las primeras tres fases de un cronograma de cinco. El trabajo consiste en la formulación, implementación computacional y evaluación de un modelo de programación lineal entera mixta (MILP) estocástico para la planificación de la producción de coproductos avícolas perecibles, complementado por cuatro algoritmos metaheurísticos (GA, SA, DE y un híbrido GA-SA) calibrados para resolver instancias de escala industrial.

A la fecha de corte, las tres primeras fases han sido completadas en su totalidad y se encuentran validadas con una suite automatizada de 234 tests unitarios y de integración. Las dos fases restantes —experimentación comparativa (Fase 4, en ejecución) y escritura de la tesis con validación final (Fase 5, pendiente)— se describen al final del documento como trabajo pendiente.

### 1.1 Cronograma General

| Fase | Alcance | Semanas | Estado |
|:----:|---------|:-------:|:------:|
| **1** | Formulación del modelo MILP estocástico | 1–8 | **Completada** |
| **2** | Diseño e implementación de metaheurísticas | 9–18 | **Completada** |
| **3** | Generación de datos y escenarios de prueba | 19–22 | **Completada** |
| **4** | Diseño experimental, ejecución y análisis estadístico | 23–27 | En ejecución |
| **5** | Validación, escritura de tesis y sustentación | 28–30 | Pendiente |

---

## 2. Fase 1: Formulación del Modelo Matemático MILP

### 2.1 Objetivo

Implementar el modelo MILP estocástico de dos etapas como código Python ejecutable y validarlo con el solver CBC, de forma que sirva como (a) evaluador de fitness para las metaheurísticas y (b) baseline exacto para el cálculo de gaps de optimalidad.

### 2.2 Modelo Matemático

El problema se formula como un *lot-sizing estocástico multi-periodo* con coproductos perecibles. Las variables de decisión se dividen en dos etapas:

- **Primera etapa (determinista):** $y_t \in \{0,1\}$ (decisión de setup) y $q_t \in [Q^{min}, Q^{max}]$ (carcasas procesadas por periodo).
- **Segunda etapa (por escenario $\omega$):** $v_{ft\omega}$ (ventas), $I_{ft\omega}$ (inventario) y $u_{ft\omega}$ (demanda insatisfecha) para cada forma de corte $f$, periodo $t$ y escenario $\omega$.

La función objetivo maximiza el beneficio esperado total (Eq. 1) sujeto a 7 restricciones: balance de material (Eq. 2), satisfacción de demanda (Eq. 3), capacidad máxima y mínima (Eqs. 4-5), límite de ventas (Eq. 6), perecibilidad con descarte total (Eq. 7) y dominios (Eq. 8).

La complejidad del problema es **NP-hard** (Florian 1980, Bitran & Yanasse 1982), lo cual justifica el uso de metaheurísticas para instancias de escala industrial.

### 2.3 Implementación

La Fase 1 se desarrolló en 4 sprints que produjeron los siguientes módulos:

| Módulo | Archivo | Responsabilidad |
|--------|---------|-----------------|
| Parámetros | `src/model/parameters.py` | Clase `ProblemInstance` con carga/exportación YAML y 15+ validaciones internas |
| Solución | `src/model/solution.py` | Clase `Solution` con desglose de Z en 5 componentes (ingresos, costos de producción, setup, inventario y penalización) |
| Función objetivo | `src/model/objective.py` | Evaluador vectorizado con `numpy.einsum` |
| Restricciones | `src/model/constraints.py` | Verificador de las 7 restricciones, incluyendo perecibilidad |
| Decodificador | `src/model/decoder.py` | Decodificador greedy FIFO con asignación por rentabilidad descendente |
| Solver exacto | `src/model/solver.py` | Integración con PuLP/CBC, con soporte para HiGHS y Gurobi |

### 2.4 Validación

Se realizó validación cruzada entre el solver exacto y los módulos de evaluación:

- El solver CBC encontró el óptimo en la instancia de referencia *toy_seed42* ($Z^* \approx 275$ millones COP).
- La función `constraints.check_all()` verifica las 7 restricciones sobre la solución del solver sin violaciones.
- El valor $Z$ calculado por `objective.evaluate()` coincide con el reportado por el solver (tolerancia < 1.0 COP).
- Se verificó que $Z_{solver} \geq Z_{greedy}$ para todas las instancias de prueba, confirmando la optimalidad.

**Tests Fase 1:** 38 tests automatizados (16 + 15 + 7), todos aprobados.

### 2.5 Decisiones de Diseño Documentadas

Se documentaron 7 decisiones de diseño en `docs/design_decisions.md`, entre las cuales destacan:

| ID | Decisión | Justificación |
|:--:|----------|---------------|
| DD-01 | Perecibilidad → descarte total (Eq. 7) | Simplificación conservadora; producto vencido no se vende |
| DD-04 | Escenarios → Monte Carlo + LogNormal | Distribución apropiada para demanda no negativa con sesgo |
| DD-07 | Codificación → 2 vectores $(y, q)$ + decoder greedy | Reduce espacio de búsqueda; segunda etapa se calcula determinísticamente |

---

## 3. Fase 2: Diseño e Implementación de Metaheurísticas

### 3.1 Objetivo

Implementar cuatro algoritmos metaheurísticos con interfaz unificada, codificación compartida y calibración automatizada de hiperparámetros.

### 3.2 Arquitectura de Software

Se diseñó una jerarquía de clases con polimorfismo para garantizar la intercambiabilidad de los algoritmos:

```
BaseMetaheuristic (ABC)
├── solve(instance) → Solution          [abstracto]
├── evaluate_fitness(y, q, instance)     [repair → decode → evaluate]
├── generate_random(instance)            [solución aleatoria factible]
└── convergence_data()                   [historial de fitness]

GeneticAlgorithm       : BaseMetaheuristic
SimulatedAnnealing     : BaseMetaheuristic
DifferentialEvolution  : BaseMetaheuristic
HybridGASA             : BaseMetaheuristic
```

La codificación compartida (`encoding.py`) provee operadores genéticos (crossover uniforme, crossover de dos puntos), operadores de vecindario (toggle, perturbación de cantidad), y una función de reparación (`repair_lot_sizing`) que garantiza factibilidad de dominio.

### 3.3 Algoritmos Implementados

#### a) Algoritmo Genético (GA)

Evolución poblacional con selección por torneo, cruce de dos puntos y mutación combinada (toggle + perturbación gaussiana). Incorpora elitismo (top-$k$ preservados) y criterio de parada por estancamiento.

#### b) Recocido Simulado (SA)

Búsqueda de vecindario con criterio de Metropolis ($P_{aceptar} = e^{-\Delta/T}$), enfriamiento geométrico ($T \leftarrow T \cdot \alpha$), y mecanismo de recalentamiento ante estancamiento. Incluye auto-estimación de $T_0$ para ~80% de aceptación inicial.

#### c) Evolución Diferencial (DE)

Operadores de mutación diferencial (estrategias `rand/1/bin` y `best/1/bin`) adaptados a variables mixtas mediante discretización (umbral 0.5 para binarias, redondeo para enteras). Selección greedy: el individuo trial reemplaza al target solo si su fitness es superior.

#### d) Híbrido GA-SA

Combina la exploración global del GA con la explotación local del SA: cada $N$ generaciones, se aplica SA como búsqueda local a los top-$k$ individuos de la población. Esta configuración se basa en los hallazgos de Akbari-Aghghaleh (2025), quienes identificaron la combinación GA+SA como la más efectiva para problemas de optimización avícola.

### 3.4 Calibración de Hiperparámetros (Optuna/TPE)

Se utilizó **Optuna** con el sampler TPE (*Tree-Parzen Estimator*) para calibrar cada algoritmo, ejecutando **30 trials por algoritmo** sobre un conjunto de 5 instancias (3 small + 2 medium), con timeout de 900 s por trial y semilla fija (42) para reproducibilidad. Los resultados se almacenan en `experiments/config/tuning_*.yaml`.

#### Tabla 1. GA — Hiperparámetros calibrados

| Parámetro | Valor | Descripción |
|-----------|:-----:|-------------|
| `pop_size` | 80 | Tamaño de población |
| `crossover_rate` | 0.7437 | Tasa de cruce |
| `mutation_rate` | 0.0889 | Tasa de mutación |
| `elitism_count` | 3 | Individuos preservados por elitismo |
| `selection_size` | 3 | Tamaño del torneo |

*Mejor fitness:* 396,845,202 COP | *Trials:* 30 (0 errores, 0 timeouts) | *Tiempo:* 23.6 min

#### Tabla 2. SA — Hiperparámetros calibrados

| Parámetro | Valor | Descripción |
|-----------|:-----:|-------------|
| `T_initial` | 203,952 | Temperatura inicial |
| `T_final` | 586.3 | Temperatura final |
| `cooling_rate` | 0.7817 | Tasa de enfriamiento geométrico |
| `max_iterations` | 27 | Iteraciones por nivel de temperatura |
| `p_toggle` | 0.4941 | Probabilidad de perturbación toggle |
| `p_quantity` | 0.2825 | Probabilidad de perturbación de cantidad |
| `delta` | 0.0661 | Magnitud de perturbación |
| `reheat_factor` | 1.2870 | Factor de recalentamiento |
| `reheat_threshold` | 54 | Iteraciones sin mejora para recalentar |

*Mejor fitness:* 396,512,715 COP | *Trials:* 30 (0 errores, 4 timeouts) | *Tiempo:* 2.55 h

#### Tabla 3. DE — Hiperparámetros calibrados

| Parámetro | Valor | Descripción |
|-----------|:-----:|-------------|
| `pop_size` | 51 | Tamaño de población |
| `CR` | 0.5112 | Tasa de cruce binomial |
| `F` | 0.3165 | Factor de escala de mutación |
| `strategy` | best/1/bin | Estrategia de mutación diferencial |

*Mejor fitness:* 397,086,621 COP | *Trials:* 30 (0 errores, 0 timeouts) | *Tiempo:* 1.33 h

#### Tabla 4. GA-SA — Hiperparámetros calibrados

| Parámetro | Valor | Descripción |
|-----------|:-----:|-------------|
| `pop_size` | 39 | Tamaño de población del GA |
| `crossover_rate` | 0.8589 | Tasa de cruce |
| `mutation_rate` | 0.0505 | Tasa de mutación |
| `elitism_count` | 1 | Individuos preservados |
| `selection_size` | 3 | Tamaño del torneo |
| `local_search_freq` | 9 | Frecuencia de SA local (cada N gen.) |
| `local_search_top_k` | 10 | Top-k individuos para SA local |
| `local_search_iters` | 26 | Iteraciones del SA local |
| `local_search_T` | 3,226.6 | Temperatura del SA local |
| `local_search_cooling` | 0.7126 | Enfriamiento del SA local |

*Mejor fitness:* 396,887,162 COP | *Trials:* 30 (0 errores, 0 timeouts) | *Tiempo:* 17.5 h

### 3.5 Benchmark Preliminar

Se ejecutó un benchmark rápido sobre la instancia de referencia para validar la implementación:

| Algoritmo | Gap vs Exacto | Solución factible |
|-----------|:-------------:|:-----------------:|
| CBC (Exacto) | 0.00% | Sí |
| GA | 1.87% | Sí |
| SA | 2.05% | Sí |
| DE | 1.81% | Sí |
| **GA-SA** | **1.49%** | **Sí** |

El resultado confirma que el híbrido GA-SA obtiene el menor gap, consistente con la literatura (Akbari-Aghghaleh, 2025).

**Tests Fase 2:** 43 tests automatizados (15 + 7 + 8 + 8 + 5), todos aprobados.

---

## 4. Fase 3: Generación de Datos y Escenarios de Prueba

### 4.1 Objetivo

Crear un generador de instancias sintéticas calibradas contra parámetros de la industria avícola colombiana, y producir un banco de 15 instancias para la fase experimental.

### 4.2 Generador de Instancias

Se implementó la clase `InstanceGenerator` con soporte para 5 perfiles de tamaño y 3 perfiles de demanda (estable, estacional, volátil). Las distribuciones de demanda se generan con LogNormal, incorporando estacionalidad multiplicativa y correlaciones entre coproductos mediante descomposición de Cholesky.

### 4.3 Calibración contra Datos Reales

Los parámetros económicos y operativos se calibraron utilizando las siguientes fuentes:

| Parámetro | Rango | Fuente |
|-----------|-------|--------|
| Proporciones anatómicas | Pechuga 30%, Muslo 18%, Ala 8%, ... | FENAVI, Guía Cobb 500 |
| Precios de venta (COP/kg) | 5,000 – 15,000 | FENAVI 2024 |
| Costo de procesamiento | 1,500 – 2,500 COP/carcasa | Solano-Blanco (2022) |
| Costo de setup | 500,000 – 1,500,000 COP/periodo | Referencia industrial |
| Costo de inventario | 100 – 500 COP/kg/periodo | Refrigeración industrial |
| Capacidad máxima | 5,000 – 20,000 carcasas/periodo | Plantas medianas Colombia |
| Vida útil (refrigerado) | 4 – 7 días | NTC 3644-2, Codex Alimentarius |

Todas las fuentes están documentadas en `docs/calibration_sources.md` con referencias bibliográficas específicas.

### 4.4 Banco de Instancias

Se generaron 15 instancias (5 perfiles × 3 semillas), almacenadas en `data/instances/`:

| Perfil | $n_f$ | $n_t$ | $n_\omega$ | Demanda media | Solver CBC |
|--------|:-----:|:-----:|:----------:|:-------------:|:----------:|
| Toy | 3 | 4 | 5 | Baja | Óptimo en < 0.3 s |
| Small | 6 | 12 | 20 | Moderada | Óptimo en < 2.8 s |
| Medium | 6 | 12 | 50 | Moderada | No evaluado (fuera de alcance CBC sin límite de tiempo) |
| Large | 8 | 24 | 100 | Alta | No evaluado |
| Industrial | 10 | 52 | 500 | Muy alta | No evaluado |

Las instancias Toy y Small fueron resueltas a optimalidad con CBC, proporcionando valores $Z^*$ de referencia para el cálculo de gaps en la Fase 4. Los valores óptimos son: Toy $Z^* \in [269\text{M}, 283\text{M}]$ COP y Small $Z^* \in [571\text{M}, 578\text{M}]$ COP.

### 4.5 Análisis Estadístico del Banco

Se generaron 5 visualizaciones para caracterizar el banco de instancias:

1. Distribuciones de demanda (KDE/ECDF) por perfil de tamaño
2. Series temporales con bandas de incertidumbre (P5–P95)
3. Catálogo con estadísticos descriptivos y tests no paramétricos
4. Soluciones óptimas con intervalos de confianza y trade-offs
5. Heatmaps de correlación de Spearman entre coproductos

**Tests Fase 3 (generación):** 79 tests automatizados, todos aprobados.

### 4.6 Tests de Calibración (`test_calibration.py` — 44 tests)

Los datos de calibración industrial se validan automáticamente con 44 tests agrupados en 3 categorías:

**A. Integridad de datos de referencia (14 tests):**

| Test | Verifica |
|------|----------|
| `test_anatomical_proportions_sum_one` | sum(α) == 1.0 exacto |
| `test_anatomical_proportions_all_positive` | Todas las proporciones > 0 |
| `test_prices_min_less_than_max` | min < max en todos los rangos de precios |
| `test_prices_default_in_range` | Precio default entre min y max |
| `test_costs_min_less_than_max` | min < max en costos |
| `test_costs_default_in_range` | Costo default entre min y max |
| `test_inv_cost_less_than_all_prices` | cost_inv < precio mínimo (coherencia económica) |
| `test_capacity_q_min_less_than_q_max` | Q^min < Q^max |
| `test_shelf_life_positive` | Vida útil default > 0 |
| `test_shelf_life_min_less_than_max` | min ≤ max en vida útil |
| `test_weight_positive` | Peso default > 0 |
| `test_weight_range` | Peso en rango razonable (1–5 kg) |
| `test_validate_calibration_data_passes` | `validate_calibration_data()` sin errores |

**B. Función `calibrate_instance()` (20 tests, 5 perfiles × 4 propiedades):**

| Test | Verifica |
|------|----------|
| `test_calibrated_instance_valid` | Instancia calibrada pasa `validate()` (5 perfiles) |
| `test_calibrate_preserves_demand` | Calibración no modifica demanda original |
| `test_calibrate_preserves_structure` | No modifica $n_f$, $n_t$, $n_\omega$ |
| `test_calibrate_does_not_mutate_original` | Instancia original no se muta (deep copy) |
| `test_calibrate_applies_overrides` | Overrides personalizados se aplican |
| `test_calibrate_applies_defaults` | Sin overrides usa defaults de `COST_REFERENCE` |
| `test_calibrate_large_uses_large_capacity` | Perfil large usa `CAPACITY_REFERENCE['large']` |
| `test_calibrate_invalid_source` | Fuente inválida lanza `ValueError` |
| `test_all_profiles_calibrate` | Los 5 perfiles se calibran sin errores |
| `test_calibrated_costs_less_than_prices` | cost_inv < prices después de calibrar |

**C. Matriz de correlación (10 tests):**

| Test | Verifica |
|------|----------|
| `test_correlation_shape` | Dimensión n × n correcta |
| `test_correlation_symmetric` | Matriz simétrica |
| `test_correlation_diagonal_one` | Diagonal = 1.0 |
| `test_correlation_positive_definite` | Eigenvalores > 0 (válida para Cholesky) |
| `test_correlation_various_sizes` | Funciona para n = 3, 6, 8, 10 |

**Tests Fase 3 (total):** 123 tests automatizados (`test_generator`: 79 + `test_calibration`: 44), todos aprobados.

---

## 5. Resumen de Evidencias de Calidad

### 5.1 Suite de Tests Automatizados

La totalidad del código implementado está respaldada por tests automatizados ejecutados con Pytest:

| Archivo de test | Fase | Tests | Cobertura |
|-----------------|:----:|:-----:|-----------|
| `test_parameters.py` | 1 | 16 | Carga, exportación, validaciones de `ProblemInstance` |
| `test_constraints.py` | 1 | 15 | 7 restricciones, decoder, objetivo, perecibilidad |
| `test_solver.py` | 1 | 7 | Optimalidad, factibilidad, consistencia con evaluador |
| `test_encoding.py` | 2 | 15 | Operadores genéticos, reparación, factibilidad |
| `test_ga.py` | 2 | 7 | Convergencia, elitismo, parada temprana |
| `test_sa.py` | 2 | 8 | Metropolis, auto-temperatura, recalentamiento |
| `test_de.py` | 2 | 8 | Discretización, estrategias, selección greedy |
| `test_ga_sa.py` | 2 | 5 | Búsqueda local, mejora sobre random |
| `test_generator.py` | 3 | 79 | 5 perfiles, validación, reproducibilidad |
| `test_calibration.py` | 3 | 44 | Coherencia paramétrica, calibración en 5 perfiles |
| `test_baseline.py` | 4 | 25 | Heurísticas, métricas, configuraciones YAML |
| **Total** | | **234** | — |

Última ejecución completa: **234 passed in 14.14 seconds** (3 de marzo de 2026).

### 5.2 Métricas del Código

| Indicador | Valor |
|-----------|:-----:|
| Módulos fuente en `src/` | 15 |
| Líneas de código fuente | ~3,180 |
| Instancias generadas | 15 archivos YAML (22.8 MB) |
| Hiperparámetros calibrados | 4 archivos YAML (GA, SA, DE, GA-SA) |
| Documentos técnicos | 9 archivos Markdown |

### 5.3 Documentación Técnica

| Documento | Contenido |
|-----------|-----------|
| `design_decisions.md` | 7 decisiones de diseño con justificación |
| `pseudocode_model.md` | Pseudocódigo del decoder, evaluador y solver |
| `calibration_sources.md` | Fuentes bibliográficas de calibración económica |
| `benchmark_reporting.md` | Formato de reporte de benchmarks |
| `optuna_tuning_reporting.md` | Protocolo de calibración con Optuna |
| `GUIA_USO_CODIGO.md` | Instrucciones de uso del código |

---

## 6. Trabajo en Progreso y Pendiente

### 6.1 Fase 4: Diseño Experimental y Análisis (Semanas 23–27) — En ejecución

La Fase 4 comprende el diseño experimental, la ejecución de las combinaciones experimentales, el análisis estadístico y la generación de tablas y gráficos para la tesis. Los scripts de ejecución y análisis ya están implementados:

- **Diseño experimental (Sprint 4.1):** Completado. Se definieron factores (6 algoritmos × 3 tamaños × 30 réplicas = 1,620 ejecuciones), 6 métricas de respuesta ($Z$, gap, nivel de servicio, inventario promedio, inventario de baja rotación, tiempo computacional), y una heurística baseline con dos estrategias (proporcional y máxima capacidad).
- **Scripts de ejecución (Sprint 4.2):** Completados. Runner de comparación con checkpoint/reanudación y runner de sensibilidad con perturbaciones de precios (±20%), costos (±20%) y variabilidad de demanda (±50%).
- **Tests estadísticos (Sprint 4.3):** Script completado. Implementa tests para las 3 hipótesis del proyecto: H1 (reducción ≥5% vs baseline), H2 (gap ≤2% de GA-SA vs mejores individuales), H3 (reducción de inventario ≥15%). Incluye verificación de normalidad (Shapiro-Wilk), tests pareados (t-test o Wilcoxon), ANOVA+Tukey HSD, tamaño de efecto (Cohen's d) e intervalos de confianza al 95%.
- **Tablas y gráficos (Sprint 4.4):** Script completado. Genera tabla principal de resultados, boxplots, gráficos de Pareto (calidad vs tiempo), y reporte Markdown para la tesis.
- **Ejecución:** En curso. El script `run_comparison.py` se encuentra ejecutando las 1,620 combinaciones experimentales.

### 6.2 Fase 5: Validación, Tesis y Presentación (Semanas 28–30) — Pendiente

La Fase 5 es la fase de consolidación final y comprende:

- **Validación operativa:** Verificar que las soluciones generadas son realistas y robustas ante perturbaciones.
- **Reproducibilidad:** Crear un script que ejecute la pipeline completa desde cero.
- **Escritura de la tesis:** 7 capítulos según formato UTP/MIOE.
- **Presentación de sustentación:** Reveal.js con gráficos interactivos (Chart.js) y fórmulas (MathJax).
- **Publicación del repositorio:** Limpieza, documentación, y release con tag `v1.0.0-thesis`.

---

## 7. Estructura del Repositorio

```
OBC/
├── src/
│   ├── model/              ← Fase 1: MILP (6 módulos)
│   ├── metaheuristics/     ← Fase 2: GA, SA, DE, GA-SA (6 módulos)
│   └── instances/          ← Fase 3: Generador + calibración (3 módulos)
├── data/instances/         ← 15 instancias YAML
├── experiments/
│   ├── config/             ← Configuraciones (comparison, sensitivity, tuning)
│   ├── scripts/            ← Runners experimentales y análisis
│   └── results/            ← CSV de resultados (en generación)
├── tests/                  ← 11 archivos, 234 tests
├── docs/                   ← Documentación técnica
└── documentacion/          ← Planes de proyecto, reportes
```

---

**Firma del estudiante:**

Daniel Andrés Castañeda Rodríguez  
Marzo de 2026
