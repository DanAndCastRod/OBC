# Validacion FENAVI con OCR (2026-03-09)

## Alcance

Se extrajeron y validaron dos tablas del PDF escaneado:

- Tabla 5.5.3: precio mensual de carne de pollo en canal (2013-2023)
- Tabla 5.3.1: produccion mensual de pollo (2010-2023)

Archivo fuente:

- `data/Avicultura-en-Cifras-2024_17-09-2024.pdf`

## Artefactos generados

- `data/references/fenavi_price_pollo_en_canal_2013_2023.csv` (132 filas)
- `data/references/fenavi_production_pollo_2010_2023.csv` (168 filas)
- `data/references/fenavi_monthly_reference_extended.csv` (432 filas)

## Ejecuciones realizadas

```powershell
.\.venv\Scripts\python experiments\scripts\extract_fenavi_pdf_reference.py

.\.venv\Scripts\python experiments\scripts\run_fenavi_validation.py `
  --fenavi-csv data/references/fenavi_monthly_reference_extended.csv `
  --fenavi-variable-type price_cop_kg

.\.venv\Scripts\python experiments\scripts\run_fenavi_validation.py `
  --output-dir experiments/results/fenavi_validation_production `
  --fenavi-csv data/references/fenavi_monthly_reference_extended.csv `
  --fenavi-variable-type production_tons
```

## Resultado rapido

Validacion por precios (`experiments/results/fenavi_validation/fenavi_external_monthly_comparison.csv`):

- Productos comparados: 4
- `medio_pollo`: `spearman_rho=0.0060`, `rmse_index=0.2958`
- `pechuga`: `spearman_rho=0.1093`, `rmse_index=0.1261`
- `ala`: `spearman_rho=0.0663`, `rmse_index=0.1160`
- `pernil_completo`: `spearman_rho=-0.1307`, `rmse_index=0.1129`

Validacion por produccion (`experiments/results/fenavi_validation_production/fenavi_external_monthly_comparison.csv`):

- Productos comparados: 1 (`medio_pollo`)
- `spearman_rho=-0.0190`, `rmse_index=0.1805`

## Nota tecnica

`markitdown` offline no logra extraer texto de este PDF (escaneado sin capa OCR).  
El pipeline final usa OCR local con `PyMuPDF + RapidOCR`.
