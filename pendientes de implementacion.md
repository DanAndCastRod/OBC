# Pendientes de Implementación - Feedback Director (05/02/2026)

Este documento centraliza los ajustes solicitados por el director de investigación para la tesis y el anteproyecto.

## 1. Formato y Redacción
- [x] **Numeración de Ecuaciones**: Asegurar que todas las ecuaciones matemáticas tengan numeración consecutiva y referenciable en `anteproyecto_dlbp_coproductos.md` y `INFORME_FINAL_COMPLETO.md`.
- [x] **Tiempos Verbales**:
    - [x] **Resumen**: Cambiar a tiempo PASADO (lo que se hizo).
    - [x] **Metodología**: Cambiar a tiempo PRESENTE (lo que se hace/propone).
- [x] **Tablas del Estado del Arte**: Organizar y optimizar la presentación de las tablas de revisión literaria. Robustecer esta sección en el anteproyecto.

## 2. Resultados y Validación
- [x] **Comparativas**:
    - [x] Agregar tablas comparando: Modelo Exacto vs. Cada Metaheurística.
    - [x] Incluir métricas de Tiempo Computacional y Valor de Función Objetivo.
    - [x] Tabla MILP vs. Metaheurísticas insertada en **Sección 5.1.5** del cuerpo principal (no como Anexo).
- [x] **Hiperparámetros**:
    - [x] Revisar y documentar el valor de mutación del individuo genético (default: 0.15, calibrado: 0.20).
    - [x] Clarificar: Optuna calibró **cada algoritmo de forma independiente** (GA, TS, Híbrido por separado).
    - [x] Tabla expandida default vs. calibrado insertada en **Sección 4.2.2** del informe final.

## 3. Reproducibilidad y Datos
- [x] **Enlace a Datos/Código**: Enlace a GitHub (`https://github.com/DanAndCastRod/OBC`) agregado en `INFORME_FINAL_COMPLETO.md` (Anexo A, Anexo B) y `anteproyecto_dlbp_coproductos.md` (Sección 8.1).
- [x] **Documentación Simulador**: Sección 4.1.4 agregada en `INFORME_FINAL_COMPLETO.md` documentando el generador de instancias (algoritmo, parámetros, reproducibilidad, comando de ejecución).

## 4. Archivos Impactados ✅
- `anteproyecto_dlbp_coproductos.md` — Enlace GitHub en Sección 8.1
- `docs/tesis/INFORME_FINAL_COMPLETO.md` — Sección 4.1.4, Anexo A, Anexo B, Sección 4.2.2, Sección 5.1.5
- `docs/tesis/cap6_resultados.md` — Sección 6.2.1, 6.2.3
- `docs/presentacion/sustentacion_dlbp.html` — Pendiente de revisión



## 5. Integración Anteproyecto - Informe Final
- [x] **Validación de Consistencia**: Asegurar que la formulación matemática detallada en `anteproyecto_dlbp_coproductos.md` esté completa y correctamente reflejada en el Capítulo 2 de `docs/tesis/INFORME_FINAL_COMPLETO.md`.
- [x] **Trazabilidad**: Verificar que los objetivos planteados en el anteproyecto se aborden explícitamente en las conclusiones del informe final.

## 6. Robustecimiento Estado del Arte
- [x] **Protocolo de Búsqueda**: Ejecutar el protocolo definido en `GEMINI.md` (Queries Q1-Q4) para identificar literatura reciente (2024-2026).
- [x] **Refinamiento de Tablas**:
    - [x] Estandarizar columnas en ambos documentos.
    - [x] Agregar análisis crítico de brechas (gaps) cubiertas por este trabajo.
- [x] **Gestión Bibliográfica**:
    - [x] Actualizar `referencias_dlbp.bib` con nuevos hallazgos (Tan 2026, Wang 2026, Tahraoui 2025).
    - [x] Validar citaciones usando el script de consistencia.
- [x] **Redacción**:
    - [x] Incluir sección "Tendencias Emergentes 2025-2026" en `anteproyecto_dlbp_coproductos.md`.

## 7. Sincronización Informe Final ✅
- [x] **Sincronización Informe Final**:
    - [x] Copiada sección "Tendencias Emergentes" como Sección 1.3.4 en `INFORME_FINAL_COMPLETO.md`.
    - [x] Tabla de brechas (Tabla 1.1) actualizada con Tan2026 y Tahraoui2025.

## 8. Declaración Uso de IA ✅
- [x] Página de declaración insertada después del índice en `INFORME_FINAL_COMPLETO.md`.
- Herramientas declaradas: **Google Gemini Pro 3**, **Anthropic Claude Opus 4.5** y **Claude Opus 4.6**.

> **Nota:** La plantilla de ejemplo original (basada en ChatGPT/DeepL) fue adaptada para este proyecto usando las herramientas reales: Gemini Pro 3 y Claude Opus 4.5/4.6.