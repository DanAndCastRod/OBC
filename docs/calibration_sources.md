# Fuentes de Calibración — Parámetros del Modelo

## Proporciones Anatómicas

| Pieza | Proporción (%) | Fuente | Referencia |
|-------|:--------------:|--------|------------|
| Pechuga | 30% | USDA/FAO Ross 308 | Cobb Broiler Management Guide 2024, Tabla rendimiento |
| Muslo | 18% | Solano-Blanco 2022 | Tabla 2, planta Santa Marta |
| Contramuslo | 14% | Solano-Blanco 2022 | Tabla 2, planta Santa Marta |
| Ala | 8% | USDA/FAO | Rendimiento estándar broiler 2.3-2.5 kg |
| Menudencias | 5% | NTC 3644-2 | Hígado, corazón, molleja |
| Otros | 25% | Estimación | Espalda, cuello, grasa, piel |
| **Total** | **100%** | | |

## Precios al Productor (COP/kg)

| Producto | Rango (COP/kg) | Default | Fuente |
|----------|:--------------:|:-------:|--------|
| Pechuga | 12,000 - 15,000 | 14,000 | FENAVI Boletín Estadístico 2024 — Canal mayorista Bogotá |
| Pernil completo | 9,500 - 12,000 | 11,000 | FENAVI 2024 — Precio pernil/pierna |
| Muslo solo | 8,000 - 10,000 | 9,000 | FENAVI 2024 — Muslo individual |
| Contramuslo | 7,500 - 9,500 | 8,500 | FENAVI 2024 — Contramuslo individual |
| Ala | 5,000 - 7,500 | 6,000 | FENAVI 2024 — Ala entera |
| Menudencias | 3,000 - 5,000 | 4,000 | FENAVI 2024 — Menudencias empacadas |
| Subproducto fresco | 1,000 - 2,500 | 1,500 | Estimación — Subproducto para rendering |
| Harina avícola | 1,800 - 3,000 | 2,200 | Estimación — Harina para alimentación animal |
| Filete pechuga | 14,000 - 18,000 | 16,000 | FENAVI 2024 — Filete premium deshuesado |
| Medio pollo | 10,000 - 13,000 | 12,000 | FENAVI 2024 — Medio pollo empacado |

## Costos Operativos

| Concepto | Rango | Default | Unidad | Fuente |
|----------|:-----:|:-------:|--------|--------|
| Costo procesamiento | 1,500 - 2,500 | 2,000 | COP/carcasa | Solano-Blanco 2022 §4.2 |
| Costo setup | 500,000 - 1,500,000 | 500,000 | COP/periodo | Solano-Blanco 2022 — Arranque línea |
| Costo inventario | 100 - 500 | 300 | COP/kg/periodo | Solano-Blanco 2022 — Refrigeración |
| Penalización demanda | 2,000 - 6,000 | 4,000 | COP/kg insatisfecho | Estimación (~30-50% precio venta) |

## Capacidades de Planta

| Perfil | Q_min (carcasas/periodo) | Q_max (carcasas/periodo) | Fuente |
|--------|:------------------------:|:------------------------:|--------|
| Estándar | 500 | 5,000 | Solano-Blanco 2022 — Planta mediana Santa Marta |
| Grande | 1,000 | 10,000 | Estimación — Planta tipo PPC/Bucanero |
| Industrial | 2,000 | 20,000 | Estimación — Planta industrial integrada |

## Vida Útil (días)

| Categoría | Rango | Default | Fuente |
|-----------|:-----:|:-------:|--------|
| Refrigerado fresco | 4 - 7 | 5 | NTC 3644-2 — Pollo fresco 0-4°C |
| Menudencias frescas | 2 - 4 | 3 | NTC 3644-2 — Mayor tasa de degradación |
| Congelado | 30 - 365 | 30 | NTC 3644-2 — Pollo congelado -18°C |
| Harina/deshidratados | 90 - 365 | 180 | Codex CAC/RCP 44-1995 |

## Peso Carcasa

| Parámetro | Valor | Fuente |
|-----------|:-----:|--------|
| Rango | 2.0 - 3.0 kg | Cobb 500 / Ross 308 Performance Objectives 2024 |
| Default | 2.5 kg | Estándar industrial colombiano |

## Referencias Bibliográficas

1. **Solano-Blanco, A.M. et al. (2022)**. *Multi-objective optimization model for poultry supply chain planning*. Planta Santa Marta, Colombia.
2. **FENAVI (2024)**. *Boletín Estadístico del Sector Avícola*. Federación Nacional de Avicultores de Colombia. https://fenavi.org/estadisticas/
3. **Tahraoui, H. et al. (2025)**. *Multi-product lot-sizing with stochastic demand*. Parámetros de estructura multi-producto.
4. **NTC 3644-2 (Colombia)**. *Norma Técnica Colombiana para carnes de aves*. Vida útil y condiciones de almacenamiento.
5. **Codex Alimentarius CAC/RCP 44-1995**. *Code of Practice for the Reduction of Hydrocyanic Acid (HCN)*. Subproductos deshidratados.
6. **Cobb Broiler Management Guide (2024)**. Rendimientos de carcasa y proporciones anatómicas.

## Referencia OCR desde PDF FENAVI

Se integró extracción OCR para la **Tabla 5.5.3** del documento:

- `data/Avicultura-en-Cifras-2024_17-09-2024.pdf`

Script:

```powershell
.\.venv\Scripts\python experiments\scripts\extract_fenavi_pdf_reference.py
```

Archivos generados:

- `data/references/fenavi_price_pollo_en_canal_2013_2023.csv`
- `data/references/fenavi_production_pollo_2010_2023.csv`
- `data/references/fenavi_monthly_reference_extended.csv`

Guía completa:

- `docs/fenavi_pdf_extraction.md`
