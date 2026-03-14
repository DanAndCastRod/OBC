---
bibliography: "../referencias_dlbp.bib"
csl: "../apa.csl"
title: "Anteproyecto: Modelo DLBP para Coproductos con Metaheurísticas en la Industria Avícola"
date: "2025-11-25"
author: "Daniel Castañeda"
institution: "Universidad Tecnológica de Pereira"
program: "Maestría en Investigación de Operaciones y Estadística"
start_date: "15 de septiembre de 2025"
description: "Desarrollo de un modelo de balanceo de línea de desensamble (DLBP) para optimizar el aprovechamiento de coproductos en la industria avícola mediante técnicas metaheurísticas"
pdf-engine: xelatex
filters:
  - pandoc-mermaid
---

# Anteproyecto: Modelo DLBP para Coproductos con Metaheurísticas en la Industria Avícola

## Información del Proyecto

**Estudiante**: Daniel Castañeda  
**Programa**: Maestría en Investigación de Operaciones y Estadística  
**Institución**: Universidad Tecnológica de Pereira  
**Fecha de inicio propuesta**: 15 de septiembre de 2025  
**Fecha de elaboración del anteproyecto**: 25 de noviembre de 2025  

---

## Resumen Ejecutivo

Este anteproyecto propone el desarrollo de un **modelo de optimización para el Problema de Balanceo de Líneas de Desensamble (DLBP)** aplicado a la industria avícola colombiana. El problema central abordado es el desbalance estructural entre la oferta rígida de coproductos (determinada por la anatomía del ave) y la demanda variable del mercado. Utilizando un enfoque **cuantitativo y experimental (simulación)**, se implementarán y compararán técnicas **metaheurísticas** (Algoritmos Genéticos, Búsqueda Tabú y algoritmos híbridos) para maximizar la rentabilidad del proceso de despiece. La investigación se fundamenta en evidencia empírica local, como el estudio de Solano-Blanco et al. en Santa Marta, que demostró reducciones de costos del **8.6%** mediante planificación integrada [@SolanoBlanco2022].

---

## 1. Introducción

### 1.1. El Desafío del Balanceo de Carcasa en la Industria Avícola

La industria avícola, reconocida como un pilar económico en Colombia y a nivel mundial, enfrenta un desafío operativo fundamental conocido como el **problema de balanceo de la carcasa**. Este problema surge de la discrepancia inherente entre la oferta de coproductos, que se derivan en proporciones relativamente fijas del despiece de cada ave (carcasa), y la demanda variable y a menudo desalineada del mercado para cada uno de esos cortes (pechuga, alas, muslos, vísceras, etc.).

La industria avícola opera bajo una dinámica compleja de **"Push" (Empuje) y "Pull" (Tracción)**. Por un lado, el factor "Push" proviene de la granja: una vez que las aves alcanzan su peso de mercado, deben ser procesadas inmediatamente, generando una oferta fija de coproductos (alas, pechugas, muslos) en proporciones biológicamente determinadas. Por otro lado, el factor "Pull" es la demanda del mercado, que es estocástica, estacional y a menudo desbalanceada respecto a la oferta anatómica (alta demanda de pechuga pero baja de alas, por ejemplo).

Un plan de ventas que, por ejemplo, prioriza la comercialización de pechuga para maximizar ingresos, inevitablemente genera una sobreoferta de otros coproductos como alas y patas. Si no se gestiona adecuadamente, este excedente debe ser almacenado (incrementando costos de refrigeración), vendido a precios de liquidación o incluso desechado, ocasionando pérdidas económicas significativas y un desperdicio de recursos valiosos.

Este conflicto genera ineficiencias operativas significativas, como la acumulación de inventarios de baja rotación, la venta de productos premium a precios de liquidación, y la pérdida de oportunidades de mercado. La literatura científica, incluyendo el trabajo seminal de Becker y Scholl sobre balanceo de líneas [@BeckerScholl2006], y estudios recientes en Colombia [@SolanoBlanco2022], sugieren que la aplicación de modelos matemáticos avanzados de optimización puede mitigar estos efectos y mejorar la sostenibilidad financiera y ambiental del sector.

### 1.2. Relevancia Económica y Contexto Nacional

La relevancia económica de resolver el problema del balanceo de carcasa es crucial para la competitividad y sostenibilidad de la industria avícola colombiana. Según FENAVI [@FENAVI2024], la avicultura representa uno de los renglones pecuarios más importantes del país, con una producción anual que supera las 1.7 millones de toneladas de carne de pollo. La agroindustria avícola aporta aproximadamente 0.52% del valor agregado bruto nacional [@DANE2024].

Una gestión optimizada del balanceo de carcasa permite:

*   **Maximizar la Rentabilidad:** Asegurando que cada parte del ave se venda al mejor precio posible, transformando potenciales excedentes en oportunidades de ingreso.
*   **Mejorar la Eficiencia Operativa:** Minimizando los costos asociados al inventario, la refrigeración y la logística de productos no vendidos.
*   **Aumentar la Satisfacción del Cliente:** Garantizando la disponibilidad de la gama completa de productos que el mercado demanda.
*   **Promover la Sostenibilidad:** Reduciendo el desperdicio de alimentos y optimizando el uso de los recursos, en línea con los objetivos de sostenibilidad corporativa y ambiental.

Estudios de eficiencia en plantas colombianas han documentado pérdidas significativas debido a la gestión subóptima del balanceo. Casos documentados en la industria local, como el trabajo de optimización implementado por Pollos y Huevos Altair en Santa Marta [@AltairOptimization2019], han demostrado que la aplicación de técnicas de optimización matemática puede generar reducciones de costos del 23% en costos totales y del 64% en costos de inventario.

### 1.3 El Enfoque de Optimización: Disassembly Line Balancing Problem (DLBP)

Desde la perspectiva de la investigación de operaciones, el balanceo de carcasa se enmarca en la categoría de **Problemas de Balanceo de Líneas de Desensamble (Disassembly Line Balancing Problem - DLBP)**. A diferencia de las líneas de ensamble tradicionales, donde los componentes convergen para crear un producto final, en el desensamble un producto se descompone en múltiples componentes o coproductos [@BeckerScholl2006; @KimLee2007].

El DLBP es un problema de optimización combinatoria clasificado como **NP-hard**, lo que significa que encontrar una solución óptima se vuelve computacionalmente intratable a medida que aumenta la escala del problema [@BeckerScholl2006]. Esta complejidad computacional ha motivado el desarrollo de enfoques heurísticos y metaheurísticos para encontrar soluciones de alta calidad en tiempos de cómputo razonables.

La revisión de literatura de Güngör y Gupta [@KimLee2007] identifica que, aunque existe una extensa investigación en DLBP aplicado a reciclaje de electrónicos y recuperación de materiales, hay una notable escasez de estudios que aborden el DLBP en la industria de procesamiento de alimentos, y particularmente en el sector avícola.

Este anteproyecto se centra en abordar este desafío mediante el desarrollo de un modelo DLBP avanzado, que utiliza **técnicas metaheurísticas** para optimizar el proceso de despiece en la industria avícola. El objetivo es desarrollar una herramienta de apoyo a la decisión que permita a las empresas del sector mejorar su planificación, reducir sus pérdidas y fortalecer su competitividad en un mercado cada vez más exigente.

---

## 2. Planteamiento del Problema

### 2.1. Problema Central: Desbalance y Consecuencias en la Cadena de Suministro Avícola

El problema central que aborda esta investigación es el **desbalance estructural** entre la oferta de coproductos generada por el proceso de desensamble avícola y la **demanda estocástica y heterogénea del mercado**. Este desajuste, inherente a la naturaleza del negocio, se traduce en una cascada de ineficiencias operativas y pérdidas económicas que impactan a toda la cadena de valor.

El desbalance se manifiesta en dos frentes principales:

1.  **Excedentes de Inventario (Sobreproducción):** Cuando la producción de ciertos cortes (alas, patas, vísceras) supera la demanda del mercado, las empresas se ven forzadas a incurrir en costos adicionales de almacenamiento en frío, transporte y, en el peor de los casos, vender estos productos a precios de liquidación, erosionando significativamente los márgenes de ganancia.

2.  **Faltantes de Inventario (Subproducción):** De forma simultánea, la demanda de cortes de alto valor (pechuga) puede exceder la capacidad de producción balanceada, resultando en oportunidades de venta perdidas y una potencial insatisfacción del cliente.

Esta dualidad de excedentes y faltantes evidencia una **asignación subóptima de los recursos**, donde el valor potencial de cada carcasa no se maximiza.

### 2.2. Evidencia Empírica y Brecha en la Literatura

Estudios locales validan la magnitud de este problema. En un caso de estudio realizado en una empresa avícola de Santa Marta, Colombia, Solano-Blanco et al. [@SolanoBlanco2022] demostraron que la falta de una planificación integrada genera sobrecostos operativos y violaciones de restricciones de bioseguridad. Su modelo de planificación estocástica en dos etapas logró una **reducción de costos del 8.6%**, evidenciando el potencial de la optimización matemática en este contexto específico.

De manera similar, el caso documentado de Pollos y Huevos Altair [@AltairOptimization2019] en la misma región mostró mejoras sustanciales en eficiencia operativa mediante la implementación de sistemas de optimización, con reducciones del 23% en costos totales y del 64% en costos de inventario.

Sin embargo, existe una **brecha significativa en la literatura**: aunque existen modelos de planificación agregada (como el de Solano-Blanco), hay una escasez de modelos específicos de **DLBP (Disassembly Line Balancing Problem)** que aborden el despiece operativo diario con técnicas metaheurísticas para manejar la estocasticidad de la demanda a nivel de línea de producción [@KimLee2007]. La mayoría de los estudios de DLBP se enfocan en industrias de reciclaje o remanufactura, dejando un vacío en la aplicación de estas técnicas al sector alimentario y específicamente al procesamiento avícola.

Estudios recientes sobre minimización de "giveaway" (sobrepeso) en el porcionado de aves [@AwadPoultryOptimization2023] han abordado aspectos relacionados con la eficiencia del corte, pero no integran completamente la dimensión del balanceo de coproductos con la demanda del mercado.

### 2.3. Pregunta de Investigación

**Pregunta Principal:**
¿Cómo puede un modelo de optimización DLBP, resuelto mediante técnicas metaheurísticas, minimizar las pérdidas económicas asociadas al desbalance entre la oferta de coproductos y la demanda del mercado en una planta de procesamiento avícola colombiana?

**Preguntas Secundarias:**
1. ¿Qué formulación matemática del DLBP captura adecuadamente las restricciones de precedencia, los tiempos de procesamiento y la variabilidad de la demanda en el contexto avícola?
2. ¿Qué técnicas metaheurísticas (Algoritmos Genéticos, Búsqueda Tabú, o híbridos) presentan el mejor desempeño para resolver el modelo DLBP propuesto?
3. ¿En qué magnitud se pueden reducir las pérdidas económicas asociadas al desbalance de carcasa mediante la implementación del modelo de optimización?

### 2.4. Hipótesis de Investigación

**Hipótesis Principal (H1):**
La aplicación de un modelo DLBP con metaheurísticas puede generar una reducción de al menos un 8% en las pérdidas económicas totales asociadas al desbalance de carcasa, tomando como referencia el benchmark del caso de Santa Marta [@SolanoBlanco2022].

**Hipótesis Secundarias:**
*   **H2:** Un algoritmo metaheurístico híbrido (que combine Algoritmos Genéticos y Búsqueda Tabú) superará en desempeño a cada técnica aplicada individualmente.
*   **H3:** El modelo de optimización permitirá una reducción de al menos un 15% en el inventario promedio de productos de baja rotación.

---

## 3. Justificación

Esta investigación se justifica desde múltiples dimensiones que abarcan aspectos económicos, sociales, ambientales y científicos:

### 3.1. Conveniencia y Relevancia Económica

La optimización del balanceo de carcasa tiene un impacto directo en la rentabilidad de las empresas avícolas. Como demostró el caso de Santa Marta [@SolanoBlanco2022], las mejoras en la planificación pueden traducirse en ahorros de costos cercanos al **8.6%**. En una industria de márgenes estrechos y alto volumen, este porcentaje representa una ventaja competitiva crítica y puede significar la diferencia entre la rentabilidad y las pérdidas operativas.

El sector avícola colombiano, que según FENAVI [@FENAVI2023] genera más de 600,000 empleos directos e indirectos, se beneficiaría significativamente de herramientas que mejoren su eficiencia operativa. La implementación de modelos de optimización no solo mejora la rentabilidad de las empresas individuales, sino que fortalece la competitividad del sector a nivel nacional e internacional.

### 3.2. Relevancia Social y Ambiental (Sostenibilidad)

Mejorar el equilibrio de la carcasa contribuye directamente a la sostenibilidad del sector. Al reducir el desperdicio de alimentos y optimizar el uso de recursos (energía para refrigeración de inventarios no deseados), el proyecto se alinea con los **Objetivos de Desarrollo Sostenible (ODS)**, específicamente:

*   **ODS 12 (Producción y Consumo Responsables):** Reduciendo el desperdicio de alimentos y optimizando el aprovechamiento de cada ave procesada.
*   **ODS 9 (Industria, Innovación e Infraestructura):** Mediante la aplicación de técnicas avanzadas de optimización y el desarrollo de herramientas tecnológicas para la industria.

La reducción del desperdicio de alimentos es particularmente relevante en un contexto global donde aproximadamente el 14% de los alimentos se pierde en la cadena de suministro antes de llegar al consumidor (FAO, 2023). Un mejor balanceo de la carcasa significa un proceso más sostenible, con menor huella de carbono y mejor utilización de los recursos naturales.

### 3.3. Implicaciones Prácticas

El desarrollo de una herramienta de toma de decisiones basada en metaheurísticas permitirá a los planificadores de producción pasar de decisiones basadas en la intuición ("gut feeling") y la experiencia personal a decisiones basadas en datos y modelado matemático robusto. Esto mejorará la capacidad de respuesta ante fluctuaciones del mercado y permitirá una planificación más ágil y eficiente.

La implementación de tecnologías de sensores inteligentes [@SensorsPoultry2022] y sistemas de automatización [@AutomationSystems2023] en la industria avícola está generando grandes volúmenes de datos que pueden ser aprovechados por modelos de optimización como el propuesto en este proyecto.

### 3.4. Valor Teórico y Científico

El proyecto contribuye significativamente a la literatura del **DLBP**, extendiendo los modelos clásicos deterministas [@BeckerScholl2006] hacia enfoques estocásticos que consideran la incertidumbre de la demanda, un área identificada como línea futura de investigación por Güngör y Gupta [@KimLee2007].

Adicionalmente, la comparación rigurosa de diferentes técnicas metaheurísticas (Algoritmos Genéticos, Búsqueda Tabú, y algoritmos híbridos) en el contexto específico de la industria avícola generará conocimiento valioso sobre la efectividad de estas técnicas en problemas del mundo real con características particulares (perecibilidad, estocasticidad, restricciones sanitarias).

### 3.5. Utilidad Metodológica

Se validará la efectividad de algoritmos híbridos para resolver problemas NP-Hard en contextos industriales reales, proporcionando un marco de referencia metodológico para futuras aplicaciones en otras industrias de desensamble (reciclaje de electrónicos, desmantelamiento de vehículos, procesamiento de otros tipos de carne).

La generación de un conjunto de datos sintéticos calibrados para validación del modelo también representa una contribución metodológica, siguiendo las mejores prácticas en investigación de operaciones [@SyntheticDataChicken2025].

---

## 4. Marco Teórico y Estado del Arte

### 4.1. El Problema de Balanceo de Líneas de Desensamble (DLBP)

El **Problema de Balanceo de Líneas de Desensamble (DLBP)** es un área fundamental de la investigación de operaciones que se enfoca en la optimización de sistemas de producción donde un producto principal se descompone en varios componentes o subproductos. A diferencia de su contraparte, el Problema de Balanceo de Líneas de Ensamble (ALBP), que trata de la convergencia de partes para formar un producto, el DLBP aborda un proceso de divergencia [@BeckerScholl2006].

El objetivo del DLBP es asignar las tareas de desensamble a una secuencia de estaciones de trabajo de tal manera que se optimice una o varias métricas de desempeño, como minimizar el número de estaciones, minimizar el tiempo de ciclo, o maximizar la eficiencia de la línea, sujeto a restricciones de precedencia entre las tareas [@KimLee2007; @OptimizationAssemblyLine2019].

La revisión exhaustiva de Güngör y Gupta [@KimLee2007] identifica que el DLBP tiene aplicaciones principales en:
- Reciclaje de productos electrónicos
- Remanufactura de componentes industriales
- Procesamiento de alimentos (área con menor desarrollo)

El DLBP es computacionalmente complejo, clasificado como NP-hard [@BeckerScholl2006], lo que implica que no existen algoritmos que puedan encontrar la solución óptima en tiempo polinomial para instancias grandes del problema. Esta complejidad ha motivado el uso extensivo de heurísticas y metaheurísticas.

### 4.2. Metaheurísticas para la Optimización de Líneas de Producción

Debido a la complejidad computacional del DLBP, las **metaheurísticas** se han convertido en el enfoque predominante para resolver este tipo de problemas. Las metaheurísticas son algoritmos de optimización de alto nivel que pueden ser aplicados a una amplia gama de problemas, y que a menudo se inspiran en procesos naturales.

### 4.3. Aplicaciones del DLBP en la Industria Alimentaria y Avícola

La industria alimentaria, y en particular el sector avícola, presenta un caso de estudio natural para la aplicación de modelos DLBP. El proceso de despiece de un pollo es un claro ejemplo de un sistema de desensamble, donde la carcasa es el producto principal y los diferentes cortes (pechuga, muslos, alas, vísceras) son los coproductos.

La literatura ha comenzado a explorar estas aplicaciones de manera limitada. Awad et al. [@AwadPoultryOptimization2023] abordan el problema de la minimización del sobrepeso (*giveaway*) en el porcionado de aves, un problema directamente relacionado con la eficiencia del proceso de despiece, aunque no incorporan explícitamente el balanceo de la demanda de mercado.

Solano-Blanco et al. [@SolanoBlanco2022] abordan un problema de planificación integrada para la cadena de suministro de pollos de engorde, demostrando que la optimización matemática puede generar beneficios significativos. Sin embargo, su enfoque está en la planificación agregada (nivel táctico) más que en el balanceo operativo de la línea de desensamble.

La integración de sensores inteligentes [@SensorsPoultry2022] y sistemas de automatización [@AutomationSystems2023] en plantas de procesamiento avícola está generando oportunidades para la implementación de modelos de optimización en tiempo real, aunque la literatura en este ámbito sigue siendo escasa.

### 4.4. Vacíos de Investigación Identificados

A pesar de la extensa literatura sobre ALBP y el creciente interés en DLBP, la revisión del estado del arte revela varios vacíos de investigación que este proyecto busca abordar:

1.  **Falta de Modelos Específicos para la Industria Avícola:** Aunque existen modelos generales de DLBP, hay una escasez de modelos que capturen las características específicas y las complejidades del proceso de despiece avícola, como la variabilidad en el peso de las carcasas, las restricciones de calidad, la perecibilidad del producto, y las demandas estacionales de los coproductos.

2.  **Integración Limitada con la Planificación de la Demanda:** Muchos de los modelos existentes asumen una demanda determinista, lo cual no refleja la realidad del mercado avícola. Es necesario desarrollar modelos que integren la estocasticidad de la demanda para generar planes de producción más robustos y realistas.

3.  **Comparación Insuficiente de Metaheurísticas en Contextos Reales:** Si bien se han aplicado diversas metaheurísticas al DLBP en contextos académicos, faltan estudios comparativos rigurosos que evalúen el desempeño de diferentes algoritmos en un conjunto de instancias de problemas realistas para la industria avícola, considerando tanto la calidad de la solución como la eficiencia computacional.

4.  **Validación con Datos Reales o Sintéticos Calibrados:** Muchos de los modelos propuestos en la literatura se validan con datos sintéticos arbitrarios o instancias de problemas de pequeña escala. Existe la necesidad de validar estos modelos con datos reales o, en su defecto, con datos sintéticos que hayan sido cuidadosamente calibrados para reflejar las condiciones operativas reales de la industria.

Este proyecto de investigación se posiciona para abordar estos vacíos, con el objetivo de desarrollar una contribución significativa tanto al campo académico del DLBP como a la práctica industrial de la gestión de la producción avícola.

---

## 5. Diseño Metodológico

La metodología de esta investigación se estructura en cinco fases principales, diseñadas para abordar de manera sistemática las preguntas de investigación y validar las hipótesis planteadas.

### 5.1. Clasificación de la Investigación

*   **Enfoque:** Cuantitativo. Se basa en la medición numérica de variables (costos, tiempos, cantidades) y el análisis estadístico riguroso de resultados.
*   **Alcance:** Explicativo y Correlacional. Busca explicar la relación causal entre la optimización del balanceo mediante DLBP y la rentabilidad/eficiencia operativa.
*   **Diseño:** Experimental (Simulación). Se manipularán variables independientes (algoritmos metaheurísticos, escenarios de demanda) en un entorno controlado (*in silico*) para observar su efecto en la variable dependiente (costo total, nivel de servicio, inventario).
*   **Método de Inferencia:** Deductivo. Se parte de teorías generales de optimización y DLBP para aplicarlas a un caso específico de la industria avícola.
*   **Temporalidad:** Transversal. Los experimentos computacionales se realizarán en un corte de tiempo específico, aunque considerando escenarios de demanda que reflejan variabilidad temporal.

### 5.2. Fases de la Investigación

#### Fase 1: Formulación del Modelo Matemático (Semanas 1-8)

El primer paso consiste en desarrollar un modelo matemático de optimización para el DLBP adaptado a la industria avícola. Este modelo será la base para la implementación de los algoritmos de solución.

*   **Definición de Variables de Decisión:** Se identificarán las variables clave del problema, como la asignación de tareas de despiece a las estaciones de trabajo, el secuenciamiento de las tareas, y las cantidades de cada coproducto a procesar en cada período.
*   **Función Objetivo:** Se formulará una función objetivo que buscará maximizar la rentabilidad de la operación. Esto implicará maximizar los ingresos por la venta de coproductos y minimizar los costos de producción, inventario y penalizaciones por demanda no satisfecha.
*   **Restricciones:** Se incorporarán al modelo todas las restricciones relevantes del problema:
    *   Restricciones de precedencia entre las tareas de despiece (basadas en la anatomía del ave).
    *   Restricciones de capacidad de las estaciones de trabajo.
    *   Restricciones de tiempo de ciclo de la línea.
    *   Restricciones de balance de materiales (cantidad de coproductos generados).
    *   Restricciones de demanda estocástica del mercado.
    *   Restricciones de perecibilidad y vida útil de los productos.

#### Fase 2: Diseño e Implementación de Metaheurísticas (Semanas 9-16)

Dada la complejidad NP-hard del DLBP, se recurrirá a metaheurísticas para encontrar soluciones de alta calidad en tiempos computacionales razonables. Se explorarán e implementarán las siguientes técnicas:

*   **Algoritmo Genético (GA):** Implementación de un GA con representación permutacional de soluciones, operadores de cruce y mutación adaptados al problema de balanceo [@Sivasankaran2014].
*   **Búsqueda Tabú (TS):** Implementación de TS con estrategias de diversificación e intensificación, siguiendo las mejores prácticas documentadas en [@Suwannarongsri2007].
*   **Algoritmo Híbrido GA-TS:** Desarrollo de un algoritmo híbrido que combine la exploración global del GA con la explotación local de TS.

Para cada metaheurística se realizará:
*   Codificación adecuada de la solución.
*   Diseño de operadores de búsqueda específicos para el problema.
*   Calibración de parámetros mediante diseño experimental.

La implementación se realizará en Python, utilizando librerías de optimización estándar y frameworks de experimentación controlada.

#### Fase 3: Generación de Datos y Escenarios de Prueba (Semanas 17-20)

Para validar el modelo y los algoritmos propuestos, se generará un conjunto de instancias de prueba que representen de manera realista las condiciones de la industria avícola colombiana.

*   **Datos Sintéticos Calibrados:** Se utilizarán datos sintéticos para las pruebas, siguiendo las mejores prácticas en generación de datos sintéticos [@SyntheticDataChicken2025]. Estos datos serán calibrados utilizando:
    *   Rendimientos estándar de carcasa publicados en la literatura.
    *   Costos de producción del sector avícola colombiano.
    *   Patrones de demanda históricos (cuando estén disponibles) o generados mediante distribuciones probabilísticas.
    *   Parámetros de la industria local (caso Santa Marta como referencia).
*   **Generación de Instancias:** Se crearán múltiples instancias del problema con diferentes tamaños (número de estaciones, número de cortes) y niveles de complejidad (variabilidad de demanda, estacionalidad) para evaluar la escalabilidad y robustez de los algoritmos.

#### Fase 4: Diseño Experimental y Análisis de Resultados (Semanas 21-24)

Se llevará a cabo un diseño experimental riguroso para evaluar el desempeño de las metaheurísticas propuestas y validar las hipótesis de la investigación.

*   **Métricas de Desempeño:** Se definirán métricas cuantitativas para evaluar:
    *   Rentabilidad total (función objetivo).
    *   Nivel de servicio al cliente (% de demanda satisfecha).
    *   Niveles de inventario promedio.
    *   Tiempo computacional.
    *   Gap de optimalidad (cuando sea posible comparar con soluciones exactas en instancias pequeñas).
*   **Análisis Comparativo:** Se comparará el desempeño de:
    *   GA vs. TS vs. Híbrido.
    *   Modelo optimizado vs. Métodos heurísticos simples (baseline).
*   **Análisis Estadístico:** Se utilizarán herramientas estadísticas (ANOVA, pruebas t, pruebas no paramétricas) para analizar los resultados y obtener conclusiones con significancia estadística.
*   **Análisis de Sensibilidad:** Se evaluará la sensibilidad del modelo ante cambios en parámetros clave (precios, costos, variabilidad de demanda).

#### Fase 5: Validación y Documentación (Semanas 25-26)

Finalmente, se validará el enfoque general y se documentarán las conclusiones de la investigación.

*   **Validación del Modelo:** Se verificará que el modelo y los algoritmos propuestos generan soluciones realistas y aplicables en el contexto industrial.
*   **Documentación y Escritura:** Se redactará el documento final de tesis y un artículo científico para publicación en revista indexada.
*   **Transferencia de Conocimiento:** Se preparará material de divulgación para la industria (presentaciones, infografías) que faciliten la adopción de los resultados del proyecto.

---

## 6. Cronograma de Actividades

El proyecto se desarrollará en un período de **26 semanas** (aproximadamente 6 meses), distribuidas según las fases metodológicas:

| Fase | Actividad | Semanas | Duración |
|------|-----------|---------|----------|
| **Fase 1** | Revisión de Literatura | 1-4 | 4 semanas |
| | Formulación del Modelo Matemático | 5-8 | 4 semanas |
| **Fase 2** | Implementación de GA | 9-11 | 3 semanas |
| | Implementación de TS | 12-14 | 3 semanas |
| | Implementación de Híbrido | 15-16 | 2 semanas |
| **Fase 3** | Diseño del Generador de Datos | 17-18 | 2 semanas |
| | Calibración y Generación de Instancias | 19-20 | 2 semanas |
| **Fase 4** | Diseño Experimental | 21 | 1 semana |
| | Ejecución de Experimentos | 22-23 | 2 semanas |
| | Análisis de Resultados | 24 | 1 semana |
| **Fase 5** | Validación | 25 | 1 semana |
| | Documentación y Escritura Final | 26 | 1 semana |

---

## 7. Presupuesto

El presupuesto estimado para el desarrollo de esta investigación durante 26 semanas (aproximadamente 6 meses) se detalla a continuación:

### 7.1. Rubros de Inversión

| Categoría | Descripción | Cantidad | Costo Unitario (COP) | Costo Total (COP) |
|-----------|-------------|----------|----------------------|-------------------|
| **1. Personal** | | | | |
| | Estudiante investigador (dedicación 20h/sem × 26 sem) | 520 horas | $0 | $0* |
| | Asesoría metodológica | 26 semanas | Cubierto por maestría | $0 |
| **2. Equipos y Software** | | | | |
| | Computadora personal (disponible) | 1 | Recurso propio | $0 |
| | Python 3.9+ y librerías (PuLP, SciPy, Pandas, NumPy) | - | Código abierto | $0 |
| | Git/GitHub para control de versiones | - | Gratuito | $0 |
| | Jupyter Notebooks | - | Código abierto | $0 |
| **3. Recursos Bibliográficos** | | | | |
| | Acceso a bases de datos académicas (Scopus, WoS, IEEE) | 6 meses | UTP institucional | $0 |
| | Descarga de artículos científicos | ~50 artículos | UTP institucional | $0 |
| | Gestor bibliográfico (Zotero) | - | Código abierto | $0 |
| **4. Recursos Computacionales** | | | | |
| | Tiempo de cómputo local (simulaciones) | ~200 horas | Recurso propio | $0 |
| | Almacenamiento en la nube (GitHub, Google Drive) | 100 GB | Planes gratuitos | $0 |
| **5. Difusión de Resultados** | | | | |
| | Preparación de artículo científico | 1 | Tiempo investigador | $0 |
| | Publicación en revista indexada (APC - Article Processing Charge)** | 1 artículo | $1,500,000 - $3,500,000 | $2,500,000 |
| | Presentación en conferencia nacional (opcional) | 1 | $500,000 - $800,000 | $650,000 |
| **6. Otros Gastos** | | | | |
| | Materiales de presentación (impresiones, poster) | - | - | $100,000 |
| | Imprevistos (10% del total de gastos) | - | - | $325,000 |
| | | | **TOTAL** | **$3,575,000** |

### 7.2. Notas Aclaratorias

**\* Dedicación del estudiante:** El trabajo del estudiante investigador no se costea directamente, ya que forma parte de los requisitos académicos del programa de Maestría en Investigación de Operaciones y Estadística de la UTP.

**\*\* Publicación científica (APC):** El costo más significativo del proyecto corresponde a la publicación del artículo científico en una revista indexada de alto impacto. Los APCs (Article Processing Charges) varían según la revista:
- Revistas Q1-Q2 en Scopus: COP $2,000,000 - $4,000,000
- Revistas Q3-Q4 en Scopus: COP $800,000 - $1,500,000

Se estima un costo promedio de $2,500,000 para una revista Q2.

### 7.3. Fuentes de Financiación

El proyecto cuenta con las siguientes fuentes de financiación y apoyo:

1. **Recursos institucionales (UTP):**
   - Infraestructura computacional
   - Acceso a bases de datos académicas
   - Asesoría académica y metodológica
   - Espacios de trabajo

2. **Recursos propios del estudiante:**
   - Equipo de cómputo personal
   - Dedicación de tiempo (520 horas)

3. **Financiación requerida:**
   - **Publicación científica:** $2,500,000 (a gestionar mediante convocatorias UTP, recursos propios, o cofinanciación con asesor)
   - **Otros gastos:** $1,075,000 (recursos propios del estudiante)

### 7.4. Presupuesto Alternativo (Mínimo)

En caso de restricciones presupuestarias, se puede considerar un escenario mínimo:

| Concepto | Costo |
|----------|-------|
| Publicación en revista de acceso abierto sin APC | $0 |
| Presentación virtual en conferencia | $0 - $200,000 |
| Materiales básicos | $50,000 |
| **Total Mínimo** | **$50,000 - $250,000** |

---

## 8. Resultados Esperados

Al finalizar este proyecto de investigación, se espera obtener los siguientes resultados y contribuciones:

### 8.1. Contribuciones Científicas y Tecnológicas

*   **Un modelo matemático de DLBP validado** para la industria avícola, que sirva como base para futuras investigaciones en el área.
*   **Algoritmos metaheurísticos (GA, TS e híbrido) implementados y calibrados**, que podrán ser utilizados para resolver problemas de optimización similares en otros contextos industriales.
*   **Un conjunto de datos sintéticos de prueba calibrados**, que estará a disposición de la comunidad científica para la evaluación y comparación de nuevos algoritmos para el DLBP.
*   **Un artículo científico** con los resultados de la investigación, que será enviado para su publicación en una revista indexada de alto impacto en el área de Investigación de Operaciones o Gestión de Operaciones.

### 8.2. Impacto Potencial en la Industria Avícola

*   **Una herramienta de software (prototipo)** que implemente el modelo y los algoritmos desarrollados, y que pueda ser utilizada por las empresas del sector para mejorar su planificación y toma de decisiones.
*   **Una reducción potencial de al menos un 8% en las pérdidas económicas** asociadas al desbalance de carcasa, tomando como referencia el benchmark del estudio de Santa Marta [@SolanoBlanco2022], validada a través de simulación rigurosa.
*   **Una mejora estimada en la eficiencia operativa**, cuantificada en términos de:
    *   Reducción de inventarios (objetivo: 15%).
    *   Aumento del nivel de servicio (satisfacción de demanda).
    *   Mayor utilización de la capacidad instalada de la línea de despiece.

### 8.3. Formación de Capital Humano

*   **La formación de un estudiante de maestría** con altas competencias en investigación, modelado matemático, programación de algoritmos de optimización y análisis de datos.
*   **La transferencia de conocimiento** a la comunidad académica y a la industria a través de publicaciones, presentaciones en conferencias, y el software desarrollado (con licencia de código abierto cuando sea posible).

---

## 9. Referencias

Las referencias completas se encuentran en el archivo `referencias_dlbp.bib` y siguen el formato APA 7ª edición.

**Referencias clave citadas en este documento:**

*   Solano-Blanco, A. L., et al. (2022). Integrated planning decisions in the broiler chicken supply chain. *International Transactions in Operational Research*. DOI: 10.1111/itor.12861
*   Becker, C., & Scholl, A. (1998). A survey of the assembly line balancing procedures. *European Journal of Operational Research*.
*   Güngör, A., & Gupta, S. M. (2021). Disassembly scheduling: Literature review and future research directions. *International Journal of Production Research*.
*   Akpınar, Ş., & Baykasoğlu, A. (2019). A hybrid tabu search algorithm for the assembly line balancing problem. *Computers & Industrial Engineering*.
*   Awad, M., et al. (2023). The minimisation of giveaway and underweight in poultry proportioning process. *Food Control*.

**Estadísticas oficiales:**
*   FENAVI (2023). Estadísticas del Sector Avícola Colombiano.
*   DANE (2023). Encuesta Nacional Agropecuaria (ENA).
*   FAO (2023). Poultry Production and Trade Statistics.

---

## Anexos

### Anexo A: Estructura del Modelo Matemático (Formulación Preliminar)

La formulación matemática completa del modelo DLBP se desarrollará en la Fase 1, pero se anticipa que incluirá:

**Conjuntos:**
- $T$: Conjunto de tareas de despiece
- $S$: Conjunto de estaciones de trabajo
- $P$: Conjunto de coproductos
- $D$: Conjunto de períodos de demanda

**Parámetros:**
- $t_i$: Tiempo de procesamiento de la tarea $i$
- $d_{pt}$: Demanda del coproducto $p$ en el período $t$
- $c_p$: Precio de venta del coproducto $p$
- $h_p$: Costo de mantener inventario del coproducto $p$
- Precedencias entre tareas (grafo dirigido acíclico)

**Variables de decisión:**
- $x_{is}$: Asignación de tarea $i$ a estación $s$ (binaria)
- $y_{pt}$: Cantidad producida del coproducto $p$ en período $t$
- $I_{pt}$: Inventario del coproducto $p$ al final del período $t$

**Función objetivo:**
Maximizar el beneficio neto = Ingresos por ventas - Costos de producción - Costos de inventario - Penalizaciones por demanda no satisfecha

### Anexo B: Herramientas Tecnológicas a Utilizar

*   **Lenguaje de Programación:** Python 3.9+
*   **Librerías de Optimización:** PuLP, SciPy
*   **Librerías de Análisis de Datos:** Pandas, NumPy
*   **Visualización:** Matplotlib, Seaborn
*   **Control de Versiones:** Git/GitHub
*   **Documentación:** Jupyter Notebooks, LaTeX

---

**Total de palabras:** ~8,500 | **Total de líneas:** ~455
