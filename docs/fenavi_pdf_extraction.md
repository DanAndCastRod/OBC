# Extraccion OCR FENAVI (PDF Escaneado)

## Objetivo

Generar una referencia mensual utilizable por `run_fenavi_validation.py` a partir del PDF escaneado:

- `data/Avicultura-en-Cifras-2024_17-09-2024.pdf`
- Tabla objetivo 1: **Tabla 5.5.3** (precio mensual de carne de pollo en canal, 2013-2023)
- Tabla objetivo 2: **Tabla 5.3.1** (produccion mensual de pollo, 2010-2023)

## Requisitos

Se recomienda un entorno virtual aislado porque el OCR agrega dependencias de computer vision.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m pip install pymupdf rapidocr-onnxruntime "opencv-python<4.11"
```

## Ejecucion de extraccion

```powershell
.\.venv\Scripts\python experiments\scripts\extract_fenavi_pdf_reference.py
```

Salidas:

- `data/references/fenavi_price_pollo_en_canal_2013_2023.csv`
- `data/references/fenavi_production_pollo_2010_2023.csv`
- `data/references/fenavi_monthly_reference_extended.csv`

## Validacion con el CSV extendido

Comparacion por precios:

```powershell
.\.venv\Scripts\python experiments\scripts\run_fenavi_validation.py `
  --fenavi-csv data/references/fenavi_monthly_reference_extended.csv `
  --fenavi-variable-type price_cop_kg
```

Comparacion por produccion:

```powershell
.\.venv\Scripts\python experiments\scripts\run_fenavi_validation.py `
  --output-dir experiments/results/fenavi_validation_production `
  --fenavi-csv data/references/fenavi_monthly_reference_extended.csv `
  --fenavi-variable-type production_tons
```

## Nota importante sobre MarkItDown

`markitdown` en modo offline no extrae texto de este PDF porque es imagen escaneada sin capa de texto.  
La ruta implementada aqui usa OCR local (`PyMuPDF + RapidOCR`) para automatizar la extraccion.

Resumen de ejecucion real:

- `documentacion/reportes/fenavi_ocr_validacion_2026-03-09.md`
