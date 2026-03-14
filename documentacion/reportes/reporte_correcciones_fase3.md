# Reporte de Fase 3: Correcciones al Cuerpo del Documento
**Fecha:** 2026-02-26  
**Sprints:** 3.1 + 3.2 + 3.3  
**Documento modificado:** `anteproyecto_coproductos.md`

---

## 1. Resumen Ejecutivo

Se aplicaron **~25 correcciones** al cuerpo del anteproyecto, cubriendo: estado del arte ampliado con papers de la búsqueda bibliográfica, hipótesis cuantificadas, tabla de impactos con fuentes, cronograma extendido, solver definido, prototipo acotado, y sección de trabajo futuro.

---

## 2. Sprint 3.1 — Estado del Arte Ampliado

### Nuevos contenidos en sección 5.1
| Párrafo | Contenido | Referencias |
|---------|-----------|-------------|
| NP-hard formal | Cadena Florian 1980 → Bitran & Yanasse 1982 → Goren 2016, extensión estocástica Rahmani 2025, lote mínimo Mahdieh 2018 | 5 citas nuevas |
| Perecibilidad FPI | Non-triangular setups + product decay, taxonomía de setups | Claassen 2016, Stefánsdóttir 2017 |
| Papers avícolas | CLSP chance-constraints, SC ciclo cerrado con metaheurísticas, MILP colombiano, broiler estocástico | Dadaneh, Akbari-Aghghaleh, González-Neira, Juwitaa |

### Sección 5.2 reescrita
- **5.2.2** TS → SA (Recocido Simulado) con Roshani 2017, Akbari-Aghghaleh 2025
- **5.2.3** Nuevo: DE (Evolución Diferencial) con Akbari-Aghghaleh 2025
- **5.2.4** GA-TS → GA-SA con evidencia de mejor rendimiento

### Tabla 3 ampliada
- **Tabla 3a** (nueva): 478 resultados en 8 queries de Scopus
- **Tabla 3b**: +5 filas (Claassen, Rahmani, Dadaneh, Akbari-Aghghaleh, González-Neira)

### Limpieza TS→SA/DE/GA-SA
7 reemplazos en: Resumen, Mermaid, preguntas, hipótesis, objetivos, secciones 4.6, 5.2. **0 residuales.**

---

## 3. Sprint 3.2 — Rigor Científico

### Hipótesis cuantificadas

| Hipótesis | Antes | Después |
|-----------|-------|---------|
| **H1** | "reducción significativa" | **≥5%** costo total vs. baseline proporcional (α=0.05) |
| **H2** | "superará en desempeño" | GA-SA: gap **≤2%**, tiempo **≤50%** del solver CBC |
| **H3** | "estadísticamente significativo" | **≥15%** reducción inventario baja rotación (prueba t, α=0.05) |

### Tabla 1 corregida
- Título: "Rangos representativos de impacto del desbalance **según la literatura**"
- Columna de **Referencia** agregada por fila (SolanoBlanco, Sel, Amorim, FENAVI, Claassen, Akbari-Aghghaleh)

### Multi-objetivo (Sección 4.6)
Frase de cierre: *"Si bien el modelo propuesto utiliza una función objetivo escalar (beneficio esperado ponderado), los principios de optimización multi-criterio documentados por Arteaga-Cabrera et al. representan una línea de extensión natural..."*

---

## 4. Sprint 3.3 — Viabilidad y Gestión

| Cambio | Antes | Después |
|--------|-------|---------|
| **Cronograma** | 26 semanas, Fase 5 = 2 sem | **30 semanas**, Fase 5 = 6 sem |
| **Fase 2** | GA (3s) + TS (3s) + Híbrido (2s) | GA (3s) + SA (2s) + DE (2s) + GA-SA (2s) |
| **Solver** | "cuando sea posible" | **CBC (PuLP)** para $n_t ≤ 12$, $n_ω ≤ 50$; Gurobi académico |
| **Prototipo** | "herramienta de software" | **"scripts Python CLI"** + documentación |
| **Trabajo Futuro** | No existía | **Sección 8.4**: DE-SA, multi-objetivo, datos reales, scheduling |

### Presupuesto
Omitido por decisión del usuario — no requerido por la evaluación (era sugerencia del director, no exigencia del evaluador).

---

## 5. Verificación de Consistencia

- ✅ 0 menciones de "Búsqueda Tabú" o "GA-TS"
- ✅ Metaheurísticas consistentes en todo el documento: GA, SA, DE, GA-SA
- ✅ Hipótesis con métricas, umbrales, pruebas estadísticas y baselines
- ✅ Tabla 1 con fuentes por fila
- ✅ Cronograma realista (30 semanas, ≥4 sem escritura)
- ✅ Solver definido explícitamente
- ✅ Prototipo acotado
- ✅ Sección Trabajo Futuro con DE-SA

---

## 6. Próximos Pasos → Fase 4

1. Verificar que todas las nuevas citas estén en `referencias_coproductos.bib`
2. Compilar documento con Pandoc para verificar formato
3. Validación bibliográfica (script de consistencia citas↔bib)
