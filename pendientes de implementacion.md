# Pendientes de Implementación - Feedback Director (05/02/2026)

Este documento centraliza los ajustes solicitados por el director de investigación para la tesis y el anteproyecto.

## 1. Formato y Redacción
- [ ] **Numeración de Ecuaciones**: Asegurar que todas las ecuaciones matemáticas tengan numeración consecutiva y referenciable en `anteproyecto_dlbp_coproductos.md` y `INFORME_FINAL_COMPLETO.md`.
- [ ] **Tiempos Verbales**:
    - [ ] **Resumen**: Cambiar a tiempo PASADO (lo que se hizo).
    - [ ] **Metodología**: Cambiar a tiempo PRESENTE (lo que se hace/propone).
- [ ] **Tablas del Estado del Arte**: Organizar y optimizar la presentación de las tablas de revisión literaria. Robustecer esta sección en el anteproyecto.

## 2. Resultados y Validación
- [ ] **Comparativas**:
    - [ ] Agregar tablas comparando: Modelo Exacto vs. Cada Metaheurística.
    - [ ] Incluir métricas de Tiempo Computacional y Valor de Función Objetivo.
- [ ] **Hiperparámetros**:
    - [ ] Revisar y documentar el valor de mutación del individuo genético.
    - [ ] Clarificar si la refinación con Optuna fue por modelo individual o para el híbrido.

## 3. Reproducibilidad y Datos
- [ ] **Enlace a Datos/Código**: Colocar enlace directo al GitHub o al repositorio de datos generados para la comunidad académica.
- [ ] **Documentación Simulador**: Documentar el simulador de instancias utilizado para generar los datos sintéticos.

## 4. Archivos a Impactar
- `anteproyecto_dlbp_coproductos.md`
- `docs/tesis/INFORME_FINAL_COMPLETO.md`
- `docs/presentacion/sustentacion_dlbp.html` (revisar si aplica)

## 5. Integración Anteproyecto - Informe Final
- [ ] **Validación de Consistencia**: Asegurar que la formulación matemática detallada en `anteproyecto_dlbp_coproductos.md` esté completa y correctamente reflejada en el Capítulo 2 de `docs/tesis/INFORME_FINAL_COMPLETO.md`.
- [ ] **Trazabilidad**: Verificar que los objetivos planteados en el anteproyecto se aborden explícitamente en las conclusiones del informe final.

## 6. Robustecimiento Estado del Arte
- [ ] **Protocolo de Búsqueda**: Ejecutar el protocolo definido en `GEMINI.md` (Queries Q1-Q4) para identificar literatura reciente (2024-2026).
- [ ] **Refinamiento de Tablas**:
    - [ ] Estandarizar columnas en ambos documentos.
    - [ ] Agregar análisis crítico de brechas (gaps) cubiertas por este trabajo.
- [ ] **Gestión Bibliográfica**:
    - [ ] Actualizar `referencias_dlbp.bib` con nuevos hallazgos.
    - [ ] Validar citaciones usando el script de consistencia.
