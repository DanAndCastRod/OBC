# Contraste de Datos Sinteticos: Stable vs Seasonal

## Objetivo

Cuantificar si el resultado de hipotesis cambia por la estructura de demanda sintetica:

- Perfil `stable` (sin estacionalidad)
- Perfil `seasonal` (con estacionalidad)

El runner ejecuta en paralelo, con `resume` y `checkpoint`.

## Script

- `experiments/scripts/run_data_profile_contrast.py`

## Configuraciones disponibles

- Completa: `experiments/config/data_profile_contrast.yaml`
- Rapida (smoke): `experiments/config/data_profile_contrast_smoke.yaml`

## Ejecucion recomendada

Smoke (validar pipeline):

```powershell
.\.venv\Scripts\python experiments\scripts\run_data_profile_contrast.py `
  --config experiments/config/data_profile_contrast_smoke.yaml `
  --workers 2
```

Experimento completo (paralelo + reanudable):

```powershell
.\.venv\Scripts\python experiments\scripts\run_data_profile_contrast.py `
  --config experiments/config/data_profile_contrast.yaml `
  --resume `
  --workers -1
```

## Salidas principales

- `experiments/results/data_profile_contrast_runs.csv`
- `experiments/results/data_profile_contrast_summary.csv`
- `experiments/results/data_profile_contrast_paired.csv`
- `experiments/results/data_profile_contrast_paired_summary.csv`
- `experiments/results/data_profile_contrast_hypotheses.json`
- `experiments/results/data_profile_contrast_report.md`

## Lectura rapida

- `summary.csv`: comportamiento por `demand_profile` y algoritmo.
- `paired_summary.csv`: delta `seasonal vs stable` por algoritmo/tamano.
- `hypotheses.json`: soporte de H1/H2/H3 por perfil.

## Nota

Si solo incluyes `baseline` y `ga_sa`, los tests que dependen de `ga`, `sa` y `de`
quedaran sin datos. Para evaluar H2 completo, usa la configuracion completa.
