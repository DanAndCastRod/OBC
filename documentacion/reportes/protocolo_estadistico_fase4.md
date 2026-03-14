# Protocolo Estadístico Fase 4 (v2.1)

**Fecha de actualización:** 10 de marzo de 2026  
**Ámbito:** `experiments/results/comparison.csv` (1098 corridas, 9 instancias)

## 1. Objetivo

Definir un protocolo reproducible para evaluar H1, H2 y H3 con unidad de análisis explícita, control de comparaciones múltiples y separación entre evidencia confirmatoria y exploratoria.

## 2. Unidad de análisis

- **Primaria (confirmatoria):** instancia (promedio sobre seeds).
- **Secundaria (complementaria):** corrida `instance-seed` para trazabilidad.

## 3. Hipótesis y endpoints

- **H1:** mejora de utilidad (`z_value`) ≥ 5% vs baseline.
- **H2:** gap de GA-SA ≤ 2% vs mejor metaheurística individual.
- **H2-tiempo (componente operativo):** tiempo GA-SA ≤ 50% del tiempo CBC.
- **H3 primario (confirmatorio):** reducción de `avg_inventory` ≥ 15%.
- **H3-lowrot (exploratorio):** reducción de `low_rotation_inventory` ≥ 15% solo cuando baseline > 0.

## 4. Pruebas estadísticas

- Normalidad de diferencias: Shapiro-Wilk.
- Contrastes umbral one-sided: t-test una muestra o Wilcoxon one-sided.
- Comparación global por corridas: ANOVA 1 factor + Tukey HSD.
- Comparación bloqueada por instancia: Friedman + Wilcoxon pareado con ajuste Holm.

## 5. Reglas de decisión

- Nivel de significancia: `alpha = 0.05`.
- Soporte de hipótesis por umbral: requiere cumplir simultáneamente:
  - dirección del efecto respecto al umbral,
  - p-valor < 0.05,
  - tamaño de muestra informativa suficiente cuando aplique.
- Para H3 y H3-lowrot se exige `n_informativo >= 5` para soporte confirmatorio.

## 6. Reporte mínimo obligatorio

- `experiments/results/statistical_tests.json` con:
  - resultados por hipótesis y algoritmo,
  - ranking global y pruebas pareadas,
  - metadatos de protocolo (`protocol.version`, fecha, endpoint primario/secundario).

## 7. Comando de reproducción

```bash
python experiments/scripts/run_statistical_tests.py
```

## 8. Observaciones de interpretación

- H2 puede estar soportada en calidad, pero no necesariamente en tiempo frente a CBC.
- H3-lowrot debe tratarse como exploratoria cuando el número de instancias informativas sea bajo.
- Las conclusiones finales se deben alinear con tesis y sustentación para evitar mezclar lectura preliminar (anteproyecto) con lectura final (proyecto).
