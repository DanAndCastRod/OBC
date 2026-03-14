# Checklist Pre-Envio (2026-03-10)

## Objetivo

Validar si el paquete de tesis + presentación está listo para envío a evaluación.

## Resultado general

**Estado: LISTO PARA ENVIO**, con una observación operativa menor (codificación de consola en el script de compilación).

## Checklist (10 puntos)

1. **Compilación de tesis PDF**  
   Estado: ✅  
   Evidencia: `tesis/generar_tesis.py` ejecutado exitosamente. PDF generado: `tesis/tesis_coproductos.pdf` (~1299 KB).

2. **Dependencias de compilación (Pandoc/XeLaTeX)**  
   Estado: ✅  
   Evidencia: Pandoc 3.7.0.2 y MiKTeX-XeTeX 4.10 detectados por el generador.

3. **Consistencia de hipótesis H1/H2/H3 en tesis**  
   Estado: ✅  
   Evidencia: H3 reportada como endpoint primario (p=0.455) y endpoint de baja rotación como exploratorio.

4. **Protocolo estadístico formal documentado**  
   Estado: ✅  
   Evidencia: `documentacion/reportes/protocolo_estadistico_fase4.md`.

5. **JSON estadístico regenerado y trazable**  
   Estado: ✅  
   Evidencia: `experiments/results/statistical_tests.json` incluye `protocol.version = v2.1`, metadatos y resultados H3/H3-lowrot.

6. **Validación externa FENAVI reforzada**  
   Estado: ✅  
   Evidencia:  
   - `fenavi_external_monthly_comparison.csv` (Spearman/Pearson/lag/KS/Wasserstein)  
   - `fenavi_external_monthly_summary.csv` (agregado por variable_type)  
   - `fenavi_validation_summary.json` (`|rho|` sin lag ~0.19; con lag ~0.65)

7. **Presentación sincronizada con resultados científicos**  
   Estado: ✅  
   Evidencia: `docs/presentacion/presentation_data.js` contiene `scientific_audit.protocol`, `h3_summary`, `fenavi_validation` con lag.

8. **Integridad de la presentación HTML (UX técnica)**  
   Estado: ✅  
   Evidencia: IDs únicos (`22/22`), sin duplicados; todos los canvas interactivos esperados presentes.

9. **Política visual sin emojis en presentación**  
   Estado: ✅  
   Evidencia: escaneo Unicode U+1F300–U+1FAFF en HTML = `0`.

10. **Regresión de código**  
    Estado: ✅  
    Evidencia: `pytest -q` ejecutado, **234/234 tests passing**.

## Observación menor

- En consola Windows puede aparecer `UnicodeEncodeError` si se ejecuta el generador sin:
  - `PYTHONIOENCODING=utf-8`
- No afecta el contenido científico, pero para ejecución limpia del script se recomienda mantener esa variable durante compilación.

## Comandos clave ejecutados

```bash
python experiments/scripts/run_statistical_tests.py
python experiments/scripts/run_fenavi_validation.py --fenavi-csv data/references/fenavi_monthly_reference_extended.csv
python docs/presentacion/scripts/build_presentation_data.py
pytest -q
```
