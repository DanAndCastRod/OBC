A continuación encontrarás un plan de investigación paso a paso, estructurado según los ítems que indicas, para abordar el problema de optimización del balanceo de carcasa en la industria avícola. El lenguaje es formal e investigativo, y cada sección incluye tareas concretas.

---

## 1. Descripción de la naturaleza, dinámica e impacto del problema

1.1 **Definición del balanceo de carcasa**

* Explicar qué es el balanceo de carcasa y en qué consiste el proceso de despiece en plantas avícolas.
* Detallar los cortes típicos (pechuga, muslo, ala, vísceras, etc.) y su proporción en función del producto final.

1.2 **Dinámica del proceso productivo**

* Mapear el flujo de producción: llegada de aves, sacrificio, despiece, clasificación y empaque.
* Identificar variabilidad en materia prima (peso y tamaño de aves) y en demanda de referen­cias.

1.3 **Impacto económico y operativo**

* Cuantificar pérdidas por desbalance: sobrantes de piezas no vendibles, reasignaciones de inventario, paradas de línea.
* Evaluar costes asociados: materia prima desperdiciada, horas-hombre, reprocesos, satisfacción del cliente.
* Considerar impactos en sostenibilidad: uso de recursos (agua, energía) y generación de residuos.

---

## 2. Generación de los objetivos

**Objetivo General**
– Diseñar y validar un modelo de optimización para el balanceo de carcasa en la industria avícola con el fin de minimizar costos y pérdidas, manteniendo niveles de servicio y calidad.

**Objetivos Específicos**

1. Analizar la variabilidad de la materia prima y la demanda de cortes para parametrizar el modelo.
2. Seleccionar y formular una técnica de optimización (programación lineal estocástica, metaheurísticas, etc.).
3. Desarrollar un prototipo computacional (por ejemplo en Python/GAMS) para la resolución del modelo.
4. Validar el modelo con datos históricos y realizar análisis de sensibilidad.
5. Proponer pautas de implementación práctica en planta piloto.

---

## 3. Marco Contextual (Entorno)

3.1 **Entorno macroeconómico y sectorial**

* Describir la importancia de la avicultura en la economía local y global.
* Analizar tendencias de consumo de carne de pollo y proyecciones de demanda.

3.2 **Cadena de valor y actores clave**

* Identificar actores: granjas, mataderos, procesadoras, distribuidores y minoristas.
* Relacionar su papel en la dinámica de suministro y demanda de cortes.

3.3 **Tecnologías vigentes**

* Revisar sistemas de trazabilidad, automatización en líneas de producción y software de planificación (ERP/MES).

---

## 4. Marco Teórico (Literatura mayor a 4 años)

4.1 **Modelos clásicos de optimización**

* Programación lineal y entera aplicada a balanceo de lotes.
* Programación estocástica: manejo de incertidumbre en peso y demanda.

4.2 **Metaheurísticas y algoritmos evolutivos**

* Genéticos, enjambre de partículas, recocido simulado, etc., enfocados en combinatoria de cortes.

4.3 **Simulación y modelos híbridos**

* Simulación de eventos discretos para validar heurísticos.
* Enfoques RAG (Reinforcement Learning + Optimización).

4.4 **Identificación de vacíos de investigación**

* Comparar enfoques existentes y señalar limitaciones (escala, adaptabilidad en tiempo real, costos computacionales).

---

## 5. Antecedentes

* **Local**: estudios o tesis en universidades de la región que hayan abordado el tema (por ejemplo, proyectos en la Universidad Tecnológica de Pereira).
* **País**: trabajos de centros de investigación o boletines técnicos de asociaciones avícolas colombianas.
* **Internacional**: artículos de revistas indexadas (Journal of Food Engineering, Computers & Industrial Engineering, etc.) sobre balanceo de carcasa y optimización.
  Para cada antecedente, describir: autor, año, enfoque metodológico, hallazgos y relevancia.

---

## 6. Marco Legal (País – Colombia)

6.1 **Normativa sanitaria**

* Resoluciones INVIMA sobre procesos de sacrificio y despiece.
  6.2 **Regulaciones de inocuidad y calidad**
* Buenas Prácticas de Manufactura (BPM) en plantas avícolas.
  6.3 **Requisitos de etiquetado y trazabilidad**
* Decretos sobre registro de lote y trazabilidad de productos cárnicos.

---

## 7. Metodología

7.1 **Diseño de la propuesta**

* Enfoque cuantitativo: modelado matemático y análisis numérico.

7.2 **Definición de criterios de optimización**

* Función objetivo: minimizar costos totales (materia prima, mano de obra, reprocesos).
* Restricciones: demanda de cada referencia, capacidad de línea, pesos mínimos/máximos.

7.3 **Recopilación de datos**

* Fuentes primarias: registros de planta, bases de datos internas de producción.
* Fuentes secundarias: literatura, informes sectoriales.

7.4 **Desarrollo del modelo**

* Formulación matemática paso a paso (variables, parámetros, ecuaciones).
* Implementación en software (Python + PuLP/Gurobi, GAMS, R).

7.5 **Validación y análisis**

* Pruebas con datos históricos.
* Análisis de sensibilidad ante variaciones de peso y demanda.
* Comparación de resultados con prácticas actuales.

---

## 8. Conclusiones

* **Síntesis de hallazgos**: resumen de cómo el modelo mejora el balanceo de cortes.
* **Contribuciones**: aportes al conocimiento académico e industrial.
* **Limitaciones**: supuestos y alcance de la propuesta.
* **Recomendaciones**: líneas futuras (integración en tiempo real, IA, extensión a otras especies).

