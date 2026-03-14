---
bibliography: "referencias_dlbp.bib"
csl: "ieee.csl"
title: false
pdf-engine: xelatex
reference-section-title: "Referencias"
header-includes:
  - \usepackage{xcolor}
  - \usepackage{graphicx}
filters:
  - pandoc-mermaid
---

<!-- PRIMERA PORTADA: Simple -->
\begin{titlepage}
    \centering
    \thispagestyle{empty}
    
    \vspace*{2cm}
    
    {\LARGE \textbf{Modelo de Optimización para la Planificación de Coproductos con Metaheurísticas en la Industria Avícola}}
    
    \vspace{3cm}
    
    {\large Daniel Castañeda}
    
    \vspace{3cm}
    
    \includegraphics[width=4cm]{logo_utp.png}
    
    \vspace{3cm}
    
    {\normalsize Universidad Tecnológica de Pereira}
    
    \vspace{0.3cm}
    
    {\normalsize Maestría en Investigación de Operaciones y Estadística}
    
    \vspace{0.5cm}
    
    {\normalsize Enero 2026}
    
\end{titlepage}

\newpage

<!-- SEGUNDA PORTADA: Académica detallada -->
\begin{titlepage}
    \centering
    \thispagestyle{empty}
    
    \vspace*{1cm}
    
    {\large \textbf{UNIVERSIDAD TECNOLÓGICA DE PEREIRA}}
    
    \vspace{0.3cm}
    
    {\normalsize Facultad de Ingeniería Industrial}
    
    \vspace{0.3cm}
    
    {\normalsize Maestría en Investigación de Operaciones y Estadística}
    
    \vspace{2cm}
    
    {\Large \textbf{ANTEPROYECTO DE INVESTIGACIÓN}}
    
    \vspace{1cm}
    
    {\large \textbf{Modelo de Optimización para la Planificación de Coproductos con Metaheurísticas en la Industria Avícola}}
    
    \vspace{2cm}
    
    {\normalsize \textbf{Presentado por:}}
    
    \vspace{0.3cm}
    
    Daniel Castañeda
    
    \vspace{1cm}
    
    {\normalsize \textbf{Director:}}
    
    \vspace{0.3cm}
    
    Ing. Eliana Mirledy Ocampo Toro, PhD.
    
    \vspace{1cm}
    
    {\normalsize \textbf{Línea de Investigación:}}
    
    \vspace{0.3cm}
    
    Optimización y Modelado Matemático
    
    \vspace{2cm}
    
    Pereira, Colombia
    
    Enero, 2026
    
\end{titlepage}


\newpage

\tableofcontents

\newpage

## Resumen Ejecutivo

Este anteproyecto propone el desarrollo de un **modelo de optimización para la planificación de coproductos** en la industria avícola colombiana, resuelto mediante **técnicas metaheurísticas**. El problema central abordado es el desbalance estructural entre la oferta rígida de coproductos (determinada por la anatomía del ave) y la demanda variable del mercado: un problema de **producción conjunta (joint production)** donde el procesamiento de cada carcasa genera múltiples productos en proporciones fijas que no se alinean con la demanda. Utilizando un enfoque **cuantitativo y experimental (simulación)**, se implementarán y compararán técnicas metaheurísticas (Algoritmos Genéticos, Búsqueda Tabú y algoritmos híbridos) para maximizar la rentabilidad del proceso de despiece. La investigación se fundamenta en evidencia empírica local, como el estudio de Solano-Blanco et al. en Santa Marta, que demostró mejoras en costos de hasta un **8.6%** mediante planificación integrada con modelos estocásticos [@SolanoBlanco2022].

La industria avícola colombiana, un pilar económico con una producción anual superior a 1.7 millones de toneladas de carne de pollo [@FENAVI2024], enfrenta el desafío de optimizar el aprovechamiento de coproductos. La gestión ineficiente de este desbalance genera pérdidas económicas significativas, incluyendo altos costos de inventario, desperdicio de productos y oportunidades de venta perdidas.

Este problema de optimización combinatoria, clasificado como NP-hard por su naturaleza multi-periodo, multi-producto y estocástica, requiere enfoques avanzados como las metaheurísticas para encontrar soluciones de alta calidad en tiempos razonables. A pesar de la creciente investigación en optimización de cadenas de suministro avícolas [@Yazdekhasti2021; @Tahraoui2025], existe una notable escasez de estudios que integren metaheurísticas para la planificación operativa de coproductos bajo incertidumbre, especialmente en el contexto colombiano.

Este proyecto busca cerrar esta brecha, desarrollando un modelo de optimización avanzado que integre la estocasticidad de la demanda, las restricciones de producción conjunta y las particularidades del procesamiento avícola. La implementación de metaheurísticas permitirá generar una herramienta de apoyo a la decisión que mejore la rentabilidad, reduzca el desperdicio y fortalezca la competitividad del sector.

---

## 1. Introducción

### 1.1. El Problema de Producción Conjunta en la Industria Avícola

La industria avícola, reconocida como un pilar económico en Colombia y a nivel mundial, enfrenta un desafío operativo fundamental: el **problema de producción conjunta (joint production) y balanceo de carcasa**. Este problema surge de la discrepancia inherente entre la oferta de coproductos, que se derivan en proporciones relativamente fijas del despiece de cada ave, y la demanda variable y a menudo desalineada del mercado para cada uno de esos cortes (pechuga, alas, muslos, vísceras, etc.). Se trata de un problema clásico de **optimización de mezcla de producción bajo restricciones de co-producción** [@Heij2021; @Gicquel2017].

La industria avícola opera bajo una dinámica compleja de **"Push" (Empuje) y "Pull" (Tracción)**. Por un lado, el factor "Push" proviene de la granja: una vez que las aves alcanzan su peso de mercado, deben ser procesadas inmediatamente, generando una oferta fija de coproductos (alas, pechugas, muslos) en proporciones biológicamente determinadas. Por otro lado, el factor "Pull" es la demanda del mercado, que es estocástica, estacional y a menudo desbalanceada respecto a la oferta anatómica (alta demanda de pechuga pero baja de alas, por ejemplo).

Un plan de ventas que, por ejemplo, prioriza la comercialización de pechuga para maximizar ingresos, inevitablemente genera una sobreoferta de otros coproductos como alas y patas. Si no se gestiona adecuadamente, este excedente debe ser almacenado (incrementando costos de refrigeración), vendido a precios de liquidación o incluso desechado, ocasionando pérdidas económicas significativas y un desperdicio de recursos valiosos.

Este conflicto genera ineficiencias operativas significativas, como la acumulación de inventarios de baja rotación, la venta de productos premium a precios de liquidación, y la pérdida de oportunidades de mercado. Estudios recientes en Colombia [@SolanoBlanco2022] y en planificación de plantas de beneficio avícola [@Tahraoui2025] demuestran que la aplicación de modelos matemáticos avanzados de optimización puede mitigar estos efectos y mejorar la sostenibilidad financiera y ambiental del sector.

### 1.2. Relevancia Económica y Contexto Nacional

La relevancia económica de resolver el problema de la planificación de coproductos es crucial para la competitividad y sostenibilidad de la industria avícola colombiana. Según FENAVI [@FENAVI2024], la avicultura representa uno de los renglones pecuarios más importantes del país, con una producción anual que supera las 1.7 millones de toneladas de carne de pollo. La agroindustria avícola aporta aproximadamente 0.52% del valor agregado bruto nacional [@DANE2024].

Una gestión optimizada de la producción conjunta permite:

*   **Reducir costos de inventario:** Minimizando la acumulación de productos de baja rotación.
*   **Maximizar ingresos:** Aprovechando oportunidades de mercado para cortes de alta demanda.
*   **Mejorar la eficiencia operativa:** Optimizando las cantidades procesadas por periodo y canal de venta.
*   **Reducir el desperdicio:** Contribuyendo a la sostenibilidad ambiental del sector.

El problema de planificación de coproductos bajo demanda estocástica es un problema de optimización combinatoria clasificado como **NP-hard** cuando se consideran múltiples periodos, productos y escenarios de incertidumbre [@Birge2011; @MirzapourAlHashem2011]. Esta complejidad computacional ha motivado el desarrollo de enfoques metaheurísticos para encontrar soluciones de alta calidad en tiempos de cómputo razonables.

La literatura reciente en optimización de cadenas de suministro avícolas [@SolanoBlanco2022; @Yazdekhasti2021; @Tahraoui2025] ha demostrado la viabilidad de modelos matemáticos para la planificación integrada. Sin embargo, estos trabajos emplean predominantemente métodos exactos (MILP/CPLEX) que resultan intratables para instancias de gran escala con incertidumbre.

Este anteproyecto se centra en abordar este desafío mediante el desarrollo de un **modelo de optimización para la planificación de coproductos**, resuelto con **técnicas metaheurísticas** (Algoritmos Genéticos, Búsqueda Tabú e híbridos). El objetivo es desarrollar una herramienta de apoyo a la decisión que permita a las empresas del sector mejorar su planificación, reducir sus pérdidas y fortalecer su competitividad en un mercado cada vez más exigente.

---

## 2. Planteamiento del Problema

### 2.1. Problema Central

El problema central que aborda esta investigación es el **desbalance estructural** entre la oferta de coproductos generada por el proceso de despiece avícola y la **demanda estocástica y heterogénea del mercado**. Este desajuste, resultado directo de la naturaleza de **producción conjunta (joint production)** del negocio avícola [@Heij2021], se traduce en una cascada de ineficiencias operativas y pérdidas económicas que impactan a toda la cadena de valor.

### 2.2. Manifestaciones del Problema

El desbalance se manifiesta en dos frentes principales:

1.  **Excedentes de Inventario (Sobreproducción):** Cuando la producción de ciertos cortes (alas, patas, vísceras) supera la demanda del mercado, las empresas se ven forzadas a incurrir en costos adicionales de almacenamiento en frío, transporte y, en el peor de los casos, vender estos productos a precios de liquidación, erosionando significativamente los márgenes de ganancia.

2.  **Faltantes de Inventario (Subproducción):** De forma simultánea, la demanda de cortes de alto valor (pechuga) puede exceder la capacidad de producción balanceada, resultando en oportunidades de venta perdidas y una potencial insatisfacción del cliente.

### 2.3. Causas del Problema

Las causas fundamentales del desbalance incluyen:

*   **Restricción biológica:** La anatomía del ave determina proporciones fijas de cada coproducto (aproximadamente 30% pechuga, 20% muslos, 10% alas, etc.).
*   **Variabilidad de la demanda:** El mercado presenta patrones estacionales, promociones y preferencias cambiantes que no se alinean con las proporciones de la carcasa.
*   **Planificación tradicional:** Los métodos empíricos de programación no consideran la naturaleza estocástica del problema ni optimizan múltiples objetivos simultáneamente.
*   **Complejidad computacional:** El problema de planificación multi-producto con co-producción y demanda estocástica es NP-hard, lo que dificulta encontrar soluciones óptimas con métodos exactos en tiempos razonables [@Birge2011].

### 2.4. Consecuencias del Problema

Las consecuencias del desbalance no gestionado incluyen:

| Consecuencia | Impacto Estimado |
|--------------|------------------|
| Costos de almacenamiento refrigerado | +15-25% del costo operativo |
| Pérdidas por ventas de liquidación | -20-40% del margen en productos afectados |
| Oportunidades de venta perdidas | Variable según temporada |
| Desperdicio de producto | 5-10% de la producción total |

*Fuente: Estimaciones basadas en literatura [@SolanoBlanco2022] y reportes sectoriales [@FENAVI2024]*

### 2.5. Pregunta de Investigación

**Pregunta Principal:**
¿Cómo puede un modelo de optimización de coproductos, resuelto mediante técnicas metaheurísticas, minimizar las pérdidas económicas asociadas al desbalance entre la oferta conjunta de coproductos y la demanda del mercado en una planta de procesamiento avícola colombiana?

**Preguntas Secundarias:**

1. ¿Qué formulación matemática del problema de planificación de coproductos captura adecuadamente las restricciones de producción conjunta, los costos de inventario y la variabilidad de la demanda en el contexto avícola?

2. ¿Qué técnicas metaheurísticas (Algoritmos Genéticos, Búsqueda Tabú, o híbridos) presentan el mejor desempeño para resolver el modelo de optimización de coproductos propuesto?

3. ¿En qué magnitud se pueden reducir las pérdidas económicas asociadas al desbalance de carcasa mediante la implementación del modelo de optimización?

### 2.6. Hipótesis de Investigación

**Hipótesis Principal (H1):**
La aplicación de un modelo de optimización de coproductos con metaheurísticas puede generar una reducción significativa en los costos de inventario y una mejora sustancial en la utilidad operativa, tomando como referencia los benchmarks de Solano-Blanco et al. [-@SolanoBlanco2022] y Tahraoui et al. [-@Tahraoui2025].

**Hipótesis Secundarias:**

*   **H2:** Un algoritmo metaheurístico híbrido (que combine Algoritmos Genéticos y Búsqueda Tabú) superará en desempeño a cada técnica aplicada individualmente.
*   **H3:** El modelo de optimización permitirá una reducción de al menos un 15% en el inventario promedio de productos de baja rotación.

---

## 3. Objetivos

### 3.1. Objetivo General

Desarrollar un modelo de optimización para la planificación de coproductos que, mediante la aplicación de técnicas metaheurísticas, minimice las pérdidas económicas asociadas al desbalance entre la oferta conjunta de coproductos y la demanda del mercado en la industria avícola colombiana.

### 3.2. Objetivos Específicos

1.  **Formular** un modelo matemático de optimización de coproductos que capture las restricciones de producción conjunta, costos de inventario, balance de materiales y variabilidad de la demanda propias del procesamiento avícola.

2.  **Implementar** algoritmos metaheurísticos (Algoritmo Genético, Búsqueda Tabú y un enfoque híbrido) adaptados al problema de planificación de coproductos avícolas.

3.  **Diseñar** un generador de instancias de prueba con datos sintéticos calibrados que reflejen las condiciones operativas reales de la industria avícola colombiana.

4.  **Comparar** el desempeño de las metaheurísticas propuestas mediante un diseño experimental riguroso, evaluando calidad de solución y eficiencia computacional.

5.  **Validar** el modelo propuesto mediante simulación, cuantificando las mejoras potenciales en términos de reducción de costos de inventario, nivel de servicio y rentabilidad operativa.

## 4. Justificación

### 4.1. Beneficiarios de la Investigación

**Beneficiarios Directos:**

*   Empresas procesadoras de pollo en Colombia
*   Planificadores de producción del sector avícola
*   Gerentes de operaciones y logística

**Beneficiarios Indirectos:**

*   Consumidores (mayor disponibilidad y precios estables)
*   Comunidad académica (avance en DLBP aplicado a alimentos)
*   Sector ambiental (reducción de desperdicio)

### 4.2. Magnitud del Problema

| Indicador | Valor | Fuente |
|-----------|-------|--------|
| Producción anual de pollo | 1.7 millones de toneladas | FENAVI 2024 |
| Empleos generados | 600,000+ directos e indirectos | FENAVI 2024 |
| Participación en PIB agropecuario | 0.52% | DANE 2024 |
| Potencial de ahorro en inventario | 30-60% | Solano-Blanco et al. 2022 |

*Fuente: Elaboración propia con datos de [@FENAVI2024; @DANE2024; @SolanoBlanco2022]*

### 4.3. Conveniencia y Relevancia Económica

La optimización de la planificación de coproductos tiene un impacto directo en la rentabilidad de las empresas avícolas. Como demostró el caso de Solano-Blanco et al. [@SolanoBlanco2022], las mejoras en la planificación integrada pueden traducirse en reducciones de costos del **8.6%**. Tahraoui et al. [@Tahraoui2025] confirmaron que la planificación operativa optimizada con modelos MILP reduce significativamente los costos en plantas multi-producto. En una industria de márgenes estrechos y alto volumen, estas mejoras representan una ventaja competitiva crítica.

El sector avícola colombiano, que según FENAVI [@FENAVI2024] genera más de 600,000 empleos directos e indirectos, se beneficiaría significativamente de herramientas que mejoren su eficiencia operativa. La implementación de modelos de optimización no solo mejora la rentabilidad de las empresas individuales, sino que fortalece la competitividad del sector a nivel nacional e internacional.

### 4.4. Relevancia Social y Ambiental (Sostenibilidad)

Mejorar el equilibrio de la carcasa contribuye directamente a la sostenibilidad del sector. Al reducir el desperdicio de alimentos y optimizar el uso de recursos (energía para refrigeración de inventarios no deseados), el proyecto se alinea con los **Objetivos de Desarrollo Sostenible (ODS)**, específicamente:

*   **ODS 12 (Producción y Consumo Responsables):** Reduciendo el desperdicio de alimentos y optimizando el aprovechamiento de cada ave procesada.
*   **ODS 9 (Industria, Innovación e Infraestructura):** Mediante la aplicación de técnicas avanzadas de optimización y el desarrollo de herramientas tecnológicas para la industria.

La reducción del desperdicio de alimentos es particularmente relevante en un contexto global donde aproximadamente el 14% de los alimentos se pierde en la cadena de suministro antes de llegar al consumidor [@FAO2023]. Un mejor balanceo de la carcasa significa un proceso más sostenible, con menor huella de carbono y mejor utilización de los recursos naturales.

En el contexto más amplio del desensamble industrial, Darghouth et al. [-@Darghouth2021] han demostrado que la **optimización de la programación de desensamble** con enfoque en sostenibilidad puede generar beneficios significativos en términos de **eficiencia energética** y **reducción de costos**. Su modelo de programación capacitada consideró la selección de tecnologías de procesamiento y el consumo energético de diferentes técnicas de desensamble, proporcionando un marco metodológico para integrar criterios de sostenibilidad en la toma de decisiones operativas. Aunque su enfoque se centró en remanufactura industrial, los principios de optimización con restricciones de capacidad y consideraciones ambientales son directamente aplicables al procesamiento avícola, donde la selección de secuencias de corte eficientes puede minimizar el consumo energético de equipos de refrigeración y reducir el desperdicio de subproductos.


### 4.5. Implicaciones Prácticas

El desarrollo de una herramienta de toma de decisiones basada en metaheurísticas permitirá a los planificadores de producción pasar de decisiones basadas en la intuición ("gut feeling") y la experiencia personal a decisiones basadas en datos y modelado matemático robusto. Esto mejorará la capacidad de respuesta ante fluctuaciones del mercado y permitirá una planificación más ágil y eficiente.

La implementación de tecnologías de sensores inteligentes [@SensorsPoultry2022] y sistemas de automatización [@AutomationSystems2023] en la industria avícola está generando grandes volúmenes de datos que pueden ser aprovechados por modelos de optimización como el propuesto en este proyecto.

### 4.6. Valor Teórico y Científico

El proyecto contribuye significativamente a la literatura de **optimización de producción conjunta (joint production)** en la industria alimentaria, extendiendo los modelos clásicos de planificación de producción deterministas [@Gicquel2017] hacia enfoques estocásticos que consideran la incertidumbre de la demanda, una área identificada como línea futura de investigación por diversos autores [@Birge2011; @MirzapourAlHashem2011].

La **optimización multi-objetivo** en la industria alimentaria ha experimentado un avance significativo en los últimos años. Arteaga-Cabrera et al. [-@Arteaga2025] presentaron una revisión comprehensiva sobre la evolución de las estrategias de optimización en alimentos, identificando la transición desde métodos univariados tradicionales hacia técnicas multi-objetivo integradas con tecnologías emergentes. Su trabajo destaca que la industria alimentaria moderna requiere **optimizar simultáneamente múltiples objetivos competitivos** (costos de producción, eficiencia energética, calidad del producto, sostenibilidad), lo cual se alinea perfectamente con la planificación de coproductos avícolas, donde se deben balancear simultáneamente:

- Maximización de ingresos por venta de coproductos
- Minimización de costos de inventario
- Minimización de penalizaciones por demanda no satisfecha
- Maximización del nivel de servicio al cliente

La incorporación de **algoritmos evolutivos** y metaheurísticas hibridizadas, como lo documentan Arteaga-Cabrera et al. [@Arteaga2025], ha permitido abordar estos problemas complejos de forma efectiva en la industria alimentaria, generando soluciones robustas que equilibran trade-offs entre objetivos contradictorios. Este proyecto se posiciona como una **contribución directa** a esta línea de investigación, aplicando metaheurísticas (GA, TS, híbridos) a un problema multi-objetivo de planificación de coproductos en el procesamiento avícola.

Adicionalmente, la comparación rigurosa de diferentes técnicas metaheurísticas (Algoritmos Genéticos, Búsqueda Tabú, y algoritmos híbridos) en el contexto específico de la industria avícola generará conocimiento valioso sobre la efectividad de estas técnicas en problemas del mundo real con características particulares (perecibilidad, estocasticidad, restricciones sanitarias).

## 5. Marco Teórico y Antecedentes

### 5.1. El Problema de Producción Conjunta y Planificación de Coproductos

El **problema de producción conjunta (joint production)** ocurre cuando el procesamiento de una materia prima genera múltiples productos en proporciones fijas o semifijas. En la industria avícola, el despiece de cada carcasa produce inevitablemente pechuga, muslos, alas, vísceras y otros cortes en proporciones determinadas por la anatomía del ave. Esta característica, compartida con otras industrias cárnicas, crea un desafío único de planificación cuando la demanda del mercado para cada coproducto no refleja estas proporciones naturales [@Heij2021].

Desde la perspectiva de la investigación de operaciones, este problema se clasifica como un **problema de optimización de mezcla de producción multi-producto con restricciones de co-producción** [@Gicquel2017]. A diferencia de los problemas clásicos de planificación de producción, donde las cantidades de cada producto pueden decidirse independientemente, aquí la decisión de producir una unidad de un coproducto (e.g., pechuga) implica necesariamente la producción de cantidades proporcionales de todos los demás coproductos.

Solano-Blanco et al. [@SolanoBlanco2022] abordaron este problema específico en la industria avícola colombiana mediante un modelo de planificación integrada basado en MILP con programación estocástica de dos etapas, logrando reducciones de costos del 8.6% en un caso de estudio en Santa Marta. Más recientemente, Tahraoui et al. [@Tahraoui2025] desarrollaron un modelo MILP para la planificación operativa de plantas de beneficio avícola multi-producto, validado con CPLEX. Sin embargo, ambos enfoques dependen de métodos exactos que se vuelven intratables para instancias de gran escala.

El problema se ha modelado como un problema de **programación estocástica multi-periodo** [@Birge2011], donde las decisiones de producción en cada periodo deben considerar la incertidumbre en la demanda futura de cada coproducto. Modelos robustos multi-objetivo [@MirzapourAlHashem2011] han demostrado la viabilidad de optimizar simultáneamente múltiples criterios (costo, nivel de servicio, inventario) bajo incertidumbre, proporcionando un marco teórico directo para este trabajo.

En el contexto específico de productos perecederos, Sel et al. [@Sel2015] demostraron la importancia de considerar restricciones de vida útil en la planificación integrada de cadenas de suministro, mientras que Kopanos et al. [@Kopanos_2012] establecieron marcos matemáticos eficientes para el scheduling en procesamiento de alimentos. Akkerman y van Donk [@Akkerman_2008] analizaron la estructura de tareas en esta industria, y Véghová et al. [@Veghova_2016] enfatizaron la trazabilidad en el procesamiento de carne. Estas investigaciones fundamentan la necesidad de modelos especializados para la industria alimentaria.

### 5.2. Relación con el Problema de Balanceo de Líneas de Desensamble (DLBP)

El **Problema de Balanceo de Líneas de Desensamble (DLBP)** es un área relacionada de la investigación de operaciones que se enfoca en la asignación óptima de tareas a estaciones de trabajo en líneas de desensamble, minimizando el número de estaciones o balanceando los tiempos de operación [@BeckerScholl2006; @GungorGupta2001]. Aunque el DLBP se distingue del problema de planificación de coproductos —ya que se enfoca en el balanceo de **tiempos de tarea** y no en el balanceo de **demanda vs. producción**—, comparte con este proyecto la naturaleza combinatoria NP-hard y el uso de metaheurísticas como estrategia de solución.

Investigaciones recientes en DLBP han desarrollado enfoques estocásticos y multi-objetivo que ofrecen lecciones metodológicas valiosas para este trabajo. Mete et al. [@Mete2022] realizaron un análisis comparativo de metaheurísticas para DLBP con tiempos estocásticos, demostrando la superioridad de los Algoritmos Genéticos. Hu et al. [@Hu_2023] propusieron hiper-heurísticas para balanceo paralelo bajo estocasticidad. Tian et al. [@Tian_2023] desarrollaron algoritmos evolutivos híbridos para DLBP multi-objetivo. Estas contribuciones informan directamente el diseño de las metaheurísticas propuestas en este proyecto.

### 5.3. Metaheurísticas para Problemas de Optimización Combinatoria

Debido a la complejidad computacional de los problemas de optimización combinatoria como la planificación de coproductos, las **metaheurísticas** se han convertido en el enfoque predominante para resolverlos. Las metaheurísticas son algoritmos de optimización de alto nivel que pueden ser aplicados a una amplia gama de problemas de ingeniería complejos [@MetaheuristicsPower2023], y que a menudo se inspiran en procesos naturales. En el contexto de problemas de balanceo y planificación, estos algoritmos han demostrado ser efectivos para abordar problemas de optimización multi-criterio [@Paprocka2022; @Arteaga2025].

En el contexto de la industria alimentaria, Arteaga-Cabrera et al. [@Arteaga2025] documentaron la efectividad de **algoritmos evolutivos** y metaheurísticas para resolver problemas de optimización multi-objetivo en sistemas de producción alimentaria. Su revisión comprehensiva destaca que estas técnicas son particularmente efectivas cuando se deben equilibrar objetivos contradictorios (e.g., minimizar costos vs. maximizar calidad), una característica intrínseca de la planificación de coproductos avícolas. A continuación se detallan las metaheurísticas más relevantes para este proyecto:

#### 5.3.1. Algoritmos Genéticos (GA)

Los Algoritmos Genéticos, inspirados en la teoría de la evolución de Darwin, operan sobre una población de soluciones, aplicando operadores de selección, cruce y mutación para generar nuevas y mejores soluciones. Su efectividad en problemas de optimización combinatoria ha sido ampliamente demostrada [@Sivasankaran2014], particularmente cuando el espacio de búsqueda es grande y complejo.

En problemas con incertidumbre, Mete et al. [@Mete2022] demostraron empíricamente que los Algoritmos Genéticos **superan consistentemente** a otras metaheurísticas (como Simulated Annealing) cuando se enfrentan a parámetros estocásticos, lo que los posiciona como una técnica especialmente adecuada para el problema de planificación de coproductos avícolas, donde la variabilidad en la demanda introduce estocasticidad inherente.

####  5.3.2. Búsqueda Tabú (TS)

La Búsqueda Tabú es un método de búsqueda local que utiliza una lista "tabú" para evitar volver a visitar soluciones ya exploradas y así escapar de óptimos locales. El trabajo de Suwannarongsri et al. [@Suwannarongsri2007] ha demostrado la efectividad de la búsqueda tabú híbrida en problemas combinatorios de optimización, con resultados prometedores adaptables al contexto de la planificación de producción.

#### 5.3.3. Enfoques Híbridos y Multi-objetivo
La tendencia actual prioriza el uso de algoritmos híbridos para superar las limitaciones de las técnicas individuales. Wang et al. [@Wang_2021] demostraron que combinar Algoritmos Genéticos con Recocido Simulado mejora la capacidad de escapar de óptimos locales. En el ámbito multi-objetivo, Saif et al. [@Saif_2014] aplicaron algoritmos de colonias de abejas artificiales (ABC) basados en Pareto para manejar parámetros inciertos, y Li et al. [@Li_2021] extendieron este enfoque a configuraciones alternativas. Adicionalmente, Babazadeh et al. [@Babazadeh_2018_CIE] mejoraron el algoritmo NSGA-II para problemas fuzzy bi-objetivo, evidenciando la superioridad de los enfoques híbridos y evolutivos para resolver instancias complejas de optimización combinatoria.

### 5.3. Tecnologías Habilitadoras y Tendencias Recientes

Mahalik y Nambiar [@Mahalik2010] destacan la tendencia creciente hacia la automatización y el uso de sensores inteligentes en los sistemas de manufactura de alimentos, elementos clave para asegurar la calidad y trazabilidad. La integración de estos sensores [@SensorsPoultry2022] y la planificación automatizada de desensamble [@Hartono2022] en plantas de procesamiento están generando oportunidades para la implementación de modelos de optimización en tiempo real. Hartono et al. [@Hartono2022] demostraron la eficacia del *Bees Algorithm* para optimizar planes de desensamble robótico, un enfoque que podría adaptarse al procesamiento de carcasas avícolas.

Recientemente, el uso de tecnologías avanzadas como la visión por computador y la generación de datos sintéticos ha comenzado a transformar el procesamiento avícola. Feng et al. [@Feng2025] demostraron cómo el aumento de datos sintéticos puede mejorar significativamente la segmentación de instancias de carcasas de pollo, lo cual es fundamental para la automatización de procesos de despiece y control de calidad.

Asimismo, la integración de robótica colaborativa [@IndustrialRobots2023] promete flexibilizar las líneas de producción, permitiendo una mejor adaptación a la variabilidad de la materia prima. Estas innovaciones tecnológicas proporcionan la base para implementar modelos de optimización más sofisticados.

#### 5.4.1. Tendencias Emergentes (2025-2026)

La literatura más reciente muestra una clara evolución hacia la integración de **inteligencia artificial avanzada** y **sistemas colaborativos**. Tan et al. [@Tan2026] y Wang et al. [@Wang2026] han aplicado algoritmos de **Aprendizaje por Refuerzo Profundo (Deep Reinforcement Learning)** y optimización Kepleriana para resolver problemas de balanceo dinámico en entornos de manufactura, donde la incertidumbre proviene de la variabilidad en los tiempos humano-robot. 

Paralelamente, Tahraoui et al. [@Tahraoui2025] han avanzado en el estado del arte de la **planeación operativa** para plantas de beneficio avícola utilizando modelos exactos (MILP), abordando la complejidad de la demanda fluctuante en entornos multi-producto. Sin embargo, su enfoque permanece limitado a métodos exactos que se vuelven intratables para instancias de gran escala, confirmando que la aplicación de metaheurísticas para la planificación de coproductos avícolas sigue siendo un área inexplorada.

### 5.5. Vacíos de Investigación Identificados

A pesar de la creciente investigación en optimización de cadenas de suministro avícolas y en metaheurísticas para problemas combinatorios, la revisión del estado del arte revela varios vacíos de investigación que este proyecto busca abordar. La Tabla 1 resume los trabajos más relevantes y su posicionamiento respecto a esta propuesta.

**Tabla 1. Resumen del Estado del Arte y Brechas Identificadas**

| Autor(es) | Técnica | Objetivo | Manejo de Incertidumbre | Aplicación |
|-----------|---------|----------|------------------------|------------|
| Solano-Blanco et al. [-@SolanoBlanco2022] | MILP (Estocástico) | Planificación Integrada | Estocástico (2 etapas) | Avícola (Colombia) |
| Tahraoui et al. [-@Tahraoui2025] | MILP (CPLEX) | Planeación Operativa | Demanda Fluctuante | Avícola (Multi-producto) |
| Yazdekhasti et al. [-@Yazdekhasti2021] | MILP Multi-modal | SC Estocástica | Estocástico (Demanda) | Avícola (Mississippi) |
| Mirzapour et al. [-@MirzapourAlHashem2011] | MILP Robusto | Planificación Agregada | Robusto (Multi-objetivo) | Manufactura Multi-sitio |
| Mete et al. [-@Mete2022] | GA, Dijkstra | Minimizar Estaciones | Estocástico (Tiempos) | DLBP (Benchmark) |
| Hu et al. [-@Hu_2023] | Hiper-heurística (SA) | Balanceo Paralelo | Estocástico | Remanufactura |
| Gicquel & Miègeville [-@Gicquel2017] | MILP | Producción + Transporte | Determinista | Alimentaria (Multi-sitio) |
| **Esta Propuesta** | **GA, TS, Híbrido** | **Max Profit / Min Costos** | **Estocástico (Demanda)** | **Avícola (Coproductos)** |

Este proyecto de investigación se posiciona para abordar estos vacíos, con el objetivo de desarrollar una contribución significativa tanto al campo académico de la optimización de producción conjunta como a la práctica industrial de la gestión de la producción avícola.

---

## 6. Metodología

La metodología de esta investigación se estructura en cinco fases principales, diseñadas para abordar de manera sistemática las preguntas de investigación y validar las hipótesis planteadas.

### 5.1. Clasificación de la Investigación

*   **Enfoque:** Cuantitativo. Se basa en la medición numérica de variables (costos, tiempos, cantidades) y el análisis estadístico riguroso de resultados.
*   **Alcance:** Explicativo y Correlacional. Busca explicar la relación causal entre la optimización de la planificación de coproductos y la rentabilidad/eficiencia operativa.
*   **Diseño:** Experimental (Simulación). Se manipulan variables independientes (algoritmos metaheurísticos, escenarios de demanda) en un entorno controlado (*in silico*) para observar su efecto en la variable dependiente (costo total, nivel de servicio, inventario).
*   **Método de Inferencia:** Deductivo. Se parte de teorías generales de optimización y producción conjunta para aplicarlas a un caso específico de la industria avícola.
*   **Temporalidad:** Transversal. Los experimentos computacionales se realizan en un corte de tiempo específico, aunque considerando escenarios de demanda que reflejan variabilidad temporal.

### 5.2. Fases de la Investigación

#### Fase 1: Formulación del Modelo Matemático (Semanas 1-8)

El primer paso consiste en desarrollar un modelo matemático de optimización para la planificación de coproductos avícolas. Este modelo será la base para la implementación de los algoritmos de solución.

*   **Definición de Variables de Decisión:** Se identifican las variables clave del problema, como las cantidades de carcasas a procesar por periodo, las cantidades de cada coproducto a destinar a cada canal de venta, y los niveles de inventario.
*   **Función Objetivo:** Se formula una función objetivo que busca maximizar la rentabilidad de la operación. Esto implica maximizar los ingresos por la venta de coproductos y minimizar los costos de producción, inventario y penalizaciones por demanda no satisfecha.
*   **Restricciones:** Se incorporan al modelo todas las restricciones relevantes del problema:

    *   Restricciones de co-producción (proporciones fijas de coproductos por carcasa).
    *   Restricciones de capacidad de procesamiento de la planta.
    *   Restricciones de balance de materiales (conservación de masa y flujo de coproductos).
    *   Restricciones de demanda estocástica del mercado.
    *   Restricciones de perecibilidad y vida útil de los productos.

#### Fase 2: Diseño e Implementación de Metaheurísticas (Semanas 9-16)

Dada la complejidad NP-hard del problema de planificación de coproductos, se recurre a metaheurísticas para encontrar soluciones de alta calidad en tiempos computacionales razonables. Se exploran e implementan las siguientes técnicas:

*   **Algoritmo Genético (GA):** Implementación de un GA con representación vectorial de soluciones (cantidades de producción por periodo), operadores de cruce y mutación adaptados al problema [@Sivasankaran2014].
*   **Búsqueda Tabú (TS):** Implementación de TS con estrategias de diversificación e intensificación, siguiendo las mejores prácticas documentadas en [@Suwannarongsri2007].
*   **Algoritmo Híbrido GA-TS:** Desarrollo de un algoritmo híbrido que combina la exploración global del GA con la explotación local de TS.

Para cada metaheurística se realizará:
*   Codificación adecuada de la solución.
*   Diseño de operadores de búsqueda específicos para el problema.
*   Calibración de parámetros mediante diseño experimental.

La implementación se realizará en Python, utilizando librerías de optimización estándar y frameworks de experimentación controlada.

#### Fase 3: Generación de Datos y Escenarios de Prueba (Semanas 17-20)

Para validar el modelo y los algoritmos propuestos, se genera un conjunto de instancias de prueba que representan de manera realista las condiciones de la industria avícola colombiana.

*   **Datos Sintéticos Calibrados:** Se utilizan datos sintéticos para las pruebas, siguiendo las mejores prácticas en generación de datos sintéticos [@SyntheticDataChicken2025]. Estos datos son calibrados utilizando:
    *   Rendimientos estándar de carcasa publicados en la literatura.
    *   Costos de producción del sector avícola colombiano.
    *   Patrones de demanda históricos (cuando están disponibles) o generados mediante distribuciones probabilísticas, siguiendo el enfoque predictivo basado en datos históricos propuesto por [@Paprocka2022].
    *   Parámetros de la industria local (caso Santa Marta como referencia).
*   **Generación de Instancias:** Se crean múltiples instancias del problema con diferentes tamaños (número de coproductos, número de periodos, número de canales de venta) y niveles de complejidad (variabilidad de demanda, estacionalidad) para evaluar la escalabilidad y robustez de los algoritmos.

#### Fase 4: Diseño Experimental y Análisis de Resultados (Semanas 21-24)

Se lleva a cabo un diseño experimental riguroso para evaluar el desempeño de las metaheurísticas propuestas y validar las hipótesis de la investigación.

*   **Métricas de Desempeño:** Se definen métricas cuantitativas para evaluar:
    *   Rentabilidad total (función objetivo).
    *   Nivel de servicio al cliente (% de demanda satisfecha).
    *   Niveles de inventario promedio.
    *   Tiempo computacional.
    *   Gap de optimalidad (cuando sea posible comparar con soluciones exactas en instancias pequeñas).
*   **Análisis Comparativo:** Se compara el desempeño de:
    *   GA vs. TS vs. Híbrido.
    *   Modelo optimizado vs. Métodos heurísticos simples (baseline).
*   **Análisis Estadístico:** Se utilizan herramientas estadísticas (ANOVA, pruebas t, pruebas no paramétricas) para analizar los resultados y obtener conclusiones con significancia estadística.
*   **Análisis de Sensibilidad:** Se evalúa la sensibilidad del modelo ante cambios en parámetros clave (precios, costos, variabilidad de demanda).

#### Fase 5: Validación y Documentación (Semanas 25-26)

Finalmente, se valida el enfoque general y se documentan las conclusiones de la investigación.

*   **Validación del Modelo:** Se verifica que el modelo y los algoritmos propuestos generen soluciones realistas y aplicables en el contexto industrial.
*   **Documentación y Escritura:** Se redacta el documento final de tesis.
*   **Transferencia de Conocimiento:** Se prepara material de divulgación para la industria (presentaciones, infografías) que faciliten la adopción de los resultados del proyecto.

---

## 7. Cronograma

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

## 8. Resultados Esperados

> Los resultados están directamente vinculados con los objetivos específicos de la investigación.

Al finalizar este proyecto de investigación, se espera obtener los siguientes resultados y contribuciones:

### 8.1. Contribuciones Científicas y Tecnológicas

*   **Un modelo matemático de optimización de coproductos validado** para la industria avícola, que sirva como base para futuras investigaciones en el área.
*   **Algoritmos metaheurísticos (GA, TS e híbrido) implementados y calibrados**, que podrán ser utilizados para resolver problemas de optimización similares en otros contextos industriales.
*   **Un conjunto de datos sintéticos de prueba calibrados**, que estará a disposición de la comunidad científica para la evaluación y comparación de nuevos algoritmos para problemas de planificación de coproductos.
*   **Código fuente y datos públicos**: Todo el código, instancias sintéticas y resultados experimentales están disponibles en el repositorio público: [https://github.com/DanAndCastRod/OBC](https://github.com/DanAndCastRod/OBC).
<!-- *   **Un artículo científico** con los resultados de la investigación, que será enviado para su publicación en una revista indexada de alto impacto en el área de Investigación de Operaciones o Gestión de Operaciones. -->

### 8.2. Impacto Potencial en la Industria Avícola

*   **Una herramienta de software (prototipo)** que implemente el modelo y los algoritmos desarrollados, y que pueda ser utilizada por las empresas del sector para mejorar su planificación y toma de decisiones.
*   **Una reducción significativa en los costos de inventario** y una mejora sustancial en la utilidad operativa, tomando como referencia los benchmarks de Solano-Blanco et al. [@SolanoBlanco2022] y Tahraoui et al. [@Tahraoui2025], validada a través de simulación rigurosa.
*   **Una mejora estimada en la eficiencia operativa**, cuantificada en términos de:
    *   Reducción de inventarios (objetivo: 15%).
    *   Aumento del nivel de servicio (satisfacción de demanda).
    *   Mayor utilización de la capacidad instalada de la línea de despiece.

### 8.3. Formación de Capital Humano

*   **La formación de un estudiante de maestría** con altas competencias en investigación, modelado matemático, programación de algoritmos de optimización y análisis de datos.
*   **La transferencia de conocimiento** a la comunidad académica y a la industria a través de publicaciones, presentaciones en conferencias, y el software desarrollado (con licencia de código abierto cuando sea posible).

---

## 9. Consideraciones Éticas

### 9.1. Uso de Datos Sintéticos

Esta investigación utiliza exclusivamente datos sintéticos calibrados con parámetros de la industria avícola colombiana, lo que evita la necesidad de acceder a información confidencial de empresas específicas. Los parámetros de calibración se obtienen de fuentes públicas (FENAVI, DANE) y literatura científica publicada.

### 9.2. Protección de Información Industrial

En caso de que futuras etapas de la investigación requieran validación con datos reales de plantas de procesamiento, se establecerán acuerdos formales de confidencialidad. Toda información sensible será anonimizada antes de su inclusión en publicaciones o presentaciones.

### 9.3. Transparencia Metodológica

Los algoritmos desarrollados, el código fuente y los conjuntos de datos sintéticos serán documentados y puestos a disposición de la comunidad científica, garantizando la reproducibilidad de los resultados y facilitando la verificación independiente de las conclusiones.

### 9.4. Responsabilidad en las Recomendaciones

Las soluciones propuestas por el modelo de optimización se presentan como herramientas de apoyo a la decisión. Se reconoce que la implementación práctica de cualquier recomendación requiere el juicio experto de los profesionales de la industria y la consideración de factores contextuales que pueden no estar capturados en el modelo.

---

## 10. Referencias

Las referencias completas se generan automáticamente mediante Pandoc utilizando el formato IEEE.

**Referencias clave citadas en este documento:**

*   Solano-Blanco, A. L., et al. (2022). Production planning decisions in the broiler chicken supply chain with growth uncertainty. *International Transactions in Operational Research*. DOI: 10.1111/itor.12861
*   Tahraoui, N., et al. (2025). Operational planning of the production and the processing of chickens in multi-products slaughter unit. *OPSEARCH*. DOI: 10.1007/s12597-024-00846-1
*   Yazdekhasti, A., et al. (2021). A multi-period multi-modal stochastic supply chain model under COVID pandemic: A poultry industry case study. *Transportation Research Part E*. DOI: 10.1016/j.tre.2021.102463
*   Gicquel, C. & Miègeville, N. (2017). Formulations and solution methods for the joint production and transportation planning in multi-site food supply chains. *Computers & Industrial Engineering*. DOI: 10.1016/j.cie.2017.07.025
*   Awad, M., et al. (2023). The minimisation of giveaway and underweight in poultry proportioning process. *Food Control*.

**Estadísticas oficiales:**

*   FENAVI (2023). Estadísticas del Sector Avícola Colombiano.
*   DANE (2023). Encuesta Nacional Agropecuaria (ENA).
*   FAO (2023). Poultry Production and Trade Statistics.

::: {#refs}
:::

## Anexos

### Anexo A: Formulación Matemática del Modelo de Optimización de Coproductos

El modelo propuesto se formula como un problema de **Programación Lineal Entera Mixta (MILP) multi-periodo** para la planificación óptima de coproductos avícolas bajo demanda estocástica.

**Conjuntos:**

- $P = \{1, 2, ..., n_p\}$: Conjunto de coproductos (pechuga, muslos, alas, etc.)
- $T = \{1, 2, ..., n_t\}$: Conjunto de periodos de planificación
- $\Omega = \{1, 2, ..., n_\omega\}$: Conjunto de escenarios de demanda

**Parámetros:**

- $\alpha_p$: Proporción fija del coproducto $p$ por carcasa (restricción anatómica, $\sum_p \alpha_p = 1$)
- $W$: Peso promedio de una carcasa (kg)
- $d_{pt\omega}$: Demanda del coproducto $p$ en el periodo $t$ bajo el escenario $\omega$ (kg)
- $r_p$: Precio de venta del coproducto $p$ (\$/kg)
- $c^{prod}$: Costo de procesamiento por carcasa (\$/carcasa)
- $c^{inv}_p$: Costo de mantener inventario del coproducto $p$ (\$/kg/periodo)
- $c^{pen}_p$: Costo de penalización por demanda no satisfecha del coproducto $p$ (\$/kg)
- $Q^{max}$: Capacidad máxima de procesamiento (carcasas/periodo)
- $L_p$: Vida útil máxima del coproducto $p$ (periodos)
- $\pi_\omega$: Probabilidad del escenario $\omega$

**Variables de Decisión:**

- $q_t$: Número de carcasas a procesar en el periodo $t$ (primera etapa)
- $v_{pt\omega}$: Cantidad vendida del coproducto $p$ en el periodo $t$, escenario $\omega$ (segunda etapa)
- $I_{pt\omega}$: Inventario del coproducto $p$ al final del periodo $t$, escenario $\omega$
- $u_{pt\omega}$: Demanda no satisfecha del coproducto $p$ en el periodo $t$, escenario $\omega$

**Función Objetivo:**

Maximizar el beneficio esperado:

\begin{equation}
\max Z = \sum_{\omega \in \Omega} \pi_\omega \left[ \sum_{t \in T} \left( \sum_{p \in P} r_p \cdot v_{pt\omega} - c^{prod} \cdot q_t - \sum_{p \in P} c^{inv}_p \cdot I_{pt\omega} - \sum_{p \in P} c^{pen}_p \cdot u_{pt\omega} \right) \right]
\end{equation}

**Restricciones:**

Balance de materiales (co-producción):
\begin{equation}
I_{pt\omega} = I_{p,t-1,\omega} + \alpha_p \cdot W \cdot q_t - v_{pt\omega} \quad \forall p \in P, t \in T, \omega \in \Omega
\end{equation}

Satisfacción de demanda:
\begin{equation}
v_{pt\omega} + u_{pt\omega} = d_{pt\omega} \quad \forall p \in P, t \in T, \omega \in \Omega
\end{equation}

Capacidad de procesamiento:
\begin{equation}
0 \leq q_t \leq Q^{max} \quad \forall t \in T
\end{equation}

Restricción de ventas (no se puede vender más de lo disponible):
\begin{equation}
v_{pt\omega} \leq I_{p,t-1,\omega} + \alpha_p \cdot W \cdot q_t \quad \forall p \in P, t \in T, \omega \in \Omega
\end{equation}

No negatividad:
\begin{equation}
q_t, v_{pt\omega}, I_{pt\omega}, u_{pt\omega} \geq 0
\end{equation}

### Anexo B: Herramientas Tecnológicas a Utilizar

*   **Lenguaje de Programación:** Python 3.9+
*   **Librerías de Optimización:** PuLP, SciPy
*   **Librerías de Análisis de Datos:** Pandas, NumPy
*   **Visualización:** Matplotlib, Seaborn
*   **Control de Versiones:** Git/GitHub
*   **Documentación:** Jupyter Notebooks, LaTeX
