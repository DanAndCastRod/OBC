# Fase 1: Búsqueda Bibliográfica y Sustento del Modelo NP-Hard

> **Estado:** 🔴 Pendiente  
> **Prioridad:** MÁXIMA — Todo lo demás depende de estos hallazgos  
> **Duración estimada:** 3-5 días de trabajo conjunto (usuario ejecuta queries, agente procesa resultados)

---

## Objetivo General de la Fase

Encontrar, descargar, clasificar y analizar artículos científicos que **demuestren formalmente** que el modelo propuesto en el Anexo A (lot-sizing estocástico multi-producto con setup, lote mínimo y perecibilidad) pertenece a la clase de problemas **NP-hard**, y que las **metaheurísticas** (GA, TS, Híbridos) son el enfoque apropiado y establecido en la literatura para resolver este tipo de problemas.

### Resultados Esperados de esta Fase
1. **3-5 papers clave** que sustenten directamente la complejidad NP-hard del modelo
2. **2-3 papers** que documenten el uso de metaheurísticas en lot-sizing/producción alimentaria
3. **1-2 papers** recientes (2024-2026) sobre optimización avícola/cárnica para actualizar la Tabla 3
4. **Estadísticas de búsqueda** (# resultados por query) para incluir en el Estado del Arte
5. **Entradas BibTeX completas** (con abstract) integradas a `referencias_coproductos.bib`

---

## 🏃 Sprint 1.1: Preparación del Entorno de Búsqueda

### 📋 Checklist

- [x] **1.1.1 Acceso a Scopus:**
  - [x] Verificar acceso institucional UTP a [Scopus](https://www.scopus.com)
  - [x] Si no hay acceso directo, usar VPN institucional o proxy de la biblioteca
  - [x] Alternativa: Web of Science como respaldo

- [x] **1.1.2 Preparación de la carpeta de resultados:**
  - [x] Crear carpeta `data/scopus_results/` en el workspace
  - [x] Subcarpetas por query: `Q1_lotsizing_nphard/`, `Q2_meta_setup/`, etc.

- [x] **1.1.3 Configuración de exportación en Scopus:**
  - [x] Formato de exportación: **BibTeX** (.bib)
  - [x] Campos a incluir: **Citation information + Abstract + Keywords + References**
  - [x] Ordenamiento: **Relevance** (por defecto en Scopus)
  - [x] Exportar TODOS los resultados de cada query (no solo los primeros 20)

---

## 🏃 Sprint 1.2: Ejecución de Queries — Bloque A (NP-Hardness Core)

> **Prioridad 🔴 MÁXIMA** — Estas queries son el corazón de la justificación

### Query Q1: Lot-Sizing Estocástico + NP-Hard + Setup

**¿Qué buscamos?** La demostración formal de que el lot-sizing con costos fijos de setup bajo incertidumbre es NP-hard. Este es el teorema que ancla todo el Anexo A.

```
TITLE-ABS-KEY(
  ("lot sizing" OR "lot-sizing") 
  AND ("stochastic" OR "uncertain*") 
  AND ("setup cost" OR "setup time" OR "fixed charge") 
  AND ("NP-hard" OR "complexity" OR "metaheuristic*" OR "genetic algorithm")
) 
AND PUBYEAR > 2014
```

**Instrucciones para el usuario:**
1. Copiar y pegar la ecuación exacta en la barra de búsqueda avanzada de Scopus
2. Anotar el **número total de resultados**
3. Exportar TODOS los resultados en formato BibTeX con abstracts
4. Guardar archivo como `data/scopus_results/Q1_lotsizing_nphard/Q1_results.bib`

**¿Qué buscar en los abstracts?** Palabras clave: "NP-hard", "computational complexity", "proof", "reduction", "polynomial", "intractable"

### 📋 Checklist Q1
- [x] Query ejecutada en Scopus
- [x] Número de resultados anotado: _9_
- [x] BibTeX exportado con abstracts
- [x] Archivo guardado en `data/scopus_results/Q1_lotsizing_nphard/`
- [x] Top 5 papers identificados por relevancia de abstract

---

### Query Q6: CLSP Clásico + Complejidad Computacional

**¿Qué buscamos?** El CLSP (Capacitated Lot-Sizing Problem) es el "ancestro" formal de nuestro modelo. Bitran y Yanasse (1982) demostraron que el CLSP es NP-hard. Buscamos esa referencia clásica + extensiones modernas.

```
TITLE-ABS-KEY(
  ("capacitated lot sizing" OR "CLSP" OR "CLSP-SD") 
  AND ("NP-hard" OR "computational complexity") 
  AND ("heuristic*" OR "metaheuristic*")
) 
AND PUBYEAR > 2015
```

**Instrucciones para el usuario:**
1. Ejecutar en Scopus búsqueda avanzada
2. Anotar número total de resultados
3. Exportar BibTeX completo con abstracts
4. Guardar en `data/scopus_results/Q6_clsp_nphard/Q6_results.bib`

**¿Qué buscar en los abstracts?** Papers de tipo "survey", "review", o que citen explícitamente a Bitran & Yanasse (1982), Florian et al. (1980), o Maes et al. (1991) como fuente de la demostración NP-hard.

### 📋 Checklist Q6
- [x] Query ejecutada en Scopus
- [x] Número de resultados anotado: _30_
- [x] BibTeX exportado con abstracts
- [x] Archivo guardado en `data/scopus_results/Q6_clsp_nphard/`
- [x] Top 5 papers identificados por relevancia de abstract

---

## 🏃 Sprint 1.3: Ejecución de Queries — Bloque B (Perecibilidad y Avicultura)

> **Prioridad 🟠 ALTA** — Valida la restricción de vida útil y actualiza el estado del arte sectorial

### Query Q3: Lot-Sizing con Perecibilidad

**¿Qué buscamos?** Papers que modelen restricciones de vida útil (shelf life) en problemas de lot-sizing con setup. Esto valida directamente nuestra ecuación de $L_p$.

```
TITLE-ABS-KEY(
  ("lot sizing" OR "lot-sizing" OR "production planning") 
  AND ("perishab*" OR "shelf life" OR "food") 
  AND ("setup" OR "fixed cost") 
  AND ("optimization" OR "mixed integer")
) 
AND PUBYEAR > 2015
```

**Instrucciones para el usuario:**
1. Ejecutar en Scopus
2. Anotar número de resultados
3. Exportar BibTeX con abstracts
4. Guardar en `data/scopus_results/Q3_perishable_lotsizing/Q3_results.bib`

**¿Qué buscar en los abstracts?** Formulaciones donde el inventario se descarta después de X periodos, o donde existe una restricción tipo $I_{pt} = 0$ si $t - t_{produccion} > L$. También modelos con "deteriorating items" o "food waste minimization".

### 📋 Checklist Q3
- [x] Query ejecutada en Scopus
- [x] Número de resultados anotado: _20_
- [x] BibTeX exportado con abstracts
- [x] Archivo guardado en `data/scopus_results/Q3_perishable_lotsizing/`
- [x] Top 5 papers identificados

---

### Query Q4: Optimización Avícola y Cárnica Reciente

**¿Qué buscamos?** Papers publicados entre 2018-2026 sobre optimización en la industria avícola o cárnica. Estos actualizan la Tabla 3 del estado del arte y pueden revelar competidores o trabajos complementarios.

```
TITLE-ABS-KEY(
  ("poultry" OR "chicken" OR "meat" OR "carcass") 
  AND ("production planning" OR "supply chain" OR "co-product*" OR "joint production") 
  AND ("optimization" OR "MILP" OR "mathematical model")
) 
AND PUBYEAR > 2018
```

**Instrucciones para el usuario:**
1. Ejecutar en Scopus
2. Anotar número de resultados
3. Exportar BibTeX con abstracts
4. Guardar en `data/scopus_results/Q4_poultry_optimization/Q4_results.bib`

**¿Qué buscar en los abstracts?** Papers aplicados a plantas de beneficio avícola, despiece de carcasas, co-productos cárnicos, o cadena de suministro de pollo. Especial atención a papers colombianos o latinoamericanos.

### 📋 Checklist Q4
- [x] Query ejecutada en Scopus
- [x] Número de resultados anotado: _186_
- [x] BibTeX exportado con abstracts
- [x] Archivo guardado en `data/scopus_results/Q4_poultry_optimization/`
- [x] Top 5 papers identificados

---

## 🏃 Sprint 1.4: Ejecución de Queries — Bloque C (Metaheurísticas Aplicadas)

> **Prioridad 🟡 MEDIA** — Refuerza la justificación del enfoque metaheurístico

### Query Q2: Metaheurísticas para Producción con Setup

**¿Qué buscamos?** Evidencia empírica de que GA, TS y/o Híbridos se han usado exitosamente para resolver problemas de producción con costos fijos de setup.

```
TITLE-ABS-KEY(
  ("production planning" OR "lot sizing") 
  AND ("setup" OR "fixed cost") 
  AND ("metaheuristic*" OR "genetic algorithm" OR "tabu search" OR "hybrid") 
  AND ("stochastic" OR "demand uncertainty")
) 
AND PUBYEAR > 2017
```

### 📋 Checklist Q2
- [x] Query ejecutada en Scopus
- [x] Número de resultados anotado: _11_
- [x] BibTeX exportado con abstracts
- [x] Archivo guardado en `data/scopus_results/Q2_meta_setup/Q2_results.bib`
- [x] Top 5 papers identificados

---

### Query Q5: Programación Estocástica 2-Etapas + Metaheurísticas

**¿Qué buscamos?** Papers que demuestren la viabilidad de resolver programas estocásticos de 2 etapas con metaheurísticas en lugar de solvers exactos.

```
TITLE-ABS-KEY(
  ("two-stage stochastic" OR "2-stage stochastic" OR "stochastic programming") 
  AND ("metaheuristic*" OR "evolutionary" OR "genetic algorithm" OR "tabu search") 
  AND ("production" OR "manufacturing" OR "planning")
) 
AND PUBYEAR > 2016
```

### 📋 Checklist Q5
- [x] Query ejecutada en Scopus
- [x] Número de resultados anotado: _218_
- [x] BibTeX exportado con abstracts
- [x] Archivo guardado en `data/scopus_results/Q5_twostage_meta/Q5_results.bib`
- [x] Top 5 papers identificados

---

## 🏃 Sprint 1.5: Ejecución de Queries — Bloque D (Complementarias)

> **Prioridad 🟢 COMPLEMENTARIA** — Solo si el tiempo permite

### Query Q7: Reviews de Multi-Product Lot-Sizing Estocástico

```
TITLE-ABS-KEY(
  ("multi-product" OR "multi-item") 
  AND ("lot sizing" OR "lot-sizing") 
  AND ("stochastic" OR "uncertain*") 
  AND ("review" OR "survey")
) 
AND PUBYEAR > 2018
```

### Query Q8: Setup + Lote Mínimo + Programación Entera

```
TITLE-ABS-KEY(
  ("minimum lot size" OR "minimum batch" OR "minimum order") 
  AND ("setup" OR "fixed charge") 
  AND ("integer programming" OR "MILP" OR "mixed integer")
) 
AND PUBYEAR > 2015
```

### 📋 Checklist Q7 y Q8
- [x] Q7 ejecutada — Resultados: _0_
- [x] Q8 ejecutada — Resultados: _4_
- [x] BibTeX exportados y guardados

---

## 🏃 Sprint 1.6: Procesamiento y Clasificación de Resultados ✅

> **Estado:** ✅ Completado (2026-02-26)
> **Herramienta:** Script `parse_bib.py` + análisis manual de abstracts

**Objetivo:** Usando análisis automatizado y revisión de abstracts, clasificar todos los papers descargados por relevancia para el proyecto.

### 📋 Checklist

- [x] **1.6.1 Lectura de archivos .bib:**
  - [x] Se creó `parse_bib.py` para procesar cada archivo Q*_results.bib
  - [x] Se extrajeron títulos, autores, años y abstracts con scoring automático de relevancia (keywords: lot sizing, setup, NP-hard, metaheuristic, poultry, two-stage, stochastic, sequence, batch)
  - [x] Resúmenes generados en `data/q2_summary.md`, `data/q4_summary.md`, `data/q5_summary.md`

- [x] **1.6.2 Clasificación por relevancia:**
  - [x] **Alta relevancia** identificados por query (ver tabla abajo)
  - [x] **Media relevancia:** Papers de metaheurísticas en producción genérica, perecibilidad sin setup
  - [x] **Baja relevancia:** Mayoría de Q4 (food safety, AI, IoT) y Q5 (energía, UAV, transporte) — descartados

- [x] **1.6.3 Selección de candidatos core:**
  - [x] Candidatos identificados (ver sección "Papers Candidatos" abajo)
  - [ ] Pendiente: Descargar PDFs de los papers core para lectura de texto completo
  - [ ] Pendiente: Leer papers con markitdown-mcp para extraer ecuaciones y resultados

- [x] **1.6.4 Registro de estadísticas de búsqueda:**

| Query | Tema | # Resultados | # Alta Relevancia | Papers Candidatos |
|-------|------|:------------:|:-----------------:|-------------------|
| Q1 | Lot-sizing NP-hard | 9 | 1 | `deSaintGermain2018` |
| Q2 | Meta + Setup | 11 | 3 | `Rahmani202555`, `Taş2025370`, `Slama2021` |
| Q3 | Perecibilidad | 20 | 3 | `Claassen2016`, `Stefansdottir2017`, papers con "non-triangular setups" |
| Q4 | Avícola/Cárnica | 186 | 4 | `Akbari-Aghghaleh2025`, `Juwitaa202413`, `González-Neira2025`, `Dadaneh2024` |
| Q5 | 2-Etapas + Meta | 218 | 2 | `Geiger2025121`, `Ghasemi2024` |
| Q6 | CLSP NP-hard | 30 | 5+ | `Goren2016`, `Roshani2016`, múltiples confirmaciones NP-hard |
| Q7 | Reviews | 0 | 0 | Sin resultados |
| Q8 | Min Batch + Setup | 4 | 1 | `Mahdieh2018` |

### 📌 Papers Candidatos por Categoría

**🔴 Justificación NP-hard (de Q1, Q6, Q8):**
- Papers de Q6 confirman que el CLSP es NP-hard (Goren & Tunali 2016, Roshani et al. 2016)
- `Mahdieh2018` (Q8): Modela minimum lot size + setup en IP

**🟠 Metaheurísticas + Lot-Sizing Estocástico (de Q2):**
- `Rahmani202555`: Two-stage stochastic capacitated lot-sizing con service level constraints — **directamente aplicable**
- `Taş2025370`: Lot sizing estocástico con inventario limitado, modeled como stochastic programming
- `Slama2021`: GA + Monte Carlo para stochastic disassembly lot-sizing — **usa GA para lot-sizing estocástico**

**🟡 Industria Avícola (de Q4):**
- `Akbari-Aghghaleh2025`: **¡Hallazgo perfecto!** Perishable closed-loop poultry supply chain con metaheurísticas
- `Juwitaa202413`: Broiler chicken supply chains con two-stage stochastic programming
- `González-Neira2025`: MILP para poultry supply chain (scheduling + transporte)
- `Dadaneh2024`: Capacitated lot-sizing problem en la industria avícola para egg production

**🟢 Programación Estocástica 2-Etapas (de Q5):**
- `Geiger2025121`: Sample Average Approximation para Production Routing Problem estocástico
- `Ghasemi2024`: Two-stage stochastic MINLP en supply chain multi-nivel

---

## 🏃 Sprint 1.7: Integración Bibliográfica

**Objetivo:** Incorporar los papers seleccionados al archivo .bib del proyecto y preparar las citas para el documento.

### 📋 Checklist

- [ ] **1.7.1 Actualización de `referencias_coproductos.bib`:**
  - [ ] Agregar entradas BibTeX de los papers seleccionados (con abstract y DOI)
  - [ ] Verificar que el citekey siga el formato `AutorAñoTemaCorto` (ej. `BitranYanasse1982`, `Chen2023LotSizing`)
  - [ ] Agregar campo `note` con descripción del aporte (ej. `note = {Demuestra NP-hardness del CLSP vía reducción desde 3-PARTITION}`)

- [ ] **1.7.2 Script de validación bib↔md:**
  - [ ] Ejecutar `validate_new.ps1` para verificar que no hay citas huérfanas
  - [ ] Verificar que no hay entradas .bib sin uso en el documento

- [ ] **1.7.3 Crear reporte de hallazgos:**
  - [ ] Generar `documentacion/reportes/reporte_busqueda_fase1.md` con:
    - Resumen ejecutivo de hallazgos
    - Tabla de estadísticas de búsqueda (para el Estado del Arte)
    - Lista de papers seleccionados con justificación
    - Decisiones tomadas sobre el modelo (¿confirmar setup + batch? ¿agregar algo?)

---

## Criterio de Salida de la Fase 1

✅ La fase se considera **COMPLETA** cuando:
1. Las 8 queries han sido ejecutadas y los resultados descargados
2. Al menos 3-5 papers core han sido identificados y clasificados
3. Las entradas BibTeX están en `referencias_coproductos.bib`
4. Existe un reporte de hallazgos que oriente las decisiones de la Fase 2
5. Se tiene certeza de que el modelo lot-sizing con setup + batch + perecibilidad ES NP-hard según la literatura
