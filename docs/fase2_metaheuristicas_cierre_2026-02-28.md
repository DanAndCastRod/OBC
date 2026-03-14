# Fase 2 Metaheuristicas - Cierre tecnico (2026-02-28)

## Objetivo

Dejar documentadas las correcciones y el estado actual de la Fase 2
(`documentacion/planes/proyecto_v3/fase2_metaheuristicas.md`) para
calibracion, reporte y presentacion.

## Cambios implementados

### 1) Correccion de mutacion en GA y GA-SA

Problema detectado:
- `mutation_rate` no controlaba realmente la perturbacion de `q`.
- Incluso con tasa de mutacion baja, `q` se perturbaba siempre en periodos activos.

Correccion:
- `mutate()` ahora separa:
  - `p_toggle`: probabilidad de mutar `y`
  - `p_quantity`: probabilidad de mutar `q` (si `None`, hereda `p_toggle`)
- Se agregaron validaciones de rango `[0, 1]`.
- Se aplica `repair_lot_sizing()` al final para consistencia.

Archivo:
- `src/metaheuristics/encoding.py`

### 2) Correccion metodologica de benchmark (gap)

Problema detectado:
- El benchmark podia reportar gap contra solver exacto sin verificar estado OPTIMAL.

Correccion:
- Solo se toma baseline de gap cuando `solve_exact()` retorna `OPTIMAL` y factible.
- Si no hay baseline optimo, el gap se reporta como `NaN` con advertencia.
- Se incluye `status` en la tabla de salida.

Archivo:
- `experiments/scripts/run_benchmark.py`

Mejora adicional:
- `run_benchmark.py` ahora guarda `CSV/JSON` y genera graficas por instancia
  para reporte/presentacion.

### 3) Robustez de calibracion SA en Optuna

Problema detectado:
- El espacio de busqueda permitia `p_toggle + p_quantity > 1`, anulando la rama "both".

Correccion:
- Restriccion del espacio para garantizar:
  - `p_toggle + p_quantity <= 0.9`
  - `p_both >= 0.1`

Archivo:
- `experiments/scripts/run_tuning.py`

### 4) Trazabilidad de tuning para graficas

Se agrego persistencia automatica por algoritmo:
- `tuning_<algo>_trials.csv` (detalle por trial)
- `tuning_<algo>_history.json` (series para visualizacion)
- `tuning_<algo>_evolution.png` (curva individual)

Y comparativa multi-algoritmo:
- `tuning_evolution_comparison.png`

Archivos:
- `experiments/scripts/run_tuning.py`
- `experiments/scripts/plot_tuning_evolution.py`

Control operativo adicional:
- `run_tuning.py` incluye timeout duro por trial (`--trial-timeout`) para evitar
  bloqueos prolongados en una sola evaluacion.
- El estado por trial (`ok/timeout/error`) queda registrado en el CSV como
  `user_eval_status`.
- La evaluacion aislada usa proceso + archivo temporal para intercambio de
  resultado (evita fallas por `multiprocessing.Queue` en algunos entornos
  Windows).

### 5) Exposicion del paquete metaheuristics

Se exportan explicitamente:
- `GeneticAlgorithm`
- `SimulatedAnnealing`
- `DifferentialEvolution`
- `HybridGASA`

Archivo:
- `src/metaheuristics/__init__.py`

### 6) Correccion de factibilidad (Eq.2) en decoder

Problema detectado:
- El decoder eliminaba inventario por perecibilidad durante la simulacion.
- Eso podia romper el balance de material (Eq.2) al no existir variable explicita de merma.

Correccion:
- Se removio el descarte explicito de inventario por edad dentro de `decode()`.
- El flujo de inventario ahora conserva balance exacto por periodo:
  `I[t] = I[t-1] + p[t] - v[t]`.
- Se mantuvo consumo FIFO por capas para ventas.

Archivo:
- `src/model/decoder.py`

## Pruebas y validacion

Pruebas ejecutadas:

```bash
pytest -q
```

Resultado:
- `86 passed`

## Impacto sobre tuning en curso

Si un `run_tuning.py` ya estaba ejecutandose al momento de los cambios:
- esa corrida usa el codigo cargado al inicio;
- no incorpora automaticamente estas correcciones;
- no es estrictamente comparable con corridas post-correccion.

Recomendacion:
- cerrar corrida antigua;
- relanzar calibracion con la version actual del codigo.

## Comandos recomendados (post-correccion)

Calibracion completa:

```bash
python experiments/scripts/run_tuning.py --algo all --n-trials 30 --trial-timeout 900 --results-dir experiments/results/tuning
```

Generar comparativa desde historiales ya guardados:

```bash
python experiments/scripts/plot_tuning_evolution.py --results-dir experiments/results/tuning
```

Benchmark con artefactos graficos:

```bash
python experiments/scripts/run_benchmark.py --output-dir experiments/results/benchmark
```

## Estado Fase 2

- Infraestructura de calibracion: lista y operativa.
- Corridas de calibracion: en ejecucion / pendientes de relanzar para trazabilidad limpia.
- Benchmark rapido: ajustado para reporte de gap metodologicamente consistente.
