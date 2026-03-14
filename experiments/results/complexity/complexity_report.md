# Reporte Sprint 4.5 - Complejidad Computacional

## 1) Escalabilidad empirica

Archivo: `complexity_exponent_fit.csv`

| Algoritmo | a | k | R2 |
|---|---:|---:|---:|
| Baseline | 1.997e-06 | 1.200 | 0.990 |
| CBC | 1.926e-05 | 1.439 | 0.998 |
| DE | 0.1032 | 0.892 | 1.000 |
| GA | 0.003483 | 1.279 | 0.945 |
| GA-SA | 0.01551 | 1.103 | 0.935 |
| SA | 0.06526 | 0.678 | 0.845 |

## 2) Performance profiles

Casos completos utilizados: 270
Grafico: `performance_profile.png`

## 3) Convergence profiles

Curvas generadas: si
Grafico: `convergence_profiles.png`

## 4) Diversidad poblacional

Resumen de convergencia prematura:

| Algoritmo | % convergencia prematura | N runs |
|---|---:|---:|
| DE | 100.00% | 270 |
| GA | 0.00% | 270 |
| GA-SA | 0.00% | 270 |

## 5) cProfile por componente

Ejecutado: no
CSV: `cprofile_component_breakdown.csv`
Grafico: `cprofile_component_breakdown.png`

## Archivos generados

- `complexity_scaling_by_size.csv`
- `complexity_exponent_fit.csv`
- `complexity_loglog_scaling.png`
- `performance_profile.csv`
- `performance_profile.png`
- `convergence_profiles.csv`
- `convergence_profiles.png`
- `diversity_profiles.csv`
- `diversity_profiles.png`
- `diversity_premature_summary.csv`
- `complexity_report.md`