# Plan Maestro de Implementación del Proyecto DLBP Avícola

**Versión:** 1.1 (Desglosada)
**Fecha:** 14 de Enero de 2026
**Autor:** Daniel Castañeda
**Estado:** En curso

---

## 📋 Resumen Ejecutivo
Este plan maestro organiza la ejecución del proyecto de maestría en 4 fases estratégicas. Cada fase cuenta con su propio documento de planificación detallada.

**Objetivo Central:** Desarrollar un modelo de optimización para el balanceo de líneas de desensamble (DLBP) avícola usando metaheurísticas.

---

## 🏆 Entregables Finales de la Investigación (The "Definition of Done")

El proyecto solo se considera finalizado cuando se completan estos 4 elementos:

1.  **📘 Documento de Tesis:** Manuscrito académico completo (~80-100 págs.) cumpliendo normas APA/Institucionales.
2.  **📄 Artículo Científico (Paper):** Artículo en inglés (~10-15 págs.) listo para someter a revista Q2/Q3 o congreso internacional (ej. GECCO, CEC).
3.  **💻 Producto Tecnológico:** Repositorio de código documentado, limpio y reproducible.
4.  **🗣️ Sustentación:** Presentación de defensa y aprobación por jurados.

---

## 🗂️ Índice de Fases de Implementación

Haga clic en cada fase para ver el detalle técnico, actividades y entregables específicos.

| Fase | Mes | Track Técnico (Desarrollo) | Track Académico (Escritura) | Detalle |
| :--- | :--- | :--- | :--- | :--- |
| **0** | 0 | Validación Bibliográfica | Corrección Anteproyecto | [✅ Completado](../CHECKPOINT_01_ANTEPROYECTO_APROBADO.md) |
| **1** | 1-2 | Modelado Matemático (MILP) | Redacción Cap. "Definición del Problema" y Formulación | [✅ Completado](FASE_1_MODELADO.md) |
| **2** | 3-4 | Codificación Metaheurísticas | Redacción Cap. "Metodología de Solución" (Algoritmos) | [✅ Completado](FASE_2_ALGORITMOS.md) |
| **3** | 5 | Generación de Datos y Tuning | Redacción Cap. "Diseño Experimental" | [✅ Completado](FASE_3_DATOS.md) |
| **4** | 6 | Ejecución de Experimentos | Redacción Cap. "Resultados" y **Artículo (Paper)** | [✅ Completado](FASE_4_EXPERIMENTACION.md) |

---

## 🛠️ Infraestructura Transversal

### Stack Tecnológico
*   **Lenguaje:** Python 3.10+
*   **Core:** `numpy`, `pandas`, `deap` (GA), `matplotlib`.
*   **Optimización:** `irace` (tuning), `scipy.stats`.

### Estándares de Proyecto
1.  **Docs-as-Code:** Toda documentación en Markdown + Pandoc.
2.  **Bibliografía:** Archivo único `referencias_dlbp.bib`.
3.  **Control de Versiones:** Estructura de commits semánticos.

---

## 📅 Hitos Críticos

1.  **Hito 1 (Fin Mes 2):** Modelo matemático (MILP) validado en papel y script pequeño.
2.  **Hito 2 (Fin Mes 4):** Metaheurísticas (GA, TS, Híbrido) implementadas y corriendo.
3.  **Hito 3 (Fin Mes 6):** Experimento final ejecutado y resultados estadísticos listos.
