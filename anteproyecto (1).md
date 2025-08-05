# Anteproyecto de Investigación

## Título

**Optimización del Balanceo de Línea de Desensamble de Carcasas de Pollo
mediante Algoritmo Genético**

## 1. Introducción

El equilibrio eficiente de líneas de desensamble en plantas avícolas es
crucial para maximizar la productividad y minimizar desperdicios. A
diferencia del ensamble, el DLBP (Disassembly Line Balancing Problem)
enfrenta retos de **secuencias lógicas de corte**, **variabilidad
anatómica** y **condiciones destructivas** de las piezas[@Ozceylan2019].
Aunque existen estudios de simulación en despiece de
pollo[@Pisuchpen2016], faltan enfoques de **optimización
metaheurística** aplicados específicamente a carcasas avícolas.

## 2. Estado del Arte

Investigaciones relevantes incluyen: - **Revisiones DLBP**: Ozceylan et
al. (2019) describen enfoques y tendencias, destacando metaheurísticos
como GA, ACO y PSO[@Ozceylan2019]. - **Metaheurísticos Avanzados**: Mete
et al. (2023) comparan GA vs SA bajo tiempos estocásticos, mostrando la
superioridad de GA[@Mete2023]. Liu & Wang (2017) integran criterios
ambientales con D-ABC multiobjetivo[@Liu2017]. - **Aplicaciones
Cárnicas**: Pisuchpen & Ongkunaruk (2016) emplean simulación Arena para
una planta de pollo, con mejora de eficiencia y ahorro[@Pisuchpen2016].

La bibliografía revela la eficacia de GA y la necesidad de adaptarlo al
contexto avícola para aprovechar su **flexibilidad** y **desempeño
robusto**.

## 3. Pregunta de Investigación

> **¿Cómo optimizar el balanceo de la línea de desensamble de carcasas
> de pollo utilizando Algoritmos Genéticos para minimizar estaciones y
> tiempo ocioso, maximizar el aprovechamiento de la carcasa y garantizar
> robustez ante variaciones anatómicas?**

## 4. Justificación

- **Científica**: Amplía la aplicación de GA a un sector poco explorado,
  contribuyendo al cuerpo de conocimiento del DLBP.
- **Económica**: Mejora la productividad de planta, reduce costos
  laborales y aumenta el rendimiento de producto.
- **Ambiental**: Disminuye desperdicios orgánicos y consumo energético,
  favoreciendo prácticas de economía circular[@Yang2024].

## 5. Objetivos

### 5.1 Objetivo General

Desarrollar y validar un Algoritmo Genético para el balanceo óptimo de
la línea de desensamble de carcasas de pollo.

### 5.2 Objetivos Específicos

1.  **Modelar** el proceso de despiece definiedo tareas, tiempos y
    precedencias.
2.  **Implementar** el GA con codificación y operadores adaptados a
    restricciones avícolas.
3.  **Parametrizar** el algoritmo mediante diseño experimental.
4.  **Comparar** resultados contra heurísticos clásicos y estado actual.
5.  **Evaluar** robustez ante variaciones en datos y escenarios
    multi-modelo.
6.  **Recomendar** configuraciones operativas basadas en resultados
    cuantitativos.

## 6. Metodología

1.  **Recolección de datos**: Tiempos elementales de cada corte en
    planta real.
2.  **Modelado matemático**: Formulación del DLBP con precedencias
    AND/OR y restricciones de ciclo.
3.  **Desarrollo de GA**:
    - Codificación: Representación cromosómica de asignación de tareas\
    - Operadores: Cruce de un punto, mutación por intercambio,
      reparación de precedencias\
    - Función de aptitud: Minimiza estaciones y tiempo ocioso, maximiza
      aprovechamiento\
4.  **Validación**: Pruebas en instancias de referencia y casos reales\
5.  **Optimización de parámetros**: Análisis de sensibilidad de
    población, tasas de cruce/mutación\
6.  **Comparativa**: GA vs RPW, Recocido Simulado y línea actual\
7.  **Análisis de robustez**: Variaciones en tiempo de ciclo, tamaño de
    aves, demandas de corte\
8.  **Elaboración de recomendaciones**: Plan de implementación operativo

## 7. Cronograma Resumido

  Fase                        Duración
  --------------------------- -----------
  Recolección de datos        1 mes
  Modelado y codificación     1.5 meses
  Pruebas y parametrización   2 meses
  Comparativas y análisis     1.5 meses
  Redacción y difusión        1 mes

## 8. Resultados Esperados

- **≤ 8 estaciones** vs línea actual (10--12)\
- **Uso de tiempo ≥ 90%** por estación\
- **Aprovechamiento de carcasa ≥ 98%**\
- Evidencia cuantitativa de ahorro de costos (+15%) y reducción de
  desperdicios

## 9. Limitaciones

- Datos específicos de la planta; resultados pueden variar en otras
  instalaciones\
- No se incorpora automatización robótica en primera fase

## 10. Referencias

Consulte `references.bib` para las citas completas
([@Liu2017; @Mete2023; @Yang2024; @Ozceylan2019]).
