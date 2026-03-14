# Guia de Ejecucion - Fase 4 (Sprints 4.1 a 4.5)

## 1) Verificar entorno

```bash
python -V
python -m pip install -r requirements.txt
```

## 2) Validar plan sin ejecutar corridas

```bash
python experiments/scripts/run_comparison.py --dry-run
python experiments/scripts/run_sensitivity.py --dry-run
```

## 3) Ejecutar comparacion principal (4.2)

Ejecucion completa:

```bash
python experiments/scripts/run_comparison.py
```

Reanudar corrida interrumpida:

```bash
python experiments/scripts/run_comparison.py --resume
```

## 4) Ejecutar sensibilidad (4.2)

```bash
python experiments/scripts/run_sensitivity.py
```

## 5) Ejecutar analisis estadistico (4.3)

```bash
python experiments/scripts/run_statistical_tests.py --csv experiments/results/comparison.csv --output-dir experiments/results
```

## 6) Generar tablas y figuras de resultados (4.4)

```bash
python experiments/scripts/generate_results_tables.py --csv experiments/results/comparison.csv --output-dir experiments/results
```

## 7) Ejecutar complejidad computacional (4.5)

Sin cProfile:

```bash
python experiments/scripts/run_complexity_analysis.py --comparison-csv experiments/results/comparison.csv --traces-csv experiments/results/comparison_traces.csv --output-dir experiments/results/complexity
```

Con cProfile por componente:

```bash
python experiments/scripts/run_complexity_analysis.py --comparison-csv experiments/results/comparison.csv --traces-csv experiments/results/comparison_traces.csv --output-dir experiments/results/complexity --run-cprofile
```

## 8) Revisar notebook de complejidad (4.5)

Abrir:

`notebooks/04_complexity_analysis.ipynb`

El notebook consume artefactos de `experiments/results/complexity/`.

## 9) Artefactos clave esperados

- `experiments/results/comparison.csv`
- `experiments/results/comparison_traces.csv`
- `experiments/results/sensitivity.csv`
- `experiments/results/statistical_tests.json`
- `experiments/results/main_results_table.csv`
- `experiments/results/complexity/complexity_report.md`
- `experiments/results/complexity/performance_profile.png`
- `experiments/results/complexity/convergence_profiles.png`
- `experiments/results/complexity/diversity_profiles.png`
