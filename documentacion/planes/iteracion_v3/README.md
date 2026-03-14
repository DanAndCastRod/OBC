# Iteración V3 — Plan de Robustecimiento del Anteproyecto

> **Fecha de creación:** 2026-02-25  
> **Última actualización:** 2026-02-25  
> **Objetivo:** Corregir todas las observaciones del evaluator review y sustentar el modelo NP-hard con literatura

---

## Orden de Ejecución

| # | Fase | Archivo | Estado | Dependencia |
|:-:|------|---------|:------:|:-----------:|
| 1 | **Búsqueda Bibliográfica** | [fase1_busqueda_bibliografica.md](fase1_busqueda_bibliografica.md) | 🔴 Pendiente | Ninguna |
| 2 | **Correcciones al Modelo** | [fase2_correcciones_modelo.md](fase2_correcciones_modelo.md) | 🔴 Pendiente | Fase 1 |
| 3 | **Correcciones al Documento** | [fase3_correcciones_documento.md](fase3_correcciones_documento.md) | 🔴 Pendiente | Fases 1 y 2 |
| 4 | **Integración y Verificación** | [fase4_integracion_verificacion.md](fase4_integracion_verificacion.md) | 🔴 Pendiente | Fases 1-3 |

## Flujo de Dependencias

```
Fase 1 (Scopus) ──► Fase 2 (Modelo) ──► Fase 3 (Documento) ──► Fase 4 (PDF)
    │                     │                      │
    ▼                     ▼                      ▼
  Papers              Ecuaciones            Hipótesis
  BibTeX              Restricciones         Presupuesto
  Estadísticas        Coherencia            Estado del Arte
```

## Protocolo de Trabajo

1. **Usuario** ejecuta queries Scopus y descarga BibTeX con abstracts
2. **Agente** procesa los .bib con markitdown-mcp, clasifica por relevancia
3. **Agente** aplica correcciones al modelo y documento
4. **Ambos** verifican el PDF final página por página
