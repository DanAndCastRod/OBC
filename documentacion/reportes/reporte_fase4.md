# Reporte de Resultados - Fase 4

## Tabla de Resultados Principal

| Algoritmo | Z Medio | Std | Gap (%) | Servicio (%) | Inv. Medio | Tiempo (s) | N |
|-----------|---------|-----|---------|-------------|-----------|------------|---|
| Baseline | 899,470,500 | 516,570,010 | 8.99 | 61.5 | 50,449.7 | 0.1 | 9 |
| GA | 908,817,120 | 501,216,075 | 8.52 | 59.6 | 34,500.0 | 456.0 | 270 |
| SA | 883,217,511 | 522,140,338 | 13.11 | 58.4 | 33,570.9 | 28.0 | 270 |
| DE | 916,484,283 | 512,072,980 | 8.14 | 60.0 | 36,010.9 | 300.2 | 270 |
| GA-SA | 916,865,520 | 512,578,412 | 8.12 | 60.1 | 36,337.1 | 368.2 | 270 |
| CBC (Exact) | 1,046,427,720 | 707,764,822 | 0.00 | 61.2 | 2,136.1 | 10.7 | 9 |

## Tabla de Hipotesis

| Hipotesis | Resultado | p-valor | Efecto | Veredicto |
|-----------|-----------|---------|--------|-----------|
| H1 (GA vs Baseline: mejora >= 5%...) | 0.69% | 0.1088 | d=0.021 (negligible) | RECHAZADA |
| H1 (SA vs Baseline: mejora >= 5%...) | -2.36% | 0.4258 | d=-0.011 (negligible) | RECHAZADA |
| H1 (DE vs Baseline: mejora >= 5%...) | 1.12% | 0.1088 | d=0.034 (negligible) | RECHAZADA |
| H1 (GA_SA vs Baseline: mejora >= 5...) | 1.09% | 0.1088 | d=0.033 (negligible) | RECHAZADA |
| H2 (GA-SA vs best{GA,SA,DE}: gap <...) | -0.01% | 0.0000 | d=0.000 (negligible) | APROBADA |
| H2-time (GA-SA time <= 50% CBC time (ra...) | 6434.27% | nan | d=0.000 (n/a) | RECHAZADA |
| H3 (GA vs Baseline: reduccion inve...) | 0.00% | 1.0000 | d=0.000 (negligible) | RECHAZADA |
| H3 (SA vs Baseline: reduccion inve...) | 11.04% | 0.7204 | d=0.299 (small) | RECHAZADA |
| H3 (DE vs Baseline: reduccion inve...) | 0.00% | 1.0000 | d=0.000 (negligible) | RECHAZADA |
| H3 (GA_SA vs Baseline: reduccion i...) | 0.00% | 1.0000 | d=0.000 (negligible) | RECHAZADA |

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