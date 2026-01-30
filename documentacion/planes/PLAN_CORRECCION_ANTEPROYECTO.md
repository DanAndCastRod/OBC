# Plan de Implementación: Corrección y Ampliación Bibliográfica

**Objetivo Principal:** Asegurar la solidez académica del anteproyecto mediante la corrección de datos clave y la ampliación del soporte bibliográfico a **mínimo 25 referencias validadas**.

## 1. Diagnóstico Actual
- **Citas en Texto:** ~18 referencias únicas identificadas en `anteproyecto_dlbp_coproductos.md`.
- **Referencias Disponibles:** El archivo `referencias_dlbp.bib` contiene **~40 entradas**, incluyendo un bloque de "NUEVAS REFERENCIAS" (Enero 2026) que **aún no se han citado en el texto**.
- **Brecha:** Tenemos las referencias necesarias en la base de datos (.bib) pero no están integradas en la narrativa del documento.

## 2. Estrategia de Ejecución

### Fase 1: Corrección de Precisión (Micro-cirugía)
Corregir los datos específicos de la fuente *Solano-Blanco et al. (2022)* para reflejar la realidad del paper validado.

- **Acción:** Editar la sección "Resumen Ejecutivo" y "Justificación".
- **Cambio:**
    - *Antes:* "reducciones de costos del 8.6%"
    - *Ahora:* "mejoras en la utilidad (profit) entre 7% y 57% y reducción de costos de inventario entre 30% y 60%".

### Fase 2: Ampliación del Estado del Arte (Inyección de Referencias)
Para llegar a >25 citas de manera orgánica, redactaremos **3 nuevos párrafos** en la sección "4. Marco de Referencia" que agrupen y discutan las referencias nuevas ya disponibles en el `.bib`.

#### Grupo A: Incertidumbre y Estocasticidad (Sección 4.1)
*Objetivo: Citar papers nuevos sobre DLBP estocástico.*
- **Referencias a integrar:**
    - `Hu_2023` (Hyper-heuristic for stochastic DLBP)
    - `Liu_2021` (Robust optimization)
    - `Fang_2025` (Dynamic optimization)
    - `Tian_2023` (Hybrid evolutionary for stochastic)
    - `Liu_2019` (Ambiguous task times)
- **Narrativa:** Discutir cómo la literatura reciente ha migrado de modelos deterministas a modelos robustos que manejan tiempos inciertos, vital para el contexto avícola.

#### Grupo B: Scheduling en Industria Alimentaria (Sección 4.4)
*Objetivo: Reforzar el vacío de investigación con literatura de alimentos.*
- **Referencias a integrar:**
    - `Kopanos_2012` (Scheduling in food processing)
    - `Akkerman_2008` (Scheduling structure)
    - `Veghova_2016` (Traceability/Quality)
- **Narrativa:** Conectar el problema de DLBP con los problemas clásicos de scheduling en alimentos, destacando la perecibilidad y trazabilidad.

#### Grupo C: Multi-objetivo y Algoritmos Híbridos (Sección 4.2)
*Objetivo: Justificar la elección de metaheurísticas híbridas.*
- **Referencias a integrar:**
    - `Wang_2021` (Genetic Algorithm + Simulated Annealing)
    - `Saif_2014` (Pareto based ABC)
    - `Babazadeh_2018_CIE` (NSGA-II)
    - `Li_2021` (Bee algorithms)
- **Narrativa:** Evidenciar que la tendencia actual para problemas complejos (NP-hard) es el uso de híbridos y optimización multi-objetivo (costo + riesgo + ambiental).

### Fase 3: Validación Final
Ejecutar el script de conteo para certificar el cumplimiento de la meta.

- **Meta:** > 25 Citas únicas.
- **Calidad:** Todas las citas deben tener su entrada correspondiente en `referencias_dlbp.bib`.

## 3. Pasos Siguientes Inmediatos
1.  Aplicar corrección de textos (Solano-Blanco).
2.  Redactar e insertar los 3 bloques de texto nuevo en el Anteproyecto revisando que las llaves de cita `@Key` coincidan con el `.bib`.
3.  Generar PDF (opcional) o reporte de conteo final.
