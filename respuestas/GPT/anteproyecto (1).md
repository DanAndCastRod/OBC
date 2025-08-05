
**Titulo tentativo:**

**“Optimización del Balanceo de Línea de Desensamble de Carcasas de Pollo mediante Algoritmo Genético”**

**1. Introducción y Antecedentes**
En la industria avícola, el *despiece de pollos* se realiza en líneas de producción donde cada carcasa es desensamblada en sus cortes comerciales (pechugas, alas, muslos, etc.). La eficiencia de estas líneas – medida en throughput, utilización de mano de obra y aprovechamiento de materia prima – es vital para la rentabilidad y sostenibilidad del proceso. Un problema crítico asociado es el **Balanceo de la Línea de Desensamble**, que consiste en asignar equilibradamente las tareas de corte y limpieza a estaciones de trabajo en serie, buscando minimizar tiempos ociosos y cuellos de botella. A diferencia del ensamble (donde piezas se agregan), en el desensamble se desmonta un producto en múltiples salidas, introduciendo características únicas: tareas que pueden ser destructivas, secuencias dependientes (por ejemplo, se debe quitar primero cierta pieza antes de otra) y posibles variaciones en las carcasas (tamaños, calidad). Un balanceo deficiente ocasiona estaciones congestionadas y otras desocupadas, *reduciendo la productividad* y *aumentando costos*. Por el contrario, un balanceo óptimo eleva la utilización de cada operario, acorta el tiempo de ciclo y maximiza el aprovechamiento de cada carcasa (contribuyendo a la sostenibilidad al minimizar residuos).

**Estado del Arte:** En la última década ha emergido abundante literatura sobre el **Disassembly Line Balancing Problem (DLBP)**, motivada por las tendencias de *economía circular* y *manufactura verde*. Investigaciones previas han abordado el balanceo de líneas de desensamble en contextos como el reciclaje de electrónicos, automóviles al final de su vida útil y procesamiento cárnico. Dado que el DLBP es un problema NP-complejo, la comunidad ha explorado diversos métodos de optimización: desde modelos exactos de programación entera mixta (aplicables a instancias pequeñas) hasta **heurísticas y metaheurísticas** capaces de hallar soluciones cercanas al óptimo en problemas reales de gran escala. En particular, los **Algoritmos Genéticos (GA)** se han posicionado como uno de los enfoques más exitosos. Estudios comparativos reportan que GA supera a otras metaheurísticas clásicas como Recocido Simulado o Búsqueda Tabú en métricas de equilibrio y número de estaciones necesarias. Además, los GA permiten incorporar fácilmente múltiples objetivos (p. ej. minimizar estaciones y también el *tiempo ocioso balanceado*, o maximizar la recuperación de valor de la carcasa) mediante técnicas de optimización multiobjetivo. Por ejemplo, Liu & Wang (2017) aplicaron un GA híbrido (colonia de abejas) para balancear una línea considerando objetivos económicos y ambientales, logrando eficiencia superior a métodos previos. En el ámbito específico de **carcasas de pollo**, la literatura aún es limitada. Se documentan aplicaciones de *balanceo de líneas de procesamiento avícola* mediante estudios de tiempos y simulación, pero hay una clara *oportunidad de investigación* en aplicar algoritmos de optimización avanzada (como GA) para **mejorar cuantitativamente el balanceo en plantas avícolas**.

En resumen, optimizar el balanceo de la línea de desensamble de pollos promete beneficios sustanciales: **incrementar la productividad** (más pollos procesados por hora), **reducir costos laborales** (personal mejor distribuido) y **maximizar el aprovechamiento** de cada carcasa (menor desperdicio, mayor valor obtenido por ave). Sin embargo, no se ha encontrado hasta la fecha un estudio académico enfocado exclusivamente en este problema usando métodos metaheurísticos de optimización. Esto plantea la *pregunta de investigación* a continuación.

**2. Formulación del Problema**
**Pregunta de Investigación:** *¿Cómo se puede optimizar el balanceo de la línea de desensamble de carcasas de pollo utilizando algoritmos genéticos, de manera que se minimice el tiempo ocioso y el número de estaciones, a la vez que se maximiza el aprovechamiento de cada carcasa bajo las restricciones operativas de una planta avícola?*

Esta pregunta problematizadora busca indagar en la aplicación de un GA al caso específico de una línea de procesamiento de pollos. Se enfoca en múltiples métricas de desempeño (tiempos, estaciones, aprovechamiento) y considera las restricciones típicas: precedencias entre tareas (por ejemplo, primero separar vísceras antes de cortes finales), balance de cargas y ritmo (tiempo de ciclo objetivo impuesto por la demanda).

**3. Justificación**
La justificación de este estudio es **técnica, económica y ambiental**. Desde el punto de vista técnico-científico, la investigación llenará un vacío al aplicar formalmente técnicas de inteligencia computacional (GA) al balanceo de líneas en la industria alimentaria, extendiendo conocimientos mayormente probados en manufactura discreta hacia un sector diferente. Se espera generar un *modelo de optimización* que pueda ser reutilizable para distintas plantas avícolas, contribuyendo al cuerpo de conocimiento del *Operations Research* aplicado a sistemas agroindustriales.

En términos económicos, incluso pequeñas mejoras en la eficiencia de la línea de despiece pueden traducirse en ahorros considerables y mayor rendimiento de producción. Por ejemplo, optimizar la asignación de tareas podría reducir la necesidad de 1–2 operarios por turno o incrementar el ritmo sin inversión en maquinaria adicional. Para la empresa, esto significa **reducción de costos operativos y aumento de ganancias**, mejorando su competitividad. Asimismo, un balanceo óptimo conlleva aprovechar mejor cada carcasa: es decir, sacar todas las piezas vendibles de cada pollo con el menor residuo posible, lo que incrementa el ingreso por ave procesada.

Desde la perspectiva ambiental y de sostenibilidad, el balanceo eficiente minimiza desperdicios y aprovecha al máximo la biomasa animal procesada, alineándose con prácticas de *producción más limpia*. Una línea mal balanceada podría generar “cuellos de botella” que obliguen a ralentizar el proceso, aumentando tiempos de espera y posibilitando la descomposición parcial o merma de producto (especialmente en entornos sin refrigeración inmediata), lo cual supone pérdidas de alimento. Optimizar el proceso evita tales pérdidas, contribuyendo a la seguridad alimentaria y reduciendo desechos orgánicos. Además, un proceso más corto por lote implica menor consumo energético por unidad producida (eficiencia energética). En conjunto, estos factores hacen pertinente y valiosa la investigación propuesta, tanto para mejorar la **sustentabilidad** del proceso avícola como para ofrecer un caso de éxito de aplicación de métodos avanzados de optimización en industrias tradicionales.

**4. Objetivos de la Investigación**

* **Objetivo General:** Desarrollar y validar un **método de optimización basado en Algoritmo Genético** para el balanceo de la línea de desensamble de carcasas de pollo, capaz de **minimizar el número de estaciones y el tiempo ocioso** en la línea, *maximizando simultáneamente el aprovechamiento de las carcasas*, bajo las restricciones operativas y secuenciales propias del proceso avícola.

* **Objetivos Específicos:**

  1. **Modelar matemáticamente** el proceso de despiece de pollos como un problema de balanceo de línea de desensamble, definiendo las tareas elementales, sus tiempos promedio, precedencias (e.g., qué cortes deben realizarse antes/depués) y demás restricciones (capacidades de estación, ergonomía, etc.).
  2. **Diseñar e implementar** un Algoritmo Genético (en software) adaptado a este modelo, incluyendo una codificación apropiada de soluciones (asignación de tareas a estaciones), operadores genéticos personalizados (cruce y mutación factibles respetando precedencias) y criterios de aptitud que ponderen tanto la minimización de estaciones/ocio como la maximización del rendimiento de producto.
  3. **Experimentar y optimizar parámetros** del GA (tamaño de población, probabilidad de mutación/cruce, etc.) mediante pruebas con datos reales o simulados de una planta procesadora de pollos, buscando ajustar el algoritmo para obtener soluciones de alta calidad consistentemente.
  4. **Comparar el desempeño** de la solución propuesta con métodos actuales: realizar comparativas contra (a) la situación real inicial de la línea (sin optimización), (b) algún método heurístico tradicional de balanceo (p. ej. “Ranked Positional Weight” adaptado) y (c) potencialmente otras metaheurísticas sencillas (p. ej. Recocido Simulado), para cuantificar las mejoras alcanzadas por el GA en métricas clave como eficiencia de balanceo, throughput de la línea, costo laboral y aprovechamiento porcentual de la carcasa.
  5. **Analizar la sensibilidad y robustez** del modelo GA ante variaciones en los datos de entrada: por ejemplo, cambios en la velocidad de la línea (tiempo de ciclo impuesto), diferentes tamaños de ave, o incluso escenarios multi-modelo (pollos de distinto peso o cortes demandados). Esto permitirá evaluar si el método es aplicable de forma general y adaptar el modelo a futuras expansiones (p. ej. incluir incertidumbre en tiempos o tasas de falla de equipos).
  6. **Formular recomendaciones operativas** para la planta avícola en estudio (y generalizables al sector), basadas en los resultados del modelo optimizado: número óptimo de estaciones y su configuración de tareas, posibles redistribuciones de personal, identificando también tareas cuello de botella donde enfocar mejoras (herramental, capacitación, etc.). Asimismo, cuantificar el impacto esperado: porcentajes de mejora en eficiencia, ahorro anual en costos, incremento de producción, etc., proporcionando un caso de negocio sólido para implementar las recomendaciones.

**5. Metodología y Alcance (Resumen)**
*(Nota: Este apartado es adicional para mayor claridad, aunque no se solicitó explícitamente.)*

Se adoptará una metodología cuantitativa con enfoque de *Optimización Computacional*. Inicialmente se recabarán datos detallados de la línea de proceso actual en una planta de beneficio de pollos (tiempos elementales de cada corte, secuencia tecnológica, número de operarios, etc.). Con ello se construirá el **modelo de balanceo**. Luego se codificará el Algoritmo Genético en una plataforma adecuada (como Python o MATLAB), integrando las restricciones del modelo. Se validará el algoritmo con problemas de prueba (por ejemplo, instancias pequeñas donde se puede verificar el óptimo) y posteriormente se aplicará a los datos reales. Se empleará *análisis experimental* para afinar parámetros y se documentarán los resultados comparativos. El alcance del estudio abarca hasta la generación de un plan óptimo de balanceo; la implementación física en planta queda fuera de alcance inmediato, pero los hallazgos servirán como base para pruebas piloto industriales. La investigación se circunscribe a **líneas de despiece primario de pollo**, pero la metodología podría extenderse a otros productos cárnicos (p. ej. pavo) con ajustes menores.

**6. Resultados Esperados**
Se espera obtener un modelo optimizado que **reduzca el número de estaciones** necesarias (posiblemente combinando tareas en estaciones compartidas) sin superar el tiempo de ciclo requerido por la producción. Asimismo, se espera una **mejora en la eficiencia de balanceo** (medida clásica: índice de balance o porcentaje de tiempo utilizado por estación) por encima del 90%. Esto implicaría menores tiempos muertos y un flujo más continuo de trabajo. En términos de productividad, la línea podría procesar más pollos por hora que antes, o alternativamente reducir horas extras/laborales manteniendo la misma producción. Adicionalmente, se prevé un **incremento en el rendimiento** por carcasa: al estar las tareas balanceadas, es menos probable que partes valiosas queden sin extraer por falta de tiempo; cada carcasa debería rendir la cantidad esperada de cortes (mejor *yield*). Todos estos mejoramientos se traducirían en **beneficios económicos** (costos unitarios más bajos, mayor ingreso por ave) y **ambientales** (menos desperdicio, menor consumo energético por unidad).

En conclusión, la investigación proporcionará una solución óptima *teórico-práctica* al problema de balanceo en el contexto avícola, cerrando la brecha entre la literatura de optimización de desensamble y la aplicación real en plantas de procesamiento de alimentos. Esto sentará bases para futuras implementaciones de **tecnologías inteligentes** (p. ej. líneas de despiece automatizadas con robot colaborativos) en el sector, ya que contar con un balanceo optimizado es un paso previo necesario para automatizar tareas de forma eficaz.

**7. Diagrama de Relaciones (Mermaid)**
A continuación, se incluye un diagrama conceptual que ilustra las relaciones entre los temas clave identificados en esta investigación, usando sintaxis Mermaid:

```mermaid
graph LR  
    A[Balanceo de Línea de Desensamble (DLBP)] --> B(Optimización Metaheurística)  
    A --> C(Desensamble de Carcasas de Pollo)  
    A --> D(Sostenibilidad y Circularidad)  
    B --> B1{{Algoritmo Genético (GA)}}  
    B --> B2(Recocido Simulado, Búsqueda Tabú, etc.)  
    B --> B3(Metaheurísticos Naturales: ACO, PSO, Bees...)  
    B3 --> B31[Colonia de Hormigas (ACO)]  
    B3 --> B32[Enjambre de Partículas (PSO)]  
    B3 --> B33[Algoritmo de Abejas, MBO, etc.]  
    C --> C1((Cortes y Tareas de Despiece))  
    C --> C2((Precedencias de Corte))  
    C --> C3((Estaciones y Operarios))  
    D --> D1[Maximizar Aprovechamiento]  
    D --> D2[Minimizar Residuos]  
    D --> D3[Menor Energía por Ave]  
    A --> E(Ensamble vs Desensamble)  
    E --> E1[Similitudes]  
    E --> E2[Diferencias (AND/OR, Destructivo...)]  
    A -.-> F((Robots y Autonomía))  
    D -.-> F  
    B -.-> F  
```

*Figura 1.* Mapa de relaciones entre los temas de investigación: el balanceo de línea de desensamble (centro) conecta con la optimización metaheurística (algoritmos), la aplicación específica a carcasas de pollo (dominio del problema) y la sostenibilidad (objetivos de optimización). También se relaciona con el concepto de líneas de ensamble (para contrastar características) y apunta hacia la automatización futura mediante robots (donde un balanceo óptimo es fundamental para su eficiencia).

Este diagrama evidencia cómo **el método propuesto (GA)** se ubica en el núcleo de la optimización metaheurística (B1), y cómo su aplicación al caso de despiece de pollo (C) contribuye a fines de sostenibilidad (D) al mejorar el uso de recursos. Asimismo, muestra las conexiones con otros metaheurísticos explorados (B2, B3) y con la posibilidad de integrar tecnología robótica en el proceso (F), lo cual puede verse facilitado por los resultados de esta investigación.

**8. Conclusión (Propuesta de Valor)**
La nueva investigación aquí propuesta – centrada en la aplicación de algoritmos genéticos al balanceo de líneas de desensamble de carcasas de pollo – se basa en evidencias sólidas del estado del arte y responde a necesidades prácticas de la industria avícola. Esperamos que sus resultados demuestren **la viabilidad y superioridad de los GA** para optimizar este tipo de sistemas productivos, proporcionando tanto un avance académico en la literatura de *disassembly line balancing* como una solución de impacto directo en la eficiencia industrial y la sostenibilidad alimentaria. En última instancia, el éxito de este proyecto podría sentar precedentes para que más plantas procesadoras de alimentos adopten herramientas de optimización inteligente en sus operaciones, mejorando la productividad y reduciendo desperdicios en beneficio de toda la cadena alimentaria.



