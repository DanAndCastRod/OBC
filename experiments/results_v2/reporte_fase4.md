# Reporte de Resultados - Fase 4

## Tabla de Resultados Principal

| Algoritmo | Z Medio | Std | Gap (%) | Servicio (%) | Inv. Medio | Tiempo (s) | N |
|-----------|---------|-----|---------|-------------|-----------|------------|---|
| Baseline | 570,336,848 | 92,149,776 | 20.48 | 73.1 | 20,818.6 | 0.0 | 30 |
| GA | 695,762,030 | 169,977,990 | 5.15 | 64.8 | 14,643.1 | 73.7 | 180 |
| SA | 694,878,471 | 168,883,932 | 5.24 | 64.7 | 14,377.3 | 67.5 | 180 |
| DE | 698,306,907 | 172,326,724 | 4.87 | 65.1 | 14,415.3 | 61.9 | 180 |
| GA-SA | 694,545,186 | 168,522,573 | 5.28 | 64.9 | 14,914.7 | 60.0 | 180 |
| CBC (Exact) | 734,147,038 | 184,321,932 | 0.00 | 70.4 | 5,196.3 | 62.1 | 30 |

## Tabla de Hipotesis

| Hipotesis | Resultado | p-valor | Efecto | Veredicto |
|-----------|-----------|---------|--------|-----------|
| H1 (GA vs Baseline: mejora >= 5% (...) | 20.37% | 0.0000 | d=0.908 (large) | APROBADA |
| H1 (SA vs Baseline: mejora >= 5% (...) | 20.24% | 0.0000 | d=0.906 (large) | APROBADA |
| H1 (DE vs Baseline: mejora >= 5% (...) | 20.76% | 0.0000 | d=0.916 (large) | APROBADA |
| H1 (GA_SA vs Baseline: mejora >= 5...) | 20.19% | 0.0000 | d=0.905 (large) | APROBADA |
| H2 (GA-SA vs best{GA,SA,DE}: gap <...) | 0.54% | 0.0000 | d=-0.025 (negligible) | APROBADA |
| H2-run (GA-SA vs best{GA,SA,DE}: gap <...) | 0.75% | 0.0000 | d=-0.035 (negligible) | APROBADA |
| H2-time (GA-SA time <= 50% CBC time (ra...) | 470.33% | nan | d=0.000 (n/a) | RECHAZADA |
| H3 (GA vs Baseline: reduccion inve...) | 29.50% | 0.0000 | d=1.654 (large) | APROBADA |
| H3 (SA vs Baseline: reduccion inve...) | 30.98% | 0.0000 | d=1.695 (large) | APROBADA |
| H3 (DE vs Baseline: reduccion inve...) | 30.52% | 0.0000 | d=1.730 (large) | APROBADA |
| H3 (GA_SA vs Baseline: reduccion i...) | 28.31% | 0.0000 | d=1.551 (large) | APROBADA |
| H3-lowrot (GA vs Baseline: reduccion inve...) | nan% | nan | d=nan (n/a) | RECHAZADA |
| H3-lowrot (SA vs Baseline: reduccion inve...) | nan% | nan | d=nan (n/a) | RECHAZADA |
| H3-lowrot (DE vs Baseline: reduccion inve...) | nan% | nan | d=nan (n/a) | RECHAZADA |
| H3-lowrot (GA_SA vs Baseline: reduccion i...) | nan% | nan | d=nan (n/a) | RECHAZADA |

## Graficos

### Boxplot de Fitness por Algoritmo
![Boxplot](boxplot_fitness.png)

### Pareto: Calidad vs Tiempo
![Pareto](pareto_quality_time.png)

### Nivel de Servicio
![Service Level](service_level_comparison.png)

## Limitaciones

1. Instancias generadas sinteticamente (no datos reales de planta)
2. Time limit de 300s puede limitar convergencia en instancias Large
3. CBC no garantiza optimo en instancias Medium/Large dentro del time limit
4. Baseline simple (proporcional) puede no representar practica industrial real