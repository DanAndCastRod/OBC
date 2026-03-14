# Fase 3 - Graficas Estadisticas de Instancias

## Objetivo

Documentar el pipeline de analisis estadistico para el banco de instancias de
Fase 3.

## Ejecucion

```bash
python notebooks/01_instance_analysis.py
```

Validacion adicional sintetico vs FENAVI:

```bash
python experiments/scripts/run_fenavi_validation.py
```

Con serie mensual historica FENAVI (opcional):

```bash
python experiments/scripts/run_fenavi_validation.py --fenavi-csv data/references/fenavi_monthly_reference.csv
```

Plantilla de estructura CSV:

`data/references/fenavi_monthly_reference_template.csv`

Salida esperada en `notebooks/figures/`:

- `demand_histograms.png`
- `demand_by_period.png`
- `instance_catalog_overview.png`
- `optimal_solutions.png`
- `demand_correlation_heatmaps.png`

## Que aporta cada grafica

- `demand_histograms.png`: compara perfiles con histogramas + KDE, ECDF y
  boxenplot (cola y dispersion).
- `demand_by_period.png`: muestra tendencia temporal por forma con bandas P5-P95
  (incertidumbre de escenarios y semillas).
- `instance_catalog_overview.png`: compara variabilidad por perfil y reporta
  pruebas `Kruskal-Wallis` y `Mann-Whitney`.
- `optimal_solutions.png`: resume `Z*` y trade-off `tiempo vs objetivo` para
  instancias resolubles.
- `demand_correlation_heatmaps.png`: correlacion Spearman entre coproductos
  para perfiles clave.

## Nota metodologica

Se priorizan herramientas robustas para distribuciones no normales:

- Correlacion de Spearman (monotona, no paramétrica).
- Comparaciones de grupos con Kruskal-Wallis / Mann-Whitney.
- Bandas percentiles en series temporales (no asumen simetria).
- Cobertura de rangos FENAVI en precios sinteticos.
- Si hay historico mensual, comparacion sintetico vs FENAVI con Spearman, KS y Wasserstein.
