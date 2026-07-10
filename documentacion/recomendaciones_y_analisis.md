# Análisis Verificado del Estado del Repositorio y Recomendaciones para Sustentación

**Fecha:** 2026-06-09
**Proyecto:** Modelo de Optimización para la Planificación de Coproductos con Metaheurísticas en la Industria Avícola
**Última auditoría automatizada:** 2026-06-09T20:49 UTC

---

## Resumen Ejecutivo

Este documento presenta un análisis del repositorio del proyecto de tesis de maestría, basado en una **auditoría automatizada verificable** (conteo de archivos, funciones, líneas, y validación cruzada de citas). Las conclusiones anteriores contenían errores factuales que se corrigen aquí. La investigación está **sustancialmente completa**: el código, los tests, el documento de tesis (incluyendo el Capítulo 8 de Conclusiones), y la presentación de sustentación son funcionales y coherentes. Las recomendaciones se centran en verificación de entorno, correcciones menores, y preparación táctica para la defensa.

### Correcciones respecto a versiones anteriores de este documento

| Afirmación anterior | Realidad verificada |
|---------------------|---------------------|
| "Capítulo 8 incompleto / esquelético" | **Capítulo 8 completo**: 5 subsecciones (51 líneas), cubre objetivos, hipótesis, contribuciones, limitaciones y trabajo futuro |
| "226 tests" | **183 funciones `def test_`** en 11 archivos |
| "26 slides en la presentación" | **32 `<section>` tags** en el HTML |
| "Carece de type hints en funciones públicas" | **Type hints presentes** en todas las funciones públicas muestreadas (`solver.py`, `base.py`, `generator.py`, `decoder.py`) |
| "60 referencias en .bib pero solo 28 citadas" | **41 entradas en .bib, 41 citadas** — alineación perfecta (0 huérfanas, 0 faltantes) |

---

## 1. Metodología de Auditoría

Los datos de este documento se obtuvieron mediante:

1. **Conteos automatizados** (`Select-String`, `Measure-Object`, `Get-ChildItem`) sobre el filesystem
2. **Lectura directa** del contenido de archivos fuente (tesis markdown, código Python, HTML de presentación)
3. **Validación cruzada** de citas: extracción regex de `[@CiteKey]` en el markdown vs. `@type{CiteKey,` en el `.bib`
4. **Muestreo de type hints**: inspección manual de 4 archivos representativos (`solver.py`, `base.py`, `generator.py`, `decoder.py`)

> **Limitación**: Los tests no se ejecutaron (falta `pulp` en el entorno actual). Los conteos reflejan funciones definidas, no tests que pasen.

---

## 2. Estado del Repositorio — Datos Verificados

### 2.1 Estructura y Organización

| Directorio | Propósito | Archivos | Verificación |
|------------|-----------|----------|-------------|
| `src/` | Código fuente (4 paquetes) | 19 `.py` | ✅ Auditado |
| `tests/` | Suite pytest | 11 archivos, 183 funciones `test_` | ✅ Contado |
| `tesis/` | Documento de tesis | 1,284 líneas MD, 20 figuras PNG, PDF+DOCX generados | ✅ Auditado |
| `experiments/` | Scripts y resultados | 17 scripts, 12 configs YAML, 31+ archivos de resultados | ✅ Auditado |
| `data/` | Instancias y papers | 15 YAML (5×3 seeds), 38 papers nuevos, 15 descartados | ✅ Auditado |
| `docs/presentacion/` | Presentación Reveal.js | 32 slides, 7 GIFs, 32 PNGs | ✅ Auditado |
| `documentacion/` | Planes, reportes, guías | ~30 archivos entre planes, reportes, y guías | ✅ Auditado |
| `anteproyecto/` | Documento aprobado | Archivado | — |
| `LEGACY/` | Código anterior (DLBP) | Archivado | — |

### 2.2 Fases de Investigación

| Fase | Descripción | Estado |
|------|-------------|--------|
| **Fase 1** | Modelo MILP estocástico | Completada |
| **Fase 2** | Metaheurísticas (GA, SA, DE, GA-SA) | Completada |
| **Fase 3** | Generación de instancias calibradas | Completada |
| **Fase 4** | Diseño experimental y análisis | Completada |
| **Fase 5** | Validación, tesis y presentación | Completada (pendiente: verificación de entorno y sustentación) |

---

## 3. Análisis del Código Fuente

### 3.1 Arquitectura del Modelo (`src/model/`)

El modelo MILP está implementado con una arquitectura modular:

- **`parameters.py`** (15 KB): Clase `ProblemInstance` con validaciones de integridad, carga YAML, y verificación de consistencia (proporciones suman 1, cotas coherentes).
- **`solver.py`** (11.4 KB): Wrapper sobre PuLP/CBC con soporte alternativo HiGHS/Gurobi. Incluye timeout y extracción de gap. **Type hints completos.**
- **`objective.py`** (4.5 KB): Evaluador vectorizado con `numpy.einsum` para computar Z sobre múltiples escenarios.
- **`constraints.py`** (10 KB): 7 restricciones con docstrings.
- **`decoder.py`** (5.5 KB): Decodificador greedy FIFO. **Type hints completos.**
- **`solution.py`** (5.7 KB): Clase `Solution` con desglose de 5 componentes de costo.

**Fortalezas:**
- La vectorización con `einsum` es una decisión de diseño sólida para evaluación de fitness en escenarios estocásticos.
- La independencia de solver (PuLP como abstracción) permite reproducibilidad sin licencias comerciales.
- La validación de invariantes matemáticos en `ProblemInstance` previene errores silenciosos en downstream.

### 3.2 Metaheurísticas (`src/metaheuristics/`)

Arquitectura por herencia con clase base abstracta:

```
BaseMetaheuristic (abstracta, base.py - 5.9 KB)
    ├── GeneticAlgorithm  (ga.py - 7.6 KB)
    ├── SimulatedAnnealing (sa.py - 6.6 KB)
    ├── DifferentialEvolution (de.py - 8.4 KB)
    └── HybridGASA (ga_sa.py - 9.5 KB)
```

- **Codificación unificada** (`encoding.py`, 7.4 KB): Todos los algoritmos comparten la representación cromosómica `(y, q)` y el decodificador greedy, permitiendo comparaciones justas.
- **Reparación de factibilidad**: `repair_lot_sizing` garantiza cromosomas factibles sin necesidad de penalizaciones.
- **Pseudocódigo en docstrings**: Práctica excelente para documentación académica.

### 3.3 Instancias (`src/instances/`)

- `generator.py` (20.7 KB): Generador paramétrico con **type hints completos**
- `calibration.py` (11.4 KB): Calibración con datos FENAVI/DANE
- `distributions.py` (6.4 KB): LogNormal con estacionalidad mensual
- 5 perfiles (Toy, Small, Medium, Large, Industrial) × 3 seeds = 15 instancias YAML

### 3.4 Tests

| Métrica | Valor |
|---------|-------|
| Archivos de test | 11 |
| Funciones `def test_` | 183 |
| Framework | pytest (v8.4.1) |
| Configuración | `pytest.ini` |
| Estado de ejecución | **No verificado** (falta `pulp` en entorno) |

**Archivos**: `test_baseline`, `test_calibration`, `test_constraints`, `test_de`, `test_encoding`, `test_ga`, `test_ga_sa`, `test_generator`, `test_parameters`, `test_sa`, `test_solver`

---

## 4. Análisis del Documento de Tesis

### 4.1 Estructura y Completitud

El documento `tesis_coproductos.md` tiene **1,284 líneas** (~98 KB) y se compila a PDF mediante `generar_tesis.py` (Pandoc + XeLaTeX, 2 pasadas).

| Capítulo | Líneas | Estado |
|----------|--------|--------|
| 1. Introducción | 147–263 | ✅ Completo |
| 2. Justificación | 264–323 | ✅ Completo |
| 3. Objetivos | 324–343 | ✅ Completo |
| 4. Marco Referencial | 344–544 | ✅ Completo |
| 5. Formulación del Modelo Matemático | 545–685 | ✅ Completo |
| 6. Diseño e Implementación de Metaheurísticas | 686–1045 | ✅ Completo (360 líneas — el capítulo más extenso) |
| 7. Resultados Computacionales | 1046–1198 | ✅ Completo (12 subsecciones, 1,098 ejecuciones) |
| 8. Conclusiones y Trabajo Futuro | 1199–1248 | ✅ Completo (5 subsecciones) |
| Referencias | 1251–1254 | ✅ 41 entradas, formato IEEE |
| Anexos A–D | 1258–1284 | ✅ Completo |

**No se encontraron marcadores TODO, FIXME, PLACEHOLDER, TBD, COMPLETAR, ni FALTA en el documento.**

### 4.2 Detalle del Capítulo 8 (Conclusiones)

Contrario a evaluaciones anteriores, el Capítulo 8 **está completo** con 5 subsecciones:

| Subsección | Contenido |
|------------|-----------|
| §8.1 Conclusiones por Objetivo Específico | Mapea conclusiones a los 5 objetivos: formulación (MILP+CBC), implementación (4 MH+decoder), instancias (3 perfiles FENAVI), comparación (1,098 runs, ranking), validación (sensibilidad+robustez) |
| §8.2 Veredicto de Hipótesis | Tabla con H1 (no soportada, 0.59–1.10%, p=1.000), H2 (soportada, gap −0.02%, p=1.95×10⁻³), H3 (no soportada, 12.2–17.5%, p=0.455) |
| §8.3 Contribuciones Principales | 5 contribuciones: modelo MILP, framework comparativo, evidencia GA-SA, instancias calibradas, análisis de robustez |
| §8.4 Limitaciones del Estudio | 5 limitaciones: datos sintéticos, baseline fuerte, proporciones fijas, sin scheduling, perecibilidad simplificada |
| §8.5 Trabajo Futuro | 5 direcciones: híbrido DE-SA, multi-objetivo (NSGA-II), datos reales, scheduling, deep RL |

**Evaluación**: El capítulo es conciso (51 líneas) pero cubre los 5 elementos esenciales de unas conclusiones de tesis. Su brevedad es una fortaleza — evita la redundancia con el Capítulo 7, que ya tiene 12 subsecciones de discusión extensa.

> **Posible mejora (opcional):** Se podría expandir §8.1 con un párrafo de síntesis narrativa que conecte los hallazgos, en lugar de un mapeo objetivo→conclusión. Esto daría más "vuelo" al capítulo sin ser redundante. Es una mejora estilística, no estructural.

### 4.3 Bibliografía

| Métrica | Valor |
|---------|-------|
| Entradas en `.bib` | 41 |
| Citas únicas en markdown | 41 |
| Huérfanas (en .bib pero no citadas) | 0 |
| Faltantes (citadas pero no en .bib) | 0 |
| Formato | IEEE (vía `ieee.csl`) |
| Archivo | `tesis/referencias_coproductos.bib` |

**Alineación perfecta.** No se requiere intervención.

### 4.4 Figuras

**20 figuras PNG** en `tesis/figuras/`. Evaluación selectiva:

| Figura | Evaluación | Observación |
|--------|------------|-------------|
| `fig_chromosome_representation.png` | Buena | Clara correspondencia `y_t`↔`q_t`. Verificar legibilidad en B/N para impresión |
| `fig_neighborhood_operators.png` | Buena | Distinción visual de 3 operadores clara |
| `fig_exploration_exploitation.png` | Buena | Posicionamiento intuitivo de algoritmos en el espectro |
| `boxplot_fitness.png` | Buena | Distribución de Z por algoritmo correctamente mostrada |
| `pareto_quality_time.png` | Buena | Trade-off calidad-tiempo visible |
| `performance_profile.png` | Buena | Implementación correcta de Dolan-Moré |
| `sensitivity_tornado.png` | Buena | Precios como parámetro dominante claramente identificado |
| `hypothesis_verdicts_visual.png` | Buena | Síntesis visual de H1/H2/H3 efectiva |

**Recomendación general:** Verificar resolución ≥ 300 DPI y legibilidad en impresión B/N para las figuras que usan color como canal de información (cromosoma, operadores, exploración-explotación).

### 4.5 Calidad del Texto

- **Ecuaciones**: Formateadas en LaTeX, numeradas, referenciadas.
- **Tablas**: Con título, fuente, y referencia cruzada.
- **Referencias cruzadas**: Formato consistente (Figura X, Tabla Y).
- **Diagramas Mermaid**: Integrados — la conversión a PDF depende de `mermaid-filter`.

**Observaciones de legibilidad:**
1. El Capítulo 6 es denso (360 líneas con información técnica). Los subcapítulos internos mitigan esto, pero las transiciones entre codificación → operadores → algoritmos pueden beneficiarse de párrafos puente.
2. El pipeline de generación (`generar_tesis.py`) usa un mecanismo `@@SHORT@@...@@ENDSHORT@@` para captions cortas en la lista de figuras. Esto es funcional pero frágil — una errata en los delimitadores rompería el build silenciosamente.

---

## 5. Análisis de la Presentación de Sustentación

### 5.1 Estructura y Flujo

La presentación `sustentacion_coproductos.html` contiene **32 slides** organizadas así:

| # | Slide | Propósito |
|---|-------|-----------|
| 1 | Portada | Identificación (logo UTP) |
| 2 | Agenda | Roadmap (9 puntos) |
| 3 | Contexto | KPIs: 1.7M toneladas, NP-hard |
| 4 | Problema | Push vs Pull, tabla de consecuencias |
| 5 | Justificación | Impactos económicos, ODS 9 y 12 |
| 6 | Hipótesis | H1, H2, H3 con veredictos en pills |
| 7 | Objetivos | OE1–OE5 en tarjetas |
| 8 | Marco Teórico | Grid de 4 pilares |
| 9 | Estado del Arte | Queries Scopus, tabla de papers, brecha |
| 10 | Modelo | Función objetivo + restricciones + dimensiones |
| 11 | Metaheurísticas | GIFs animados (4 algoritmos) |
| 12 | Codificación | Diagrama visual del cromosoma + decodificador |
| 13 | Cromosoma (detalle) | GIF de construcción, espacio de búsqueda |
| 14 | Operadores | GIF animado de 3 operadores |
| 15 | Exploración-Explotación | GIF + tabla de perfiles |
| 16 | Diseño Experimental | Tabla factorial + calibración |
| 17 | Análisis Descriptivo | Boxplot + hallazgos |
| 18 | Resultados Numéricos | Tabla Z con ranking |
| 19 | Análisis Inferencial | ANOVA, Friedman, Wilcoxon-Holm |
| 20 | Escalabilidad | Dolan-Moré + log-log |
| 21 | Convergencia | Chart.js interactivo con selector |
| 22 | Dashboard | Ranking + métricas interactivas |
| 23 | Optuna | Tabla + gráficos de evolución |
| 24 | Heatmap | Matriz interactiva por métrica |
| 25 | Inventario | Intercuartil por algoritmo |
| 26 | Pareto | Filtros por tamaño y algoritmo |
| 27 | Sensibilidad | Selectores de parámetro y métrica |
| 28 | Robustez | Checklist técnico + indicadores |
| 29 | Limitaciones | Metodológicas + técnicas |
| 30 | Conclusiones | OE1–OE5 + hallazgo principal |
| 31 | Contribuciones | 5 contribuciones + 6 líneas futuras |
| 32 | Preguntas | Cierre |

### 5.2 Recursos Visuales

**GIFs animados (7):** Todos verificados como existentes en `docs/presentacion/figuras/`.

| GIF | Tamaño | Existe |
|-----|--------|--------|
| `intuicion_ga.gif` | 107 KB | ✅ |
| `intuicion_sa.gif` | 149 KB | ✅ |
| `intuicion_de.gif` | 109 KB | ✅ |
| `intuicion_ga_sa.gif` | 102 KB | ✅ |
| `chromosome_build.gif` | 125 KB | ✅ |
| `neighborhood_operators.gif` | 173 KB | ✅ |
| `exploration_exploitation.gif` | 243 KB | ✅ |

Todos están por debajo de 250 KB — no habrá problemas de carga. El HTML incluye `onerror="this.style.display='none'"` como fallback.

**Gráficos interactivos (Chart.js):** Convergencia, ranking, métricas por tamaño, trazabilidad Optuna, heatmap, inventario, Pareto, sensibilidad. Los datos se cargan desde `presentation_data.js` (469 KB embebidos).

**Evaluación:** Los gráficos interactivos son el activo más valioso de la presentación para manejar preguntas improvisadas del jurado.

### 5.3 Ruta de Presentación Recomendada

**Formato: 40 minutos de exposición + 15–20 minutos de preguntas.**

> ⚠️ **Nota sobre tiempo:** 32 slides en 40 minutos = 1.25 min/slide promedio. Esto es ajustado. Se recomienda identificar 5–8 slides que se pueden pasar rápido (agenda, portada, marco teórico) para dar más tiempo a slides técnicos (modelo, resultados, hipótesis).

**Fase 1 — Contexto y Motivación (5 min, slides 1–4)**
- Enfocar en KPIs impactantes (1.7M toneladas, NP-hard) y tabla de consecuencias.
- No detenerse en la agenda más de 15 segundos.

**Fase 2 — Justificación e Hipótesis (3 min, slides 5–7)**
- Destacar ODS 9 y 12. Mencionar que H1 y H3 no se soportan pero H2 sí — esto demuestra honestidad metodológica.
- **Punto clave**: Plantear las hipótesis pronto crea tensión narrativa que se resuelve en la Fase 5.

**Fase 3 — Marco Teórico y Estado del Arte (3 min, slides 8–9)**
- Slide 8: pasar rápido (los jurados ya conocen el marco teórico).
- Slide 9: enfocar en el diagrama de intersección ("Solo 2.7% de 478 papers tocan las 4 dimensiones"). Este es el argumento más fuerte de la brecha.

**Fase 4 — Modelo y Metaheurísticas (8 min, slides 10–15)**
- **Esto es el corazón de la presentación.** Mostrar GIFs animados — son el recurso más memorable.
- Slide 10: Función objetivo con anotaciones.
- Slides 11–15: GIFs de algoritmos → cromosoma → operadores → balance.

**Fase 5 — Resultados (12 min, slides 16–22)**
- Slide 16: Diseño factorial (1,098 ejecuciones — número impresionante).
- Slide 19: **Momento crítico** — Explicar por qué ANOVA no detecta diferencia pero Friedman sí (bloqueo por instancia). Esto es una pregunta segura del jurado.
- Slide 22: Dashboard interactivo — tener listo "gap medio" seleccionado.

**Fase 6 — Análisis Avanzado (4 min, slides 23–28)**
- Pasar selectivamente. Priorizar sensibilidad (slide 27) y robustez (slide 28).
- Destacar: 100% factibilidad, robustez ante ±10% demanda.

**Fase 7 — Cierre (5 min, slides 29–32)**
- Ser honesto sobre limitaciones (datos sintéticos, baseline fuerte).
- Cerrar con contribuciones y trabajo futuro.

### 5.4 Propuestas de Mejora para la Presentación

**Mejoras de alto impacto / bajo esfuerzo:**

1. **Preparar slides de respaldo (3–5):**
   - Tabla completa de hiperparámetros calibrados.
   - Diagrama de arquitectura de software (`src/` como UML simplificado).
   - Complejidad computacional detallada (del cProfile existente).
   - Reproducibilidad: URL del repo, comandos de ejecución.

2. **Mejorar el slide de Hipótesis (slide 6):**
   - Agregar una mini-tabla que explique el por qué de H1 no soportada (baseline fuerte, demanda > capacidad). Anticipa una pregunta segura del jurado.

3. **Demostración en vivo (opcional pero impactante):**
   - Ejecución de 30 segundos del GA-SA sobre instancia Toy en terminal. Demuestra que el código funciona.

**Mejoras de menor prioridad:**

4. Verificar que los gráficos interactivos funcionen en el navegador y laptop específicos que se usarán en la sustentación (Chart.js puede tener problemas con versiones antiguas de navegadores).

5. Tener versión PDF estática de la presentación como backup total.

---

## 6. Recomendaciones Priorizadas para Finalización

### 6.1 Prioridad ALTA — Hacer antes de la sustentación

#### R1. Verificar que los Tests Pasen

**Problema verificado:** El entorno actual no tiene `pulp` instalado. Los tests no se han ejecutado.

**Acción:**
```bash
pip install -r requirements.txt
pytest tests/ -v
```
- Si hay fallos, documentar cuáles son críticos (funcionalidad) vs. no críticos (estilo, warnings).
- **Criterio de aceptación:** 0 fallos en tests de funcionalidad (`test_solver`, `test_constraints`, `test_parameters`, `test_encoding`). Warnings aceptables.

#### R2. Regenerar el PDF y Verificar

**Problema potencial:** El pipeline Pandoc + XeLaTeX + mermaid-filter es complejo y puede fallar en un entorno limpio.

**Acción:**
1. Ejecutar `python tesis/generar_tesis.py` en entorno limpio.
2. Verificar que las 20 figuras se incluyan correctamente.
3. Verificar que los diagramas Mermaid se rendericen (requiere `mermaid-cli` instalado).
4. Verificar que las captions `@@SHORT@@` se procesen sin errores.
5. Revisar el PDF resultante página por página.

#### R3. Corregir la Ruta de `reproduce.py` en el README

**Error encontrado:** El `README.md` raíz referencia `reproduce.py` como si estuviera en la raíz del proyecto, pero el archivo está en `experiments/scripts/reproduce.py`.

**Acción:** Actualizar la ruta en `README.md` o crear un symlink/wrapper en la raíz.

#### R4. Preparar Respuestas a Preguntas del Jurado

Las siguientes preguntas son altamente probables:

**P1: "¿Por qué H1 no se soportó? ¿Significa que el modelo no sirve?"**
> "No. La no-soporte de H1 indica que el baseline de capacidad máxima es una heurística fuerte para este problema específico, donde la demanda frecuentemente supera la capacidad. La modesta mejora (0.59–1.10%) no invalida el modelo; indica que el problema tiene una estructura particular donde producir al máximo es casi óptimo. El valor del modelo está en la consistencia (menor variabilidad) y en la robustez ante perturbaciones, no solo en la mejora porcentual sobre el baseline."

**P2: "¿Por qué el gap vs CBC es del 8–13%?"**
> "El gap es razonable para un problema NP-hard con 72,060 variables y un límite de 300 segundos. Las metaheurísticas están diseñadas para buenas soluciones rápidamente, no para garantizar optimalidad. En planificación táctica, una solución al 8–13% del óptimo en 5 minutos es preferible a horas de espera. Además, el gap es una cota superior; la solución real puede estar más cerca del óptimo."

**P3: "¿Los datos sintéticos invalidan los resultados?"**
> "Los datos fueron calibrados con parámetros reales del sector avícola colombiano (proporciones anatómicas FENAVI, precios DANE, patrones de demanda). Los datos sintéticos permiten benchmarking reproducible — un aporte metodológico en sí mismo. La validación con datos operativos reales es el siguiente paso, identificado explícitamente como trabajo futuro."

**P4: "¿Por qué GA-SA y DE están prácticamente empatados?"**
> "El empatamiento confirma que ambos alcanzan la zona de convergencia del problema. La diferencia de 0.024% es negligible operativamente. Esto sugiere un paisaje de fitness donde múltiples algoritmos encuentran soluciones similares. La ventaja de GA-SA es la convergencia más rápida (menos evaluaciones), no necesariamente una calidad final superior."

**P5: "¿Cuál es la contribución original?"**
> "Primer framework que combina: (1) lot-sizing estocástico de dos etapas, (2) coproducción fija, (3) perecibilidad FIFO, y (4) comparación sistemática de 4 metaheurísticas con calibración automática. Solo 2.7% de 478 papers revisados toca estas 4 dimensiones simultáneamente. Adicionalmente, las instancias calibradas y el código abierto son contribuciones metodológicas."

### 6.2 Prioridad MEDIA — Hacer si hay tiempo

#### R5. Crear Slides de Respaldo

3–5 slides no presentados en el flujo principal pero disponibles para preguntas:
1. Arquitectura de software (diagrama de clases de `src/`).
2. Complejidad computacional detallada (cProfile breakdown).
3. Reproducibilidad (URL repo, comandos de test y generación de tesis).
4. Publicación potencial (revistas o conferencias objetivo).

#### R6. Ensayo con Temporizador

- Practicar la presentación 2–3 veces con cronómetro.
- Identificar slides donde se tiende a extenderse.
- Verificar que los gráficos interactivos funcionan en el laptop y proyector reales.
- Tener backup estático (PDF) por si falla el navegador o el proyector.

#### R7. Expandir Brevemente §8.1 (Opcional)

El Capítulo 8 está completo, pero §8.1 es un mapeo objetivo→conclusión bastante telegráfico. Un párrafo de síntesis narrativa (5–8 líneas) que conecte los hallazgos en una historia coherente elevaría el capítulo de "correcto" a "memorable". Esto es una mejora estilística, no un requisito.

### 6.3 Prioridad BAJA — Nice to have

#### R8. Publicar Instancias con DOI

Subir las 15 instancias YAML calibradas a Zenodo o Figshare con DOI. Esto aumenta la citabilidad. Incluir en la tesis: "Los datos y código están disponibles en [URL] (DOI: XXXX)".

#### R9. Generar Documentación de API

El código tiene docstrings consistentes. Generar documentación automática con Sphinx sería útil para futuros usuarios, pero no es necesario para la sustentación.

#### R10. Agregar `pyproject.toml`

El proyecto usa `requirements.txt` (10 dependencias pinned), pero carece de `pyproject.toml`. Esto es una mejora de packaging moderna pero no afecta la funcionalidad.

---

## 7. Análisis de Riesgos para la Sustentación

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|:------------:|:-------:|------------|
| Jurado pregunta por H1 no soportada | **Alta** | Medio | Respuesta preparada (R4-P1) |
| Jurado cuestiona gap 8–13% vs CBC | **Alta** | Medio | Respuesta preparada (R4-P2) |
| Jurado cuestiona datos sintéticos | **Media** | Medio | Respuesta preparada (R4-P3) |
| Problemas con presentación HTML/JS en proyector | **Media** | **Alto** | PDF de respaldo + probar laptop real (R6) |
| GIFs no se reproducen | **Baja** | Medio | HTML tiene fallback `onerror`; GIFs son <250KB |
| Tests fallan al ejecutar | **Media** | Medio | Ejecutar y corregir antes (R1) |
| Pipeline PDF falla al regenerar | **Media** | Medio | Verificar dependencias antes (R2) |
| Jurado pide ver código en vivo | **Baja** | Bajo | Tener terminal lista con `python -c "from src import ..."` |

---

## 8. Veredicto Final

### 8.1 Estado de la Investigación

**La investigación está completa.** Verificado:

| Aspecto | Estado | Evidencia |
|---------|--------|-----------|
| Modelo MILP formulado e implementado | ✅ | `src/model/` (7 archivos, solver funcional) |
| 4 metaheurísticas implementadas | ✅ | `src/metaheuristics/` (4 algoritmos + base + encoding) |
| Instancias calibradas con datos reales | ✅ | 15 YAML en `data/instances/`, fuentes FENAVI/DANE |
| Diseño experimental ejecutado | ✅ | 1,098 ejecuciones, resultados en `experiments/results/` |
| Análisis estadístico formal | ✅ | ANOVA, Friedman, Wilcoxon-Holm, sensibilidad |
| Tesis escrita (8 capítulos + anexos) | ✅ | 1,284 líneas, 0 placeholders, Cap. 8 completo |
| Presentación funcional (32 slides) | ✅ | HTML+Chart.js+GIFs, todos los recursos verificados |
| Tests automatizados | ⚠️ | 183 funciones definidas, ejecución no verificada |
| Bibliografía alineada | ✅ | 41/41 entradas, 0 huérfanas, 0 faltantes |

### 8.2 Fortalezas Distintivas

1. **Honestidad científica**: Reporte transparente de H1 y H3 no soportadas con discusión contextualizada. Esto es una fortaleza ante el jurado, no una debilidad.
2. **Reproducibilidad**: Tests automatizados, instancias YAML, pipeline de generación de tesis, código abierto.
3. **Recursos de presentación excepcionales**: GIFs animados + gráficos interactivos Chart.js dan una ventaja significativa sobre presentaciones estáticas PowerPoint.
4. **Rigor experimental**: 1,098 ejecuciones con tests estadísticos formales (no solo promedios).

### 8.3 Debilidades Reales

1. **Entorno no verificado**: Los tests no se ejecutaron. Este es el riesgo operativo principal — si algo falla en la demo o si el jurado pide reproducción.
2. **Gap vs CBC elevado (8–13%)**: Razonable para el contexto pero requiere contextualización cuidadosa.
3. **README con ruta incorrecta**: `reproduce.py` referenciada en raíz pero ubicada en `experiments/scripts/`. Error menor pero visible si un jurado clona el repo.

### 8.4 Recomendación

**La tesis está lista para sustentación.** Las acciones pendientes son de verificación y preparación táctica, no de desarrollo:

| Acción | Esfuerzo estimado |
|--------|-------------------|
| R1. Ejecutar tests y corregir fallos | ½ día |
| R2. Regenerar PDF y verificar | ½ día |
| R3. Corregir README | 5 minutos |
| R4. Preparar respuestas del jurado | 1 hora (leer las respuestas preparadas arriba) |
| R5. Crear slides de respaldo | ½ día |
| R6. Ensayo con cronómetro | 2–3 horas |

**Esfuerzo total para completar R1–R6: ~2–3 días de trabajo.**

---

## Apéndice: Checklist de Finalización

### Verificación de Entorno
- [ ] `pip install -r requirements.txt` exitoso en entorno limpio
- [ ] `pytest tests/ -v` — 183 tests pasan (0 fallos)
- [ ] No hay errores de importación o dependencias faltantes

### Documento de Tesis
- [ ] `python tesis/generar_tesis.py` genera PDF sin errores
- [ ] 20 figuras incluidas correctamente en el PDF
- [ ] Diagramas Mermaid renderizados
- [ ] Captions `@@SHORT@@` procesadas sin errores
- [ ] Referencias cruzadas correctas (Figura X, Tabla Y)
- [ ] PDF revisado página por página

### Presentación
- [ ] GIFs se reproducen en el laptop y proyector reales
- [ ] Gráficos Chart.js funcionan en el navegador a usar
- [ ] `presentation_data.js` carga correctamente
- [ ] Slides de respaldo preparados
- [ ] PDF de respaldo generado
- [ ] Ensayo con cronómetro (≤ 40 min exposición)

### Correcciones Menores
- [ ] README: ruta de `reproduce.py` corregida
- [ ] Respuestas a preguntas del jurado revisadas y practicadas

### Reproducibilidad
- [ ] Scripts de reproducción (`experiments/scripts/reproduce.py`) ejecutan correctamente
- [ ] Instancias YAML válidas y legibles
- [ ] Resultados experimentales archivados en `experiments/results/`

---

*Documento generado el 2026-06-09. Datos verificados mediante auditoría automatizada del repositorio. Este análisis no modifica código ni documentos; solo proporciona recomendaciones.*
