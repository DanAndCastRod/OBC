# Anteproyecto – Balanceo de línea de desensamble (cut-up/deboning) avícola con demanda pronosticada

**Fecha:** 2025-08-04

## 1. Introducción
Contextualizar la industria avícola y la etapa de despiece/cut-up. Señalar la variabilidad de rendimientos y la necesidad de alinear el mix de cortes con la demanda.

## 2. Planteamiento del problema
- **Problema central:** Desbalance de cargas y desviación del mix objetivo bajo incertidumbre de demanda y rendimientos.
- **Pregunta de investigación (ejemplo):** ¿En qué medida un modelo [estocástico/robusto/sim-opt] para el balanceo de la línea cut-up de pollo que integra pronósticos de demanda reduce la desviación del mix y mejora el throughput frente a un enfoque determinista en [Planta X, Colombia]?

## 3. Objetivos
- **General:** Diseñar y evaluar un modelo/algoritmo para balancear la línea de desensamble integrando pronósticos de demanda.
- **Específicos (ejemplo):**
  1) Formular el modelo (MIP/estocástico/robusto).  
  2) Integrar escenarios de demanda y rendimientos (simulación/Monte Carlo).  
  3) Comparar con metaheurísticas (GA/VNS/GRASP) en desempeño y tiempo de cómputo.  
  4) Validar con datos reales o sintéticos representativos.

## 4. Marco teórico y Estado del Arte
- Line balancing (ALB/DLB): variantes (U-shaped, paralelas, buffers), criterios de desempeño.
- Aplicaciones en alimentos/cárnicos/avícola.
- Integración con demanda (pronósticos) e incertidumbre (estocástico/robusto/sim-opt).
- Metaheurísticas y exactos (escalabilidad; multiobjetivo).
> Incluir tabla comparativa y diagrama PRISMA según matrices del Excel.

## 5. Metodología
- **Diseño:** Comparativo/experimental con escenarios.
- **Datos:** Tiempos de operación, precedencias, estaciones, rendimientos de cortes; series de demanda. 
- **Modelado:** MIP/estocástico/robusto; integración de pronósticos (ARIMA/ETS/ML).
- **Solución:** Solver (CPLEX/Gurobi) y metaheurísticas (GA/VNS/GRASP).
- **Validación:** Simulación de eventos discretos y análisis de sensibilidad/robustez.
- **Métricas:** Desviación del mix, throughput, utilización, WIP, costo/kg, brecha óptima, tiempo CPU.

## 6. Delimitación del alcance
- Línea cut-up post-eviscerado; 8–12 estaciones; horizonte 4–8 semanas; demanda con modelos de pronóstico y escenarios; fuera de alcance: faenado, logística externa, ergonomía avanzada (si no hay datos).

## 7. Cronograma (alto nivel)
- Búsqueda y screening: 4–6 semanas.
- Modelado y codificación: 6–10 semanas.
- Experimentos y validación: 6–10 semanas.
- Redacción y ajustes: 4–6 semanas.

## 8. Recursos
Acceso a Scopus/IEEE/ScienceDirect, solver de optimización, ambiente de simulación, Python/R.

## 9. Resultados esperados
Reducción de desviación del mix y mejora de throughput; lineamientos de diseño/operación para planta avícola.

## 10. Referencias
Se recomienda gestionar en Zotero/Mendeley y exportar a BibTeX.
