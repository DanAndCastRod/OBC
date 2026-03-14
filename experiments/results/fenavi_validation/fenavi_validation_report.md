# Validacion Sintetico vs FENAVI

## Resumen

- Instancias analizadas: **15**
- Observaciones de precio evaluadas: **99**
- Cobertura global de precios en rango FENAVI: **100.00%**

## Archivos generados

- `fenavi_price_validation.csv`
- `fenavi_price_summary.csv`
- `fenavi_demand_summary.csv`
- `fenavi_demand_seasonality.csv`
- `fenavi_validation_summary.json`
- `price_range_coverage.png`
- `synthetic_demand_monthly_profile.png`
- `fenavi_external_monthly_comparison.csv`
- `fenavi_external_monthly_summary.csv`
- `fenavi_external_monthly_comparison.png`

## Lectura rapida

- La validacion de precios se basa en rangos FENAVI documentados en `src/instances/calibration.py`.
- La validacion de demanda sintetica reporta dispersion y fuerza estacional por perfil/producto.
- Se ejecuto comparacion externa mensual por `variable_type` con Spearman/Pearson, desfase optimo (lag), KS y Wasserstein.
- Tipos de variable externos analizados: **price_cop_kg, production_tons**.
- Correlacion Spearman absoluta media: **0.190**.
- Correlacion Spearman absoluta media con lag optimo: **0.649**.