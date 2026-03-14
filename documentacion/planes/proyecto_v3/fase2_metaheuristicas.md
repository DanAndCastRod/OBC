# Fase 2: Diseño e Implementación de Metaheurísticas

> **Estado:** ✅ Completada  
> **Semanas:** 9–18  
> **Carpeta de código:** `src/metaheuristics/`  
> **Objetivo:** Implementar GA, SA, DE y GA-SA con interfaz común, codificación de solución compartida, y calibración de hiperparámetros.

---

## Contexto

Las 4 metaheurísticas comparten una **codificación de solución** común (vectores $y_t$, $q_t$) y una **evaluación de fitness** común (función objetivo Z, calculada vía `src/model/`). La diferencia está en cómo cada una explora el espacio de búsqueda.

**Codificación de la solución (cromosoma):**
- Primera parte: vector binario $y = (y_1, ..., y_{n_t})$ → activación de línea (setup)
- Segunda parte: vector entero $q = (q_1, ..., q_{n_t})$ → carcasas por periodo
- Las variables de segunda etapa ($v$, $I$, $u$) se calculan via `decoder.decode()`

**Fitness:** `objective.evaluate(decoder.decode(y, q, instance), instance).total`

---

## 🏃 Sprint 2.1: Clase Base y Codificación Compartida (Semana 9)

**Objetivo:** Crear la infraestructura abstracta que todas las metaheurísticas heredan.

### Descripción
Se define la clase `BaseMetaheuristic` con la interfaz común (`solve()`, `evaluate()`) y la codificación/decodificación compartida. Esto garantiza que las 4 implementaciones sean sustituibles y comparables.

### 📋 Checklist

- [x] **`src/metaheuristics/base.py`** — Clase `BaseMetaheuristic` (ABC):
  - [x] Método abstracto `solve(instance, **kwargs) -> Solution`
  - [x] Método `evaluate_fitness(y, q, instance)`: repair -> decode -> evaluate pipeline
  - [x] Método `generate_random(instance)`: solución aleatoria factible
  - [x] Método `evaluate_and_get_solution()`: retorna (fitness, Solution)
  - [x] Método `update_best()`, `log_iteration()`, `reset()`, `convergence_data()`
  - [x] Atributos: `history`, `best_solution`, `best_fitness`, `config`, `n_evaluations`
- [x] **`src/metaheuristics/encoding.py`** — Codificación compartida:
  - [x] `generate_random_binary()`, `generate_random_integer()`, `random_solution()`
  - [x] `repair_lot_sizing()`: corregir setup-cantidad y clampar a [Q_min, Q_max]
  - [x] `neighborhood_toggle(k)`, `neighborhood_quantity(delta)`
  - [x] `crossover_uniform()`, `crossover_two_point()`: operadores genéticos
  - [x] `mutate()`: toggle + perturbación combinados
- [x] **Tests:** `tests/test_encoding.py` — **15 tests, todos pasaron**
  - [x] Random: shape, zero-when-inactive, factibilidad (20 repeticiones)
  - [x] Repair: clamp, activate
  - [x] Neighborhoods: toggle bits, preserve inactive
  - [x] Crossover: uniform/two-point factibilidad
  - [x] Mutation: feasibility (20 repeticiones)
  - [x] BaseMetaheuristic: evaluate, solve, convergence, reset, summary

---

## 🏃 Sprint 2.2: Algoritmo Genético (GA) (Semanas 10-11)

**Objetivo:** Implementar un GA con operadores SBX/polinomial adaptados a variables mixtas.

### Descripción
El GA opera sobre una población de cromosomas $(y, q)$. Usa selección por torneo, cruce SBX para la parte continua/entera y cruce uniforme para la parte binaria, mutación polinomial para cantidades y flip para setup.

### 📋 Checklist

- [x] **`src/metaheuristics/ga.py`** — Clase `GeneticAlgorithm(BaseMetaheuristic)`:
  - [x] Config: `pop_size=50`, `n_generations=200`, `crossover_rate=0.8`, `mutation_rate=0.1`
  - [x] `selection_size=3` (torneo), `elitism_count=2`, `stagnation_limit=50`
  - [x] `_initialize_population()`: poblacion aleatoria factible
  - [x] `_tournament_select()`: seleccion por torneo de k
  - [x] Crossover: `crossover_two_point()` (uniforme para y, SBX implícito para q)
  - [x] Mutacion: `mutate()` (toggle + perturbacion gaussiana)
  - [x] Elitismo: top-k preservados entre generaciones
  - [x] Parada: generaciones maximas o estancamiento
  - [x] Pseudocodigo en docstring de la clase
- [x] **Tests:** `tests/test_ga.py` — **7 tests, todos pasaron**
  - [x] Convergencia (fitness mejora)
  - [x] Factibilidad de solucion
  - [x] Elitismo (best monotonamente creciente)
  - [x] Stagnation early stop
  - [x] Custom config, multiple seeds, summary

---

## 🏃 Sprint 2.3: Recocido Simulado (SA) (Semanas 12-13)

**Objetivo:** Implementar SA con esquema de enfriamiento adaptativo y perturbaciones sobre $(y_t, q_t)$.

### Descripción
El SA parte de una solución inicial y explora vecindarios mediante perturbaciones. Acepta soluciones peores con probabilidad $e^{-\Delta/T}$ (criterio de Metropolis). Usa enfriamiento geométrico o adaptativo.

### 📋 Checklist

- [x] **`src/metaheuristics/sa.py`** — Clase `SimulatedAnnealing(BaseMetaheuristic)`:
  - [x] Config: `T_initial=auto`, `T_final=1.0`, `cooling_rate=0.95`, `max_iterations=500`
  - [x] `p_toggle=0.3`, `p_quantity=0.4`, `p_both=0.3`, `delta=0.15`
  - [x] `_estimate_initial_temperature()`: auto-T0 al ~80% aceptación
  - [x] `_generate_neighbor()`: toggle / quantity / ambas con probabilidades
  - [x] `_accept()`: criterio de Metropolis: exp(Δ/T)
  - [x] Enfriamiento: `T *= cooling_rate` (geométrico)
  - [x] Reheating: `T *= reheat_factor` cuando estancamiento ≥ threshold
  - [x] Pseudocódigo en docstring de la clase
- [x] **Tests:** `tests/test_sa.py` — **8 tests, todos pasaron**
  - [x] Convergencia, factibilidad
  - [x] T→∞ acepta todo (>90/100)
  - [x] T→0 rechaza peores (<5/100)
  - [x] Siempre acepta mejoras
  - [x] Auto-temperatura, reheating, summary

---

## 🏃 Sprint 2.4: Evolución Diferencial (DE) (Semanas 14-15)

**Objetivo:** Implementar DE con estrategia DE/rand/1/bin adaptada a variables mixtas.

### Descripción
El DE opera en espacio continuo pero se adapta a variables mixtas mediante discretización (redondeo para $q_t$, umbral 0.5 para $y_t$). Usa vectores de diferencia entre individuos como mecanismo de mutación dirigida.

### 📋 Checklist

- [x] **`src/metaheuristics/de.py`** — Clase `DifferentialEvolution(BaseMetaheuristic)`:
  - [x] Config: `pop_size=50`, `max_generations=200`, `F=0.8`, `CR=0.9`
  - [x] Estrategias: `rand/1/bin` (default) y `best/1/bin`
  - [x] `_encode()`: (y, q) → vector continuo [0,1] normalizado
  - [x] `_decode()`: vector continuo → (y, q) discreto (umbral 0.5, rounding)
  - [x] `_mutate_de()`: mutante = base + F*(r2-r3) (rand o best)
  - [x] `_crossover_de()`: cruce binomial con j_rand garantizado
  - [x] Selección greedy: reemplazar si trial ≥ target
  - [x] Parada por estancamiento
  - [x] Pseudocódigo en docstring de la clase
- [x] **Tests:** `tests/test_de.py` — **8 tests, todos pasaron**
  - [x] Convergencia, factibilidad, selección greedy monotónica
  - [x] Discretización válida, encode-decode roundtrip
  - [x] Estrategia best/1/bin, stagnation, summary

---

## 🏃 Sprint 2.5: Híbrido GA-SA y Calibración (Semanas 16-18)

**Objetivo:** Combinar GA + SA en un algoritmo memético y calibrar todos los algoritmos con Optuna.

### Descripción
El GA-SA ejecuta el GA normalmente, pero cada N generaciones aplica SA como búsqueda local a los top-k individuos. Esto combina la exploración global del GA con la explotación local del SA, comprobado como la mejor combinación por Akbari-Aghghaleh 2025.

### 📋 Checklist

- [x] **`src/metaheuristics/ga_sa.py`** — Clase `HybridGASA(BaseMetaheuristic)`:
  - [x] Hereda GA loop + SA búsqueda local periódica
  - [x] Config: `local_search_freq=10`, `local_search_top_k=5`, `local_search_iters=30`
  - [x] `_local_search()`: SA corto con Metropolis + cooling geométrico
  - [x] SA se aplica a top-k individuos cada N generaciones
  - [x] Pseudocódigo en docstring de la clase
- [x] **Tests:** `tests/test_ga_sa.py` — **5 tests, todos pasaron**
  - [x] Convergencia, factibilidad, SA aplicado, no peor que random, summary
- [x] **Benchmark rápido:** `experiments/scripts/run_benchmark.py`
  - [x] 5 algoritmos comparados en instancia de referencia
  - [x] Resultados: Exact 275M, GA 1.87%, SA 2.05%, DE 1.81%, **GA-SA 1.49%**
  - [x] Todas las soluciones factibles ✅
  - [x] GA-SA confirma mejor combinación (Akbari-Aghghaleh 2025)
- [x] **Infraestructura de calibración Optuna lista:**
  - [x] experiments/scripts/run_tuning.py guarda historial por trial (CSV/JSON)
  - [x] experiments/scripts/run_tuning.py genera gráficas de evolución por algoritmo
  - [x] experiments/scripts/plot_tuning_evolution.py genera comparativa multi-algoritmo
  - [x] `run_tuning.py` soporta timeout por trial (`--trial-timeout`) para evitar bloqueos prolongados
- [x] **Calibración Optuna completa:** completada (30 trials por algoritmo, timeout duro activo y trazabilidad CSV/JSON/PNG)

---

## Criterios de Salida de la Fase 2

✅ La fase se considera **completa** cuando:
1. ✅ Las 4 clases (`GA`, `SA`, `DE`, `HybridGASA`) heredan de `BaseMetaheuristic`
2. ✅ Todas producen soluciones **factibles** verificadas por `constraints.check_all()`
3. ✅ Todas mejoran respecto a una solución aleatoria en la instancia toy
4. ✅ Hiperparámetros calibrados con Optuna para instancias medianas (30 trials por algoritmo completados)
5. ✅ Benchmark rápido documentado con gap vs solver exacto
6. [OK] Todos los tests pasan: `pytest tests/test_*.py` - **86 tests, 0 fallos**





