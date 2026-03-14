# Fase 3: Generación de Datos y Escenarios de Prueba

> **Estado:** ✅ Completada  
> **Semanas:** 19–22  
> **Carpeta de código:** `src/instances/`  
> **Objetivo:** Crear un generador de instancias sintéticas calibradas contra la industria avícola colombiana.

---

## Contexto

Las metaheurísticas se evalúan sobre **instancias del problema** — conjuntos de parámetros que representan escenarios operativos de la industria avícola. Los datos deben ser **sintéticos pero calibrados** usando:

- **Proporciones anatómicas:** literatura avícola (≈30% pechuga, 20% muslos, 10% alas, 40% otros)
- **Costos y precios:** reportes FENAVI 2024, Solano-Blanco 2022
- **Demanda:** distribuciones probabilísticas con estacionalidad
- **Escala:** desde instancias toy ($n_p=3, n_t=4, n_\omega=5$) hasta industriales ($n_p=10, n_t=52, n_\omega=500$)

---

## 🏃 Sprint 3.1: Diseño del Generador de Instancias (Semanas 19-20)

**Objetivo:** Implementar una clase `InstanceGenerator` parametrizable que genere instancias válidas del problema.

### Descripción
El generador debe recibir un perfil de configuración (tamaño, nivel de variabilidad, estacionalidad) y producir una `ProblemInstance` completa y coherente. Las distribuciones de demanda deben reflejar patrones reales: estacionalidad (mayor demanda en diciembre), variabilidad por producto (pechuga más estable que alas), y correlaciones entre coproductos.

### 📋 Checklist

- [x] **`src/instances/generator.py`** — Clase `InstanceGenerator`:
  - [x] Método `generate(config: dict) -> ProblemInstance`
  - [x] Parámetro `n_products`: número de coproductos
  - [x] Parámetro `n_periods`: horizonte de planificación
  - [x] Parámetro `n_scenarios`: escenarios estocásticos
  - [x] Parámetro `demand_profile`: 'stable', 'seasonal', 'volatile'
  - [x] Parámetro `size_profile`: 'toy', 'small', 'medium', 'large', 'industrial'
  - [x] Perfiles predefinidos con valores por defecto calibrados
- [x] **`src/instances/distributions.py`** — Distribuciones de demanda:
  - [x] Función `generate_demand_normal(mean, std, n_scenarios) -> array`
  - [x] Función `generate_demand_lognormal(mu, sigma, n_scenarios) -> array`
  - [x] Función `add_seasonality(demand, amplitude, period) -> array`
  - [x] Función `add_correlation(demands, corr_matrix) -> array`
  - [x] Función `generate_scenarios(n_products, n_periods, n_scenarios, profile) -> array 3D`
- [x] **Perfiles de tamaño predefinidos:**

  | Perfil | $n_p$ | $n_t$ | $n_\omega$ | Uso |
  |--------|:-----:|:-----:|:----------:|-----|
  | Toy | 3 | 4 | 5 | Debug, tests |
  | Small | 6 | 12 | 20 | Validación con solver |
  | Medium | 6 | 12 | 50 | Calibración hiperparámetros |
  | Large | 8 | 24 | 100 | Comparación metaheurísticas |
  | Industrial | 10 | 52 | 500 | Scalability test |

- [x] **Tests:** `tests/test_generator.py` — **79 tests, todos pasaron**
  - [x] Test genera instancia válida (pasa `instance.validate()`) — 5 perfiles
  - [x] Test $\sum \alpha_p = 1$ en toda instancia — 5 perfiles
  - [x] Test demanda no negativa — 5 perfiles
  - [x] Test reproducibilidad con seed

---

## 🏃 Sprint 3.2: Calibración de Parámetros (Semanas 20-21)

**Objetivo:** Calibrar los parámetros de las instancias contra datos reportados en la literatura.

### Descripción
Los valores numéricos (precios, costos, proporciones) deben ser realistas para la industria avícola colombiana. Se usan como referencia los parámetros de Solano-Blanco 2022 (Santa Marta) y Tahraoui 2025 (multi-producto).

### 📋 Checklist

- [x] **`src/instances/calibration.py`** — Datos de calibración:
  - [x] Dict `ANATOMICAL_PROPORTIONS`: proporciones avícolas estándar
    - [x] Pechuga: 0.30, Muslo: 0.18, Contramuslo: 0.14, Ala: 0.08, Menudencias: 0.05, Otros: 0.25
  - [x] Dict `PRICE_RANGES_COP`: rangos de precios en COP/kg
    - [x] Pechuga: 12,000-15,000, Muslo: 8,000-10,000, Ala: 5,000-7,500, etc.
  - [x] Dict `COST_REFERENCE`: costos operativos de referencia
    - [x] Costo procesamiento: 1,500-2,500 COP/carcasa
    - [x] Costo setup: 500,000-1,500,000 COP/periodo
    - [x] Costo inventario: 100-500 COP/kg/periodo (refrigeración)
  - [x] Dict `CAPACITY_REFERENCE`: capacidades típicas
    - [x] $Q^{max}$: 5,000-20,000 carcasas/periodo
    - [x] $Q^{min}$: 500-2,000 carcasas/periodo (lote mínimo viable)
  - [x] Dict `SHELF_LIFE`: vidas útiles por producto (periodos)
    - [x] Fresco refrigerado: 4-7 días, congelado: 30+ días
  - [x] Función `calibrate_instance(instance, source='solano_blanco') -> ProblemInstance`
  - [x] Función `validate_calibration_data()` — verificación de coherencia interna
  - [x] Función `get_default_correlation(n)` — matriz de correlación Cholesky
- [x] **Documentar fuentes** en `docs/calibration_sources.md`:
  - [x] Tabla con cada parámetro, valor, fuente, y página de referencia
  - [x] 6 secciones: proporciones, precios, costos, capacidades, vida útil, peso
  - [x] 6 referencias bibliográficas (FENAVI, Solano-Blanco, NTC, Codex, Cobb)
- [x] **Tests:** `tests/test_calibration.py` — **44 tests, todos pasaron**
  - [x] Test parámetros calibrados son coherentes (costos < precios)
  - [x] Test $Q^{min} < Q^{max}$
  - [x] Test calibrate_instance() en 5 perfiles, preserva demanda/estructura
  - [x] Test correlación definida positiva, simétrica, diagonal=1

---

## 🏃 Sprint 3.3: Generación del Banco de Instancias (Semanas 21-22)

**Objetivo:** Generar y almacenar el banco completo de instancias para la Fase 4.

### Descripción
Se generan instancias para cada perfil de tamaño, con 3 semillas distintas por perfil para análisis estadístico. Cada instancia se almacena como YAML en `data/instances/`.

### 📋 Checklist

- [x] **Script `experiments/scripts/generate_instances.py`:**
  - [x] Generar **3 instancias × 5 perfiles** = 15 instancias ✅
  - [x] Nomenclatura: `{perfil}_seed{N}.yaml` (ej: `medium_seed42.yaml`)
  - [x] Resolver instancias toy+small con CBC y guardar solución óptima (6 OPTIMAL)
  - [x] Log de generación con estadísticas descriptivas + `instance_catalog.json`
- [x] **Documentar banco de instancias:**
  - [x] `instance_catalog.json` con: nombre, F, T, W, demanda media, CV
  - [x] Solución óptima (CBC): toy 269-283M, small 571-578M
  - [x] Tiempo de solver: toy 0.1-0.3s, small 1.0-2.8s
- [x] **Validación del banco:**
  - [x] 15/15 instancias pasan `validate()` (209 tests, 0 fallos)
  - [x] 6 instancias con solución óptima conocida (3 toy + 3 small)
  - [x] 5 gráficas estadísticas: KDE/ECDF por perfil, temporal con bandas P5-P95, catálogo con pruebas no paramétricas, soluciones óptimas (CI+trade-off), y heatmaps de correlación Spearman
  - [x] Script `notebooks/01_instance_analysis.py` con análisis estadístico para reporte/presentación
  - [x] Script `experiments/scripts/run_fenavi_validation.py` para validar cobertura de rangos FENAVI en precios y contraste mensual opcional con histórico (Spearman/KS/Wasserstein)
  - [x] Artefactos de validación en `experiments/results/fenavi_validation/`

---

## Criterios de Salida de la Fase 3

✅ La fase se considera **completa** cuando:
1. `InstanceGenerator` produce instancias válidas para los 5 perfiles
2. Parámetros calibrados contra fuentes documentadas
3. 15 instancias almacenadas en `data/instances/`
4. Instancias small resueltas con CBC (baseline)
5. Notebook de análisis de instancias generado
6. Tests pasan: `pytest tests/test_generator.py tests/test_calibration.py`
