# Fase 5: Validación, Tesis y Presentación

> **Estado:** 🟡 En ejecución — Fase 4 completada  
> **Semanas:** 28–30  
> **Objetivo:** Validar el modelo, escribir la tesis de maestría, y preparar la presentación de sustentación.

---

## Contexto

La Fase 5 cierra el proyecto con tres entregables principales:

1. **Validación final** del modelo y algoritmos
2. **Tesis de maestría** (documento principal, formato UTP/MIOE)
3. **Presentación de sustentación** (`docs/presentacion/`, Reveal.js)

La escritura se ejecuta como **actividad transversal** en paralelo con las fases anteriores (borradores desde la Fase 3), pero las semanas 28-30 se dedican a la consolidación final.

---

## 🛠️ Pipeline de Compilación

> La tesis reutiliza la misma pipeline del anteproyecto (`anteproyecto/generar_anteproyecto_coproductos.py`).

### Herramientas requeridas

| Herramienta | Versión | Propósito |
|---|---|---|
| Pandoc | ≥ 3.x | Markdown → PDF |
| XeLaTeX | TexLive | Motor PDF (soporte Unicode/español) |
| pandoc-citeproc | (integrado) | Procesamiento de citas |
| mermaid-filter | npm | Renderizado de diagramas Mermaid |

### Comando de compilación (referencia)

```bash
pandoc tesis_coproductos.md \
  --bibliography=referencias_coproductos.bib \
  --csl=ieee.csl \
  --citeproc \
  --pdf-engine=xelatex \
  --variable=geometry:margin=2.5cm \
  --variable=fontsize=12pt \
  --variable=documentclass=article \
  --variable=lang=es \
  --highlight-style=tango \
  --include-in-header=header_mermaid.tex \
  --number-sections \
  --output=tesis_coproductos.pdf
```

### Archivos de soporte (copiar de `anteproyecto/`)

- [x] `ieee.csl` — Estilo de citación IEEE
- [x] `header_mermaid.tex` — Control de tamaño de imágenes Mermaid
- [x] `logo_utp.png` — Logo UTP para portadas
- [x] `_mermaid_wrapper.bat` — Wrapper para mermaid-filter en Windows
- [x] `referencias_coproductos.bib` — Archivo de bibliografía (copia, no editar el original de anteproyecto)

### Checklist de compilación

- [x] Crear script `generar_tesis.py` basado en `generar_anteproyecto_coproductos.py`
- [x] Verificar que `pandoc --version` está disponible (Pandoc 3.7.0.2)
- [x] Verificar que `xelatex` está disponible (MiKTeX 4.10)
- [x] Verificar que `mermaid-filter` está instalado
- [x] Primera compilación de prueba con estructura esqueleto → `tesis_coproductos.pdf` (512 KB)
- [x] Verificar numeración de secciones, figuras, tablas y ecuaciones (manual, sin --number-sections)

---

## 🏃 Sprint 5.1: Validación Final y Reproducibilidad (Semana 28)

**Objetivo:** Verificar que las soluciones son realistas, robustas, y completamente reproducibles.

### Descripción
Se ejecuta una validación integral: ¿las soluciones tienen sentido operativo? ¿la pipeline completa se reproduce desde cero? ¿los resultados son robustos ante perturbaciones de datos?

### 📋 Checklist

- [x] **Validación operativa de las soluciones:**
  - [x] Tomar la mejor solución GA-SA para instancia Medium
  - [x] Verificar que el plan de producción es realista:
    - [x] ¿Las cantidades $q_t$ varían razonablemente entre periodos? (CV=0.000 — producción constante a Q_max)
    - [x] ¿El inventario no se acumula indefinidamente? (se acumula levemente en segunda mitad)
    - [x] ¿Los setups tienen sentido económico? ($F$ vs ingreso marginal — ✅ racional)
  - [x] Generar visualización del plan óptimo:
    - [x] **Figura X1:** Gráfico de barras — $q_t$ por periodo (`fig_qt_per_period.png`)
    - [x] **Figura X2:** Gráfico apilado — ventas por coproducto por periodo (`fig_sales_stacked.png`)
    - [x] **Figura X3:** Gráfico de línea — inventario por coproducto vs vida útil $L_p$ (`fig_inventory_shelf_life.png`)
- [x] **Análisis de robustez:**
  - [x] Perturbar demanda ±10% y re-evaluar solución (sin re-optimizar)
  - [x] ¿La solución sigue siendo factible? → ✅ Sí (0 violaciones en todas las perturbaciones)
  - [x] ¿El deterioro de $Z$ es < 5%? → ✅ Sí (máximo -0.04%)
  - [x] Documentar en `documentacion/reportes/reporte_validacion.md` (2.8 KB generado)
- [x] **Reproducibilidad completa:**
  - [x] Crear script `reproduce.py` que ejecute todo desde cero:
    - [x] Generar instancias → resolver con CBC → ejecutar metaheurísticas → generar tablas
  - [x] Ejecutar `pytest` completo (sin cache) — ✅ todos los tests pasan
  - [x] Verificar `requirements.txt` con versiones exactas (pinned)
  - [x] Ejecutar experimento small con seed fija → verificar resultado idéntico
  - [x] Documentar versiones: Python, PuLP, NumPy, SciPy, Optuna

---

## 🏃 Sprint 5.2: Escritura de la Tesis (Semanas 28-30)

**Objetivo:** Consolidar el documento de tesis siguiendo el formato UTP/MIOE.

### Descripción
La tesis se escribe en **Markdown → PDF** usando la misma pipeline Pandoc+XeLaTeX del anteproyecto. La estructura sigue el modelo de la tesis SMIRP de Hincapié Londoño (UTP, 2024, dirigida por Eliana Mirledy Toro Ocampo), con la estructura adaptada al proyecto de coproductos.

### Estructura de la tesis (modelo SMIRP)

La tesis sigue una estructura clásica de trabajo de grado UTP/MIOE:

```
tesis_coproductos.md
├── Portada simple (logo UTP)
├── Portada académica (título, autor, directora, línea)
├── Agradecimientos
├── Resumen / Abstract
├── Índice general
├── Índice de figuras
├── Índice de tablas
├── 1. Introducción
├── 2. Justificación
├── 3. Objetivos
├── 4. Marco referencial
│   ├── 4.1 Marco conceptual
│   └── 4.2 Marco teórico (estado del arte)
├── 5. Formulación del modelo matemático
├── 6. Diseño e implementación de metaheurísticas
├── 7. Resultados computacionales
├── 8. Conclusiones y trabajo futuro
├── Referencias
└── Anexos
```

### 📋 Checklist de Capítulos

#### Capítulo 1 — Introducción (basado en anteproyecto §1)

- [x] 1.1 El problema de producción conjunta en la industria avícola
- [x] 1.2 Relevancia económica y contexto nacional (FENAVI, DANE)
- [x] 1.3 Preguntas de investigación (principal + 3 secundarias)
- [x] 1.4 Hipótesis (H1 ≥5%, H2 ≤2%, H3 ≥15%)
- [x] 1.5 Alcance y limitaciones
- [x] **Figura 1:** Sistema entrada/salida del modelo (diagrama Mermaid)
- [x] **Figura 2:** Dinámica Push/Pull de la cadena avícola (diagrama Mermaid)

#### Capítulo 2 — Justificación (basado en anteproyecto §4)

- [x] 2.1 Conveniencia y relevancia económica
- [x] 2.2 Relevancia social y ambiental (ODS 9, ODS 12)
- [x] 2.3 Implicaciones prácticas
- [x] 2.4 Valor teórico y científico
- [x] **Tabla 1:** Magnitud del problema (producción, empleos, PIB, ahorro potencial, costos inventario, liquidación, desperdicio)

#### Capítulo 3 — Objetivos (basado en anteproyecto §3)

- [x] 3.1 Objetivo general
- [x] 3.2 Objetivos específicos (5 objetivos)

#### Capítulo 4 — Marco Referencial (basado en anteproyecto §5 + búsquedas completas)

> **IMPORTANTE:** Este capítulo incluye **todos los resultados de búsquedas bibliográficas** obtenidos durante el anteproyecto, organizados como un estado del arte exhaustivo.

##### 4.1 Marco conceptual
- [x] 4.1.1 Producción conjunta (joint production)
- [x] 4.1.2 Lot-sizing capacitado (CLSP)
- [x] 4.1.3 Programación estocástica de dos etapas
- [x] 4.1.4 Perecibilidad en la industria alimentaria
- [x] 4.1.5 Metaheurísticas: definición y clasificación

##### 4.2 Marco teórico y estado del arte

- [x] 4.2.1 Complejidad NP-hard del CLSP (cadena Florian → Bitran → Goren → Rahmani → Mahdieh)
- [x] 4.2.2 Lot-sizing con perecibilidad en FPI (Claassen, Stefánsdóttir, Entrup, Rong)
- [x] 4.2.3 Optimización en la cadena de suministro avícola:
  - [x] Solano-Blanco et al. 2022: MILP estocástico, avícola Colombia, −8.6%
  - [x] Tahraoui et al. 2025: MILP (CPLEX), planif. operativa multi-producto
  - [x] Yazdekhasti et al. 2021: MILP multi-modal, SC estocástica Mississippi
  - [x] González-Neira et al. 2025: MILP scheduling + transporte, avícola Colombia
  - [x] Dadaneh et al. 2024: CLSP chance-constraints, huevos avícolas
  - [x] Juwitaa et al. 2024: Prog. estocástica 2 etapas, pollo engorde
- [x] 4.2.4 Metaheurísticas para lot-sizing y SC avícola:
  - [x] Akbari-Aghghaleh et al. 2025: GA, SA, DE, GA-SA, DE-SA, avícola perecible
  - [x] Slama et al. 2021: GA + Monte Carlo, lot-sizing estocástico
  - [x] Roshani et al. 2017: SA para lot-sizing con perecibilidad
- [x] 4.2.5 Optimización multi-objetivo en industria alimentaria:
  - [x] Arteaga-Cabrera et al. 2025: revisión estrategias optimización alimentos
  - [x] Liang et al. 2023: optimización multi-objetivo corte cárnico
  - [x] Mirzapour Al-e-Hashem et al. 2011: MILP robusto multi-objetivo
  - [x] Amorim et al. 2014: MILP multi-objetivo perecederos
- [x] 4.2.6 Modelos deterministas de referencia:
  - [x] Gicquel & Miègeville 2017: MILP producción + transporte
  - [x] Sel et al. 2015: MILP producción + distribución perecederos
  - [x] Kopanos et al. 2012: MILP scheduling alimentaria
- [x] 4.2.7 Tecnologías habilitadoras:
  - [x] Mahalik & Nambiar 2010: automatización/sensores manufactura alimentos
  - [x] Hartono et al. 2022: Bees Algorithm, desensamble robótico
  - [x] Feng et al. 2025: visión por computador, datos sintéticos carcasas
  - [x] Awad et al. 2023: optimización desperdicio/subpeso porcionado avícola

- [x] **Tabla 2:** Resultados búsqueda sistemática Scopus (8 queries, 478 resultados totales)

| Query | Tema | Base de datos | Periodo | # Resultados |
|:-----:|------|:-------------:|:-------:|:------------:|
| Q1 | Lot-sizing estocástico + NP-hard + Setup | Scopus | 2014–2026 | 9 |
| Q2 | Metaheurísticas + Setup estocástico | Scopus | 2017–2026 | 11 |
| Q3 | Perecibilidad + Lot-sizing + Setup | Scopus | 2015–2026 | 20 |
| Q4 | Optimización avícola/cárnica | Scopus | 2018–2026 | 186 |
| Q5 | Prog. estocástica 2-etapas + Metaheurísticas | Scopus | 2016–2026 | 218 |
| Q6 | CLSP + Complejidad computacional | Scopus | 2015–2026 | 30 |
| Q7 | Reviews multi-product lot-sizing estocástico | Scopus | 2018–2026 | 0 |
| Q8 | Lote mínimo + Setup + Prog. entera | Scopus | 2015–2026 | 4 |

- [x] **Tabla 3:** Resumen estado del arte y brechas (15 papers + propuesta posicionada)
- [x] **Figura 3:** Diagrama de intersección de brechas (Mermaid: lot-sizing × perecibilidad × metaheurísticas × avícola)

##### 4.3 Vacíos de investigación identificados
- [x] Ausencia de metaheurísticas para planificación de coproductos avícolas bajo incertidumbre
- [x] Q7 = 0 resultados → no existen reviews de multi-product lot-sizing estocástico
- [x] Solo 13/478 papers en intersección directa

#### Capítulo 5 — Formulación del Modelo Matemático (basado en anteproyecto Anexo A)

- [x] 5.1 Conjuntos, parámetros, variables de decisión
- [x] 5.2 Función objetivo (Eq. 1, desglose de 5 componentes)
- [x] 5.3 Restricciones (Eqs. 2-8, con explicación y justificación)
- [x] 5.4 Estructura de programación estocástica de dos etapas
- [x] 5.5 Validación con solver exacto (CBC) — instancia de referencia
- [x] **Tabla 4:** Conteo de variables y restricciones por tamaño de instancia
- [x] **Figura 4:** Diagrama de flujo del modelo de dos etapas (Mermaid)

#### Capítulo 6 — Diseño e Implementación de Metaheurísticas

- [x] 6.1 Codificación de solución (cromosoma $y_t$, $q_t$)
- [x] 6.2 Decodificador greedy (asignación de segunda etapa)
- [x] 6.3 Algoritmo Genético (GA): cruce de dos puntos, mutación mixta, elitismo
- [x] 6.4 Recocido Simulado (SA): enfriamiento geométrico, vecindarios mixtos, Metropolis, reheating
- [x] 6.5 Evolución Diferencial (DE): estrategia DE/best/1/bin, discretización continua
- [x] 6.6 Algoritmo Híbrido GA-SA: frecuencia de búsqueda local, top-k
- [x] 6.7 Calibración de hiperparámetros (Optuna/TPE, 22 parámetros)
- [x] **Figura 5:** Diagrama de flujo — GA con decodificador greedy
- [x] **Figura 6:** Diagrama de flujo — SA con vecindarios y reheating
- [x] **Figura 7:** Diagrama de flujo — DE/best/1/bin
- [x] **Figura 8:** Diagrama de flujo — GA-SA híbrido (integración)
- [x] **Tabla 5:** Hiperparámetros calibrados por algoritmo (resultado de Optuna)
- [x] **Figura 9:** Evolución del score de Optuna durante calibración (`tuning_evolution_comparison.png`)

#### Capítulo 7 — Resultados Computacionales (basado en Fase 4)

- [x] 7.1 Diseño experimental: factores, niveles, réplicas (1098 corridas)
- [x] 7.2 Perfiles de instancias (Small × Medium × Large, 3 seeds c/u)
- [x] 7.3 Tabla de resultados principal (algoritmo × métrica, datos reales)
- [x] 7.4 Validación de hipótesis H1, H2, H3 (tests estadísticos, p-valores reales)
- [x] 7.5 Performance profiles (Dolan-Moré)
- [x] 7.6 Convergence profiles normalizados
- [x] 7.7 Análisis de escalabilidad (complejidad empírica, gráficos log-log)
- [x] 7.8 Análisis de sensibilidad (precios, costos, variabilidad — 450 ejecuciones)
- [x] 7.9 Análisis de diversidad poblacional (GA vs GA-SA vs DE)
- [x] 7.10 Discusión: comparación con SolanoBlanco, Akbari-Aghghaleh
- [x] **Tabla 6:** Perfiles de instancias
- [x] **Tabla 7:** Resultados principales (Z medio, Std, Rank, N)
- [x] **Tabla 8:** Veredicto de hipótesis (H1/H2/H3, p-valor, veredicto)
- [x] **Tabla 9:** Análisis de sensibilidad (13 configuraciones, Gap%, factibilidad)
- [x] **Figura 10:** Boxplot de fitness por algoritmo (`boxplot_fitness.png`)
- [x] **Figura 11:** Pareto calidad vs tiempo (`pareto_quality_time.png`)
- [x] **Figura 12:** Nivel de servicio por algoritmo (`service_level_comparison.png`)
- [x] **Figura 13:** Performance profile Dolan-Moré (`performance_profile.png`)
- [x] **Figura 14:** Convergence profiles normalizados (`convergence_profiles.png`)
- [x] **Figura 15:** Escalabilidad log-log (`complexity_loglog_scaling.png`)
- [x] **Figura 16:** Diversity profiles (`diversity_profiles.png`)
- [x] **Figura 17:** cProfile breakdown por componente (`cprofile_component_breakdown.png`)

#### Capítulo 8 — Conclusiones y Trabajo Futuro

- [x] 8.1 Conclusiones por objetivo específico (5 objetivos)
- [x] 8.2 Veredicto de hipótesis (tabla H1/H2/H3 con p-valores reales)
- [x] 8.3 Contribuciones principales (5 contribuciones)
- [x] 8.4 Limitaciones del estudio (5 limitaciones)
- [x] 8.5 Trabajo futuro (5 líneas: DE-SA, multi-objetivo, datos reales, scheduling, RL)
- [x] **Tabla 10:** Resumen de veredictos H1/H2/H3

#### Elementos finales

- [x] Agradecimientos
- [x] Referencias (actualizar `referencias_coproductos.bib` con refs de Fases 4-5)
- [x] Anexos: modelo completo, pseudocódigos, resultados detallados
- [x] Tabla de contenidos (autogenerada por Pandoc con `\tableofcontents`)
- [x] Lista de figuras (autogenerada con `\listoffigures`)
- [x] Lista de tablas (autogenerada con `\listoftables`)
- [x] Resumen y abstract (español + inglés)

### 📋 Inventario de Figuras y Tablas

| # | Tipo | Descripción | Fuente |
|---|------|-------------|--------|
| Fig 1 | Mermaid | Sistema entrada/salida del modelo | Anteproyecto Fig 1 |
| Fig 2 | Mermaid | Dinámica Push/Pull cadena avícola | Anteproyecto Fig 2 |
| Fig 3 | Mermaid | Diagrama de Venn — brechas investigación | Nuevo |
| Fig 4 | Mermaid | Modelo estocástico de dos etapas | Nuevo |
| Fig 5 | Mermaid | Flujo del GA con decodificador greedy | Nuevo |
| Fig 6 | Mermaid | Flujo del SA con vecindarios | Nuevo |
| Fig 7 | Mermaid | Flujo del DE/rand/1/bin | Nuevo |
| Fig 8 | Mermaid | Flujo del GA-SA híbrido | Nuevo |
| Fig 9 | PNG | Evolución Optuna tuning | `experiments/results/tuning/` |
| Fig 10 | PNG | Boxplot fitness | `experiments/results/boxplot_fitness.png` |
| Fig 11 | PNG | Pareto calidad-tiempo | `experiments/results/pareto_quality_time.png` |
| Fig 12 | PNG | Nivel de servicio | `experiments/results/service_level_comparison.png` |
| Fig 13 | PNG | Performance profile | `experiments/results/complexity/performance_profile.png` |
| Fig 14 | PNG | Convergence profiles | `experiments/results/complexity/convergence_profiles.png` |
| Fig 15 | PNG | Escalabilidad log-log | `experiments/results/complexity/complexity_loglog_scaling.png` |
| Fig 16 | PNG | Diversity profiles | `experiments/results/complexity/diversity_profiles.png` |
| Fig 17 | PNG | cProfile breakdown | `experiments/results/complexity/cprofile_component_breakdown.png` |
| Tab 1 | MD | Magnitud del problema | Anteproyecto Tab 2 |
| Tab 2 | MD | Búsqueda sistemática Scopus | Anteproyecto Tab 3a |
| Tab 3 | MD | Estado del arte y brechas | Anteproyecto Tab 3b |
| Tab 4 | MD | Conteo variables/restricciones | Nuevo |
| Tab 5 | MD | Hiperparámetros calibrados | `experiments/results/tuning/` |
| Tab 6 | CSV | Resultados principales | `experiments/results/main_results_table.csv` |
| Tab 7 | CSV | Resultados por instancia | `experiments/results/instance_results_table.csv` |
| Tab 8 | JSON | Veredicto hipótesis | `experiments/results/statistical_tests.json` |
| Tab 9 | CSV | Exponentes escalabilidad | `experiments/results/complexity/complexity_exponent_fit.csv` |
| Tab 10 | MD | Resumen veredictos H1/H2/H3 | Nuevo |

### 📋 Formato y compilación

- [x] Usar pipeline Pandoc+XeLaTeX (mismo que anteproyecto)
- [x] Crear `generar_tesis.py` adaptando `generar_anteproyecto_coproductos.py`
- [x] Numeración manual de secciones (sin `--number-sections`)
- [x] Agregar `\listoffigures` y `\listoftables` después del índice
- [x] Importar figuras generadas por Fase 4 como PNG
- [x] Diagramas de flujo de algoritmos como bloques Mermaid (inline)
- [x] Verificar normas UTP: márgenes 2.5cm, fuente 12pt, interlineado
- [x] Compilar versión completa (✅ 1,061 KB) y verificar numeración
- [ ] → Revisión de la directora (mínimo 2 rondas de feedback) *(externo)*

---

## 🏃 Sprint 5.3: Presentación de Sustentación (Semana 30)

**Objetivo:** Crear la presentación en Reveal.js para la defensa de la tesis.

### Descripción
Se crea una presentación nueva en `docs/presentacion/sustentacion_coproductos.html` (reemplazando la versión legacy `sustentacion_dlbp.html`). La presentación usa Reveal.js con diseño limpio y profesional. Duración objetivo: **20-25 minutos** (~15-18 slides).

### Referencia de diseño
Se toma como referencia visual la apariencia del material del Seminario de Investigación I (Alejandra Restrepo, UTP, MIOE): diseño limpio, tipografía profesional, paleta institucional, diagramas claros, sin exceso de texto por slide.

### 📋 Estructura de Slides

- [x] **Slide 1 — Portada:**
  - [x] Título: "Modelo de Optimización para la Planificación de Coproductos con Metaheurísticas en la Industria Avícola"
  - [x] Daniel Andrés Castañeda Rodríguez
  - [x] Directora: Ing. Eliana Mirledy Ocampo Toro, PhD.
  - [x] Logo UTP
- [x] **Slide 2 — Agenda** (9 secciones)
- [x] **Slide 3 — Contexto:** Industria avícola colombiana (stat cards con datos FENAVI)
- [x] **Slide 4 — Problema:** Dinámica Push/Pull con tabla de consecuencias
- [x] **Slide 5 — Pregunta e Hipótesis:** H1, H2, H3 con métricas específicas
- [x] **Slide 6 — Objetivos:** General + 5 específicos
- [x] **Slide 7 — Marco Teórico:** Lot-sizing estocástico, NP-hard, perecibilidad
- [x] **Slide 8 — Estado del Arte:** Tabla resumida, vacíos identificados
- [x] **Slide 9 — Modelo Matemático:** F.O. y restricciones con MathJax
- [x] **Slide 10 — Metaheurísticas:** GA, SA, DE, GA-SA con algo-boxes
- [x] **Slide 11 — Codificación:** Cromosoma + decodificador greedy (visual)
- [x] **Slide 12 — Diseño Experimental:** Factores, niveles, 1098 ejecuciones
- [x] **Slide 13 — Resultados Principales:** Tabla resumen + imágenes
- [x] **Slide 14 — Validación de Hipótesis:** H1/H2/H3 con p-valores y barras de progreso
- [x] **Slide 15 — Escalabilidad y Sensibilidad:** Performance profiles + tabla sensibilidad
- [x] **Slide 16 — Conclusiones:** Veredictos por objetivo
- [x] **Slide 17 — Contribuciones y Trabajo Futuro**
- [x] **Slide 18 — Preguntas** (slide de cierre)

### Diseño y estética

- [x] **Paleta:** Teal + naranja (EC&F) — fondos blancos/claros, texto oscuro
- [x] **Tipografía:** Outfit (headings), Inter (body), Space Grotesk (datos/métricas)
- [x] **Geometría:** Border radius sutil, white space generoso, sombras suaves
- [x] **Animaciones:** Fade-in progresivos, fragment transitions
- [x] **Gráficos interactivos:** Chart.js bar chart interactivo en slide 13
- [x] **Fórmulas:** MathJax para ecuaciones inline y display
- [x] **Responsivo:** Funcional en proyector (1280x720) y laptop
- [x] **Código:** Syntax highlighting con `Space Grotesk` para pseudocódigo de GA-SA (slide 17b)

### 📋 Logística

- [x] Mover `sustentacion_dlbp.html` a `LEGACY` (renombrado con sufijo `_LEGACY`)
- [x] Crear `docs/presentacion/sustentacion_coproductos.html`
- [x] Logo UTP en `docs/presentacion/figuras/` (ya existía)
- [x] Copiar gráficos de Fase 4 a `docs/presentacion/figuras/` (7 PNGs)
- [x] Verificar que funciona offline (CDN → local `libs/`)
- [ ] → Ensayo de tiempo: ¿cabe en 20-25 minutos? *(externo)*
- [ ] → Revisión con la directora antes de la sustentación *(externo)*

---

## 🏃 Sprint 5.4: Publicación del Repositorio (Semana 30)

**Objetivo:** Preparar el repositorio público para publicación permanente.

### Descripción
El repositorio se limpia, se documenta, y se publica como entregable abierto de la investigación. Toda la pipeline debe ser reproducible por un tercero.

### 📋 Checklist

- [x] **Limpieza de código:**
  - [x] Docstrings en todas las funciones públicas (ya existían)
  - [x] Type hints en parámetros y retornos (solo 1 trivial: `cls`)
  - [x] Eliminar código muerto y prints de debug (0 encontrados)
  - [x] Formatear con `black` y validar con `ruff`
- [x] **Documentación del repositorio:**
  - [x] `README.md` actualizado con instrucciones de reproducción paso a paso
  - [x] `LICENCE` (MIT)
  - [x] `CONTRIBUTING.md` actualizado
  - [x] `src/model/README.md`: documentación del modelo
  - [x] `src/metaheuristics/README.md`: documentación de los algoritmos
- [ ] **Release y tag:** *(requiere commit + push manual)*
  - [ ] → Crear tag `v1.0.0-thesis`
  - [ ] → Crear GitHub Release con assets (PDF tesis, presentación)
  - [ ] → Verificar que `LEGACY/` no está en el release
- [x] **Verificación final:**
  - [x] `pytest tests/ -q` → ✅ todos pasan
  - [x] Dataset de instancias disponible en `data/instances/`

---

## 🏃 Sprint 5.5: Visualizaciones de Resultados Prácticos

**Objetivo:** Agregar gráficos interpretativos de resultados a la tesis y elementos interactivos (Chart.js, GIFs) a la presentación.

### 📋 Nuevas figuras para la tesis

Script: `experiments/scripts/generate_practical_figures.py`

- [x] **Figura 18:** Heatmap — Z medio por algoritmo × tamaño de instancia (`heatmap_z_by_algo_size.png`)
- [x] **Figura 19:** Histograma — Distribución de gaps por algoritmo (`gap_distribution_by_algo.png`)
- [x] **Figura 20:** Tornado — Análisis de sensibilidad (`sensitivity_tornado.png`)
- [x] **Figura 21:** Convergencia promedio comparativa (`convergence_comparison.png`)
- [x] **Figura 22:** Veredicto de hipótesis visual — umbral vs resultado (`hypothesis_verdicts_visual.png`)
- [x] Insertar figuras 18-22 en `tesis_coproductos.md` (Sección 7.12)
- [x] Recompilar PDF (✅ 1,190 KB)

### 📋 Mejoras a la presentación

- [x] Chart.js interactivo: tornado de sensibilidad (slide 15)
- [x] Chart.js interactivo: convergencia animada por algoritmo (slide 15b)
- [x] Chart.js interactivo: Z agrupado por algoritmo × tamaño (slide 15c)
- [x] Copiar nuevas figuras a `docs/presentacion/figuras/` (5 PNGs)

---

## Criterios de Salida de la Fase 5

✅ La fase se considera **completa** cuando:
1. Validación de reproducibilidad documentada
2. Tesis escrita en Markdown, compilada a PDF con Pandoc+XeLaTeX, revisada por la directora, y aprobada
3. Presentación `sustentacion_coproductos.html` funcional y ensayada
4. Repositorio limpio con tag `v1.0.0-thesis`
5. Sustentación exitosa ante el comité

---

## 📌 Bitácora de Actualización (2026-03-09) — Extensión de Gráficas Interactivas

> Esta sección documenta la implementación solicitada de nuevas visualizaciones interactivas en la sustentación, **sin eliminar contenido previo**.

### Alcance implementado

- [x] Se agregaron 4 bloques interactivos adicionales en `docs/presentacion/sustentacion_coproductos.html`:
  - [x] **Evolución Optuna** por algoritmo (trial vs best-so-far) + filtro por hiperparámetro.
  - [x] **Heatmap algoritmo × instancia** con selector de métrica (gap, tiempo, servicio, Z).
  - [x] **Distribución de inventario de baja rotación** por percentiles (Q10, Q25, Q50, Q75, Q90) con filtro por tamaño.
  - [x] **Pareto calidad-tiempo** con filtros por tamaño y algoritmo.
- [x] Se mantuvo el diseño sin uso de emoji icons en la presentación principal.
- [x] Se conservaron y ampliaron los elementos interactivos existentes (baseline, convergencia, sensibilidad, robustez).

### Datos y pipeline de soporte

- [x] Se creó script de construcción de datos para presentación:
  - [x] `docs/presentacion/scripts/build_presentation_data.py`
- [x] Se regeneró `docs/presentacion/presentation_data.js` con nuevos bloques:
  - [x] `optuna_trials`
  - [x] `instance_heatmap`
  - [x] `low_rotation_quantiles`
  - [x] `pareto_points`
- [x] Se preservó compatibilidad con bloques previos:
  - [x] `algorithm_summary`, `algorithm_by_size`
  - [x] `convergence_profiles`, `diversity_profiles`
  - [x] `sensitivity`

### Archivos actualizados/añadidos

- [x] `docs/presentacion/sustentacion_coproductos.html`
- [x] `docs/presentacion/presentation_data.js`
- [x] `docs/presentacion/scripts/build_presentation_data.py`
- [x] (ya existentes, reutilizados) GIFs de intuición:
  - [x] `docs/presentacion/figuras/intuicion_ga.gif`
  - [x] `docs/presentacion/figuras/intuicion_sa.gif`
  - [x] `docs/presentacion/figuras/intuicion_de.gif`
  - [x] `docs/presentacion/figuras/intuicion_ga_sa.gif`

### Comando de regeneración (recomendado)

```bash
python docs/presentacion/scripts/build_presentation_data.py
```

### Verificación rápida realizada

- [x] Validación de estructura HTML/IDs sin duplicados.
- [x] Confirmación de inclusión de nuevos canvas/selectores y funciones JS.
- [x] Confirmación de presencia de nuevas claves en `presentation_data.js`.
- [x] Escritura de archivos en UTF-8.

---

## 📌 Bitácora de Actualización (2026-03-10) — Robustecimiento Científico y Trazabilidad

> Actualización incremental sin borrar contenido previo.

### Nota de alcance anteproyecto/proyecto

- [x] Se añadió nota de actualización metodológica en:
  - [x] `anteproyecto/anteproyecto_coproductos.md`
- [x] La nota aclara que los resultados oficiales se reportan en tesis/proyecto (fase 4-5), manteniendo el anteproyecto como documento de formulación original.

### Mejora estadística implementada (H3 primario/secundario)

- [x] Archivo actualizado: `experiments/scripts/run_statistical_tests.py`
- [x] Documento de protocolo añadido: `documentacion/reportes/protocolo_estadistico_fase4.md`
- [x] Cambios aplicados:
  - [x] H3 primario confirmatorio sobre `avg_inventory` (todas las instancias).
  - [x] H3 secundario exploratorio sobre `low_rotation_inventory` con filtro `baseline > 0`.
  - [x] Regla explícita de tamaño muestral informativo mínimo (`n >= 5`) para soporte confirmatorio.
  - [x] Metadatos de protocolo en salida JSON (`protocol.version = v2.1`, fecha, unidad de análisis, endpoint primario/secundario).
- [x] Resultado regenerado:
  - [x] `experiments/results/statistical_tests.json`

### Mejora de validación externa FENAVI (temporal + lags)

- [x] Archivo actualizado: `experiments/scripts/run_fenavi_validation.py`
- [x] Cambios aplicados:
  - [x] Comparación externa por `variable_type` (ej. `price_cop_kg`, `production_tons`).
  - [x] Cálculo de Spearman/Pearson en índice mensual normalizado.
  - [x] Cálculo de correlación con desfase temporal óptimo (`best_lag_months`, `best_lag_spearman_rho`).
  - [x] Resumen agregado por tipo de variable.
- [x] Resultados regenerados:
  - [x] `experiments/results/fenavi_validation/fenavi_external_monthly_comparison.csv`
  - [x] `experiments/results/fenavi_validation/fenavi_external_monthly_summary.csv`
  - [x] `experiments/results/fenavi_validation/fenavi_validation_summary.json`

### Alineación con sustentación (datos científicos)

- [x] Archivo actualizado: `docs/presentacion/scripts/build_presentation_data.py`
- [x] Se agregó en `scientific_audit`:
  - [x] Metadatos de protocolo estadístico (`protocol`).
  - [x] Resumen de H3 primario y H3-lowrot.
  - [x] Métricas FENAVI por tipo de variable y con lag.
- [x] Regenerado:
  - [x] `docs/presentacion/presentation_data.js`
- [x] Ajuste de texto en presentación:
  - [x] `docs/presentacion/sustentacion_coproductos.html` (H3 explícito como primario + secundario).

### Comandos ejecutados

```bash
python experiments/scripts/run_statistical_tests.py
python experiments/scripts/run_fenavi_validation.py --fenavi-csv data/references/fenavi_monthly_reference_extended.csv
python docs/presentacion/scripts/build_presentation_data.py
```

### Estado final de esta actualización

- [x] Cambios aplicados en UTF-8.
- [x] Artefactos regenerados y trazables.
- [x] Metodología y presentación sincronizadas para sustentación y reporte.
- [x] Checklist pre-envío registrado en:
  - [x] `documentacion/reportes/checklist_pre_envio_2026-03-10.md`


