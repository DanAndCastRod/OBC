# CHECKPOINT V3 — Resumen Ejecutivo de la Iteración

**Fecha de cierre:** 2026-02-26  
**Iteración:** V3 — Robustecimiento del modelo con sustento bibliográfico  
**Documento:** `anteproyecto_coproductos.md`

---

## Resumen

La Iteración V3 aplicó correcciones sistemáticas al anteproyecto basadas en una búsqueda bibliográfica rigurosa (478 resultados en Scopus), procesamiento de 13 papers clave, y resolución de todas las observaciones del evaluador y director.

---

## Cambios Principales

### Modelo Matemático (Anexo A)
- ✅ Restricción de perecibilidad $L_p$ agregada (Claassen 2016)
- ✅ NP-hardness con cadena formal: Florian 1980 → Bitran & Yanasse 1982 → Goren 2016 → Rahmani 2025 → Mahdieh 2018
- ✅ Canales de venta eliminados (sin sustento bibliográfico)
- ✅ 7 ecuaciones, 11 parámetros, 5 variables — todos consistentes

### Metaheurísticas
- ✅ TS+GA-TS → **GA+SA+DE+GA-SA** (Akbari-Aghghaleh 2025)
- ✅ DE-SA propuesto como trabajo futuro (sección 8.4)

### Estado del Arte (Sección 5)
- ✅ 3 párrafos nuevos en 5.1 (NP-hard, perecibilidad FPI, papers avícolas)
- ✅ Sección 5.2 reescrita: SA (5.2.2), DE (5.2.3), GA-SA (5.2.4)
- ✅ Tabla 3a: estadísticas búsqueda Scopus (478 resultados, 8 queries)
- ✅ Tabla 3b: +5 filas (Claassen, Rahmani, Dadaneh, Akbari-Aghghaleh, González-Neira)

### Rigor Científico
- ✅ H1: ≥5% reducción costo (α=0.05)
- ✅ H2: GA-SA gap ≤2%, tiempo ≤50% solver
- ✅ H3: ≥15% reducción inventario (prueba t)
- ✅ Tabla 1 con fuentes por fila

### Viabilidad
- ✅ Cronograma: 26→30 semanas
- ✅ Solver: CBC/PuLP + Gurobi académico
- ✅ Prototipo: "scripts Python CLI"
- ✅ Sección 8.4: Trabajo Futuro

### Bibliografía
- ✅ 49 citas activas en MD
- ✅ 51 entradas en BIB (+13 nuevas)
- ✅ 0 citas faltantes

---

## Observaciones del Evaluador — Estado de Resolución

| # | Observación | Estado |
|:-:|-------------|:------:|
| O1 | Título vs DLBP | ✅ Sin vestigios |
| O2 | Hipótesis vagas | ✅ Cuantificadas |
| O3 | Tabla 1 sin fuentes | ✅ Con fuentes |
| O4 | Cronograma corto | ✅ 30 semanas |
| O5 | $L_p$ sin restricción | ✅ Eq. 7 nueva |
| O6 | Canales inconsistentes | ✅ Eliminados |
| D1 | Presupuesto | ⏭️ Omitido (decisión usuario) |
| D2 | Solver no definido | ✅ CBC/PuLP |
| D3 | Prototipo ambiguo | ✅ "Scripts CLI" |

---

## Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `anteproyecto_coproductos.md` | ~30 correcciones en 15 secciones |
| `referencias_coproductos.bib` | +13 entradas nuevas |
| `anteproyecto_coproductos.pdf` | Recompilado exitosamente |
