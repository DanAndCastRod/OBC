# Fase 2: Documentación del Estado del Arte y Metodología

## Objetivo
Agregar a la presentación la metodología de revisión bibliográfica, estadísticas de búsqueda, y proceso de selección de fuentes.

---

## 2.1 Slide: Metodología de Revisión Bibliográfica (SLR)

### Contenido Propuesto

**Título:** "Revisión Sistemática de Literatura"

| Elemento | Detalle |
|----------|---------|
| **Bases de datos** | Scopus, Web of Science, Google Scholar |
| **Periodo** | 2018–2026 |
| **Idiomas** | Inglés y español |
| **Queries principales** | Ver sección 2.2 |

### Diagrama de flujo PRISMA (simplificado)

```
Registros identificados (Scopus + WoS + GScholar)
    → N resultados totales
        → Filtro por título/abstract: N₁ 
            → Removidos duplicados: N₂
                → Lectura completa: N₃
                    → Incluidos en revisión final: 46 fuentes
```

> **Nota:** Las cifras exactas deben obtenerse del historial de búsquedas en Scopus (ver `data/estudio_del_arte_09022026/`).

---

## 2.2 Queries de Búsqueda Documentadas

Estas queries ya están definidas en `documentacion/GUIA_BUSQUEDA_BIBLIOGRAFICA.md`:

| ID | Query | Base | Resultados |
|----|-------|------|-----------|
| Q1 | `("disassembly line balancing" OR "DLBP") AND ("stochastic" OR "uncertain")` | Scopus | Pendiente |
| Q2 | `("disassembly line balancing") AND ("genetic algorithm" OR "tabu search" OR "hybrid")` | Scopus | Pendiente |
| Q3 | `("food processing" OR "poultry") AND ("optimization" OR "line balancing")` | Scopus | Pendiente |
| Q4 | `("assembly line balancing") AND ("multi-objective" OR "pareto")` | Scopus | Pendiente |

> ⚠️ **Acción requerida del usuario:** Ejecutar estas queries en Scopus con credenciales UTP y reportar el número de resultados para documentar.

---

## 2.3 Slide: Criterios de Inclusión/Exclusión

**Criterios de Inclusión:**
- Publicaciones en revistas indexadas (Q1-Q4 Scimago)
- Relacionadas directamente con DLBP, ALB, o metaheurísticas aplicadas
- Publicaciones entre 2018-2026

**Criterios de Exclusión:**
- Papers sin revisión por pares
- Resúmenes de conferencia sin texto completo
- Duplicados entre bases de datos

---

## 2.4 Actualización de Documentación del Capítulo 1

### En `INFORME_FINAL_COMPLETO.md`

Agregar subsección **"1.1.x Metodología de Revisión"** que incluya:
1. Descripción del protocolo de búsqueda
2. Tabla de queries y resultados
3. Diagrama PRISMA de selección
4. Justificación de las 46 fuentes seleccionadas

---

## Entregables de Fase 2

| Archivo | Acción |
|---------|--------|
| `docs/presentacion/sustentacion_dlbp.html` | Agregar 1-2 slides de metodología SLR |
| `docs/tesis/INFORME_FINAL_COMPLETO.md` | Agregar sección de metodología de revisión |
| `documentacion/GUIA_BUSQUEDA_BIBLIOGRAFICA.md` | Completar con cifras reales de búsquedas |
