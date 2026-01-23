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
    
    {\LARGE \textbf{Modelo DLBP para Coproductos con Metaheurísticas en la Industria Avícola}}
    
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
    
    {\large \textbf{Modelo DLBP para Coproductos con Metaheurísticas en la Industria Avícola}}
    
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

Este anteproyecto propone el desarrollo de un **modelo de optimización para el Problema de Balanceo de Líneas de Desensamble (DLBP)** aplicado a la industria avícola colombiana. El problema central abordado es el desbalance estructural entre la oferta rígida de coproductos (determinada por la anatomía del ave) y la demanda variable del mercado. Utilizando un enfoque **cuantitativo y experimental (simulación)**, se implementarán y compararán técnicas **metaheurísticas** (Algoritmos Genéticos, Búsqueda Tabú y algoritmos híbridos) para maximizar la rentabilidad del proceso de despiece. La investigación se fundamenta en evidencia empírica local, como el estudio de Solano-Blanco et al. en Santa Marta, que demostró mejoras en la utilidad entre el **7% y 57%**, así como reducciones en costos de inventario entre el **30% y 60%** mediante planificación integrada [@SolanoBlanco2022].

La industria avícola colombiana, un pilar económico con una producción anual superior a 1.7 millones de toneladas de carne de pollo [@FENAVI2024], enfrenta el desafío de optimizar el aprovechamiento de coproductos. La gestión ineficiente de este desbalance genera pérdidas económicas significativas, incluyendo altos costos de inventario, desperdicio de productos y oportunidades de venta perdidas.

El DLBP, clasificado como NP-hard, requiere enfoques avanzados como las metaheurísticas para encontrar soluciones óptimas en tiempos razonables. A pesar de la extensa investigación en DLBP para otras industrias, existe una notable escasez de estudios específicos para el sector avícola, especialmente en el contexto colombiano.

Este proyecto busca cerrar esta brecha, desarrollando un modelo DLBP avanzado que integre la estocasticidad de la demanda y las particularidades del procesamiento avícola. La implementación de metaheurísticas permitirá generar una herramienta de apoyo a la decisión que mejore la rentabilidad, reduzca el desperdicio y fortalezca la competitividad del sector.

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

*   **Reducir costos de inventario:** Minimizando la acumulación de productos de baja rotación.
*   **Maximizar ingresos:** Aprovechando oportunidades de mercado para cortes de alta demanda.
 *   **Mejorar la eficiencia operativa:** Equilibrando la carga de trabajo en las estaciones de despiece.
*   **Reducir el desperdicio:** Contribuyendo a la sostenibilidad ambiental del sector.

El DLBP es un problema de optimización combinatoria clasificado como **NP-hard**, lo que significa que encontrar una solución óptima se vuelve computacionalmente intratable a medida que aumenta la escala del problema [@BeckerScholl2006]. Esta complejidad computacional ha motivado el desarrollo de enfoques heurísticos y metaheurísticos para encontrar soluciones de alta calidad en tiempos de cómputo razonables.

La revisión de literatura de Güngör y Gupta [-@GungorGupta2001] identifica que, aunque existe una extensa investigación en DLBP aplicado a reciclaje de electrónicos y recuperación de materiales, hay una notable escasez de estudios que aborden el DLBP en la industria de procesamiento de alimentos, y particularmente en el sector avícola.

Este anteproyecto se centra en abordar este desafío mediante el desarrollo de un modelo DLBP avanzado, que utiliza **técnicas metaheurísticas** para optimizar el proceso de despiece en la industria avícola. El objetivo es desarrollar una herramienta de apoyo a la decisión que permita a las empresas del sector mejorar su planificación, reducir sus pérdidas y fortalecer su competitividad en un mercado cada vez más exigente.

---

## 2. Planteamiento del Problema

### 2.1. Problema Central

El problema central que aborda esta investigación es el **desbalance estructural** entre la oferta de coproductos generada por el proceso de desensamble avícola y la **demanda estocástica y heterogénea del mercado**. Este desajuste, inherente a la naturaleza del negocio, se traduce en una cascada de ineficiencias operativas y pérdidas económicas que impactan a toda la cadena de valor.

### 2.2. Manifestaciones del Problema

El desbalance se manifiesta en dos frentes principales:

1.  **Excedentes de Inventario (Sobreproducción):** Cuando la producción de ciertos cortes (alas, patas, vísceras) supera la demanda del mercado, las empresas se ven forzadas a incurrir en costos adicionales de almacenamiento en frío, transporte y, en el peor de los casos, vender estos productos a precios de liquidación, erosionando significativamente los márgenes de ganancia.

2.  **Faltantes de Inventario (Subproducción):** De forma simultánea, la demanda de cortes de alto valor (pechuga) puede exceder la capacidad de producción balanceada, resultando en oportunidades de venta perdidas y una potencial insatisfacción del cliente.

### 2.3. Causas del Problema

Las causas fundamentales del desbalance incluyen:

*   **Restricción biológica:** La anatomía del ave determina proporciones fijas de cada coproducto (aproximadamente 30% pechuga, 20% muslos, 10% alas, etc.).
*   **Variabilidad de la demanda:** El mercado presenta patrones estacionales, promociones y preferencias cambiantes que no se alinean con las proporciones de la carcasa.
*   **Planificación tradicional:** Los métodos empíricos de programación no consideran la naturaleza estocástica del problema ni optimizan múltiples objetivos simultáneamente.
*   **Complejidad computacional:** El DLBP es NP-hard, lo que dificulta encontrar soluciones óptimas con métodos exactos en tiempos razonables.

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
¿Cómo puede un modelo de optimización DLBP, resuelto mediante técnicas metaheurísticas, minimizar las pérdidas económicas asociadas al desbalance entre la oferta de coproductos y la demanda del mercado en una planta de procesamiento avícola colombiana?

**Preguntas Secundarias:**

1. ¿Qué formulación matemática del DLBP captura adecuadamente las restricciones de precedencia, los tiempos de procesamiento y la variabilidad de la demanda en el contexto avícola?

2. ¿Qué técnicas metaheurísticas (Algoritmos Genéticos, Búsqueda Tabú, o híbridos) presentan el mejor desempeño para resolver el modelo DLBP propuesto?

3. ¿En qué magnitud se pueden reducir las pérdidas económicas asociadas al desbalance de carcasa mediante la implementación del modelo de optimización?

### 2.6. Hipótesis de Investigación

**Hipótesis Principal (H1):**
La aplicación de un modelo DLBP con metaheurísticas puede generar una reducción de costos de inventario superior al 30% y una mejora sustancial en la utilidad operativa, tomando como referencia el benchmark del caso de Santa Marta (Pollos Altair) [@SolanoBlanco2022].

**Hipótesis Secundarias:**

*   **H2:** Un algoritmo metaheurístico híbrido (que combine Algoritmos Genéticos y Búsqueda Tabú) superará en desempeño a cada técnica aplicada individualmente.
*   **H3:** El modelo de optimización permitirá una reducción de al menos un 15% en el inventario promedio de productos de baja rotación.

---

## 3. Objetivos

### 3.1. Objetivo General

Desarrollar un modelo de optimización basado en el Problema de Balanceo de Líneas de Desensamble (DLBP) que, mediante la aplicación de técnicas metaheurísticas, minimice las pérdidas económicas asociadas al desbalance entre la oferta de coproductos y la demanda del mercado en la industria avícola colombiana.

### 3.2. Objetivos Específicos

1.  **Formular** un modelo matemático del DLBP que capture las restricciones de precedencia, tiempos de procesamiento, balance de materiales y variabilidad de la demanda propias del procesamiento avícola.

2.  **Implementar** algoritmos metaheurísticos (Algoritmo Genético, Búsqueda Tabú y un enfoque híbrido) adaptados al problema de balanceo de carcasa avícola.

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

La optimización del balanceo de carcasa tiene un impacto directo en la rentabilidad de las empresas avícolas. Como demostró el caso de Santa Marta [@SolanoBlanco2022], las mejoras en la planificación pueden traducirse en un aumento de la utilidad operativa de hasta un **57%** y reducciones de costos de inventario superiores al **30%**. En una industria de márgenes estrechos y alto volumen, este porcentaje representa una ventaja competitiva crítica y puede significar la diferencia entre la rentabilidad y las pérdidas operativas.

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

El proyecto contribuye significativamente a la literatura del **DLBP**, extendiendo los modelos clásicos deterministas [@BeckerScholl2006] hacia enfoques estocásticos que consideran la incertidumbre de la demanda, un área identificada como línea futura de investigación por Güngör y Gupta [-@GungorGupta2001].

La **optimización multi-objetivo** en la industria alimentaria ha experimentado un avance significativo en los últimos años. Arteaga-Cabrera et al. [-@Arteaga2025] presentaron una revisión comprehensiva sobre la evolución de las estrategias de optimización en alimentos, identificando la transición desde métodos univariados tradicionales hacia técnicas multi-objetivo integradas con tecnologías emergentes. Su trabajo destaca que la industria alimentaria moderna requiere **optimizar simultáneamente múltiples objetivos competitivos** (costos de producción, eficiencia energética, calidad del producto, sostenibilidad), lo cual se alinea perfectamente con el DLBP aplicado al procesamiento avícola, donde se deben balancear simultáneamente:

- Maximización de ingresos por venta de coproductos
- Minimización de costos de inventario
- Minimización de penalizaciones por demanda no satisfecha
- Maximización del nivel de servicio al cliente

La incorporación de **algoritmos evolutivos** y metaheurísticas hibridizadas, como lo documentan Arteaga-Cabrera et al. [@Arteaga2025], ha permitido abordar estos problemas complejos de forma efectiva en la industria alimentaria, generando soluciones robustas que equilibran trade-offs entre objetivos contradictorios. Este proyecto se posiciona como una **contribución directa** a esta línea de investigación, aplicando metaheurísticas (GA, TS, híbridos) a un problema multi-objetivo del procesamiento avícola.

Adicionalmente, la comparación rigurosa de diferentes técnicas metaheurísticas (Algoritmos Genéticos, Búsqueda Tabú, y algoritmos híbridos) en el contexto específico de la industria avícola generará conocimiento valioso sobre la efectividad de estas técnicas en problemas del mundo real con características particulares (perecibilidad, estocasticidad, restricciones sanitarias).

## 5. Marco Teórico y Antecedentes

### 5.1. El Problema de Balanceo de Líneas de Desensamble (DLBP)

El **Problema de Balanceo de Líneas de Desensamble (DLBP)** es un área fundamental de la investigación de operaciones que se enfoca en la optimización de sistemas de producción donde un producto principal se descompone en varios componentes o subproductos. A diferencia de su contraparte, el Problema de Balanceo de Líneas de Ensamble (ALBP), que trata de la convergencia de partes para formar un producto, el DLBP aborda un proceso de divergencia [@BeckerScholl2006]. Investigaciones recientes han desarrollado enfoques predictivos para el DLBP que utilizan datos históricos para estimar tiempos de operación y optimizar múltiples objetivos simultáneamente, como tiempo de ciclo, eficiencia de línea y rentabilidad [@Paprocka2022].

El enfoque de Zhu et al. [@Zhu2025] es particularmente relevante para la industria avícola, donde:

- La **variabilidad del peso** de las carcasas afecta los tiempos de procesamiento.
- La **calidad variable** de cada ave (presencia de defectos, estado físico) introduce incertidumbre en el rendimiento de cada coproducto.
- Las **dependencias de secuencia** existen (por ejemplo, el corte de muslos antes de pechugas puede afectar la precisión del siguiente corte).

La incorporación de estos elementos estocásticos y dependientes de secuencia en el modelo DLBP representa un **avance significativo** en la literatura, cerrando la brecha entre los modelos deterministas clásicos y las condiciones operativas reales de las plantas de procesamiento.

En paralelo, Mete et al. [@Mete2022] realizaron un análisis comparativo exhaustivo de métodos metaheurísticos aplicados al DLBP con **tiempos de tarea estocásticos**, demostrando que los Algoritmos Genéticos superan en desempeño a otras técnicas como Simulated Annealing en términos de calidad de solución y eficiencia computacional. Su investigación propuso además una heurística constructiva basada en el **algoritmo de Dijkstra** que mostró resultados competitivos para la minimización del número de estaciones de trabajo. Este trabajo refuerza la validez del enfoque metaheurístico para el DLBP y confirma la superioridad de los Algoritmos Genéticos en contextos estocásticos, proporcionando un precedente metodológico directo para esta investigación.

Recientemente, la literatura ha evolucionado desde modelos deterministas hacia enfoques estocásticos y robustos, cruciales para entornos con alta incertidumbre como el avícola. Hu et al. [@Hu_2023] propusieron un algoritmo hiper-heurístico basado en recocido simulado para manejar la estocasticidad en líneas de desensamble paralelas, mientras que Liu et al. [@Liu_2021] desarrollaron modelos de optimización robusta para la asignación de fuerza laboral bajo incertidumbre. Asimismo, Fang et al. [@Fang_2025] introdujeron optimización dinámica basada en inferencia causal para estados de componentes inciertos. Estos avances, sumados a enfoques para tiempos de procesamiento ambiguos [@Liu_2019] y algoritmos evolutivos híbridos para problemas estocásticos multi-objetivo [@Tian_2023], proporcionan el marco teórico necesario para abordar la variabilidad inherente al procesamiento de carcasas.

Aunque el DLBP es menos común en la industria alimentaria, los problemas de programación detallada (scheduling) comparten características similares. Kopanos et al. [@Kopanos_2012] establecieron marcos matemáticos eficientes para el scheduling en procesamiento de alimentos, destacando la importancia de la perecibilidad. Akkerman y van Donk [@Akkerman_2008] analizaron la estructura de tareas en esta industria, mientras que Véghová et al. [@Veghova_2016] enfatizaron la trazabilidad en el procesamiento de carne. Estos estudios fundamentan la necesidad de adaptar los modelos clásicos de DLBP a las restricciones sanitarias y de calidad propias del sector avícola.

### 5.2. Metaheurísticas para la Optimización de Líneas de Producción

Debido a la complejidad computacional del DLBP, las **metaheurísticas** se han convertido en el enfoque predominante para resolver este tipo de problemas. Las metaheurísticas son algoritmos de optimización de alto nivel que pueden ser aplicados a una amplia gama de problemas de ingeniería complejos [@MetaheuristicsPower2023], y que a menudo se inspiran en procesos naturales. En el contexto del DLBP, estos algoritmos han demostrado ser efectivos para abordar problemas de optimización multi-criterio, como lo evidencia el trabajo de Paprocka y Skołud [@Paprocka2022], quienes optimizaron simultáneamente tiempo de ciclo, eficiencia y profit mediante un enfoque predictivo.

En el contexto de la industria alimentaria, Arteaga-Cabrera et al. [@Arteaga2025] documentaron la efectividad de **algoritmos evolutivos** y metaheurísticas para resolver problemas de optimización multi-objetivo en sistemas de producción alimentaria. Su revisión comprehensiva destaca que estas técnicas son particularmente efectivas cuando se deben equilibrar objetivos contradictorios (e.g., minimizar costos vs. maximizar calidad), una característica intrínseca del DLBP aplicado al procesamiento de carcasas avícolas. A continuación se detallan las metaheurísticas más relevantes para este proyecto:

#### 5.2.1. Algoritmos Genéticos (GA)

Los Algoritmos Genéticos, inspirados en la teoría de la evolución de Darwin, operan sobre una población de soluciones, aplicando operadores de selección, cruce y mutación para generar nuevas y mejores soluciones. Su efectividad en problemas de balanceo de líneas ha sido demostrada mediante análisis comparativos de diferentes variantes del algoritmo [@Sivasankaran2014], particularmente cuando el espacio de búsqueda es grande y complejo.

En el contexto específico del DLBP con incertidumbre, Mete et al. [@Mete2022] demostraron empíricamente que los Algoritmos Genéticos **superan consistentemente** a otras metaheurísticas (como Simulated Annealing) cuando se enfrentan a tiempos de tarea estocásticos. Su estudio comparativo, realizado sobre problemas benchmark del DLBP, mostró que los GA logran soluciones de mayor calidad en tiempos computacionales competitivos, lo que los posiciona como una técnica especialmente adecuada para el problema de balanceo de carcasas avícolas, donde la variabilidad en peso y calidad introduce estocasticidad inherente en los tiempos de procesamiento.

####  5.2.2. Búsqueda Tabú (TS)

La Búsqueda Tabú es un método de búsqueda local que utiliza una lista "tabú" para evitar volver a visitar soluciones ya exploradas y así escapar de óptimos locales. El trabajo de Suwannarongsri et al. [@Suwannarongsri2007] ha demostrado la efectividad de la búsqueda tabú híbrida en problemas de balanceo de líneas de ensamble, con resultados prometedores que pueden ser adaptados al contexto del DLBP.

#### 5.2.3. Enfoques Híbridos y Multi-objetivo
La tendencia actual prioriza el uso de algoritmos híbridos para superar las limitaciones de las técnicas individuales. Wang et al. [@Wang_2021] demostraron que combinar Algoritmos Genéticos con Recocido Simulado mejora la capacidad de escapar de óptimos locales en problemas de desensamble parcial. En el ámbito multi-objetivo, Saif et al. [@Saif_2014] aplicaron algoritmos de colonias de abejas artificiales (ABC) basados en Pareto para manejar tiempos inciertos, y Li et al. [@Li_2021] extendieron este enfoque a líneas en forma de U. Adicionalmente, Babazadeh et al. [@Babazadeh_2018_CIE] mejoraron el algoritmo NSGA-II para problemas fuzzy bi-objetivo, evidenciando la superioridad de los enfoques híbridos y evolutivos para resolver instancias complejas del DLBP.

### 5.3. Tecnologías Habilitadoras y Tendencias Recientes

Mahalik y Nambiar [@Mahalik2010] destacan la tendencia creciente hacia la automatización y el uso de sensores inteligentes en los sistemas de manufactura de alimentos, elementos clave para asegurar la calidad y trazabilidad. La integración de estos sensores [@SensorsPoultry2022] y la planificación automatizada de desensamble [@Hartono2022] en plantas de procesamiento están generando oportunidades para la implementación de modelos de optimización en tiempo real. Hartono et al. [@Hartono2022] demostraron la eficacia del *Bees Algorithm* para optimizar planes de desensamble robótico, un enfoque que podría adaptarse al procesamiento de carcasas avícolas.

Recientemente, el uso de tecnologías avanzadas como la visión por computador y la generación de datos sintéticos ha comenzado a transformar el procesamiento avícola. Feng et al. [@Feng2025] demostraron cómo el aumento de datos sintéticos puede mejorar significativamente la segmentación de instancias de carcasas de pollo, lo cual es fundamental para la automatización de procesos de despiece y control de calidad.

Asimismo, la integración de robótica colaborativa [@IndustrialRobots2023] promete flexibilizar las líneas de producción, permitiendo una mejor adaptación a la variabilidad de la materia prima. Estas innovaciones tecnológicas proporcionan la base para implementar modelos de optimización más sofisticados como el DLBP.

### 5.4. Vacíos de Investigación Identificados

A pesar de la extensa literatura sobre ALBP y el creciente interés en DLBP, la revisión del estado del arte revela varios vacíos de investigación que este proyecto busca abordar:

1.  **Falta de Modelos Específicos para la Industria Avícola:** Aunque existen modelos generales de DLBP, hay una escasez de modelos que capturen las características específicas y las complejidades del proceso de despiece avícola, como la variabilidad en el peso de las carcasas, las restricciones de calidad, la perecibilidad del producto [@Piewthongngam2019], y las demandas estacionales de los coproductos.

2.  **Integración Limitada con la Planificación de la Demanda:** Muchos de los modelos existentes asumen una demanda determinista, lo cual no refleja la realidad del mercado avícola. Es necesario desarrollar modelos que integren la estocasticidad de la demanda para generar planes de producción más robustos y realistas.

3.  **Comparación Insuficiente de Metaheurísticas en Contextos Reales:** Si bien se han aplicado diversas metaheurísticas al DLBP en contextos académicos, faltan estudios comparativos rigurosos que evalúen el desempeño de diferentes algoritmos en un conjunto de instancias de problemas realistas para la industria avícola, considerando tanto la calidad de la solución como la eficiencia computacional.

4.  **Validación con Datos Reales o Sintéticos Calibrados:** Muchos de los modelos propuestos en la literatura se validan con datos sintéticos arbitrarios o instancias de problemas de pequeña escala. Existe la necesidad de validar estos modelos con datos reales o, en su defecto, con datos sintéticos que hayan sido cuidadosamente calibrados para reflejar las condiciones operativas reales de la industria.

Este proyecto de investigación se posiciona para abordar estos vacíos, con el objetivo de desarrollar una contribución significativa tanto al campo académico del DLBP como a la práctica industrial de la gestión de la producción avícola.

---

## 6. Metodología

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
    *   Patrones de demanda históricos (cuando estén disponibles) o generados mediante distribuciones probabilísticas, siguiendo el enfoque predictivo basado en datos históricos propuesto por [@Paprocka2022].
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
*   **Documentación y Escritura:** Se redactará el documento final de tesis.
*   **Transferencia de Conocimiento:** Se preparará material de divulgación para la industria (presentaciones, infografías) que faciliten la adopción de los resultados del proyecto.

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

*   **Un modelo matemático de DLBP validado** para la industria avícola, que sirva como base para futuras investigaciones en el área.
*   **Algoritmos metaheurísticos (GA, TS e híbrido) implementados y calibrados**, que podrán ser utilizados para resolver problemas de optimización similares en otros contextos industriales.
*   **Un conjunto de datos sintéticos de prueba calibrados**, que estará a disposición de la comunidad científica para la evaluación y comparación de nuevos algoritmos para el DLBP.
<!-- *   **Un artículo científico** con los resultados de la investigación, que será enviado para su publicación en una revista indexada de alto impacto en el área de Investigación de Operaciones o Gestión de Operaciones. -->

### 8.2. Impacto Potencial en la Industria Avícola

*   **Una herramienta de software (prototipo)** que implemente el modelo y los algoritmos desarrollados, y que pueda ser utilizada por las empresas del sector para mejorar su planificación y toma de decisiones.
*   **Una reducción de costos de inventario superior al 30%** y una mejora sustancial en la utilidad operativa, tomando como referencia el benchmark del caso de Santa Marta (Pollos Altair) [@SolanoBlanco2022], validada a través de simulación rigurosa.
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

*   Solano-Blanco, A. L., et al. (2022). Integrated planning decisions in the broiler chicken supply chain. *International Transactions in Operational Research*. DOI: 10.1111/itor.12861
*   Becker, C., & Scholl, A. (1998). A survey of the assembly line balancing procedures. *European Journal of Operational Research*.
*   Güngör, A., & Gupta, S. M. (2021). Disassembly scheduling: Literature review and future research directions. *International Journal of Production Research*.
*   Akpınar, Ş., & Baykasoğlu, A. (2019). A hybrid tabu search algorithm for the assembly line balancing problem. *Computers & Industrial Engineering*.
*   Awad, M., et al. (2023). The minimisation of giveaway and underweight in poultry proportioning process. *Food Control*.

**Estadísticas oficiales:**

*   FENAVI (2023). Estadísticas del Sector Avícola Colombiano.
*   DANE (2023). Encuesta Nacional Agropecuaria (ENA).
*   FAO (2023). Poultry Production and Trade Statistics.

::: {#refs}
:::

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
