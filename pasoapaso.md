# Plan paso a paso para completar el anteproyecto
**Proyecto:** Balanceo de líneas de desensamble (cut-up/deboning) para carcasas de pollo con integración de demanda pronosticada  
**Fecha de elaboración:** 2025-08-04  
**Alcance temporal de la revisión:** 2015–2025 (global, todos los idiomas)  

---

## 0. Visión general y entregables
**Objetivo:** Entregar un anteproyecto sólido que incluya planteamiento del problema, pregunta de investigación, objetivos, estado del arte sistemático (con PRISMA), metodología preliminar, cronograma y recursos.  

**Entregables principales:**
1. **Libro Excel de la revisión** (PRISMA, screening, extracción) — ya creado como referencia: `anteproyecto_balanceo_avicola_revision_sistematica.xlsx`.
2. **Plantilla de anteproyecto** — ya creada como `anteproyecto_plantilla.md`.
3. **Plan de trabajo** — este documento (`pasoapaso.md`).
4. **Tabla comparativa del estado del arte** (derivada de la hoja *03_Extraccion*).
5. **Diagrama PRISMA** (conteos consolidados – hoja *05_PRISMA*).  
6. **Sección metodológica** con esquema de modelo (determinista vs estocástico/robusto) y estrategia de validación.
7. **Cronograma (Gantt)** y lista de recursos.
8. **Resumen ejecutivo (1 página)**.

**Principios de calidad (gates):**
- Trazabilidad completa: consulta → registro → filtrado → extracción → síntesis → conclusiones (con evidencias).
- Reproducibilidad: cadenas de búsqueda, filtros, fechas y versiones preservadas en repositorio.
- Claridad y coherencia: objetivos ↔ metodología ↔ métricas ↔ resultados esperados.
- Rigor metodológico: criterios de inclusión/exclusión explícitos; sesgos gestionados.

---

## 1. Preparación (Semana 0–1)
**Objetivo:** Alinear expectativas, preparar el entorno y definir artefactos.

**Actividades:**
- A1.1 Definir repositorio (carpetas mínimas)
  - `docs/` (borradores en Markdown, figuras, PRISMA)
  - `data/` (metadatos; no almacenar PDFs con derechos restringidos)
  - `review/` (Excel de revisión, exportaciones CSV)
  - `src/` (scripts de utilidades, p.ej., generación de tablas a partir del Excel)
  - `planning/` (cronograma, actas de reunión)
- A1.2 Reunión inicial con director/a (30–60 min): criterios de éxito, estilo de citación, extensión del anteproyecto.
- A1.3 Configurar gestor de referencias (Zotero/Mendeley) y estilo (APA/IEEE).  
- A1.4 Copiar al repositorio los archivos base: Excel, plantilla MD.

**Entregables:** Acta de reunión inicial; estructura de repositorio creada; lista de riesgos inicial.

**Criterios de salida:** Repositorio listo y aprobado por el director/a; acceso a Scopus, IEEE Xplore y ScienceDirect verificado.

---

## 2. Definición del problema y pregunta de investigación (Semana 1–2)
**Objetivo:** Formular con precisión el problema, la pregunta e hipótesis (si aplica), y los objetivos.

**Actividades:**
- A2.1 Borrador de **contexto y problema**: variabilidad de rendimientos, desviación del mix, cuellos de botella, incertidumbre de demanda.
- A2.2 Redactar **pregunta de investigación** (plantilla CIMO: Contexto–Intervención–Mecanismo–Outcome).
- A2.3 **Objetivo general** y **3–4 objetivos específicos** (medibles y alineados con la metodología).
- A2.4 Validación con director/a; ajustes.

**Entregables:** Sección *Introducción*, *Planteamiento del problema*, *Pregunta de investigación*, *Objetivos* (borrador 1).

**Criterios de salida:** Aprobación del director/a; coherencia entre problema ↔ pregunta ↔ objetivos.

---

## 3. Estrategia y ejecución de la búsqueda sistemática (Semana 2–4)
**Objetivo:** Identificar literatura relevante de 2015 a la fecha con cobertura global y multilingüe.

**Actividades:**
- A3.1 Afinar **tesauro** (ver hoja *08_Tesauro*) con términos de dominio, producto, método e incertidumbre.
- A3.2 Preparar **cadenas de búsqueda** por base (ver *10_Cadenas_Busqueda*); registrar cada ejecución en *01_Log_Busqueda*.
- A3.3 Aplicar **filtros**: 2015–2025, tipo de documento (Article/Review/Conference), áreas (Engineering, Decision Sciences, Computer Science, Food Science).
- A3.4 **Descarga y organización** de metadatos en el gestor de referencias (evitar PDFs cerrados en el repo).
- A3.5 **Encadenamiento de citas** (backward/forward snowballing) para expandir el conjunto.

**Entregables:** *01_Log_Busqueda* completo; repositorio con metadatos; registro de alertas (opcional).

**Criterios de salida:** Se alcanzó saturación temática (número de nuevos artículos por cadena comienza a decrecer).

---

## 4. Screening (título/resumen y texto completo) (Semana 4–6)
**Objetivo:** Depurar el conjunto de artículos a un subconjunto elegible y de alta relevancia.

**Actividades:**
- A4.1 Definir **criterios de inclusión/exclusión**; documentarlos en el Excel y en `docs/criterios_screening.md`.
- A4.2 **Screening Tit/Abs** en *02_Screening*: marcar *Relevante_TitAbs(0/1)* y motivo de exclusión.
- A4.3 **Elegibilidad a texto completo**: marcar *Elegible_texto_completo(0/1)* y motivos.
- A4.4 Resolver **duplicados** y conflictos de decisión (revisión por pares si es posible).

**Entregables:** *02_Screening* completo; listado de artículos **incluidos** para extracción.

**Criterios de salida:** Lista estable de artículos incluidos; duplicados gestionados; trazabilidad mantenida.

---

## 5. Extracción y síntesis del estado del arte (Semana 6–8)
**Objetivo:** Estructurar la evidencia y construir la tabla comparativa y la narrativa crítica.

**Actividades:**
- A5.1 Completar *03_Extraccion*: contexto, tipo de línea, modelo, técnica, incertidumbre, objetivos y métricas.
- A5.2 Exportar a CSV y **generar tabla comparativa** (autor, año, técnica, función objetivo, aplicaciones, métricas).
- A5.3 Redactar **secciones temáticas**: (i) fundamentos ALB/DLB; (ii) aplicaciones en alimentos/cárnicos/avícola; (iii) integración con pronósticos/incertidumbre; (iv) MIP vs metaheurísticas; (v) vacíos.
- A5.4 Completar **05_PRISMA** (conteos consolidados) y bosquejar diagrama PRISMA (figura).
- A5.5 Elaborar **síntesis de gaps** y **oportunidad de contribución**.

**Entregables:** Tabla comparativa; borrador del **Estado del Arte**; conteos PRISMA.

**Criterios de salida:** Estado del arte con narrativa crítica (no descriptiva); vacíos claramente identificados y conectados con la pregunta.

---

## 6. Metodología preliminar (Semana 8–10)
**Objetivo:** Definir el enfoque de modelado y solución, datos requeridos y validación.

**Actividades:**
- A6.1 Seleccionar **paradigma**: determinista, estocástico por escenarios, robusto, o sim-opt (simulación + optimización).
- A6.2 Bosquejar **formulación** (variables, función(es) objetivo, restricciones: precedencia, tiempos, ciclo, estaciones, paralelismo, mix).
- A6.3 Definir **pronóstico** (ARIMA/ETS/ML) y **generación de escenarios** (bootstrap/Monte Carlo) para demanda y, si aplica, **rendimientos**.
- A6.4 Elegir **métodos de solución**: solver (CPLEX/Gurobi) y/o metaheurísticas (GA/VNS/GRASP); criterios de paro.
- A6.5 Diseñar **métricas**: desviación del mix, throughput, utilización, WIP, costo/kg, brecha óptima, tiempo CPU, robustez.
- A6.6 Plan de **validación**: datos reales/sintéticos, simulación de eventos discretos, análisis de sensibilidad.
- A6.7 Riesgos y mitigaciones (datos incompletos, escalabilidad, tiempos de cómputo).

**Entregables:** Sección *Metodología* (borrador); mapa de datos requeridos y plan de validación.

**Criterios de salida:** Metodología consistente con objetivos; factibilidad computacional y de datos.

---

## 7. Cronograma y recursos (Semana 10–11)
**Objetivo:** Establecer tiempos realistas y recursos necesarios.

**Actividades:**
- A7.1 Construir **Gantt** (4–6 meses típicos para anteproyecto completo).
- A7.2 Listar **recursos**: acceso a bases, solver, ambiente de simulación, cómputo.
- A7.3 Definir **hitos** (aprobación pregunta, cierre screening, cierre extracción, borrador Estado del Arte, borrador Metodología, borrador completo, versión final).

**Entregables:** Cronograma; lista de recursos y responsables.

**Criterios de salida:** Cronograma validado por director/a y factible.

---

## 8. Redacción del anteproyecto (Semana 11–13)
**Objetivo:** Completar el documento con consistencia formal.

**Actividades:**
- A8.1 Completar `anteproyecto_plantilla.md` con versiones consolidadas de: Introducción, Problema, Pregunta, Objetivos, Estado del Arte, Metodología, Cronograma, Recursos, Referencias.
- A8.2 Integrar **tabla comparativa** y **PRISMA** como figuras/tablas.
- A8.3 Ajustar **formato y citación** (APA/IEEE) y verificar bibliografía.
- A8.4 Revisión lingüística y de estilo.

**Entregables:** Borrador completo del **Anteproyecto v1**.

**Criterios de salida:** Documento coherente y completo, con referencias consistentes.

---

## 9. Revisión por pares/director y ajustes (Semana 13–14)
**Objetivo:** Incorporar comentarios y cerrar versión de envío.

**Actividades:**
- A9.1 Enviar v1 a director/a y, si es posible, a colega revisor.
- A9.2 Consolidar **observaciones** y plan de correcciones.
- A9.3 Emitir **v2** (y, si procede, **v3**) hasta aprobación final.

**Entregables:** Anteproyecto **vFinal**; acta de aprobación del director/a (si aplica).

**Criterios de salida:** Observaciones resueltas; conformidad del director/a.

---

## 10. Resumen ejecutivo y preparación de la defensa (Semana 14)
**Objetivo:** Preparar una comunicación clara y sintética.

**Actividades:**
- A10.1 Redactar **resumen ejecutivo** (1 página): problema, aportes, metodología, impacto esperado.
- A10.2 Preparar **diapositivas** (10–12) para exposición breve; ensayar 2–3 veces.
- A10.3 Verificar requisitos formales de entrega de la institución.

**Entregables:** Resumen ejecutivo; diapositivas para defensa del anteproyecto.

**Criterios de salida:** Mensaje claro; tiempos de presentación controlados.

---

## 11. Riesgos y mitigaciones (vigilancia continua)
- **R1: Cobertura insuficiente de literatura.** Mitigación: snowballing (referencias/citas), ampliar términos (meat/food processing), alertas en Scopus/IEEE.
- **R2: Falta de datos reales.** Mitigación: dataset sintético calibrado con literatura y rangos industriales; validación cruzada por expertos.
- **R3: Complejidad computacional.** Mitigación: descomposición (Benders), metaheurísticas híbridas, instancias escalables.
- **R4: Deriva de alcance.** Mitigación: checklist de alcance y reuniones quincenales con director/a.
- **R5: Sesgos de selección.** Mitigación: criterios explícitos, doble revisión en fase crítica, registro PRISMA transparente.

---

## 12. Lista de verificación (checklist)
- [ ] Repositorio y plantillas listas (Sección 1).
- [ ] Problema, pregunta y objetivos aprobados (Sección 2).
- [ ] Búsquedas ejecutadas y registradas (Sección 3).
- [ ] Screening con criterios documentados (Sección 4).
- [ ] Extracción completa y tabla comparativa generada (Sección 5).
- [ ] PRISMA consolidado (Sección 5).
- [ ] Metodología definida y validada (Sección 6).
- [ ] Cronograma y recursos aprobados (Sección 7).
- [ ] Anteproyecto v1 redactado (Sección 8).
- [ ] Revisión y versión final (Sección 9).
- [ ] Resumen ejecutivo y presentación (Sección 10).

---

## 13. Plantillas rápidas (para copiar/pegar)

### 13.1. Pregunta de investigación (ejemplos)
- ¿En qué medida un modelo **estocástico/robusto/sim-opt** para el **balanceo de la línea cut-up** que integra **pronósticos de demanda** reduce la **desviación del mix** y mejora el **throughput** frente a un enfoque determinista en **[Planta X]**?
- ¿Cuál es el desempeño relativo de un **MIP por escenarios** frente a una **metaheurística híbrida (GA–VNS)** en el **balanceo de línea de desensamble avícola** bajo **incertidumbre de rendimientos y demanda**, medido por **brecha óptima, tiempo de cómputo y robustez**?

### 13.2. Delimitación del alcance (ejemplo)
Este estudio considera **línea cut-up** post-eviscerado con **8–12 estaciones**, restricciones de **precedencia** y **tiempo de ciclo**, **paralelismo limitado** y **rendimientos de cortes** modelados mediante **distribuciones empíricas**. Integra **pronósticos de demanda** a **4–8 semanas** y **escenarios Monte Carlo**. Objetivos: **minimizar la desviación del mix** y **maximizar el throughput**. Fuera de alcance: faenado, logística externa y ergonomía avanzada (si no hay datos).

### 13.3. Estructura del documento final (esqueleto)
1. Introducción  
2. Planteamiento del problema y objetivos  
3. Marco teórico y Estado del Arte (incluye tabla comparativa y PRISMA)  
4. Metodología propuesta  
5. Cronograma y recursos  
6. Resultados esperados e impacto  
7. Referencias

---

## 14. Cronograma sugerido (resumen)
- Sem 0–1: Preparación (repositorio, reunión inicial).  
- Sem 1–2: Problema, pregunta, objetivos (borrador).  
- Sem 2–4: Búsqueda sistemática (ejecución y registro).  
- Sem 4–6: Screening Tit/Abs y texto completo.  
- Sem 6–8: Extracción, síntesis, PRISMA y tabla.  
- Sem 8–10: Metodología preliminar (formulación y validación).  
- Sem 10–11: Cronograma y recursos.  
- Sem 11–13: Redacción v1 del anteproyecto.  
- Sem 13–14: Revisión y versión final; resumen ejecutivo y presentación.

---

## 15. Notas finales
- Mantenga un **registro de decisiones** (change log) en `planning/` para documentar cambios de alcance y criterios.
- Centralice **tablas/figuras** generadas desde el Excel en `docs/figuras/` con nombres y versión.
- Asegure consistencia terminológica usando la hoja **08_Tesauro** del Excel.

> Con este plan, cada fase entrega artefactos tangibles, mantiene trazabilidad y mitiga riesgos de sesgo o deriva de alcance, asegurando un anteproyecto robusto y defendible.
