# Reporte de Evolucion Optuna (Fase 2)

Este documento resume como ejecutar la calibracion y generar artefactos para
reporte/presentacion.

Nota de cierre tecnico de Fase 2:
- `docs/fase2_metaheuristicas_cierre_2026-02-28.md`

## 1) Ejecutar calibracion

```bash
python experiments/scripts/run_tuning.py --algo all --n-trials 30
```

Opciones utiles:

- `--algo {ga,sa,de,ga_sa,all}`
- `--n-trials N`
- `--seed SEED`
- `--trial-timeout SEGUNDOS` (corta trials pegados; default `900`)
- `--results-dir experiments/results/tuning`

## 2) Artefactos generados automaticamente

Por algoritmo (`<algo>`):

- `experiments/results/tuning/tuning_<algo>_trials.csv`
- `experiments/results/tuning/tuning_<algo>_history.json`
- `experiments/results/tuning/tuning_<algo>_evolution.png`
- `experiments/config/tuning_<algo>.yaml` (mejor configuracion)

Comparativa (si se corre mas de un algoritmo):

- `experiments/results/tuning/tuning_evolution_comparison.png`

## 3) Regenerar grafica comparativa (post-proceso)

```bash
python experiments/scripts/plot_tuning_evolution.py --results-dir experiments/results/tuning
```

## 4) Columnas clave para analisis en el CSV

- `trial`
- `state`
- `value`
- `best_so_far`
- `duration_seconds`
- `user_eval_status` (`ok`, `timeout`, `error`)
- `param_*` (hiperparametros evaluados por trial)

## 5) Recomendacion de trazabilidad en tesis/presentacion

- Reportar siempre: semilla, numero de trials, conjunto de instancias y fecha.
- Usar `best_so_far` para curvas de convergencia por algoritmo.
- Usar `value` para dispersion de trials (estabilidad del tuner).

## 6) Nota tecnica de robustez

- El timeout por trial se aplica con evaluacion aislada por proceso.
- El resultado del worker se serializa via archivo temporal (evita dependencia de `multiprocessing.Queue` en entornos Windows restringidos).
