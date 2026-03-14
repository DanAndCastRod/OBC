# Fase 1: Formulación del Modelo Matemático MILP

> **Estado:** ✅ Completada  
> **Semanas:** 1–8  
> **Carpeta de código:** `src/model/`  
> **Objetivo:** Implementar el modelo MILP estocástico del Anexo A como código Python ejecutable y validarlo con el solver CBC.

---

## Contexto

El modelo es un problema de **Programación Lineal Entera Mixta (MILP) multi-periodo** con estructura de *lot-sizing estocástico*. Incluye:
- Variables de primera etapa: $y_t$ (setup binario), $q_t$ (carcasas enteras)
- Variables de segunda etapa: $v_{pt\omega}$ (ventas), $I_{pt\omega}$ (inventario), $u_{pt\omega}$ (demanda insatisfecha)
- 8 ecuaciones (1 objetivo + 7 restricciones)
- Complejidad: **NP-hard** (Florian 1980, Bitran & Yanasse 1982)

El modelo debe funcionar como **evaluador de soluciones** para las metaheurísticas de la Fase 2 y como **baseline exacto** para la comparación de la Fase 4.

---

## 🏃 Sprint 1.1: Revisión Literaria e Ingeniería de Requisitos (Semanas 1-2)

**Objetivo:** Comprender a profundidad el modelo matemático y definir los requisitos funcionales del código.

### Descripción
Antes de codificar, se deben estudiar en detalle los papers clave que fundamentan el modelo: Solano-Blanco 2022 (lot-sizing avícola), Akbari-Aghghaleh 2025 (metaheurísticas avícolas), Rahmani 2025 (stochastic CLSP), y Claassen 2016 (perecibilidad FPI). Se documentan las decisiones de diseño de software.

### 📋 Checklist

- [x] Leer y anotar los 5 papers clave del modelo:
  - [x] Solano-Blanco 2022: estructura del MILP avícola (via anteproyecto + estudio del arte)
  - [x] Akbari-Aghghaleh 2025: codificación de variables mixtas
  - [x] Rahmani 2025: two-stage stochastic CLSP
  - [x] Claassen 2016: restricción de perecibilidad
  - [x] Goren 2016: setup carryover y NP-hardness
- [x] Documentar las **decisiones de diseño** en `docs/design_decisions.md`:
  - [x] DD-01: Perecibilidad → Descarte total (Eq. 7)
  - [x] DD-02: Granularidad → Semanas
  - [x] DD-03: Coproductos → 6 base
  - [x] DD-04: Escenarios → Monte Carlo + LogNormal
  - [x] DD-05: Formato → YAML (in) / JSON (out)
  - [x] DD-06: Solver → CBC (PuLP) + Gurobi backup
  - [x] DD-07: Codificación → 2 vectores (y, q) + decoder greedy
- [x] Definir la **interfaz de datos** (formato de entrada/salida):
  - [x] `data/instances/toy_seed42.yaml` — instancia de ejemplo completa
  - [x] Formato de salida definido en design_decisions.md (DD-05)
- [x] Crear `requirements.txt` actualizado con dependencias exactas

---

## 🏃 Sprint 1.2: Implementación de Parámetros y Estructuras de Datos (Semanas 3-4)

**Objetivo:** Codificar las estructuras de datos que representan una instancia del problema y una solución.

### Descripción
Se crean las clases `ProblemInstance` (parámetros del modelo) y `Solution` (variables de decisión + valor objetivo). Estas estructuras son la base para todo el proyecto — las metaheurísticas, el solver, y el evaluador las usarán directamente.

### 📋 Checklist

- [x] **`src/model/parameters.py`** — Clase `ProblemInstance` (3 capas DD-03):
  - [x] Capa 1: `n_parts`, `part_names`, `alpha` (proporciones anatomicas)
  - [x] Capa 2: `n_cut_forms`, `cut_form_names`, `composition` (matriz), `exclusivity_groups`
  - [x] `cut_config`: configuracion de corte (None = variable, array = fija)
  - [x] Periodos: `n_periods` (dias, DD-02)
  - [x] Economicos: `weight`, `prices`, `cost_prod`, `cost_setup`, `cost_inv`, `cost_pen`
  - [x] Capacidad: `capacity_max`, `capacity_min`
  - [x] Perecibilidad: `shelf_life` (dias)
  - [x] Escenarios: `n_scenarios`, `scenario_probs`, `demand` (3D: formas x periodos x escenarios)
  - [x] Método `validate()`: 15+ verificaciones de consistencia
  - [x] Método `from_yaml(path)`: carga con validacion automatica
  - [x] Método `to_yaml(path)`: exportacion completa
  - [x] Método `summary()`: resumen legible
- [x] **`src/model/solution.py`** — Clase `Solution`:
  - [x] Primera etapa: `y` (setup bool), `q` (cantidad int)
  - [x] Segunda etapa: `v` (ventas), `I` (inventario), `u` (insatisfaccion) — 3D por escenario
  - [x] `objective_value`, `breakdown` (SolutionBreakdown con 5 componentes)
  - [x] Método `check_feasibility(instance)`: 4 tipos de violaciones
  - [x] Propiedades: `n_periods`, `total_production`, `n_setups`
- [x] **Tests:** `tests/test_parameters.py` — **16 tests, todos pasaron**
  - [x] Test carga/exportación YAML round-trip
  - [x] Test validación $\sum \alpha = 1$
  - [x] Test validación $\sum \pi_\omega = 1$
  - [x] Test validación de dimensiones de demanda
  - [x] Test validación de capacidad
  - [x] Test validación de grupos de exclusividad
  - [x] Test carga instancia toy real
  - [x] Test factibilidad (setup-cantidad, lote minimo, capacidad maxima)
  - [x] Test propiedades de Solution
  - [x] Test SolutionBreakdown

---

## 🏃 Sprint 1.3: Implementación de Restricciones y Función Objetivo (Semanas 5-6)

**Objetivo:** Codificar el evaluador de la función objetivo y el verificador de restricciones.

### Descripción
Se implementa la lógica de negocio del modelo: la función objetivo (Eq. 1) y las 7 restricciones (Eqs. 2-8). Estos se usan tanto para validar soluciones como para calcular el fitness en las metaheurísticas.

### 📋 Checklist

- [x] **`src/model/objective.py`** — Evaluador del modelo:
  - [x] Función `evaluate(solution, instance)` + `evaluate_vectorized()` (np.einsum)
  - [x] Desglose: `SolutionBreakdown(revenue, prod_cost, setup_cost, inv_cost, pen_cost)`
- [x] **`src/model/constraints.py`** — Verificador de restricciones:
  - [x] `check_material_balance` (Eq. 2), `check_demand_satisfaction` (Eq. 3)
  - [x] `check_capacity_max` (Eq. 4), `check_capacity_min` (Eq. 5)
  - [x] `check_sales_limit` (Eq. 6), `check_perishability` (Eq. 7)
  - [x] `check_domains` (Eq. 8), `check_all()`, `all_satisfied()`
  - [x] `_get_effective_alpha()`: alpha por forma de corte via composición
- [x] **`src/model/decoder.py`** — Decodificador greedy:
  - [x] `decode(y, q, instance) -> Solution` con inventario FIFO
  - [x] Perecibilidad: capas envejecen y se descartan si edad > L_f
  - [x] Asignación por rentabilidad descendente (precio)
- [x] **Tests:** `tests/test_constraints.py` — **15 tests, todos pasaron**
  - [x] Decoder: all-off, full production, factibilidad, parcial
  - [x] Constraints: capacidad max/min, dominios, demanda
  - [x] Objective: Z negativo/positivo, loop vs vectorized, monotonicity
  - [x] Perecibilidad: shelf_life corto/largo
- [x] **Documentación:** `docs/pseudocode_model.md`
  - [x] Pseudocódigo del decoder greedy
  - [x] Pseudocódigo de la función objetivo
  - [x] Diagrama de flujo de restricciones
  - [x] Pipeline completo (metaheurística → decoder → evaluador)

---

## 🏃 Sprint 1.4: Solver Exacto CBC y Validación (Semanas 7-8)

**Objetivo:** Implementar el solver exacto como baseline y validar el modelo completo.

### Descripción
Se integra PuLP para resolver instancias pequeñas ($n_t \leq 12$, $n_\omega \leq 50$) de forma exacta. La solución exacta sirve como (a) prueba de que el modelo es correcto, y (b) baseline para calcular el gap de optimalidad de las metaheurísticas en la Fase 4.

### 📋 Checklist

- [x] **`src/model/solver.py`** — Wrapper PuLP/CBC:
  - [x] Función `solve_exact(instance, time_limit, solver)` → `SolverResult`
  - [x] Modelo PuLP completo: Eqs. 1-8 con perecibilidad linealizada (big-M)
  - [x] `SolverResult` con status (OPTIMAL/FEASIBLE/INFEASIBLE/TIMEOUT), gap, metricas
  - [x] Soporte para CBC (default), HiGHS, Gurobi
- [x] **Validación cruzada:** (via tests)
  - [x] Solver encuentra óptimo en instancia trivial
  - [x] `constraints.check_all()` pasa para solucion del solver
  - [x] `objective.evaluate()` coincide con Z del solver (tol < 1.0)
  - [x] Solver Z >= Greedy Z (optimalidad)
- [x] **Instancia de referencia:**
  - [x] `data/instances/toy_seed42.yaml` carga y resuelve correctamente
- [x] **Tests de integración:** `tests/test_solver.py` — **7 tests, todos pasaron**
  - [x] Test óptimo, factibilidad, solver vs evaluate, solver vs greedy
  - [x] Test timeout, métricas, carga YAML
- [x] **Documentación:** `docs/pseudocode_model.md` actualizado
  - [x] Pseudocódigo del solver MILP
  - [x] Linealización de perecibilidad (big-M)

---

## Criterios de Salida de la Fase 1

✅ La fase se considera **completa** cuando:
1. `ProblemInstance` carga/exporta YAML correctamente
2. `constraints.check_all()` valida todas las 7 restricciones
3. `decoder.decode()` produce soluciones factibles desde decisiones de primera etapa
4. `solver.solve_exact()` resuelve la instancia toy con solución óptima conocida
5. Todos los tests pasan (`pytest tests/test_model.py tests/test_constraints.py tests/test_solver.py`)
6. Instancia de referencia resuelta y documentada
