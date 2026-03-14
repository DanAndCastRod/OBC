# Reporte Benchmark (Fase 2)

## Ejecutar benchmark y generar graficas

```bash
python experiments/scripts/run_benchmark.py --output-dir experiments/results/benchmark
```

Parametros utiles:

- `--output-dir`: carpeta de artefactos
- `--time-limit`: limite del solver exacto en segundos
- `--seed`: semilla para metaheuristicas

## Artefactos de salida

- `experiments/results/benchmark/benchmark_results.csv`
- `experiments/results/benchmark/benchmark_results.json`
- `experiments/results/benchmark/benchmark_<instancia>_summary.png`

Cada imagen por instancia contiene:

- Gap porcentual vs baseline exacto (solo si exacto es OPTIMAL)
- Tiempo de ejecucion por algoritmo

## Nota metodologica

Si el solver exacto no es `OPTIMAL`, el gap se reporta como `NaN` para evitar
comparaciones invalidas.
