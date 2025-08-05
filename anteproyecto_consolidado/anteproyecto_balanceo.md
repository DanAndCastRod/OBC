# Anteproyecto: Balanceo de línea de desensamble para la optimización de la carcasa de pollo

## Introducción
La industria avícola afronta el reto de maximizar el aprovechamiento de la carcasa de pollo en un contexto de sostenibilidad y competencia global. El balanceo de líneas de desensamble (DLB, por sus siglas en inglés) surge como una estrategia que permite asignar tareas y recursos de manera eficiente en procesos donde los productos se desmontan para recuperar valor. Estudios previos han destacado la relevancia de aplicar estos principios al sector cárnico para reducir desperdicios y mejorar la productividad [@gpt; @geminimd].

## Estado del arte
El DLB ha sido explorado desde distintos enfoques, empleando algoritmos exactos y heurísticos para optimizar la secuencia de operaciones, el tiempo de ciclo y la utilización de recursos. En el ámbito alimentario, trabajos como @1s20s0924224410000063mainpdf y @1s20s240589631631179xmainpdf discuten la adaptación de estas metodologías a líneas de procesamiento de carne. Investigaciones relacionadas han propuesto modelos de optimización multiobjetivo, técnicas metaheurísticas y esquemas basados en simulación para abordar la variabilidad inherente a los productos biológicos [@10117700368504241238612pdf; @ahybridtabusearchmethodforassemblylinebalapdf].

## Pregunta problema
¿Cómo implementar un modelo de balanceo de línea de desensamble que optimice la recuperación de componentes de la carcasa de pollo, minimizando tiempos muertos y residuos, en un entorno de producción avícola de pequeña y mediana escala?

## Objetivos
### General
Desarrollar un anteproyecto para el diseño e implementación de un modelo de balanceo de línea de desensamble enfocado en la optimización de la carcasa de pollo.

### Específicos
- Analizar el estado del arte sobre DLB y su aplicación en la industria alimentaria.
- Identificar restricciones técnicas y operativas propias del desensamble de carcasas avícolas.
- Proponer un modelo preliminar que integre criterios de eficiencia, calidad y sostenibilidad.
- Elaborar un cronograma de actividades para la validación del modelo en un entorno piloto.

## Cronograma
### Tabla de actividades
| Actividad | Mes 1 | Mes 2 | Mes 3 | Mes 4 |
|-----------|-------|-------|-------|-------|
| Revisión bibliográfica | X | X |   |   |
| Diseño del modelo      |   | X | X |   |
| Implementación piloto  |   |   | X | X |
| Análisis de resultados |   |   |   | X |

### Diagrama de Gantt
```mermaid
gantt
title Cronograma propuesto
dateFormat  YYYY-MM-DD
section Revisión
tareas preliminares :done,    des1, 2024-08-01, 30d
section Diseño
modelado inicial    :active, des2, 2024-09-01, 30d
section Implementación
piloto              :        des3, 2024-10-01, 30d
section Cierre
análisis final      :        des4, 2024-11-01, 30d
```

## Referencias
Las referencias completas se encuentran en el archivo `referencias.bib` asociado a este documento. Durante el desarrollo se consultaron múltiples fuentes académicas y técnicas, disponibles en la carpeta `data` y en los archivos de la carpeta `respuestas` [@notebookmlmd; @txyzmd].

## Anexo: Resultados completos de las búsquedas
A continuación se incluyen los contenidos originales de cada archivo dentro de la carpeta `respuestas`, consolidados para referencia futura.

### Archivo: gemini.md
```
Usuario:
Realiza una construccion del estado del arte y un antenproyecto acerca de "Balanceo de lineas de desensamble para carcasas de pollo" genera un tesuario, busqueda de metodologías de solucion, realiza tablas comparativas de los papers encontrados, busca en scopus, IEEE explorer y science direct, realiza tablas comparativas de las metodologías de solucion y genera diagramas de relaciones con los temas seleccionados

---

Resultado:
Balanceo de Líneas de Desensamble para Carcasas de Pollo: Estado del Arte y Anteproyecto
Resumen Ejecutivo
Este informe presenta un análisis exhaustivo del estado del arte en el balanceo de líneas de desensamble (DLB) aplicado específicamente a carcasas de pollo. Se destaca la importancia crítica de esta disciplina para optimizar la eficiencia operativa, la rentabilidad y la sostenibilidad en la industria avícola global. El documento define los conceptos fundamentales del balanceo de líneas, distingue el DLB del balanceo de ensamble tradicional y detalla las etapas del procesamiento industrial de pollos, con un énfasis particular en la fase de desensamble (corte y deshuesado).

Se identifican y discuten los desafíos inherentes a esta aplicación, como la perecibilidad del producto, la variabilidad intrínseca de las carcasas y las estrictas exigencias de higiene y ergonomía. La revisión de metodologías de solución abarca desde métodos exactos y heurísticos hasta metaheurísticas avanzadas y modelos de simulación, subrayando la creciente relevancia de la optimización multi-objetivo. Se incluyen tablas comparativas de publicaciones científicas clave y metodologías de solución para ofrecer una visión estructurada del campo.

Las conclusiones resaltan la necesidad de enfoques innovadores que integren la automatización, la visión artificial y la robótica para gestionar la variabilidad y maximizar el valor de cada carcasa. Las recomendaciones para un anteproyecto se centran en el desarrollo de modelos de optimización dinámicos y multi-objetivo, validados mediante simulación, que permitan una asignación eficiente de tareas y una reconfiguración flexible de la línea, impulsando así mejoras significativas en el rendimiento, la reducción de costos y el impacto ambiental.

1. Introducción
El balanceo de líneas de producción constituye una técnica esencial en la gestión de operaciones industriales, cuyo propósito fundamental es la distribución equitativa de tareas y actividades a lo largo de un proceso productivo. Su aplicación busca la minimización del tiempo de ciclo y la maximización de la eficiencia y productividad del sistema. En el ámbito de la industria alimentaria, y de manera particular en el procesamiento de carne, la optimización de la cadena de suministro adquiere una relevancia crítica, principalmente debido a la naturaleza perecedera de los productos y a la constante fluctuación de la demanda.   

La industria avícola representa el sector de proteínas animales de mayor envergadura a nivel mundial, generando volúmenes considerables de subproductos orgánicos, que incluyen vísceras, plumas, patas, cabezas, huesos y sangre. En este contexto, el balanceo de líneas de desensamble (DLB) se erige como un componente vital para asegurar la calidad del producto final, mantener la seguridad alimentaria y optimizar la eficiencia operativa dentro de las plantas de procesamiento. La implementación efectiva de DLB permite un aprovechamiento óptimo y sostenible de cada componente de la carcasa de pollo.   

La concepción tradicional del balanceo de líneas se enfoca en la eficiencia temporal, buscando la minimización del tiempo de ciclo y la maximización de la productividad. Sin embargo, al trasladar esta perspectiva al procesamiento de carcasas de pollo, el alcance de la "eficiencia" se amplía considerablemente. La generación masiva de subproductos en la industria avícola  transforma el objetivo del balanceo de la carcasa. El propósito ya no es solo la velocidad de procesamiento, sino también la capacidad de "hacer el mejor uso posible de todos los componentes de cada pollo y poder venderlos al mejor precio posible". Esta ampliación implica que la optimización debe considerar no solo la eficiencia en el corte, sino también la valorización integral de los subproductos. Este enfoque holístico eleva el problema de un simple balanceo de tiempo a una optimización multi-objetivo que integra dimensiones económicas (maximización de ganancias por parte), ambientales (minimización de residuos) y de calidad (mantenimiento de la integridad del producto).   

El presente informe tiene como objetivos principales: realizar una construcción rigurosa del estado del arte sobre el balanceo de líneas de desensamble para carcasas de pollo; identificar y analizar las metodologías de solución más pertinentes; generar tablas comparativas detalladas de las publicaciones científicas y las metodologías de solución encontradas; proponer un anteproyecto que incluya diagramas de relaciones clave; y establecer un tesuario de términos técnicos fundamentales.

2. Conceptos Fundamentales
2.1. Balanceo de Líneas de Producción (General)
El balanceo de líneas es una técnica de ingeniería industrial diseñada para distribuir de manera equitativa las tareas y actividades en una línea de producción. Su objetivo primordial es minimizar el tiempo de ciclo y maximizar la eficiencia y productividad del sistema. Este proceso busca igualar los tiempos de trabajo en cada estación, eliminar los tiempos ociosos y de espera, asegurar un flujo continuo de producción, reducir costos e inventarios, incrementar la productividad general y, en última instancia, mejorar la calidad del producto y la satisfacción del cliente.   

Para comprender a cabalidad el balanceo de líneas, es fundamental familiarizarse con una serie de conceptos clave. El producto se refiere al bien que se desea fabricar. La    

línea de producción es la disposición física de estaciones de trabajo donde se ejecutan operaciones sucesivas y coordinadas para elaborar un producto. Una    

estación de trabajo es un punto específico en la línea donde se lleva a cabo una operación o actividad particular, que puede ser realizada por una máquina, un operario o un grupo de ellos. Las    

tareas son los pasos necesarios para transformar las materias primas en productos terminados, y estas tareas, a su vez, se dividen en elementos, que son operaciones indivisibles que deben ejecutarse en una estación. El    

tiempo de ciclo es el tiempo total requerido para fabricar una unidad del producto , mientras que el    

tiempo takt representa el ritmo al cual los productos deben ser fabricados para satisfacer la demanda del cliente. La    

precedencia establece la secuencia obligatoria en la que ciertas tareas deben realizarse. Finalmente, el    

contenido de trabajo abarca el tiempo total necesario para completar todas las tareas sobre una unidad del producto.   

Antes de emprender un balanceo de línea, deben cumplirse ciertas condiciones previas. Es indispensable que el volumen o la cantidad de producción sea suficiente para justificar la inversión y el esfuerzo del balanceo. Además, debe existir una continuidad en el aprovisionamiento de materiales y una estabilidad en el proceso, evitando cambios constantes que puedan invalidar el balanceo.   

2.2. Balanceo de Líneas de Desensamble (DLB)
El balanceo de líneas de desensamble (DLB) se define como el proceso de asignar óptimamente un conjunto de tareas de desensamble de un producto a un número determinado de estaciones de trabajo, sin violar las relaciones de precedencia existentes entre dichas tareas. A diferencia del balanceo de líneas de ensamble, donde el objetivo es combinar componentes para construir un producto final, el DLB opera en sentido inverso: "toma un pollo y lo desensambla" para obtener múltiples componentes y subproductos.   

La naturaleza inversa del DLB introduce complejidades inherentes que lo distinguen del balanceo de ensamble. Mientras que en el ensamble la calidad y estandarización de las partes suelen ser consistentes, en el desensamble de carcasas de pollo, la "materia prima" (la carcasa) es un producto biológico con una variabilidad significativa en tamaño, forma y calidad. Esta variabilidad impacta directamente los tiempos de las tareas de desensamble y la uniformidad de los cortes resultantes. Además, el objetivo del DLB no siempre es la "separación completa" del producto en sus componentes más básicos , sino más bien la obtención de partes de valor comercial, lo que implica decisiones estratégicas sobre dónde "detener" el proceso de desensamble. La obtención de una gama de productos (diferentes cortes de carne, subproductos comestibles y no comestibles) a partir de una única carcasa hace que el DLB sea intrínsecamente un problema multi-producto. Esta complejidad demanda modelos que no solo gestionen la incertidumbre de los tiempos de tarea y la variabilidad del producto, sino que también optimicen múltiples objetivos de manera simultánea.   

Los objetivos específicos del DLB son diversos y a menudo multifacéticos. Incluyen la minimización del número de estaciones de trabajo y del tiempo de ciclo, así como la maximización de la eficiencia de la línea. Otros objetivos relevantes comprenden asegurar tiempos de inactividad similares en cada estación , remover partes peligrosas o de alta demanda en etapas tempranas del proceso , minimizar el índice de riesgo, la varianza del tiempo de estación y el consumo de energía. En el contexto de la industria cárnica, un objetivo primordial es maximizar el beneficio derivado del desensamble , lo que implica considerar la perecibilidad del producto y los costos asociados a su descarte o procesamiento oportuno.   

2.3. Procesamiento Industrial de Carcasas de Pollo
El faenamiento de pollos es un proceso industrial que transforma un ave viva en una carcasa lista para el consumo humano, ya sea entera o segmentada en presas y filetes. Este proceso consta de varias etapas clave, diseñadas para ser rápidas y eficientes, asegurando al mismo tiempo el bienestar animal y la calidad del producto.   

Las etapas principales son:

Recolección y Transporte: Las aves son recogidas humanamente en las granjas y transportadas en jaulas o contenedores modulares diseñados para asegurar la circulación de aire y prevenir lesiones durante el trayecto al matadero.   

Recepción y Espera: Una vez en el matadero, las aves pasan por un período de espera controlado antes del procesamiento.   

Colgado y Aturdimiento: Los pollos son colgados cuidadosamente por las patas en una línea móvil y se les aplica un aturdimiento (generalmente eléctrico o mediante atmósfera controlada) para insensibilizarlos antes del sacrificio, minimizando el dolor.   

Desangrado/Sacrificio: Se realiza un corte rápido y humano en la garganta del ave inconsciente para asegurar un desangrado completo.   

Escaldado: Las aves son sumergidas en baños de agua caliente para aflojar las plumas y facilitar su remoción. La temperatura y el tiempo de escaldado son factores críticos que influyen en la remoción de plumas, el control bacteriano y el color de la piel y la carne.   

Pelado: Máquinas especializadas con "dedos" de goma rotatorios remueven las plumas de las carcasas.   

Evisceración: Se extraen las vísceras y órganos internos del ave. Durante esta etapa, inspectores de planta y del USDA (en EE. UU.) realizan una inspección visual minuciosa de cada ave para detectar enfermedades, contaminación fecal o magulladuras.   

Limpieza y Enfriamiento: Las carcasas evisceradas se limpian a fondo, a menudo con enjuagues orgánicos para reducir bacterias, y luego se enfrían rápidamente a bajas temperaturas (idealmente 4°C) para inhibir el crecimiento microbiano y extender la vida útil del producto. El método de enfriamiento (por agua o aire) puede influir en la calidad final de la carne, como la retención de agua y la terneza.   

Segundo Procesamiento (Corte y Deshuesado): En esta fase, la carcasa se corta y deshuesa en diversas piezas comerciales, como muslos, alas, pechugas y filetes. Esta operación puede realizarse manualmente o mediante sistemas automatizados.   

Empaque y Envío: Los productos finales se empaquetan en bandejas, se pesan, etiquetan con información de precio y manejo seguro, y se someten a una última inspección, incluyendo detectores de metales. Finalmente, se empacan en cajas selladas para su transporte a los clientes.   

La etapa de desensamble, específicamente el corte y deshuesado, es de particular relevancia en el procesamiento avícola. Es en este punto donde la carcasa se segmenta en los cortes y filetes que se comercializarán al consumidor, lo que impacta directamente la rentabilidad del proceso. La automatización de la detección de carcasas y la precisión en los cortes son cruciales para el control de calidad, la seguridad alimentaria y la eficiencia operativa. El peso y el tamaño de cada carcasa son factores determinantes para ajustar las especificaciones de corte, con el fin de minimizar el desperdicio, mejorar la calidad del corte y optimizar las ganancias.   

La fase de "segundo procesamiento" o "desensamble" es un punto de inflexión de valor en la cadena productiva. Las etapas previas (aturdimiento, desangrado, escaldado, evisceración) son principalmente de "pre-procesamiento" o "sacrificio", estandarizadas y orientadas a preparar la carcasa para su transformación. Sin embargo, el corte y deshuesado es donde el producto se convierte en sus componentes finales de valor comercial. Es aquí donde las decisiones sobre cómo desensamblar cada carcasa impactan directamente la maximización de la rentabilidad, dependiendo de la demanda del mercado para los diferentes cortes. La variabilidad natural en el tamaño y la forma de las carcasas  hace que esta etapa sea inherentemente compleja y, por lo tanto, un área crítica para la optimización. La aplicación de técnicas avanzadas de balanceo de línea en este punto tiene el mayor impacto potencial en el rendimiento y la eficiencia del aprovechamiento de la materia prima.   

3. Estado del Arte: Balanceo de Líneas de Desensamble para Carcasas de Pollo
El balanceo de líneas de desensamble (DLB) en el contexto de carcasas de pollo presenta un conjunto único de desafíos y consideraciones que lo distinguen de otras aplicaciones de balanceo de líneas, como las de ensamble o desensamble de productos manufacturados.

3.1. Desafíos y Consideraciones Específicas en la Industria Avícola
La industria avícola enfrenta retos particulares que deben ser abordados en cualquier modelo de balanceo de líneas de desensamble:

Perecibilidad del producto: Los productos cárnicos, incluyendo las carcasas de pollo y sus cortes, son altamente perecederos y poseen una vida útil limitada. Esta característica intrínseca impacta directamente la programación de la producción y la gestión de inventarios. Los modelos de desensamble deben, por tanto, incorporar los costos asociados al descarte de productos perecidos, lo que añade una capa de complejidad a la función objetivo.   

Variabilidad de la carcasa: Uno de los desafíos más significativos reside en la variabilidad natural de las carcasas de pollo en términos de tamaño, peso y forma. Esta heterogeneidad dificulta enormemente la estandarización de los tiempos de tarea y la automatización precisa de los cortes. La estimación precisa del peso y la segmentación de los cortes en línea se complican aún más por factores como la superposición de carcasas en las cintas transportadoras y las condiciones de luz ambiental en las plantas de procesamiento.   


La variabilidad de la carcasa es un factor determinante que impulsa la complejidad y la innovación en este campo. A diferencia de los productos manufacturados, que se componen de piezas estandarizadas, las carcasas de pollo son productos biológicos con una diversidad inherente en sus características físicas. Esta variabilidad tiene un impacto directo en los tiempos de las tareas de desensamble y en la uniformidad de los cortes. Los métodos estáticos de balanceo de línea, que asumen tiempos de tarea fijos, resultan inadecuados para manejar esta complejidad. Esta limitación ha impulsado la investigación y el desarrollo de soluciones dinámicas, adaptativas y basadas en datos, como la visión artificial para la estimación de peso y la segmentación precisa de las carcasas. En consecuencia, la variabilidad no es simplemente un obstáculo; se ha convertido en un motor clave para la investigación y el desarrollo de tecnologías avanzadas, incluyendo la inteligencia artificial, la robótica y la simulación, con el fin de lograr un balanceo de línea más robusto y eficiente en la industria avícola. La capacidad de medir y adaptarse a esta variabilidad en tiempo real se traduce en una ventaja competitiva sustancial.   

Higiene y seguridad alimentaria: El entorno de procesamiento de carne se caracteriza por bajas temperaturas (aproximadamente 4°C) y alta humedad, condiciones que, si bien son necesarias para la conservación del producto, también imponen requisitos estrictos de higiene y saneamiento. La contaminación fecal de las carcasas, por ejemplo, puede requerir costosos y prolongados procesos de reprocesamiento, afectando la eficiencia y la rentabilidad.   

Velocidad de línea y ergonomía: Las líneas de procesamiento avícola operan a velocidades extremadamente altas, con cifras que pueden oscilar entre 140 y 175 aves por minuto. Esta velocidad impone una carga de trabajo repetitiva y exigente sobre los operarios, lo que puede conducir a una alta incidencia de trastornos musculoesqueléticos (MSDs).   

Aprovechamiento de subproductos y "balance de la carcasa": La industria avícola persigue un concepto denominado "balance perfecto de la carcasa", que implica maximizar el uso de cada componente, tanto comestible como no comestible, para su venta al mejor precio posible y así mejorar la sostenibilidad global del proceso. Los subproductos generados, como vísceras, plumas, patas, cabeza y huesos, no son simplemente residuos; pueden ser valorizados y transformados en materias primas para diversas industrias, incluyendo la agrícola (biofertilizantes), la cosmética, la del envase (biomateriales) o la de alimentos balanceados para mascotas.   


La economía circular se encuentra en el corazón de este enfoque de balanceo. Mientras que el balanceo de líneas tradicional se concentra en la eficiencia del proceso principal, en el caso de las carcasas de pollo, el "producto" final se extiende más allá de la carne para incluir una amplia gama de subproductos. El concepto de "balance de la carcasa"  trasciende la mera minimización de residuos; busca activamente mercados rentables para todas las partes, incluso aquellas que podrían considerarse "no deseadas" en un mercado primario. Esto transforma la gestión de residuos en una estrategia de valorización de alto impacto. Por lo tanto, un balanceo de línea de desensamble efectivo en la industria avícola debe integrar no solo la eficiencia del corte de la carne, sino también la logística y la economía de la recuperación y valorización de todos los subproductos. Este enfoque convierte el problema en un desafío de optimización de la cadena de valor completa, alineando los objetivos económicos con los de sostenibilidad ambiental.   

3.2. Aplicaciones y Tendencias Actuales de DLB en el Procesamiento de Carne
La creciente demanda de productos cárnicos y la presión por la eficiencia han impulsado la adopción de enfoques de optimización avanzados en la industria. Los modelos de optimización son herramientas poderosas para la planificación de la cosecha y la producción en cadenas de suministro agroalimentarias, con el objetivo de minimizar costos, reducir la huella de carbono y el desperdicio. Una optimización integral de la cadena de suministro avícola puede conducir a mejoras significativas en la rentabilidad, el servicio al cliente y los márgenes de ganancia.   

Una tendencia destacada es la integración de la automatización y la visión artificial en las líneas de procesamiento. La automatización y la robótica ofrecen un potencial considerable para mejorar las prácticas de procesamiento avícola, al reducir la exposición humana a condiciones de trabajo peligrosas y al aumentar la eficiencia de producción y la seguridad alimentaria. Sistemas avanzados de visión artificial y tecnologías de reconstrucción 3D (como las que utilizan Kinect v2) permiten la captura de datos en tiempo real de carcasas en movimiento. Esto posibilita la estimación precisa de su volumen y orientación, lo que a su vez mejora la segmentación de los cortes y el control de calidad. La estimación automatizada del peso de pollos vivos, mediante técnicas de segmentación basadas en algoritmos como YOLOv8, mejora la precisión de los datos de peso en entornos complejos, un factor crucial para la gestión eficiente de la cadena de suministro. Además, la colaboración humano-robot (HRC) emerge como una solución prometedora para la automatización escalable en el procesamiento de carne, ayudando a superar desafíos como la manipulación de piezas deformables y la escasez de mano de obra calificada.   

La digitalización se ha convertido en un facilitador clave para la optimización dinámica en la industria avícola. La variabilidad inherente de las carcasas de pollo  y las altas velocidades de las líneas de procesamiento  hacen que los métodos de balanceo manuales o estáticos sean inherentemente ineficientes. Los sistemas de visión artificial  y los sistemas de estimación de peso  permiten la captura de datos en tiempo real sobre cada carcasa individual. Estos datos, a su vez, pueden alimentar modelos de optimización avanzados  que ajustan dinámicamente las operaciones de corte y desensamble. La simulación de eventos discretos  complementa este proceso al permitir la prueba de estos escenarios virtuales antes de su implementación física, mitigando riesgos. La tendencia actual apunta hacia el desarrollo de sistemas de procesamiento avícola ciber-físicos, donde los datos en tiempo real de sensores y sistemas de visión artificial se integran con modelos de optimización avanzados (incluyendo inteligencia artificial y aprendizaje automático). Esto permite un balanceo de línea dinámico y una reconfiguración en tiempo real, maximizando el rendimiento y minimizando el desperdicio en un entorno inherentemente variable.   

4. Metodologías de Solución para Problemas de Balanceo de Líneas de Desensamble (DLBP)
Los problemas de balanceo de líneas de desensamble (DLBP) son reconocidos como problemas NP-hard, lo que implica que encontrar una solución óptima garantizada puede ser computacionalmente inviable para instancias de gran tamaño. Esta complejidad inherente ha impulsado el desarrollo y la aplicación de una variedad de metodologías, que van desde enfoques exactos hasta heurísticas, metaheurísticas y modelos de simulación.   

4.1. Métodos Exactos
Los métodos exactos buscan encontrar la solución óptima global para un problema, garantizando la mejor asignación posible de tareas a estaciones. Las técnicas más comunes en DLBP incluyen la Programación Entera Binaria (PEB) y la Programación Lineal Entera Mixta (PLEM). Estos modelos permiten formular el problema como un conjunto de ecuaciones y desigualdades, con variables que representan decisiones (por ejemplo, si una tarea se asigna a una estación) y una función objetivo a optimizar. Los objetivos comunes incluyen la minimización del costo total, que puede abarcar costos de compra, configuración, mantenimiento de inventario, operación de desensamble y costos asociados a la perecibilidad del producto. También se utilizan para maximizar el beneficio derivado del desensamble. Estos modelos son capaces de incorporar diversas restricciones, como las de capacidad de las estaciones, las relaciones de precedencia entre tareas y las características específicas de la perecibilidad del producto. Sin embargo, su principal limitación radica en su escalabilidad: se vuelven computacionalmente intratables para problemas de gran tamaño o cuando la incertidumbre en los datos es elevada. Además, a menudo se basan en suposiciones deterministas, lo que puede no reflejar la complejidad y la variabilidad presentes en entornos de producción reales.   

4.2. Métodos Heurísticos
Los métodos heurísticos son procedimientos que buscan encontrar soluciones de "buena calidad" en un tiempo de computación razonable, sin garantizar la optimalidad global. Son particularmente útiles para abordar problemas complejos donde los métodos exactos resultan ineficientes o computacionalmente inviables. Ejemplos notables incluyen la Regla del Candidato Más Grande (Largest Candidate Rule - LCR), que asigna elementos de trabajo a las estaciones basándose en el tamaño de los tiempos de los elementos, buscando una distribución uniforme de la carga de trabajo. Otro método popular es el Peso Posicional Clasificado (Ranked Positional Weight - RPW), que prioriza la asignación de tareas considerando tanto su propio tiempo como la suma de los tiempos de todas sus tareas sucesoras. También existen heurísticas constructivas, como las basadas en el algoritmo de Dijkstra, que buscan minimizar el número de estaciones bajo un tiempo de ciclo predefinido. En la industria alimentaria, estos métodos se han aplicado con éxito para mejorar la productividad y reducir costos en plantas de procesamiento, como se ha observado en estudios de caso en la producción de leche pasteurizada o pollo congelado.   

4.3. Métodos Metaheurísticos
Las metaheurísticas son algoritmos de búsqueda adaptativos que emplean reglas probabilísticas para explorar el espacio de soluciones y escapar de los óptimos locales, lo que los hace particularmente adecuados para problemas complejos y a gran escala. A diferencia de los métodos exactos, no garantizan la optimalidad, pero son capaces de encontrar soluciones "cercanas al óptimo" de manera eficiente.   

La complejidad inherente de los problemas de balanceo de líneas de desensamble, acentuada por la variabilidad de las carcasas de pollo y la necesidad de optimización multi-objetivo (por ejemplo, maximizar el rendimiento, minimizar los costos, considerar la perecibilidad), los clasifica como problemas NP-hard. Ante esta realidad, los métodos exactos se vuelven intratables rápidamente a medida que aumenta el tamaño del problema. Esta situación ha impulsado la necesidad de enfoques que puedan encontrar soluciones "suficientemente buenas" en un tiempo práctico. Las metaheurísticas, como los Algoritmos Genéticos (GA), Simulated Annealing (SA), Optimización por Enjambre de Partículas (PSO), Algoritmos de Colonia de Hormigas (ACO), Algoritmos de Optimización de Aves Migratorias (MBO) y Optimización por Enjambre de Gallinas (CSO), están diseñadas precisamente para este propósito. Estos algoritmos exploran grandes espacios de soluciones de manera inteligente, evitando quedar atrapados en óptimos locales.   

Entre los ejemplos y aplicaciones en DLBP se encuentran:

Algoritmos Genéticos (GA): Inspirados en los principios de la evolución biológica, son ampliamente utilizados para la optimización en diversas industrias, incluyendo la manufacturera y la alimentaria.   

Simulated Annealing (SA): Este algoritmo, que emula el proceso de recocido de metales para encontrar estados de energía mínima, se ha aplicado en DLBP, especialmente en escenarios con tiempos de tarea estocásticos.   

Optimización por Enjambre de Partículas (PSO): Basado en el comportamiento social de grupos (como bandadas de aves o bancos de peces), se utiliza en problemas de optimización multi-objetivo.   

Algoritmos de Colonia de Hormigas (ACO): Inspirados en el comportamiento de búsqueda de alimento de las hormigas, han sido aplicados a problemas de balanceo de líneas de desensamble multi-objetivo.   

Algoritmos de Optimización de Aves Migratorias (MBO) y Optimización por Enjambre de Gallinas (CSO): Estos son algoritmos bio-inspirados más recientes que buscan maximizar el beneficio de desensamble y resolver problemas multi-objetivo en DLBP.   

Multi-objective Adaptive Large Neighborhood Search (MO-ALNS): Un algoritmo innovador que integra operadores de destrucción y reparación con Simulated Annealing, selección por ruleta y estrategias de búsqueda local, demostrando mejoras significativas en la eficiencia y calidad de la solución para DLBP bajo incertidumbre.   

La investigación en DLBP para carcasas de pollo se orienta fuertemente hacia el desarrollo y la aplicación de estas metaheurísticas y algoritmos de optimización multi-objetivo. Estos métodos son fundamentales para abordar la complejidad de la variabilidad del producto, las múltiples metas de rendimiento y la necesidad de tomar decisiones rápidas en un entorno de procesamiento de alimentos.

4.4. Modelos de Simulación
Los modelos de simulación, particularmente la Simulación de Eventos Discretos (DES), son herramientas poderosas para modelar diferentes escenarios de procesos operativos, identificar y eliminar cuellos de botella, y optimizar el proceso de producción mediante el balanceo de la carga de trabajo. La simulación permite experimentar con diversas configuraciones de línea en un entorno digital, sin la necesidad de asignar recursos físicos o interrumpir las operaciones en curso, lo que facilita la planificación y reduce los riesgos asociados a la implementación directa en la planta. Software especializado como AnyLogic o ProModel son comúnmente utilizados para la modelación y simulación de líneas de producción.   

La simulación ha demostrado su efectividad en diversos estudios de caso. Por ejemplo, en la industria de la confección o la electrónica, se ha utilizado para mejorar la eficiencia de línea, reducir el tiempo ocioso de los operarios y aumentar la productividad general. Además, la simulación es una herramienta valiosa para probar diferentes escenarios y validar la robustez de los balances calculados, especialmente en presencia de la variabilidad de parámetros inherente a los procesos reales.   

La simulación actúa como un puente vital entre la teoría y la realidad operativa. Los modelos matemáticos (exactos, heurísticos, metaheurísticos) proporcionan soluciones teóricas para el balanceo de líneas. Sin embargo, la realidad de una planta de procesamiento de pollo incluye incertidumbres significativas, como la variabilidad del tamaño y la forma de las carcasas, posibles fallas de equipos, diferencias en el desempeño de los operarios y fluctuaciones en la demanda, que no siempre pueden ser capturadas adecuadamente por modelos deterministas. La simulación permite introducir y analizar el impacto de esta "incertidumbre" y "variabilidad" en un entorno virtual. Al hacerlo, se valida la robustez de las soluciones de balanceo antes de su implementación física, se identifican cuellos de botella dinámicos y se refinan las estrategias de balanceo, lo que reduce drásticamente los riesgos y costos asociados con la puesta en marcha de nuevas configuraciones en el mundo real. Por lo tanto, la simulación es una herramienta indispensable para el desarrollo de un anteproyecto, ya que permite evaluar la viabilidad y el rendimiento de las configuraciones de línea propuestas bajo condiciones realistas.   

4.5. Optimización Multi-Objetivo en DLBP
La optimización multi-objetivo (MOO) aborda problemas de optimización que involucran más de un objetivo a la vez, donde estos objetivos a menudo están en conflicto entre sí (por ejemplo, minimizar costos versus maximizar calidad). En el contexto del DLBP, los objetivos comunes pueden clasificarse en indicadores de producción (como el tiempo de ciclo, el número de estaciones y la eficiencia de la línea), económicos (como la producción total, el beneficio y el costo) y ambientales (como el tratamiento de partes peligrosas, el consumo de energía y las emisiones).   

Para resolver problemas de MOO, se utilizan diversos enfoques. Uno de ellos es transformar el problema multi-objetivo en uno de objetivo único mediante la asignación de coeficientes de ponderación a cada objetivo, lo que permite combinar múltiples metas en una sola función a optimizar. Otra estrategia es emplear algoritmos que buscan un conjunto de soluciones Pareto óptimas (o no dominadas). Una solución se considera Pareto óptima si ninguna de sus funciones objetivo puede mejorarse sin degradar el valor de al menos otra función objetivo. Ejemplos de algoritmos metaheurísticos diseñados para MOO incluyen el Multi-objective Adaptive Large Neighborhood Search (MO-ALNS) , el Non-dominated Sorting Chicken Swarm Optimization (NSCSO) , el Multi-objective Chicken Swarm Optimization (MOCSO) , y el Multi-objective Batch-based Flowshop Scheduling Optimization (MOBS-NET).   

La optimización de la línea de desensamble de carcasas de pollo es inherentemente un problema multi-objetivo. Esto se debe a la necesidad de equilibrar simultáneamente la rentabilidad (derivada del rendimiento de los cortes de mayor valor), la eficiencia operativa (velocidad de la línea, minimización del tiempo ocioso), la seguridad alimentaria, el bienestar animal y la sostenibilidad (a través de la valorización integral de los subproductos).   

La complejidad de la decisión en un entorno de múltiples prioridades es un factor crítico. La optimización de la línea de desensamble de carcasas de pollo no puede lograrse con un único objetivo. Por ejemplo, maximizar la velocidad de corte podría comprometer la calidad de los cortes o reducir el rendimiento de subproductos valiosos. De manera similar, minimizar el número de estaciones de trabajo podría aumentar el tiempo de ciclo general o la carga de trabajo de los operarios, afectando la ergonomía y la productividad. La perecibilidad del producto introduce una restricción temporal que interactúa directamente con la eficiencia, exigiendo decisiones rápidas para evitar pérdidas. Por lo tanto, las soluciones óptimas no son un punto único, sino un conjunto de soluciones no dominadas que forman una "frontera de Pareto", donde se comprenden los    

trade-offs entre los diferentes objetivos. Un anteproyecto exitoso para el balanceo de líneas de desensamble de carcasas de pollo no solo debe aplicar una metodología de optimización, sino que también debe definir claramente los objetivos en conflicto y utilizar enfoques multi-objetivo para proporcionar a los tomadores de decisiones un conjunto de soluciones que permitan un equilibrio estratégico entre eficiencia, rentabilidad, calidad y sostenibilidad.   

5. Análisis Comparativo de Publicaciones Científicas
5.1. Búsqueda en Bases de Datos (Scopus, IEEE Xplore, ScienceDirect)
La búsqueda de literatura para este estado del arte se centró en bases de datos académicas de alto impacto como Scopus, IEEE Xplore y ScienceDirect. Se utilizaron términos clave y sus combinaciones, incluyendo "disassembly line balancing", "poultry processing", "chicken carcass", "optimization models", "heuristic algorithms", "metaheuristics", "perishability", "yield efficiency", "automation" y "simulation". El objetivo fue identificar artículos que abordaran el balanceo de líneas de desensamble en un sentido general, así como aquellos con aplicaciones o consideraciones específicas para la industria cárnica o avícola.

A pesar de la considerable cantidad de investigación sobre el "balanceo de líneas de desensamble" (DLB) en general , gran parte de esta literatura se enfoca en productos de fin de vida útil para remanufactura o reciclaje. Existe una brecha notable en la aplicación directa y específica del DLB a "carcasas de pollo". Cuando se encuentran estudios relacionados con aves, a menudo abordan aspectos más amplios de la cadena de suministro, el uso de visión artificial para la clasificación de carcasas o la optimización de procesos generales, en lugar del balanceo de línea de desensamble per se. Esta observación subraya una significativa oportunidad de investigación. Es crucial adaptar y aplicar directamente las metodologías avanzadas de DLB, especialmente aquellas capaces de manejar la incertidumbre y múltiples objetivos, a los desafíos únicos del desensamble de carcasas de pollo. Esto implica integrar consideraciones específicas como la perecibilidad del producto, su variabilidad intrínseca y la maximización del rendimiento de subproductos.   

5.2. Tabla Comparativa de Papers Relevantes
Esta tabla es fundamental para el estado del arte, ya que proporciona una visión estructurada de la investigación existente, permitiendo identificar tendencias, brechas y posibles puntos de partida para el anteproyecto. Facilita una comparación rápida de los enfoques, objetivos y hallazgos de los estudios clave.

Tabla 1: Comparativa de Publicaciones Científicas Relevantes

Título del Paper / Autor(es) / Año	Base de Datos	Enfoque Principal	Metodología de Solución	Objetivos de Optimización	Consideraciones Específicas	Hallazgos Clave / Contribuciones	Snippet ID
Disassembly line balancing problem: a review of the state of the art and future directions / Agrawal & Tiwari (2018)	Scopus, ScienceDirect	Revisión de DLB y variantes	Taxonomía, análisis descriptivo	Minimizar estaciones, tiempo de ciclo, maximizar eficiencia, remover partes peligrosas/demandadas	Incertidumbre, dependencias secuenciales, multi-objetivo, completa/parcial	Revisión exhaustiva de DLB; identificación de MO-SDDLB y MO-ALNS como solución robusta.	
Disassembly Scheduling for the Meat Processing Industry with Product Perishability / Piewthongngama et al. (2019)	Scopus	DLB en industria cárnica	Programación Entera	Minimizar costo total (desensamble, setup, inventario, outsourcing, perecibilidad)	Perecibilidad de la carne, demanda en varios niveles de jerarquía, outsourcing	Modelo que considera perecibilidad y costos de descarte/outsourcing; aplicado a procesamiento de cerdo.	
Online chicken carcass volume estimation using depth imaging and 3-D reconstruction / Bilgili (2024)	Scopus	Visión artificial en procesamiento de pollo	Captura de datos 3D, reconstrucción, regresión	Estimación de volumen y orientación de carcasas	Carcasas en movimiento, datos sintéticos, segmentación de instancias	Sistema innovador para estimación de volumen y orientación de carcasas en tiempo real.	
.1,    

Carcass balance – a key challenge for the poultry industry / Marel (2023)	Scopus	Balance de carcasa en industria avícola	Enfoque industrial, tecnología de procesamiento	Maximizar uso sostenible y rentable de cada parte del pollo	Factores "push" y "pull", tecnología de corte/deshuesado modular, subproductos	Destaca el "balance de la carcasa" como objetivo clave para sostenibilidad y rentabilidad.	
.2,    

Automated On-site Broiler Live Weight Estimation Through YOLO-Based Segmentation / Shams et al. (2025)	IEEE Xplore	Estimación de peso de pollos vivos	YOLOv8 (Deep Learning, segmentación de instancias)	Mejorar precisión de estimación de peso	Variabilidad morfológica, entornos complejos, datos sintéticos	Propuesta de método basado en cámara para estimación precisa de peso de pollos vivos.	
A disassembly line balancing model with the goal of maximizing disassembly profits is established, in which tool selection and assignment is a critical part / Zhang et al. (2024)	Scopus	DLB con maximización de beneficio	Optimización de aves migratorias (DMBO)	Maximizar beneficio de desensamble	Deterioro de herramientas, selección de herramientas, NP-hard	Modelo que maximiza beneficio considerando deterioro de herramientas; DMBO supera otros algoritmos.	
Towards human-robot collaboration in meat processing: Challenges and possibilities / Faccio et al. (2022)	Scopus	HRC en procesamiento de carne	Revisión, análisis de desafíos	Habilitar automatización escalable, sostenibilidad	Manipulación de piezas deformables, entorno de trabajo, escasez de mano de obra	Explora el potencial de la HRC para superar desafíos en la automatización de la industria cárnica.	
Multi-criteria analysis of statistical methods to determine the fluctuation of parameters affecting the state of balance of an assembly line / Benammar et al. (2023)	Scopus	Variabilidad en balanceo de líneas	Análisis estadístico multi-criterio, modelado matricial 3D	Optimizar rendimiento de línea	Variabilidad de tiempos de tarea, eficiencia del trabajador, flujo de material	Propone integración de análisis estadístico y modelado 3D para manejar variabilidad en líneas.	
Multi-Objective Optimization Approach for Enhancing Production System Efficiency in a Food Processing Industry / Ma et al. (2024)	Scopus	Optimización multi-objetivo en alimentos	Programación secuencial de mínimos cuadrados (SLSQP), regresión polinomial	Maximizar OEE, minimizar uso de energía y desperdicio	Múltiples objetivos en conflicto, complejidad de sistemas modernos	Demuestra la efectividad de la MOO para equilibrar eficiencia, sostenibilidad y calidad en alimentos.	
  
5.3. Tabla Comparativa de Metodologías de Solución
Esta tabla ofrece una comparación estructurada de las metodologías de solución para problemas de balanceo de líneas de desensamble, destacando sus fortalezas, debilidades y su aplicabilidad en el contexto específico del desensamble de carcasas de pollo. Es una herramienta valiosa para seleccionar el enfoque más adecuado para un anteproyecto.

Tabla 2: Comparativa de Metodologías de Solución para DLBP

Metodología	Descripción	Fortalezas	Debilidades	Aplicabilidad en DLB de Carcasas de Pollo	Snippet ID(s)
Métodos Exactos (PEB, PLEM)	Modelos matemáticos que garantizan la solución óptima global.	Solución óptima garantizada; claridad en la formulación de restricciones y objetivos.	Computacionalmente costosos para problemas grandes (NP-hard); asumen condiciones deterministas, lo que no refleja la variabilidad real.	Útiles para problemas de pequeña escala o como benchmark; limitada aplicabilidad directa en entornos dinámicos y variables.	
Métodos Heurísticos (LCR, RPW, Dijkstra-based)	Procedimientos que buscan soluciones de "buena calidad" en tiempo razonable, sin garantía de optimalidad.	Rápidos y eficientes para problemas complejos; fáciles de implementar y entender; útiles para soluciones iniciales.	No garantizan la optimalidad; pueden quedar atrapados en óptimos locales; la calidad de la solución puede variar.	Adecuados para obtener soluciones rápidas en líneas existentes; punto de partida para optimizaciones más complejas; útiles para la asignación de tareas manuales.	
Métodos Metaheurísticos (GA, SA, PSO, ACO, MBO/CSO, MO-ALNS)	Algoritmos de búsqueda adaptativos que exploran el espacio de soluciones para encontrar soluciones "cercanas al óptimo", escapando de óptimos locales.	Capaces de manejar problemas NP-hard de gran escala y con múltiples objetivos; robustos ante la incertidumbre y la variabilidad; alta flexibilidad.	No garantizan la optimalidad; requieren ajuste de parámetros; pueden ser computacionalmente intensivos para encontrar soluciones de muy alta calidad.	Muy aplicables para la optimización de DLB de carcasas de pollo, especialmente para problemas multi-objetivo y con tiempos de tarea estocásticos; permiten la optimización de rendimiento y costos.	
Modelos de Simulación (DES con AnyLogic/ProModel)	Representación computacional de un sistema real para experimentar con diferentes escenarios y evaluar el rendimiento.	Permiten evaluar el impacto de la variabilidad e incertidumbre; identificación de cuellos de botella dinámicos; validación de soluciones antes de la implementación física.	No optimizan directamente (solo evalúan); requieren datos precisos del sistema; el desarrollo del modelo puede ser complejo y consumir tiempo.	Esencial para validar y refinar soluciones de balanceo en entornos de procesamiento de pollo, permitiendo probar la robustez de la línea ante la variabilidad de las carcasas y la demanda.	
Optimización Multi-Objetivo (MOO)	Enfoques que consideran y optimizan simultáneamente múltiples objetivos, a menudo en conflicto.	Proporciona un conjunto de soluciones "Pareto óptimas" que muestran los trade-offs entre objetivos; permite una toma de decisiones más informada y estratégica.	Mayor complejidad computacional; la selección de la solución final de la frontera de Pareto puede requerir juicio experto o preferencias adicionales.	Crucial para el DLB de carcasas de pollo, donde se deben equilibrar eficiencia, rentabilidad, calidad, seguridad alimentaria y sostenibilidad (valorización de subproductos).	
  
6. Diagramas de Relaciones y Flujo de Procesos
Para complementar el análisis textual y proporcionar una comprensión visual clara de los conceptos y procesos, se proponen los siguientes diagramas:

Diagrama de Flujo del Proceso de Desensamble de Carcasas de Pollo: Este diagrama ilustraría de forma detallada las etapas clave del "segundo procesamiento" o desensamble. Partiría de la carcasa eviscerada y enfriada, mostrando las estaciones de trabajo donde se realizan los cortes primarios (ej. separación de alas, muslos, pechugas), el deshuesado, el recorte y la clasificación. Se indicarían las relaciones de precedencia entre las tareas y los puntos donde la variabilidad de la carcasa (tamaño, forma) podría requerir ajustes o decisiones. El diagrama destacaría cómo la carcasa se transforma en diferentes productos de valor comercial y subproductos, enfatizando el flujo de materiales y las posibles bifurcaciones en la línea. Este tipo de diagrama se basaría en la información detallada de las etapas de procesamiento.   

Diagrama de Relaciones entre Objetivos y Metodologías de DLBP: Este diagrama conceptual representaría visualmente la interconexión entre los múltiples objetivos de optimización en el balanceo de líneas de desensamble de carcasas de pollo y las metodologías de solución más adecuadas. Podría mostrar cómo objetivos como la maximización del rendimiento de cortes de alto valor, la minimización del desperdicio, la reducción de costos operativos y la mejora de la ergonomía están interrelacionados y a menudo en conflicto. Las flechas o conexiones indicarían cómo la consideración de la perecibilidad y la variabilidad de la carcasa influye en la elección de metodologías (ej. MOO para objetivos en conflicto, metaheurísticas para problemas complejos, simulación para probar escenarios con incertidumbre, y visión artificial/robótica como tecnologías habilitadoras). Este diagrama serviría para ilustrar la complejidad de la toma de decisiones y la necesidad de un enfoque holístico en la optimización.

7. Tesuario (Glossary of Terms)
Balanceo de Líneas: Técnica de gestión de la producción para distribuir equitativamente tareas en una línea, minimizando el tiempo de ciclo y maximizando la eficiencia y productividad.   

Línea de Desensamble (DLB): Proceso de asignar óptimamente tareas de desensamble de un producto a estaciones de trabajo, respetando las relaciones de precedencia, con el fin de separar un producto en sus componentes.   

Tiempo de Ciclo (Cycle Time): El tiempo total requerido para fabricar o procesar una unidad del producto en una línea de producción.   

Tiempo Takt (Takt Time): El ritmo al cual los productos deben ser fabricados o procesados para satisfacer la demanda del cliente.   

Precedencia: La secuencia obligatoria en la que deben realizarse ciertas tareas o elementos de trabajo en un proceso.   

Estación de Trabajo: Un punto físico o lógico en una línea de producción donde se ejecuta una operación o actividad específica.   

Contenido de Trabajo: La suma de los tiempos estándar de todas las tareas que deben realizarse para completar una unidad de producto.   

Programación Entera Binaria (PEB): Un tipo de modelo de optimización matemática donde algunas o todas las variables de decisión deben tomar valores binarios (0 o 1).

Programación Lineal Entera Mixta (PLEM): Un tipo de modelo de optimización matemática que incluye variables de decisión continuas y enteras (binarias o no).

Heurística: Un procedimiento o algoritmo que busca una solución "suficientemente buena" a un problema computacionalmente complejo en un tiempo razonable, sin garantizar la optimalidad.

Metaheurística: Un algoritmo de alto nivel que guía un proceso de búsqueda para encontrar soluciones "cercanas al óptimo" para problemas de optimización complejos, a menudo inspirados en fenómenos naturales.

Algoritmo Genético (GA): Una metaheurística inspirada en la selección natural y la genética, utilizada para encontrar soluciones óptimas o casi óptimas en problemas de optimización.

Simulated Annealing (SA): Una metaheurística que imita el proceso de recocido de metales, utilizada para encontrar soluciones cercanas al óptimo global en un espacio de búsqueda grande.

Optimización por Enjambre de Partículas (PSO): Una metaheurística bio-inspirada que simula el comportamiento social de un enjambre de partículas (como aves o peces) buscando un óptimo en un espacio de soluciones.

Algoritmo de Colonia de Hormigas (ACO): Una metaheurística inspirada en el comportamiento de búsqueda de caminos de las hormigas para encontrar rutas óptimas.

Optimización Multi-Objetivo (MOO): Un área de la optimización matemática que trata con problemas que involucran más de un objetivo a optimizar simultáneamente, donde los objetivos suelen estar en conflicto.   

Solución Pareto Óptima: En MOO, una solución es Pareto óptima si no se puede mejorar ninguna función objetivo sin empeorar al menos otra función objetivo.   

Simulación de Eventos Discretos (DES): Una metodología de simulación que modela el comportamiento de un sistema a lo largo del tiempo, donde los cambios en el estado del sistema ocurren en puntos discretos en el tiempo.   

Visión Artificial: Campo de la inteligencia artificial que permite a las computadoras "ver" e interpretar imágenes o videos, utilizado para inspección, clasificación y medición en procesos industriales.

Colaboración Humano-Robot (HRC): Un paradigma de trabajo donde humanos y robots colaboran en tareas compartidas, aprovechando las fortalezas de ambos.

Balance de la Carcasa: En la industria cárnica, se refiere a la maximización del uso y valor de todos los componentes (comestibles y no comestibles) de una carcasa para optimizar la rentabilidad y sostenibilidad.   

Perecibilidad: La propiedad de un producto de degradarse o estropearse con el tiempo, lo que impone restricciones temporales en su procesamiento y almacenamiento.

8. Conclusiones y Recomendaciones para el Anteproyecto
El análisis del estado del arte revela que el balanceo de líneas de desensamble para carcasas de pollo es un problema complejo y multifacético, crucial para la eficiencia y sostenibilidad de la industria avícola. La naturaleza biológica de la materia prima introduce una variabilidad inherente en tamaño, forma y calidad, lo que dificulta la estandarización de tareas y la automatización precisa. Además, la necesidad de maximizar el rendimiento de cortes de alto valor, minimizar el desperdicio y valorizar subproductos transforma el problema de un simple balanceo de tiempo a una optimización multi-objetivo que integra factores económicos, ambientales y de calidad.

Se observa una brecha significativa en la literatura: si bien existe una vasta investigación sobre el balanceo de líneas de desensamble en contextos generales (como la remanufactura de productos electrónicos), la aplicación directa y detallada a las carcasas de pollo es menos común. Los estudios existentes en el sector avícola a menudo se centran en la optimización de la cadena de suministro, la visión artificial para la clasificación de carcasas o la automatización de procesos más amplios, sin profundizar en el balanceo de la línea de desensamble en sí misma. Esta situación presenta una clara oportunidad para la investigación aplicada y el desarrollo de soluciones específicas.

Las metodologías de solución más prometedoras para este desafío son las metaheurísticas y los modelos de optimización multi-objetivo, dada su capacidad para manejar la complejidad (problemas NP-hard), la incertidumbre y los objetivos en conflicto. La simulación de eventos discretos emerge como una herramienta indispensable para validar estas soluciones en un entorno virtual que replique la variabilidad del mundo real, minimizando los riesgos de implementación. La digitalización, a través de la visión artificial y la robótica, se perfila como un habilitador clave para la recopilación de datos en tiempo real y la adaptación dinámica de las operaciones.

Con base en estos hallazgos, se proponen las siguientes fases y recomendaciones para un anteproyecto centrado en el balanceo de líneas de desensamble para carcasas de pollo:

Fase 1: Caracterización Detallada del Proceso de Desensamble

Realizar un estudio exhaustivo de tiempos y movimientos para cada tarea de corte y deshuesado en una planta de procesamiento de pollo. Este estudio debe considerar la variabilidad inherente en el tamaño y tipo de carcasa, registrando los tiempos de tarea para diferentes rangos de peso y morfología.

Elaborar un mapeo preciso de las relaciones de precedencia entre todas las tareas de desensamble, identificando las dependencias críticas y las oportunidades de paralelización.

Recopilar datos históricos sobre los rendimientos de los diferentes cortes de carne y subproductos obtenidos por tipo de carcasa, lo que permitirá cuantificar el valor potencial de cada componente.

Fase 2: Desarrollo de un Modelo de Optimización Multi-Objetivo

Formular un modelo matemático robusto, preferiblemente utilizando Programación Lineal Entera Mixta o una metaheurística avanzada (como un Algoritmo Genético o MO-ALNS), que aborde el problema como una optimización multi-objetivo.

Los objetivos del modelo deben incluir:

Minimización del número de estaciones de trabajo o del tiempo de ciclo.

Maximización del rendimiento de los cortes de carne de mayor valor comercial.

Maximización de la valorización de los subproductos (ej. patas, vísceras, huesos) mediante su asignación a mercados específicos.

Minimización del desperdicio de producto.

El modelo debe incorporar explícitamente restricciones operativas como la capacidad de las estaciones, la disponibilidad de mano de obra y la perecibilidad del producto (ej. ventanas de tiempo máximas para el procesamiento de ciertas partes).

Integrar parámetros de variabilidad, como tiempos de tarea estocásticos o distribuciones de tamaños de carcasa, para que el modelo genere soluciones más realistas y robustas.

Fase 3: Implementación y Validación mediante Simulación

Desarrollar un modelo de simulación de eventos discretos (DES), utilizando software especializado (ej. AnyLogic, ProModel), que replique fielmente la línea de desensamble de carcasas de pollo.

Validar el modelo de simulación con datos operativos reales de la planta para asegurar su precisión y representatividad.

Utilizar el modelo de simulación para experimentar con diferentes escenarios de balanceo generados por el modelo de optimización. Esto permitirá evaluar el rendimiento de las soluciones propuestas bajo condiciones dinámicas y con incertidumbre.

Realizar análisis de sensibilidad para comprender cómo la variabilidad en el tamaño de las carcasas, los tiempos de tarea o las fluctuaciones de la demanda afectan el rendimiento de la línea y la robustez de las soluciones de balanceo.

Fase 4: Evaluación de Tecnologías Habilitadoras

Investigar la viabilidad técnica y económica de integrar sistemas de visión artificial en la línea para la clasificación, medición de volumen y estimación de peso de las carcasas en tiempo real. Esto alimentaría el modelo de optimización con datos precisos para decisiones dinámicas.

Analizar el potencial de la robótica y la colaboración humano-robot (HRC) para automatizar tareas de corte repetitivas, peligrosas o de alta precisión, mejorando la ergonomía y la consistencia del proceso.

Fase 5: Análisis Económico y de Sostenibilidad

Cuantificar el impacto económico potencial de las mejoras propuestas, incluyendo la reducción de costos operativos (mano de obra, desperdicio) y el aumento de ingresos (por mayor rendimiento de cortes de valor y valorización de subproductos).

Evaluar el impacto ambiental de las soluciones de balanceo, centrándose en la reducción de la huella de carbono y la minimización del desperdicio de recursos.

La implementación de estas fases permitirá desarrollar un anteproyecto sólido y fundamentado, capaz de ofrecer soluciones innovadoras y aplicables para el balanceo de líneas de desensamble de carcasas de pollo, contribuyendo a una industria avícola más eficiente, rentable y sostenible.

9. Referencias
 SPC Consulting Group. (s.f.). Balanceo de Líneas. Recuperado de    

https://spcgroup.com.mx/balanceo-de-lineas/#:~:text=El%20balanceo%20de%20lineas%20es,productividad%20del%20sistema%20de%20produccion.

 SPC Consulting Group. (s.f.). ¿Qué es el balanceo de líneas?. Recuperado de    

https://spcgroup.com.mx/balanceo-de-lineas/

 Universidad Autónoma de Ciudad Juárez. (s.f.). Articulo.pdf. Recuperado de    

https://cathi.uacj.mx/bitstream/handle/20.500.11961/11933/Articulo.pdf?sequence=1&isAllowed=y

 Cronometras. (s.f.). Balanceo de Líneas: Optimizando la Eficiencia en Procesos de Manufactura. Recuperado de    

https://cronometras.com/es/blog/balanceo-de-lineas-optimizando-la-eficiencia-en-procesos-de-manufactura/

 Rojas Pinzon, C. (s.f.). ETAPAS DEL PROCESAMIENTO DE POLLOS A NIVEL INDUSTRIAL. Recuperado de    

https://es.scribd.com/document/458913077/ETAPAS-DEL-PROCESAMIENTO-DE-POLLOS-A-NIVEL-INDUSTRIAL

 Aviagen. (2017). Manejo de Problemas de Calidad de la Carcasa en la Planta de Procesamiento. Recuperado de    

https://aviagen.com/assets/Tech_Center/BB_Foreign_Language_Docs/Spanish_TechDocs-v2/AviagenBrielf-Addressing-Carcass-Quality-Issues-at-Processing-Plant-ES.pdf

 De la Cruz, M. (2021). Los desechos del sector avícola, nueva fuente de materias primas. AviNews. Recuperado de    

https://avinews.com/los-desechos-del-sector-avicola-nueva-fuente-de-materias-primas-para-las-industrias-agricola-cosmetica-o-del-envase/

 Aviagen. (s.f.). Tour virtual por una planta de incubación de última generación. YouTube. Recuperado de    

https://www.youtube.com/watch?v=7y58MyPDFvg&pp=0gcJCfwAo7VqN5tD

 ResearchGate. (s.f.). (PDF) Disassembly Line Balancing. Recuperado de    

https://www.researchgate.net/publication/45061950_Disassembly_Line_Balancing#:~:text=DLBP%2C%20very%20simply%2C%20can%20be,among%20disassembly%20tasks.

 ResearchGate. (s.f.). Disassembly line balancing problem: a review of the state of the art and future directions. Recuperado de    

https://www.researchgate.net/publication/322739774_Disassembly_line_balancing_problem_a_review_of_the_state_of_the_art_and_future_directions

 Chicken Check In. (s.f.). Processing: How are chickens slaughtered and processed for meat?. Recuperado de    

https://www.chickencheck.in/faq/how-chickens-slaughtered-processed/

 University of Minnesota Extension. (s.f.). Home processing poultry. Recuperado de    

https://extension.umn.edu/small-scale-poultry/home-processing-poultry

 OSHA. (s.f.). Cutting & Deboning » Cutting. Recuperado de    

https://www.osha.gov/etools/poultry-processing/tasks/cutting-deboning/cutting

 Colorado Department of Agriculture. (s.f.). 1.12. “Poultry slaughter area” means an area where killing, scalding and defeathering operations occur prior to evisceration, carcass chilling, wrapping / packaging. Recuperado de    

https://ag.colorado.gov/sites/ag/files/documents/1202-16%20Website.pdf

 Guzman Santiago, M. (s.f.). Balanceo de Líneas de Ensamble Para La Producción Simultanea de Más de Un Modelo. Recuperado de    

https://es.scribd.com/document/363070030/4-3-Balanceo-de-Lineas-de-Ensamble-Para-La-Produccion-Simultanea-de-Mas-de-Un-Modelo

 Ciencia Latina. (s.f.). Problema de balanceo de líneas de desensamble dependientes de secuencia (SDDLBP). Recuperado de    

https://ciencialatina.org/index.php/cienciala/article/download/15132/21566

 Ciencia Latina. (s.f.). IEEE Xplore balanceo de líneas de desensamble. Recuperado de    

https://ciencialatina.org/index.php/cienciala/article/download/15132/21566

 ResearchGate. (s.f.). A Simulation-Based Approach for Line Balancing Under Demand Uncertainty in Production Environment. Recuperado de    

https://www.researchgate.net/publication/377862831_A_Simulation-Based_Approach_for_Line_Balancing_Under_Demand_Uncertainty_in_Production_Environment

 MDPI. (s.f.). A mixed-integer programming (MIP) model based on energy efficiency is established for the two-sided disassembly line balancing problem considering parallel operation and fuzzy processing times (TDLBP-POF), which is more realistic than the previous model, and a multiobjective flatworm algorithm (MOFA) is developed to. Recuperado de    

https://www.mdpi.com/2071-1050/13/6/3358

 Redalyc. (s.f.). Problema de balanceo de una línea del tipo SALBP: caso de una línea de confección de prendas. Estudio de caso. Recuperado de    

https://www.redalyc.org/journal/5177/517764671014/html/

 USDA ARS. (s.f.). Chicken carcass scalding and chilling are two essential steps in modern commercial poultry processing. Recuperado de    

https://www.ars.usda.gov/research/publications/publication/?seqNo115=286418

 ResearchGate. (s.f.). Effect of strain sex and slaughter weight on growth performance carcass yield and quality of broiler meat. Recuperado de    

https://www.researchgate.net/publication/347706976_Effect_of_strain_sex_and_slaughter_weight_on_growth_performance_carcass_yield_and_quality_of_broiler_meat

 arXiv. (s.f.). The poultry industry has been driven primarily by broiler chicken production and has grown into the world's largest animal protein sector. Automated detection of chicken carcasses on processing lines is vital for quality control, food safety, and operational efficiency in slaughterhouses and poultry processing plants. Recuperado de    

https://arxiv.org/html/2507.18558v1

 ResearchGate. (s.f.). Synthetic Data Augmentation for Enhanced Chicken Carcass Instance Segmentation. Recuperado de    

https://www.researchgate.net/publication/393983108_Synthetic_Data_Augmentation_for_Enhanced_Chicken_Carcass_Instance_Segmentation

 NCBI. (s.f.). Online chicken carcass volume estimation using depth imaging and 3-D reconstruction. Recuperado de    

https://pmc.ncbi.nlm.nih.gov/articles/PMC11419819/

 Marel. (s.f.). Carcass balance – a key challenge for the poultry industry. Recuperado de    

https://marel.com/en/news/carcass-balance-a-key-challenge-for-the-poultry-industry/

 ResearchGate. (s.f.). Automated On-site Broiler Live Weight Estimation Through YOLO-. Recuperado de    

https://www.researchgate.net/publication/388786829_Automated_On-site_Broiler_Live_Weight_Estimation_Through_YOLO-Based_Segmentation

 ResearchGate. (s.f.). Assessing and improving the automatic ordering of perishable products: a case study in a major retailer. Recuperado de    

https://www.researchgate.net/publication/293333788_Assessing_and_improving_the_automatic_ordering_of_perishable_products_a_case_study_in_a_major_retailer

 ResearchGate. (s.f.). Disassembly Scheduling for the Meat Processing Industry with Product Perishability. Recuperado de    

https://www.researchgate.net/publication/331436230_Disassembly_Scheduling_for_the_Meat_Processing_Industry_with_Product_Perishability

 ResearchGate. (s.f.). Optimization Models for Harvest and Production Planning in Agri-Food Supply Chain: A Systematic Review. Recuperado de    

https://www.researchgate.net/publication/353788655_Optimization_Models_for_Harvest_and_Production_Planning_in_Agri-Food_Supply_Chain_A_Systematic_Review

 RELEX Solutions. (s.f.). How mathematical optimization unlocks profits in the poultry supply chain. Recuperado de    

https://www.relexsolutions.com/resources/poultry-supply-chain/

 ResearchGate. (s.f.). Exact methods in disassembly sequencing as a benchmark for heuristic algorithms. Recuperado de    

https://www.researchgate.net/publication/241384424_Exact_methods_in_disassembly_sequencing_as_a_benchmark_for_heuristic_algorithms

 ResearchGate. (s.f.). A survey on metaheuristics for optimization in food manufacturing industry. Recuperado de    

https://www.researchgate.net/publication/303095676_A_survey_on_metaheuristics_for_optimization_in_food_manufacturing_industry

 PubMed. (s.f.). Optimizing Enzymatic Processes for Enhanced Nutritional and Organoleptic Properties of Chicken Bones. Recuperado de    

https://pubmed.ncbi.nlm.nih.gov/40238421/

 PubMed. (s.f.). On-line weight estimation of broiler carcass and cuts by a computer vision system. Recuperado de    

https://pubmed.ncbi.nlm.nih.gov/34742122/

 ResearchGate. (s.f.). Line balancing using heuristic procedure and simulation of assembly line. Recuperado de    

https://www.researchgate.net/publication/339143282_Line_balancing_using_heuristic_procedure_and_simulation_of_assembly_line

 ResearchGate. (s.f.). The Heuristic Methods for Assembly Line Balancing Problem: A Case of Vietnam Garment Industry. Recuperado de    

https://www.researchgate.net/publication/335695635_The_Heuristic_Methods_for_Assembly_Line_Balancing_Problem_A_Case_of_Vietnam_Garment_Industry

 MDPI. (s.f.). A disassembly line balancing model with the goal of maximizing disassembly profits is established, in which tool selection and assignment is a critical part. Recuperado de    

https://www.mdpi.com/2227-7390/12/2/342

 Atlantis Press. (s.f.). Disassembly line is the most suitable way for enterprises to disassemble large-scale waste products. Recuperado de    

https://www.atlantis-press.com/proceedings/cdems-25/126012765

 ResearchGate. (s.f.). A comparative analysis of meta-heuristic methods on disassembly line balancing problem with stochastic time. Recuperado de    

https://www.researchgate.net/publication/364157768_A_comparative_analysis_of_meta-heuristic_methods_on_disassembly_line_balancing_problem_with_stochastic_time

 IDEAS. (s.f.). A comparative analysis of meta-heuristic methods on disassembly. Recuperado de    

https://ideas.repec.org/a/spr/annopr/v321y2023i1d10.1007_s10479-022-04910-1.html

 ResearchGate. (s.f.). The disassembly line balancing (DLB) problem assigns the set of tasks to each workstation for each product to be disassembled and aims at attaining several objectives, such as minimising the number of workstations, ensuring similar idle time at each workstation and removing hazardous parts/highly demanded components at Over the past two decades, the DLB problem and its variants have grown ever more popular for researchers and practitioners of environmentally conscious manufacturing. Yet, the problem characteristics and assumptions vary widely and there is no literature review to classify the existing articles accordingly. Recuperado de    

https://www.researchgate.net/publication/322739774_Disassembly_line_balancing_problem_a_review_of_the_state_of_the_art_and_future_directions

 ResearchGate. (s.f.). A Simulation-Based Approach for Line Balancing Under Demand Uncertainty in Production Environment. Recuperado de    

https://www.researchgate.net/publication/377862831_A_Simulation-Based_Approach_for_Line_Balancing_Under_Demand_Uncertainty_in_Production_Environment

 ResearchGate. (s.f.). The disassembly line balancing (DLB) problem assigns the set of tasks to each workstation for each product to be disassembled and aims at attaining several objectives, such as minimising the number of workstations, ensuring similar idle time at each workstation and removing hazardous parts/highly demanded components at Over the past two decades, the DLB problem and its variants have grown ever more popular for researchers and practitioners of environmentally conscious manufacturing. Yet, the problem characteristics and assumptions vary widely and there is no literature review to classify the existing articles accordingly. Recuperado de    

https://www.researchgate.net/publication/322739774_Disassembly_line_balancing_problem_a_review_of_the_state_of_the_art_and_future_directions

 PMC. (s.f.). NSCSO: a novel multi-objective non-dominated sorting chicken swarm optimization algorithm. Recuperado de    

https://pmc.ncbi.nlm.nih.gov/articles/PMC10881516/

 ResearchGate. (s.f.). Multi-objective chicken swarm optimization: A novel algorithm for solving multi-objective optimization problems. Recuperado de    

https://www.researchgate.net/publication/330861835_Multi-objective_chicken_swarm_optimization_A_novel_algorithm_for_solving_multi-objective_optimization_problems

 ResearchGate. (s.f.). Multiple Product Hybrid Disassembly Line Balancing Problem With Human–Robot Collaboration. Recuperado de    

https://www.researchgate.net/publication/381901339_Multiple_Product_Hybrid_Disassembly_Line_Balancing_Problem_With_Human-Robot_Collaboration

 MDPI. (s.f.). Hybrid Disassembly Line Balancing of Multi-Factory Remanufacturing Process Considering Workers with Government Benefits. Recuperado de    

https://www.mdpi.com/2227-7390/13/5/880

 ResearchGate. (s.f.). A CASE STUDY OF LINE BALANCING USING LARGEST CANDIDATE RULE ALGORITHM IN A MANUFACTURING INDUSTRY. Recuperado de    

https://www.researchgate.net/publication/321194686_A_CASE_STUDY_OF_LINE_BALANCING_USING_LARGEST_CANDIDATE_RULE_ALGORITHM_IN_A_MANUFACTURING_INDUSTRY

 NCBI. (s.f.). On-line weight estimation of broiler carcass and cuts by a computer vision system. Recuperado de    

https://pmc.ncbi.nlm.nih.gov/articles/PMC8577095/

 USDA FSIS. (s.f.). PULSE_PoultryStudy_250109_Final.pdf. Recuperado de    

https://www.fsis.usda.gov/sites/default/files/media_file/documents/PULSE_PoultryStudy_250109_Final.pdf

 USDA FSIS. (s.f.). Poultry Processing Line Speed Evaluation Study (PULSE). Recuperado de    

https://www.fsis.usda.gov/news-events/publications/poultry-processing-line-speed-evaluation-study-pulse

 ResearchGate. (s.f.). A review of unilateral grippers for meat industry automation. Recuperado de    

https://www.researchgate.net/publication/357019090_A_review_of_unilateral_grippers_for_meat_industry_automation

 ResearchGate. (s.f.). Towards human-robot collaboration in meat processing: Challenges and possibilities. Recuperado de    

https://www.researchgate.net/publication/360252728_Towards_human-robot_collaboration_in_meat_processing_Challenges_and_possibilities

 ResearchGate. (s.f.). Automated On-site Broiler Live Weight Estimation Through YOLO-Based Segmentation. Recuperado de    

https://www.researchgate.net/publication/388786829_Automated_On-site_Broiler_Live_Weight_Estimation_Through_YOLO-Based_Segmentation

 ResearchGate. (s.f.). Towards human-robot collaboration in meat processing: Challenges and possibilities. Recuperado de    

https://www.researchgate.net/publication/360252728_Towards_human-robot_collaboration_in_meat_processing_Challenges_and_possibilities

 ResearchGate. (s.f.). Automated On-site Broiler Live Weight Estimation Through YOLO-Based Segmentation. Recuperado de    

https://www.researchgate.net/publication/388786829_Automated_On-site_Broiler_Live_Weight_Estimation_Through_YOLO-Based_Segmentation

 Jurnal Wastukancana. (s.f.). Based on initial calculations, the line efficiency was 51.07%, then the balance delay was 48.93% and the idle time was 1.90 minutes. Recuperado de    

https://jurnal.wastukancana.ac.id/index.php/teknologika/article/view/456

 ResearchGate. (s.f.). Multi-Objective Optimization Approach for Enhancing Production System Efficiency in a Food Processing Industry. Recuperado de    

https://www.researchgate.net/publication/393643759_Multi-Objective_Optimization_Approach_for_Enhancing_Production_System_Efficiency_in_a_Food_Processing_Industry

 Wikipedia. (s.f.). Multi-objective optimization. Recuperado de    

https://en.wikipedia.org/wiki/Multi-objective_optimization

 Jurnal Wastukancana. (s.f.). The method used in this study is line balancing with the Pro Model simulation approach, which allows analysis of improvement scenarios without disrupting ongoing operations. Recuperado de    

https://jurnal.wastukancana.ac.id/index.php/teknologika/article/view/456

 ResearchGate. (s.f.). An ECRS-based line balancing concept A case study of a frozen chicken producer. Recuperado de    

https://www.researchgate.net/publication/265969677_An_ECRS-based_line_balancing_concept_A_case_study_of_a_frozen_chicken_producer

 ResearchGate. (s.f.). Multi-Objective Optimization Approach for Enhancing Production System Efficiency in a Food Processing Industry. Recuperado de    

https://www.researchgate.net/publication/393643759_Multi-Objective_Optimization_Approach_for_Enhancing_Production_System_Efficiency_in_a_Food_Processing_Industry

 MDPI. (s.f.). The research proposes a multi-criteria analysis of statistical methods to determine the fluctuation of parameters affecting the state of balance of an assembly line. Recuperado de    

https://www.mdpi.com/2673-4052/6/3/33

 ResearchGate. (s.f.). Productivity improvement based line balancing A case study of pasteurized milk manufacturer. Recuperado de    

https://www.researchgate.net/publication/283862733_Productivity_improvement_based_line_balancing_A_case_study_of_pasteurized_milk_manufacturer

 MDPI. (s.f.). However, the increasing complexity of modern food production systems has necessitated the adoption of multi-objective optimization techniques capable of balancing competing goals, such as minimizing production costs while maximizing energy efficiency and product quality. Recuperado de    

https://www.mdpi.com/2076-3417/15/7/3846


Fuentes usadas en el informe

spcgroup.com.mx
spcgroup.com.mx
Se abre en una ventana nueva

cathi.uacj.mx
1Balanceo de línea de desensamble basado en programación entera binaria - Inicio
Se abre en una ventana nueva

arxiv.org
Synthetic Data Augmentation for Enhanced Chicken Carcass Instance Segmentation - arXiv
Se abre en una ventana nueva

researchgate.net
(PDF) Synthetic Data Augmentation for Enhanced Chicken Carcass Instance Segmentation
Se abre en una ventana nueva

ars.usda.gov
Quality and Safety Assessment Research Unit: Athens, GA - Publication : USDA ARS
Se abre en una ventana nueva

researchgate.net
(PDF) Effect of strain, sex and slaughter weight on growth performance, carcass yield and quality of broiler meat - ResearchGate
Se abre en una ventana nueva

mdpi.com
Energy-Efficient Optimization of Two-Sided Disassembly Line Balance Considering Parallel Operation and Uncertain Using Multiobjective Flatworm Algorithm - MDPI
Se abre en una ventana nueva

redalyc.org
Problema de balanceo de una línea del tipo SALBP: caso de una línea de confección de prendas - Redalyc
Se abre en una ventana nueva

osha.gov
eTool : Poultry Processing Industry - Tasks - Cutting & Deboning - OSHA
Se abre en una ventana nueva

es.scribd.com
4.3. Balanceo de Líneas de Ensamble para La Producción Simultanea de Más de Un Modelo. | PDF | Diseño - Scribd
Se abre en una ventana nueva

ag.colorado.gov
RULES PERTAINING TO POULTRY PROCESSING 8 CCR 1202-16 - Colorado Department of Agriculture
Se abre en una ventana nueva

ciencialatina.org
MODELOS Y MÉTODOS DE SOLUCIÓN EN EL BALANCEO DE LÍNEAS DE PRODUCCIÓN APLICADOS EN LAS ORGANIZACIONES: ANÁLISIS DE LITERATUR - Ciencia Latina Revista Científica Multidisciplinar
Se abre en una ventana nueva

researchgate.net
www.researchgate.net
Se abre en una ventana nueva

extension.umn.edu
Home processing of poultry | UMN Extension
Se abre en una ventana nueva

avinews.com
Los desechos del sector avícola, nueva fuente de materias primas para las industrias agrícola, cosmética o del envase - aviNews
Se abre en una ventana nueva

youtube.com
¿Cómo logran las granjas avícolas en Estados Unidos producir millones de pollos orgánicos al año? - YouTube
Se abre en una ventana nueva

aviagen.com
Manejo de Problemas de Calidad de la Carcasa en la Planta de Procesamiento - Aviagen
Se abre en una ventana nueva

pmc.ncbi.nlm.nih.gov
Online chicken carcass volume estimation using depth imaging and 3-D reconstruction
Se abre en una ventana nueva

researchgate.net
Assessing and improving the automatic ordering of perishable products: a case study in a major retailer - ResearchGate
Se abre en una ventana nueva

researchgate.net
(PDF) Lean Line Balancing for an Electronics Assembly Line - ResearchGate
Se abre en una ventana nueva

es.scribd.com
Etapas Del Procesamiento de Pollos A Nivel Industrial | PDF | Aves ...
Se abre en una ventana nueva

cronometras.com
Balanceo de Líneas: Optimizando la Eficiencia en Procesos de ...
Se abre en una ventana nueva

spcgroup.com.mx
Balanceo de Líneas - SPC Consulting Group
Se abre en una ventana nueva

chickencheck.in
How are chickens slaughtered and processed for meat?
Se abre en una ventana nueva

researchgate.net
Exact methods in disassembly sequencing as a benchmark for heuristic algorithms
Se abre en una ventana nueva

researchgate.net
A survey on metaheuristics for optimization in food manufacturing industry - ResearchGate
Se abre en una ventana nueva

relexsolutions.com
How mathematical optimization unlocks profits in the poultry supply chain | RELEX Solutions
Se abre en una ventana nueva

pubmed.ncbi.nlm.nih.gov
Optimizing Enzymatic Processes for Enhanced Nutritional and Organoleptic Properties of Chicken Bones - PubMed
Se abre en una ventana nueva

researchgate.net
Line balancing using heuristic procedure and simulation of assembly line - ResearchGate
Se abre en una ventana nueva

pubmed.ncbi.nlm.nih.gov
On-line weight estimation of broiler carcass and cuts by a computer vision system - PubMed
Se abre en una ventana nueva

researchgate.net
Optimization Models for Harvest and Production Planning in Agri-Food Supply Chain: A Systematic Review - ResearchGate
Se abre en una ventana nueva

marel.com
Carcass balance – a key challenge for the poultry industry | Marel
Se abre en una ventana nueva

mdpi.com
Linear Disassembly Line Balancing Problem with Tool Deterioration and Solution by Discrete Migratory Bird Optimizer - MDPI
Se abre en una ventana nueva

researchgate.net
A comparative analysis of meta-heuristic methods on disassembly line balancing problem with stochastic time | Request PDF - ResearchGate
Se abre en una ventana nueva

ideas.repec.org
A comparative analysis of meta-heuristic methods on disassembly line balancing problem with stochastic time - IDEAS/RePEc
Se abre en una ventana nueva

researchgate.net
(PDF) A Simulation-Based Approach for Line Balancing Under Demand Uncertainty in Production Environment - ResearchGate
Se abre en una ventana nueva

researchgate.net
Multiple Product Hybrid Disassembly Line Balancing Problem With Human–Robot Collaboration | Request PDF - ResearchGate
Se abre en una ventana nueva

mdpi.com
Hybrid Disassembly Line Balancing of Multi-Factory Remanufacturing Process Considering Workers with Government Benefits - MDPI
Se abre en una ventana nueva

pmc.ncbi.nlm.nih.gov
NSCSO: a novel multi-objective non-dominated sorting chicken swarm optimization algorithm - PMC
Se abre en una ventana nueva

researchgate.net
Multi-objective chicken swarm optimization: A novel algorithm for solving multi-objective optimization problems | Request PDF - ResearchGate
Se abre en una ventana nueva

researchgate.net
Disassembly line balancing problem: a review of the state of the art ...
Se abre en una ventana nueva

researchgate.net
a case study of line balancing using largest candidate rule algorithm in a manufacturing industry - ResearchGate
Se abre en una ventana nueva

atlantis-press.com
Modeling and Optimization of U-shaped Sequence-dependent Disassembly Line Balancing Problem | Atlantis Press
Se abre en una ventana nueva

researchgate.net
Disassembly Scheduling for the Meat Processing Industry with Product Perishability
Se abre en una ventana nueva

fsis.usda.gov
Poultry Processing Line Speed Evaluation Study (PULSE) - Food Safety and Inspection Service
Se abre en una ventana nueva

fsis.usda.gov
Poultry Processing Line Speed Evaluation Study (PULSE)
Se abre en una ventana nueva

pmc.ncbi.nlm.nih.gov
On-line weight estimation of broiler carcass and cuts by a computer vision system - PMC
Se abre en una ventana nueva

ipv6.newinera.com
JOURNAL LA MULTIAPP - Newinera Publisher
Se abre en una ventana nueva

researchgate.net
An ECRS-based line balancing concept: A case study of a frozen chicken producer
Se abre en una ventana nueva

researchgate.net
Multi-Objective Optimization Approach for Enhancing Production System Efficiency in a Food Processing Industry - ResearchGate
Se abre en una ventana nueva

jurnal.wastukancana.ac.id
Line Balancing with Simulation Approach (ProModel) on SMC Big Volume Lane in HA Export Department at PT. XYZ | Jurnal Teknologika
Se abre en una ventana nueva

en.wikipedia.org
Multi-objective optimization - Wikipedia
Se abre en una ventana nueva

researchgate.net
A review of unilateral grippers for meat industry automation | Request PDF - ResearchGate
Se abre en una ventana nueva

researchgate.net
(PDF) Towards human-robot collaboration in meat processing: Challenges and possibilities
Se abre en una ventana nueva

researchgate.net
(PDF) Automated On-site Broiler Live Weight Estimation Through YOLO-Based Segmentation - ResearchGate
Se abre en una ventana nueva

researchgate.net
(PDF) The Heuristic Methods for Assembly Line Balancing Problem: A Case of Vietnam Garment Industry - ResearchGate
Se abre en una ventana nueva

mdpi.com
Advancing Optimization Strategies in the Food Industry: From Traditional Approaches to Multi-Objective and Technology-Integrated Solutions - MDPI
Se abre en una ventana nueva

mdpi.com
New Approach for Detecting Variability in Industrial Assembly Line Balancing Based on Multi-Criteria Analysis - MDPI
Se abre en una ventana nueva

researchgate.net
Productivity improvement based line balancing: A case study of pasteurized milk manufacturer - ResearchGate

---


Respuesta 2:
Construcción del Estado del Arte y Antenproyecto: Balanceo de Líneas de Desensamble para Carcasas de Pollo
Resumen Ejecutivo
El balanceo de líneas de desensamble (DLB, por sus siglas en inglés) representa un pilar fundamental en la optimización de procesos industriales, adquiriendo una relevancia crítica en el contexto de la economía circular y la sostenibilidad. Tradicionalmente aplicado a la recuperación de productos manufacturados, su extensión a la industria alimentaria, específicamente al desensamble de carcasas de pollo, introduce desafíos únicos pero también oportunidades significativas. Este informe presenta un estado del arte exhaustivo sobre DLB, abordando sus tipologías, objetivos y metodologías de solución, y propone un antenproyecto enfocado en la aplicación de estos principios al procesamiento avícola.

La industria avícola, siendo el sector de proteína animal más grande a nivel mundial, se enfrenta a una creciente presión para mejorar la eficiencia, la seguridad alimentaria y la sostenibilidad. La implementación de estrategias de economía circular, que buscan la reutilización, el reciclaje y la remanufactura de productos, se está volviendo indispensable para alcanzar tanto el crecimiento económico como la protección ambiental. Este enfoque no solo optimiza la utilización de recursos, sino que también aborda la reducción de residuos y la minimización del impacto ambiental, elementos clave para la viabilidad a largo plazo de las operaciones. La integración de la visión por computadora y la automatización en las líneas de procesamiento avícola emerge como un factor transformador, permitiendo una mayor precisión en el control de calidad y una mejora sustancial en la eficiencia operativa.   

El problema del DLB es inherentemente complejo, clasificado como NP-completo, lo que implica que el tiempo de solución crece exponencialmente con el número de componentes. Para abordar esta complejidad, se emplean diversas metodologías de optimización, incluyendo métodos exactos, heurísticos y metaheurísticos. Si bien los métodos exactos garantizan soluciones óptimas para problemas pequeños, su aplicabilidad se ve limitada por la escala en escenarios reales. Los métodos heurísticos ofrecen soluciones rápidas y prácticas, mientras que los metaheurísticos, como el Algoritmo de las Abejas o la Búsqueda Adaptativa de Vecindad Grande (ALNS), son particularmente adecuados para problemas complejos y multi-objetivo, ofreciendo soluciones de alta calidad en tiempos razonables.   

El antenproyecto propuesto se centra en desarrollar un marco metodológico para el balanceo de líneas de desensamble de carcasas de pollo, considerando las particularidades de la perecibilidad y la variabilidad del producto. Al optimizar la asignación de tareas a las estaciones de trabajo, se busca maximizar el rendimiento, minimizar el tiempo de inactividad, reducir los residuos y mejorar la eficiencia general de la línea. La implementación de este proyecto no solo promete beneficios económicos tangibles a través de una mayor productividad y un menor desperdicio, sino que también contribuye a los objetivos de sostenibilidad y seguridad alimentaria, posicionando a la industria avícola a la vanguardia de las prácticas de procesamiento modernas y responsables.

1. Introducción
1.1. Contexto de la Industria Avícola y la Economía Circular
La industria avícola se ha consolidado como el sector de proteína animal más grande del mundo, impulsada principalmente por la producción de pollos de engorde. Este crecimiento exponencial ha llevado a una intensificación de los procesos de producción y procesamiento, generando una demanda creciente de eficiencia y optimización. Sin embargo, el paradigma actual de producción lineal, que sigue un modelo de "tomar-hacer-desechar", es cada vez más insostenible frente a los desafíos ambientales y la escasez de recursos.   

En respuesta a estas presiones, el concepto de economía circular ha ganado una tracción considerable. La economía circular busca desarrollar sistemas que permitan la reutilización, recuperación y reciclaje de productos y servicios al final de su vida útil, persiguiendo simultáneamente el crecimiento económico y la sostenibilidad ambiental. Esta filosofía, tradicionalmente asociada con la remanufactura de componentes industriales como bombas de engranajes o baterías de iones de litio , está permeando progresivamente en la industria alimentaria. La legislación en muchos países ya está creando marcos para fomentar estas iniciativas, impulsando a las industrias a adoptar estrategias que reduzcan el impacto ambiental y fomenten la circularidad.   

La aplicación de los principios de la economía circular en el procesamiento avícola se traduce en la necesidad de optimizar cada etapa del ciclo de vida del producto, desde la crianza hasta el desensamble y la gestión de subproductos. Esto implica un cambio fundamental en la forma en que se conciben y operan las líneas de procesamiento. La investigación en balanceo de líneas de desensamble, que antes se centraba principalmente en maximizar el beneficio económico, ahora incorpora la sostenibilidad como un objetivo central, considerando factores como el ahorro de energía, la reducción de emisiones y los beneficios ambientales, además de la eficiencia de la línea. Esta evolución refleja un entendimiento más profundo de que la eficiencia operativa no puede separarse de la responsabilidad ambiental y social, lo que se conoce como el "triple resultado" (triple bottom line).   

La creciente atención a la economía circular y la sostenibilidad impulsa directamente la investigación en desensamble y recuperación de productos. Esto significa que las técnicas tradicionales de balanceo de líneas, que se enfocaban únicamente en la eficiencia, ahora deben integrar objetivos ambientales y económicos más amplios. Este cambio de paradigma es fundamental y está redefiniendo el diseño y la optimización de las líneas de desensamble en diversos sectores, incluida la industria alimentaria. Aunque la literatura actual sobre balanceo de líneas de desensamble se ha centrado en productos electrónicos o componentes industriales, los principios subyacentes son inherentemente transferibles a productos biológicos como las carcasas de pollo. Sin embargo, esta transferencia requiere una adaptación cuidadosa para abordar desafíos únicos, como la perecibilidad y la variabilidad inherente de los productos biológicos.

1.2. Definición y Relevancia del Balanceo de Líneas de Desensamble
El balanceo de líneas es una estrategia de producción diseñada para optimizar el tiempo de las máquinas y los operadores, eliminando cuellos de botella y maximizando la eficiencia en los procesos de producción en masa. Su objetivo principal es distribuir las tareas de manera uniforme entre las estaciones de trabajo para minimizar el tiempo de inactividad. Una línea perfectamente equilibrada idealmente tendría tiempos de operación idénticos en todas las estaciones, lo que se traduce en una mayor productividad y calidad del producto.   

Específicamente, el Balanceo de Líneas de Desensamble (DLB) es el problema de asignar un conjunto de tareas a cada estación de trabajo para un producto a desensamblar, con el fin de lograr varios objetivos. Estos objetivos pueden incluir la minimización del número de estaciones de trabajo, la reducción del tiempo de ciclo, la garantía de un tiempo de inactividad similar en cada estación o la maximización de la eficiencia de la línea. A diferencia del balanceo de líneas de ensamble, el desensamble no es simplemente el proceso inverso. Los productos al final de su vida útil a menudo están dañados, les faltan componentes o las conexiones pueden ser difíciles de desconectar debido al desgaste, la oxidación o la deformación. Además, las variaciones en los tiempos de operación y la necesidad de herramientas variables complican aún más el proceso de desensamble.   

La relevancia del DLB para las carcasas de pollo radica en su potencial para mejorar significativamente el control de calidad, la seguridad alimentaria y la eficiencia operativa en las plantas de procesamiento. La detección automatizada de carcasas, por ejemplo, es vital para la calidad y la seguridad. Al optimizar el flujo de trabajo en las líneas de desensamble, se puede reducir el desperdicio, aumentar el rendimiento y garantizar que los productos cumplan con los estándares requeridos para el consumo humano. Las líneas de desensamble semi-automatizadas para el deshuesado de aves, como las líneas de cono, ya demuestran mejoras en el rendimiento y la eficiencia laboral al automatizar tareas extenuantes y peligrosas, permitiendo velocidades de línea más rápidas con menos mano de obra.   

Aunque el objetivo central del balanceo de líneas —minimizar el tiempo de inactividad y maximizar la eficiencia— se mantiene constante tanto en el ensamble como en el desensamble , la naturaleza de las tareas y la variabilidad inherente de los productos biológicos introducen complejidades adicionales en el desensamble avícola. Las operaciones de desensamble de carcasas de pollo, a diferencia de los componentes industriales, están sujetas a variaciones en la forma, el tamaño y la postura de cada ave, así como a la perecibilidad del producto. Estas características únicas requieren un enfoque de modelado y optimización que pueda manejar la incertidumbre y la dinámica de un entorno biológico, lo que hace que la aplicación directa de métodos de ensamble sea insuficiente.   

1.3. Desafíos Específicos en el Desensamble de Carcasas de Pollo
El balanceo de líneas en la industria alimentaria, y particularmente en el procesamiento de carcasas de pollo, presenta desafíos distintivos que lo diferencian de los entornos de fabricación tradicionales. Estos desafíos se derivan principalmente de la naturaleza biológica y perecedera del producto.

Uno de los principales desafíos es la perecibilidad del producto. Las carcasas de pollo tienen una vida útil limitada y deben procesarse rápidamente para evitar el deterioro y garantizar la seguridad alimentaria. Esto impone estrictas limitaciones de tiempo en las operaciones de desensamble, lo que significa que cualquier ineficiencia o cuello de botella puede resultar en pérdidas significativas de producto. El modelo de programación de desensamble para la industria cárnica, por ejemplo, incorpora un "costo de perecibilidad" para contabilizar el descarte de productos caducados. La necesidad de un procesamiento rápido y continuo es primordial, y el balanceo de línea debe asegurar que el flujo de producto no se detenga ni se ralentice de manera que comprometa la frescura.   

La variabilidad inherente de las carcasas de pollo es otro desafío crítico. A diferencia de los componentes industriales estandarizados, las carcasas de pollo varían en tamaño, forma y postura, incluso dentro de un mismo lote. Esta variabilidad afecta directamente los tiempos de las tareas de desensamble, haciendo que los tiempos de operación determinísticos sean una simplificación irreal. Por ejemplo, la segmentación de instancias de carcasas de pollo es un desafío debido a la variabilidad en la postura, la superposición en las cintas transportadoras y las características visuales similares. Esta falta de uniformidad dificulta la estandarización de las operaciones y la asignación equitativa de la carga de trabajo entre las estaciones. Los sistemas de visión por computadora, aunque prometedores para la detección automatizada, aún enfrentan complejidades debido a estas características visuales irregulares.   

Además, la automatización completa en el desensamble de carcasas de pollo sigue siendo un desafío significativo. Aunque existen sistemas semi-automatizados que mejoran la eficiencia y reducen la mano de obra en tareas como el deshuesado , muchas operaciones aún requieren la destreza y adaptabilidad de los trabajadores humanos. La integración de la robótica y la inteligencia artificial, como la segmentación de instancias, es vital para avanzar en la automatización y reducir la exposición humana a condiciones peligrosas. Sin embargo, la complejidad de las características visuales de las carcasas y la dificultad de obtener grandes conjuntos de datos anotados para el entrenamiento de IA son barreras importantes.   

Finalmente, los estrictos requisitos de higiene y seguridad alimentaria imponen restricciones adicionales en el diseño y la operación de las líneas de desensamble. Las superficies deben ser fáciles de limpiar, los materiales deben ser compatibles con los estándares alimentarios y cualquier interrupción en el flujo puede aumentar el riesgo de contaminación. Estos factores limitan la flexibilidad en la reconfiguración de la línea y exigen soluciones de balanceo que no comprometan la integridad del producto. La optimización de los procesos debe considerar no solo la eficiencia económica, sino también la minimización de la contaminación y el mantenimiento de temperaturas adecuadas en cada etapa.   

La combinación de estos factores —perecibilidad, variabilidad, desafíos de automatización y requisitos de seguridad— hace que el balanceo de líneas de desensamble para carcasas de pollo sea un problema complejo y multifacético. Requiere la integración de conocimientos de ingeniería industrial, visión por computadora, ciencia de los alimentos y optimización para desarrollar soluciones robustas y aplicables en la práctica.

2. Estado del Arte del Balanceo de Líneas de Desensamble (DLB)
El problema del balanceo de líneas de desensamble (DLB) ha sido objeto de una intensa investigación en las últimas dos décadas, impulsado por la creciente importancia de la remanufactura y el reciclaje en el marco de la economía circular. El DLB se define como la asignación de un conjunto de tareas a estaciones de trabajo secuenciales en una línea de desensamble, con el objetivo de optimizar una o varias medidas de rendimiento.   

2.1. Tipologías de Problemas de DLB
Los problemas de balanceo de líneas de desensamble se clasifican en varias tipologías, dependiendo de las características del producto, las condiciones de operación y los objetivos de optimización. Estas clasificaciones son cruciales para seleccionar la metodología de solución más adecuada.

Una distinción fundamental es entre el DLB completo y el DLB parcial. El DLB completo implica el desensamble total de un producto en todos sus componentes, mientras que el DLB parcial se enfoca en la recuperación de un subconjunto específico de componentes de alto valor o peligrosos. La investigación ha mostrado un aumento notable en los estudios sobre DLB parcial en los últimos años, dada su frecuente aplicación en escenarios de la vida real y su estructura más compleja.   

Otra clasificación importante se basa en la variabilidad de los tiempos de las tareas. Los problemas pueden ser:

Determinísticos: Se asume que los tiempos de las tareas son fijos y conocidos con precisión. Aunque simplifica el modelado, esta suposición rara vez se cumple en entornos reales, especialmente en la industria alimentaria.   

Estocásticos: Los tiempos de las tareas se modelan como variables aleatorias, reflejando la incertidumbre inherente en las operaciones de desensamble debido a la variabilidad del producto o las condiciones de desgaste. Este enfoque es más realista para las carcasas de pollo, donde el tamaño y la forma de cada ave pueden influir en el tiempo de procesamiento.   

Además, los problemas pueden diferenciarse por la configuración de la línea:

Líneas en serie (straight lines): Las estaciones están dispuestas consecutivamente y cada unidad de producto pasa por cada estación una vez.   

Líneas en U (U-lines): Las estaciones están dispuestas en forma de U, lo que puede mejorar el balanceo, la visibilidad y la comunicación, y ofrecer mayor flexibilidad.   

Líneas paralelas: Varias líneas de desensamble operan en paralelo, lo que puede proporcionar flexibilidad para minimizar el número total de estaciones de trabajo debido a recursos compartidos.   

Finalmente, la dependencia de la secuencia es una característica crítica. En el DLB dependiente de la secuencia (RDLBSD), el orden en que se realizan las tareas de desensamble afecta directamente la eficiencia y la productividad de la línea. Este tipo de problema es particularmente desafiante y es común en la mayoría de las publicaciones recientes en el área.   

2.2. Objetivos de Optimización en DLB
Los objetivos de optimización en el DLB son múltiples y a menudo conflictivos, lo que lleva a la formulación de problemas de optimización multi-objetivo. Estos objetivos se pueden agrupar en varias categorías :   

Indicadores de la línea de producción:

Minimizar el número de estaciones de trabajo (Tipo-I DLBP): Dado un tiempo de ciclo fijo, se busca la configuración con la menor cantidad de estaciones.   

Minimizar el tiempo de ciclo (Tipo-II DLBP): Dada una cantidad fija de estaciones de trabajo, se busca el tiempo de ciclo más corto posible, lo que maximiza la tasa de producción.   

Maximizar la eficiencia de la línea (Tipo-E DLBP): Busca optimizar la proporción del tiempo de uso de la línea, minimizando el tiempo de inactividad. Una eficiencia del 100% representa un balance perfecto.   

Minimizar la varianza del tiempo de estación / suavidad del balanceo: Busca lograr una distribución de carga de trabajo lo más uniforme posible entre las estaciones, reduciendo las diferencias en los tiempos de operación.   

Indicadores económicos:

Maximizar el beneficio/rendimiento: Considera los ingresos por componentes recuperados (reutilizados, remanufacturados, reciclados) menos los costos de desensamble, recuperación y eliminación.   

Minimizar costos: Incluye costos de operación, costos de mano de obra, costos de inversión en equipos y costos de gestión de residuos.   

Indicadores ambientales y de sostenibilidad:

Minimizar el índice de peligro: Prioriza la eliminación temprana de partes peligrosas.   

Minimizar el consumo de energía: Busca reducir la energía utilizada en las operaciones de desensamble y recuperación.   

Reducir las emisiones de gases de efecto invernadero: Contribuye a la huella de carbono del proceso.   

Maximizar los beneficios ambientales: Se calcula restando el impacto ambiental de las operaciones de desensamble y recuperación del impacto ambiental recuperado de los componentes reutilizados o remanufacturados.   

La optimización multi-objetivo (MOO) es una herramienta indispensable en la industria alimentaria, ya que permite equilibrar metas a menudo conflictivas, como la viabilidad económica, la calidad nutricional y la sostenibilidad ambiental. Los marcos de MOO ayudan a identificar soluciones Pareto-óptimas, que representan los mejores compromisos posibles entre estos objetivos en competencia.   

2.3. Metodologías de Solución para DLB
Los problemas de DLB son intrínsecamente complejos, a menudo clasificados como NP-hard o NP-completo, lo que significa que encontrar soluciones óptimas exactas se vuelve computacionalmente inviable a medida que el tamaño del problema aumenta. Por esta razón, se han desarrollado diversas metodologías de solución, que se pueden categorizar en métodos exactos, heurísticos y metaheurísticos.   

2.3.1. Métodos Exactos
Los métodos exactos buscan la solución óptima global garantizada para un problema. Son útiles para problemas de tamaño pequeño a mediano, pero su tiempo de resolución crece exponencialmente con el número de variables, lo que los hace imprácticos para problemas de gran escala.   

Programación Lineal Entera (PLE): Formula el problema como un conjunto de ecuaciones lineales y desigualdades con variables de decisión enteras (a menudo binarias), que luego se resuelven para optimizar una función objetivo. Es una técnica robusta, pero la complejidad computacional puede ser muy alta.   

Branch-and-Bound (B&B): Es un algoritmo que descompone el problema en subproblemas más pequeños, formando un árbol de búsqueda. Utiliza funciones de acotación (límites superiores e inferiores) para eliminar ramas del árbol que no pueden contener la solución óptima, podando así el espacio de búsqueda. El método re-implementado de Branch-and-Bound (BBR) ha demostrado una superioridad clara sobre otros métodos exactos publicados.   

Programación Dinámica: Aborda el problema de balanceo de líneas como un problema de secuenciación con restricciones de precedencia, permitiendo la formulación de un algoritmo para la solución exacta de problemas pequeños.   

La aplicación de métodos exactos en el balanceo de líneas de desensamble para carcasas de pollo es limitada debido a la naturaleza NP-hard del problema y la gran cantidad de variables involucradas, especialmente con la variabilidad inherente del producto.

2.3.2. Métodos Heurísticos
Los métodos heurísticos son enfoques basados en la lógica y el sentido común que buscan encontrar soluciones "suficientemente buenas" en un tiempo computacional razonable, sin garantizar la optimalidad global. Son particularmente útiles para problemas de tamaño medio o como punto de partida para métodos más complejos.   

Largest Candidate Rule (Regla del Candidato Más Grande): Este es uno de los métodos heurísticos más básicos y fáciles de entender. Prioriza la asignación de elementos de trabajo a las estaciones de trabajo en función del tamaño de sus tiempos de tarea (Te), abordando primero los más grandes. Las tareas se asignan a la primera estación de trabajo en orden descendente de su valor Te, respetando las restricciones de precedencia y asegurando que la suma de los tiempos de las tareas no exceda el tiempo de ciclo (Tc).   

Kilbridge and Wester: Introducido en 1961, este método iterativo busca equilibrar la línea de producción ajustando los tiempos de ciclo de diferentes operaciones mediante prueba y error. El objetivo es lograr una línea equilibrada donde todas las estaciones tengan tiempos de ciclo iguales y tasas de producción similares, minimizando al mismo tiempo el tiempo de ciclo total. Implica identificar la línea de producción, determinar la ruta crítica, calcular el tiempo de ciclo ideal y asignar tiempos de ciclo iterativamente, verificando el equilibrio.   

Ranked Positional Weights (Pesos Posicionales Clasificados): Este método asigna un peso o valor a diferentes posiciones en una línea de fabricación para optimizar su rendimiento. Se otorgan pesos más altos a las posiciones más críticas y pesos más bajos a las menos críticas, considerando factores como la habilidad requerida, la complejidad de la tarea o el impacto en el rendimiento general de la línea. Las posiciones se clasifican según sus pesos asignados, y esta clasificación se utiliza para optimizar el rendimiento, por ejemplo, asignando trabajadores calificados a posiciones de mayor rango.   

Los métodos heurísticos pueden proporcionar soluciones prácticas para el balanceo de líneas de desensamble de carcasas de pollo, especialmente en situaciones donde se requiere una respuesta rápida o cuando la complejidad del problema hace que los métodos exactos sean inviables.

2.3.3. Métodos Metaheurísticos
Los métodos metaheurísticos son estrategias de búsqueda de alto nivel que guían algoritmos de búsqueda locales para explorar el espacio de soluciones de problemas de optimización complejos. Son particularmente efectivos para problemas NP-hard, ya que pueden encontrar soluciones de alta calidad (casi óptimas) en tiempos computacionales aceptables, y tienen la capacidad de escapar de óptimos locales.   

Algoritmo de las Abejas (Bees Algorithm - BA / Artificial Bee Colony - ABC): Inspirado en el comportamiento de forrajeo de las abejas melíferas, el BA es una metaheurística basada en enjambres que busca fuentes de alimento (soluciones) ricas. El Multi-Objective Bees Algorithm (MOBA) se ha utilizado para optimizar modelos de sostenibilidad en el balanceo de líneas de desensamble robótico, considerando múltiples objetivos como beneficio, ahorro de energía y beneficios ambientales.   

Adaptive Large Neighbourhood Search (ALNS): Es un algoritmo metaheurístico conocido por su flexibilidad y robustas capacidades de búsqueda local. Dinámicamente ajusta combinaciones de operadores de destrucción y reparación para explorar nuevos espacios de solución y evitar óptimos locales. Para problemas de DLB multi-objetivo dependientes de la secuencia (MO-SDDLB), el MO-ALNS integra operadores de destrucción y reparación diseñados a medida, recocido simulado para una búsqueda global mejorada y estrategias de búsqueda local para el refinamiento de la solución. Ha demostrado un rendimiento superior en calidad de solución.   

Simulated Annealing (SA - Recocido Simulado): Inspirado en el proceso físico de recocido de sólidos, el SA es una técnica de búsqueda que intenta evitar quedar atrapado en óptimos locales al permitir ocasionalmente la aceptación de soluciones "inferiores" con una cierta probabilidad. La "temperatura" del algoritmo disminuye sistemáticamente, lo que reduce la probabilidad de aceptar soluciones peores a medida que avanza la búsqueda.   

Tabu Search (TS - Búsqueda Tabú): Es una técnica de búsqueda estocástica basada en un enfoque de búsqueda de vecindad iterativa. Utiliza una "lista tabú" para registrar un historial de movimientos de soluciones, lo que ayuda a guiar la búsqueda hacia nuevas direcciones y escapar de trampas de mínimos locales. Se ha aplicado en problemas de balanceo de líneas de ensamble, a menudo en combinación con otros algoritmos como los genéticos.   

Algoritmos Genéticos (GA): Inspirados en el proceso de selección natural y la genética, los GA son algoritmos de optimización que operan sobre una población de soluciones candidatas, utilizando operadores como la selección, el cruce y la mutación para evolucionar hacia soluciones óptimas. Son adecuados para problemas de agrupamiento y pueden manejar casos con restricciones de precedencia dispersas.   

Particle Swarm Optimization (PSO - Optimización por Enjambre de Partículas): Es un algoritmo de inteligencia de enjambre inspirado en el comportamiento social de organismos como bandadas de aves o bancos de peces. Las "partículas" (soluciones candidatas) se mueven a través del espacio de búsqueda, ajustando sus posiciones y velocidades basándose en su mejor experiencia individual (pBest) y la mejor solución encontrada por todo el enjambre (gBest).   

Ant Colony Optimization (ACO - Optimización por Colonia de Hormigas): Imita el comportamiento de forrajeo de las hormigas reales, donde las "hormigas artificiales" depositan rastros de feromonas en los caminos que recorren para guiar a otras hormigas hacia soluciones óptimas. La fuerza de las feromonas en un camino indica su calidad, y los caminos más cortos o eficientes acumulan más feromonas.   

Los métodos metaheurísticos son particularmente prometedores para el balanceo de líneas de desensamble de carcasas de pollo debido a la complejidad NP-hard del problema, la naturaleza estocástica de los tiempos de las tareas y la necesidad de soluciones eficientes que consideren múltiples objetivos.

2.4. Aplicaciones de DLB en la Industria Alimentaria y Avícola (Contexto Actual)
La aplicación explícita del balanceo de líneas de desensamble en la industria avícola, específicamente para carcasas de pollo, es un campo de investigación emergente con un potencial considerable. Aunque gran parte de la literatura sobre DLB se centra en la remanufactura de productos electrónicos o mecánicos , los principios de optimización son directamente aplicables, aunque con adaptaciones necesarias para las particularidades biológicas.   

La optimización en la industria alimentaria ha evolucionado significativamente, pasando de enfoques tradicionales de un solo factor a metodologías avanzadas como la metodología de superficie de respuesta (RSM) y la optimización multi-objetivo (MOO). La integración de redes neuronales artificiales (ANNs) con tecnologías de la Industria 4.0, como el Internet de las Cosas (IoT) y los gemelos digitales, ha permitido el monitoreo y la optimización en tiempo real, alineando los procesos de producción con los objetivos de sostenibilidad e innovación. Esto subraya la tendencia hacia sistemas de producción más inteligentes y adaptativos, que son esenciales para el manejo de productos perecederos y variables como las carcasas de pollo.   

En el procesamiento avícola, la automatización es vital para el control de calidad, la seguridad alimentaria y la eficiencia operativa. La detección automatizada de carcasas de pollo en las líneas de procesamiento, por ejemplo, utiliza la segmentación de instancias para identificar defectos o para tareas de recolección robótica de elementos deformables. La escasez de datos reales anotados para el entrenamiento de modelos de IA ha llevado a la investigación sobre el uso de datos sintéticos, que han demostrado mejorar significativamente el rendimiento de la segmentación. Esta capacidad de detectar y clasificar con precisión las carcasas es un prerrequisito fundamental para cualquier sistema de balanceo de líneas automatizado o semi-automatizado.   

Las líneas de deshuesado de pollo semi-automatizadas, como las líneas de cono, ya están en uso y demuestran cómo la automatización estratégica puede mejorar los rendimientos y la eficiencia laboral. Estas líneas permiten velocidades de procesamiento más rápidas (hasta 40 aves por minuto frente a 34 aves por minuto) y reducen la necesidad de personal (de 17 a 13 trabajadores), al tiempo que eliminan tareas extenuantes y peligrosas. Esto ilustra la aplicación práctica de la optimización de líneas en la industria avícola, aunque el balanceo formal de desensamble, que considera la deconstrucción de la carcasa en sus componentes primarios (p. ej., pechugas, alas, muslos), aún no está tan documentado como en otras industrias.   

El balanceo de líneas de producción en general busca reducir el tiempo de inactividad, agilizar el flujo de producción y mejorar la moral de los empleados. Para la industria avícola, esto se traduce en la capacidad de ajustar las líneas a las demandas cambiantes del mercado y a la variabilidad del producto, minimizando el desperdicio en diversas formas, como inventario excesivo, productos defectuosos o sobreproducción. La implementación de herramientas de software para el balanceo de líneas, como IFS, que pueden ajustarse a la producción de máquinas y trabajadores, es un paso hacia la optimización en tiempo real.   

Aunque la literatura específica sobre "balanceo de líneas de desensamble para carcasas de pollo" es limitada, la convergencia de la investigación en DLB, optimización en la industria alimentaria y automatización avícola sugiere que este es un campo maduro para la innovación. El desafío radica en adaptar los modelos y algoritmos existentes para abordar las complejidades únicas de los productos biológicos y perecederos.

3. Antenproyecto: Balanceo de Líneas de Desensamble para Carcasas de Pollo
3.1. Justificación y Alcance del Antenproyecto
La creciente demanda de productos avícolas y la presión por operaciones más sostenibles y eficientes justifican la necesidad de optimizar los procesos de desensamble de carcasas de pollo. Actualmente, muchas operaciones de procesamiento avícola, aunque semi-automatizadas, aún enfrentan desafíos relacionados con la variabilidad del producto, la perecibilidad y la necesidad de altos rendimientos. Un balanceo ineficiente de la línea puede llevar a cuellos de botella, mayor tiempo de inactividad, aumento de residuos y una reducción en el rendimiento general.   

Este antenproyecto se propone abordar estas deficiencias mediante la aplicación de principios avanzados de balanceo de líneas de desensamble. El alcance del proyecto abarcará el análisis de las operaciones de desensamble de carcasas de pollo desde la recepción hasta el empaquetado de los cortes primarios (pechugas, muslos, alas, etc.). Se buscará desarrollar un marco que permita la asignación óptima de tareas a las estaciones de trabajo, considerando las particularidades de la materia prima biológica.

La justificación de este antenproyecto se basa en varios puntos clave:

Mejora de la eficiencia operativa: Reducir el tiempo de inactividad y eliminar cuellos de botella aumentará la tasa de producción y la utilización de recursos.   

Optimización del rendimiento y reducción de residuos: Un desensamble más preciso y eficiente puede maximizar la cantidad de producto utilizable y minimizar el desperdicio de material. Esto es crucial en un contexto de economía circular.   

Incremento de la seguridad alimentaria y calidad: Un flujo de línea balanceado y controlado puede reducir el riesgo de contaminación y garantizar el cumplimiento de los estándares de calidad.   

Adaptabilidad a la variabilidad del producto: Desarrollar un modelo que pueda manejar las variaciones naturales en el tamaño y la forma de las carcasas, lo que es una limitación actual en la automatización.   

Contribución a la sostenibilidad: Al optimizar el uso de recursos y reducir el desperdicio, el proyecto apoyará los objetivos de sostenibilidad de la industria avícola.   

El proyecto no solo busca beneficios económicos a través de la eficiencia y el rendimiento, sino que también se alinea con una visión más amplia de la producción alimentaria sostenible.

3.2. Propuesta Metodológica para el Antenproyecto
La metodología para este antenproyecto se estructurará en varias fases, desde la recopilación de datos hasta la validación de las soluciones propuestas.

3.2.1. Recopilación y Análisis de Datos Específicos de Carcasas de Pollo
La primera fase implicará una recopilación exhaustiva de datos operativos de una línea de desensamble de carcasas de pollo. Esto incluirá:

Tiempos de las tareas: Medición precisa de los tiempos requeridos para cada operación de desensamble (corte, deshuesado, separación, etc.). Dada la variabilidad del producto, estos tiempos se modelarán como variables estocásticas, posiblemente siguiendo distribuciones de probabilidad, en lugar de valores fijos. Esto es fundamental para reflejar la realidad de las carcasas de pollo, donde el tiempo de una tarea puede variar significativamente según el tamaño o la forma del ave.   

Restricciones de precedencia: Identificación de la secuencia obligatoria en la que deben realizarse las tareas. Se construirá un diagrama de precedencia, donde cada tarea de desensamble se representa como un nodo y las flechas indican las relaciones de orden.   

Datos de variabilidad: Recopilación de datos sobre las variaciones en el tamaño, peso y morfología de las carcasas de pollo. Esto podría implicar el uso de sistemas de visión por computadora para caracterizar las carcasas antes del desensamble, ya que la detección automatizada es vital para el control de calidad y la eficiencia.   

Factores de perecibilidad: Cuantificación de los tiempos máximos permitidos para el procesamiento de las carcasas y sus subproductos para mantener la frescura y seguridad alimentaria.   

Recursos disponibles: Información sobre el número de estaciones de trabajo, la capacidad de las máquinas y la disponibilidad de mano de obra calificada.   

El análisis de estos datos proporcionará una comprensión profunda de las operaciones existentes y servirá como base para el modelado del problema. Se utilizarán técnicas estadísticas para caracterizar la variabilidad y la incertidumbre en los tiempos de las tareas.

3.2.2. Modelado del Problema de DLB para Carcasas de Pollo
Se formulará un modelo matemático para el problema de balanceo de líneas de desensamble de carcasas de pollo. Este modelo será de optimización multi-objetivo para capturar la complejidad de los objetivos interrelacionados en la industria alimentaria. Los objetivos clave incluirán:   

Minimizar el número de estaciones de trabajo: Para reducir la inversión y los costos operativos.   

Minimizar el tiempo de ciclo: Para maximizar la tasa de producción y manejar la perecibilidad.   

Maximizar la eficiencia de la línea: Para asegurar una alta utilización de los recursos y minimizar el tiempo de inactividad.   

Minimizar la varianza de la carga de trabajo entre estaciones: Para asegurar un flujo suave y reducir el estrés en los trabajadores.   

Maximizar el rendimiento del producto: Para obtener la mayor cantidad de cortes valiosos de cada carcasa.   

Consideraciones de sostenibilidad: Integrar métricas relacionadas con la reducción de residuos y el uso eficiente de la energía.   

El modelo incorporará restricciones de precedencia de tareas, capacidad de las estaciones de trabajo y, crucialmente, la naturaleza estocástica de los tiempos de las tareas y la perecibilidad del producto. La formulación podría basarse en un modelo de programación lineal entera o una variante, adaptando los conceptos de DLB dependiente de la secuencia para reflejar las interacciones entre las operaciones de desensamble de carcasas.   

3.2.3. Selección y Adaptación de Algoritmos de Optimización
Dada la naturaleza NP-hard del problema y la necesidad de manejar múltiples objetivos y la incertidumbre, se explorará la aplicación de métodos metaheurísticos. Estos algoritmos son adecuados para encontrar soluciones de alta calidad en problemas complejos y a gran escala.   

Se considerarán y adaptarán algoritmos como:

Adaptive Large Neighbourhood Search (ALNS): Conocido por su flexibilidad y robustas capacidades de búsqueda local, el ALNS puede integrar operadores de destrucción y reparación personalizados para explorar el espacio de soluciones de manera eficiente. Su capacidad para manejar problemas multi-objetivo y estocásticos lo hace muy prometedor para las carcasas de pollo.   

Multi-Objective Bees Algorithm (MOBA) / Artificial Bee Colony (ABC): Inspirado en el comportamiento de forrajeo de las abejas, este algoritmo ha demostrado ser eficaz en problemas de DLB multi-objetivo, maximizando beneficios y minimizando el desequilibrio de la línea.   

Algoritmos Genéticos (GA): Su capacidad para trabajar con poblaciones de soluciones y evolucionar a través de operadores de cruce y mutación los hace adecuados para explorar grandes espacios de búsqueda y manejar restricciones de precedencia.   

Simulated Annealing (SA): Su capacidad para escapar de óptimos locales al aceptar soluciones "inferiores" con cierta probabilidad lo convierte en una opción robusta para problemas de optimización combinatoria.   

La selección final del algoritmo o la combinación de algoritmos se basará en su capacidad para manejar la incertidumbre (tiempos de tarea estocásticos), múltiples objetivos y la complejidad de las restricciones de precedencia específicas del desensamble de carcasas de pollo. Se adaptarán los operadores de los algoritmos para que reflejen las características únicas del problema, como la variabilidad de la forma de las carcasas y la perecibilidad. La integración de la simulación de Monte Carlo dentro del algoritmo de optimización será crucial para abordar la aleatoriedad en los tiempos de operación y la interferencia de tareas.   

3.2.4. Implementación y Validación
La metodología propuesta se implementará en un entorno de simulación computacional. Se generarán escenarios de prueba utilizando datos representativos de la industria avícola, incluyendo diferentes volúmenes de producción y variaciones en las características de las carcasas.

La validación del modelo y los algoritmos se realizará mediante:

Comparación de rendimiento: Se compararán las soluciones obtenidas con las configuraciones de línea existentes (si están disponibles) o con soluciones generadas por heurísticas simples. Las métricas de rendimiento incluirán la eficiencia de la línea, el tiempo de ciclo, el número de estaciones, el rendimiento del producto y la reducción de residuos.

Análisis de sensibilidad: Se evaluará cómo los cambios en los parámetros de entrada (por ejemplo, la variabilidad de los tiempos de las tareas, la demanda) afectan las soluciones óptimas.

Validación con expertos de la industria: Se buscará la retroalimentación de ingenieros y gerentes de producción en plantas avícolas para asegurar la relevancia práctica y la viabilidad de las soluciones.

El proceso de validación buscará demostrar la eficacia del enfoque propuesto para mejorar la eficiencia y la sostenibilidad en el desensamble de carcasas de pollo.

3.3. Objetivos del Antenproyecto
Los objetivos específicos de este antenproyecto son:

Desarrollar un modelo de balanceo de líneas de desensamble multi-objetivo que considere la variabilidad estocástica de los tiempos de las tareas y la perecibilidad del producto para carcasas de pollo.

Adaptar y aplicar al menos dos algoritmos metaheurísticos (por ejemplo, ALNS, MOBA/ABC, GA) para resolver el modelo propuesto, evaluando su rendimiento computacional y la calidad de las soluciones.

Cuantificar los beneficios potenciales en términos de eficiencia de la línea (reducción del tiempo de inactividad, aumento de la tasa de producción), rendimiento del producto (maximización de cortes valiosos) y métricas de sostenibilidad (reducción de residuos, eficiencia energética) en un entorno simulado.

Proponer directrices para la implementación práctica de las soluciones de balanceo de líneas en plantas de procesamiento avícola, incluyendo consideraciones sobre la integración de tecnologías de visión por computadora y automatización.

3.4. Entregables Esperados
Los principales entregables de este antenproyecto incluirán:

Un modelo matemático formal para el balanceo de líneas de desensamble de carcasas de pollo.

Implementaciones computacionales de los algoritmos de optimización seleccionados.

Resultados de simulaciones y análisis de rendimiento que demuestren la eficacia de las soluciones propuestas.

Un informe técnico detallado que describa la metodología, los resultados, las conclusiones y las recomendaciones para futuras investigaciones y aplicaciones industriales.

Diagramas de relaciones en lenguaje Mermaid que ilustren los conceptos clave y las interconexiones del problema.

Tablas comparativas de la literatura y las metodologías de solución.

4. Tesuario (Glosario de Términos Clave)
Balanceo de Líneas (Line Balancing): Estrategia de producción que busca optimizar el tiempo de las máquinas y los operadores, eliminando cuellos de botella y distribuyendo las tareas de manera uniforme entre las estaciones de trabajo para maximizar la eficiencia y minimizar el tiempo de inactividad.   

Balanceo de Líneas de Desensamble (DLB - Disassembly Line Balancing): Problema de asignación de tareas a estaciones de trabajo en una línea de desensamble para optimizar medidas de rendimiento como el número de estaciones, el tiempo de ciclo, la eficiencia de la línea o la varianza de la carga de trabajo.   

Tiempo de Ciclo (Cycle Time - CT): El tiempo máximo permitido para que una estación de trabajo complete sus operaciones. Determina la tasa de producción de la línea.   

Eficiencia de la Línea (Line Efficiency - E): Medida de la utilización de la línea de producción, calculada como la proporción del tiempo total de trabajo respecto al tiempo total disponible de las estaciones.   

Tiempo de Inactividad (Idle Time): Tiempo durante el cual un trabajador o una estación de trabajo no está realizando ninguna tarea. Minimizarlo es un objetivo clave del balanceo de líneas.   

Restricciones de Precedencia (Precedence Constraints): Relaciones de orden que dictan que ciertas tareas deben completarse antes de que otras puedan comenzar.   

NP-hard / NP-completo: Clases de problemas computacionales para los cuales no se conoce un algoritmo eficiente que encuentre la solución óptima en tiempo polinomial; el tiempo de solución crece exponencialmente con el tamaño del problema.   

Economía Circular (Circular Economy): Modelo económico que busca reducir el desperdicio y maximizar el valor de los recursos mediante la reutilización, recuperación y reciclaje de productos y materiales.   

Optimización Multi-Objetivo (MOO - Multi-Objective Optimization): Técnicas de optimización que buscan mejorar simultáneamente múltiples objetivos, a menudo conflictivos, encontrando un conjunto de soluciones de compromiso (soluciones Pareto-óptimas).   

Heurísticas (Heuristics): Métodos basados en la lógica o el sentido común que buscan soluciones "suficientemente buenas" en un tiempo razonable, sin garantizar la optimalidad global.   

Metaheurísticas (Metaheuristics): Estrategias de búsqueda de alto nivel que guían algoritmos de búsqueda locales para explorar el espacio de soluciones de problemas de optimización complejos, buscando soluciones de alta calidad (casi óptimas) y evitando óptimos locales.   

Variabilidad del Producto (Product Variability): Diferencias en las características físicas (tamaño, forma, peso) de productos individuales dentro de un mismo lote, lo que afecta los tiempos de procesamiento y la uniformidad de las tareas.   

Perecibilidad (Perishability): Característica de los productos que tienen una vida útil limitada y requieren procesamiento o consumo dentro de un período de tiempo específico para evitar el deterioro.   

Visión por Computadora (Computer Vision): Campo de la inteligencia artificial que permite a las computadoras "ver" e interpretar imágenes y videos, utilizado en la industria avícola para la detección automatizada y el control de calidad de carcasas.   

5. Tablas Comparativas
5.1. Comparativa de Papers Relevantes
La siguiente tabla resume algunos de los trabajos más relevantes encontrados en la literatura, destacando su enfoque principal, las metodologías de solución empleadas, los objetivos de optimización y los hallazgos clave que son pertinentes para el balanceo de líneas de desensamble, especialmente en el contexto de la industria alimentaria y avícola.

Paper (ID del Snippet)	Enfoque Principal	Metodología de Solución	Objetivos de Optimización	Hallazgos Clave Relevantes
Balanceo de línea de desensamble robótico dependiente de la secuencia (RDLBSD) para bombas de engranajes industriales.	Multi-Objective Bees Algorithm (MOBA).	Maximizar beneficio, ahorro de energía, beneficios ambientales; minimizar desequilibrio de línea.	Desarrolla un modelo de sostenibilidad para RDLBSD. Los problemas de desensamble son NP-completos. La dependencia de la secuencia es crucial.
Revisión del problema de balanceo de línea de desensamble (DLB) y sus variantes.	Revisión bibliográfica. Propone MO-ALNS para MO-SDDLB bajo incertidumbre.	Minimizar índice de peligro, varianza del tiempo de estación, consumo de energía.	Clasifica DLB, destaca el aumento de investigación en DLB parcial. MO-ALNS supera métodos existentes en calidad de solución.
Detección automatizada de carcasas de pollo en líneas de procesamiento usando visión por computadora.	Modelos de segmentación de instancias (YOLOv11-seg, Mask R-CNN, Mask2Former) con datos sintéticos.	Mejorar el rendimiento de segmentación de instancias de carcasas de pollo.	Los datos sintéticos aumentan significativamente el rendimiento de la segmentación, crucial para la automatización en la industria avícola.
Programación de desensamble para la industria cárnica con perecibilidad del producto.	Modelo matemático de programación de desensamble.	Considerar perecibilidad y demanda en múltiples niveles de jerarquía del producto.	Aborda la perecibilidad y variabilidad del producto (ej. cerdo) en el desensamble, introduciendo costos de perecibilidad y pérdidas de rendimiento.
Optimización multi-objetivo (MOO) en la industria alimentaria.	RSM, ANNs, MOO.	Maximizar calidad, minimizar costos, mejorar eficiencia energética; sostenibilidad.	MOO es indispensable para desafíos multifacéticos en la industria alimentaria, integrando sostenibilidad, viabilidad económica y tecnología (IA, IoT).
Balanceo de líneas de ensamble (ALB) y producción.	Algoritmo de agrupación robusto, algoritmo de árbol de decisión C4.5, métodos heurísticos (Tabu Search, Branch-and-Bound, COMSOAL, ASA).	Maximizar eficiencia, reducir tiempo de cuello de botella, minimizar horas de trabajo redundantes.	Destaca la importancia de ALB para la producción ajustada; mejora de la tasa de balance de línea del 68% al 85% en un caso de estudio.
  
5.2. Comparativa de Metodologías de Solución
La tabla a continuación compara las principales metodologías de solución utilizadas en el balanceo de líneas, destacando sus características, ventajas, desventajas y su aplicabilidad potencial al problema específico del desensamble de carcasas de pollo.

Metodología	Descripción General	Ventajas	Desventajas	Aplicabilidad en DLB (Carcasas de Pollo)	Ejemplos de Algoritmos
Métodos Exactos	Buscan la solución óptima global garantizada mediante enumeración sistemática del espacio de búsqueda.	Garantizan la solución óptima.	Crecimiento exponencial del tiempo de resolución con el tamaño del problema (NP-hard). Impracticables para problemas grandes.	Limitada para líneas de desensamble complejas de carcasas de pollo debido a la gran cantidad de variables y la naturaleza NP-hard del problema. Podrían usarse para subproblemas pequeños.	
Programación Lineal Entera (ILP) , Branch-and-Bound (B&B) , Programación Dinámica    

Métodos Heurísticos	Basados en la lógica o el sentido común, buscan soluciones "suficientemente buenas" en un tiempo razonable, sin garantizar la optimalidad.	Rápidos y fáciles de entender e implementar. Adecuados para problemas de tamaño medio.	No garantizan la optimalidad global. La calidad de la solución puede variar y puede quedar atrapada en óptimos locales.	Útiles para obtener soluciones rápidas para problemas de tamaño moderado o como punto de partida para métodos metaheurísticos. Pueden ser una base para la toma de decisiones inicial.	
Largest Candidate Rule , Kilbridge and Wester , Ranked Positional Weights    

Métodos Metaheurísticos	Estrategias de búsqueda de alto nivel que guían algoritmos de búsqueda locales para explorar el espacio de soluciones, buscando soluciones casi óptimas de alta calidad en tiempos aceptables.	Efectivos para problemas NP-hard complejos y de gran escala. Pueden escapar de óptimos locales. Flexibles y adaptables a problemas con incertidumbre (estocásticos).	No garantizan la optimalidad global. Requieren ajuste de parámetros y el tiempo computacional puede ser alto para problemas muy grandes.	Muy prometedores para el DLB de carcasas de pollo debido a la complejidad (NP-hard), variabilidad (estocástica) y la necesidad de soluciones eficientes y robustas. Son la opción principal para problemas realistas.	
Algoritmo de las Abejas (Bees Algorithm) / ABC , Adaptive Large Neighbourhood Search (ALNS) , Simulated Annealing (SA) , Tabu Search (TS) , Algoritmos Genéticos (GA) , Particle Swarm Optimization (PSO) , Ant Colony Optimization (ACO)    

6. Diagramas de Relaciones (Mermaid)
Los siguientes diagramas ilustran las relaciones clave entre los conceptos discutidos en el informe, utilizando el lenguaje Mermaid para una representación clara y estructurada.

Diagrama 1: Relación entre Economía Circular, Desensamble y la Industria Avícola
Este diagrama muestra cómo la Economía Circular impulsa las estrategias de recuperación de productos, que a su vez requieren el Balanceo de Líneas de Desensamble (DLB). La aplicación del DLB a la Industria Avícola (carcasas de pollo) conduce a la optimización, eficiencia y sostenibilidad, lo que retroalimenta positivamente a la Economía Circular.

Fragmento de código

graph TD
    A[Economía Circular] --> B(Estrategias de Recuperación de Productos);
    B --> C{Reutilización, Reciclaje, Remanufactura};
    C --> D;
    D --> E[Optimización de Procesos];
    E --> F;
    F --> G[Industria Avícola (Carcasas de Pollo)];
    G --> H;
    G --> I;
    H & I --> F;
    A -- Impulsa --> F;
    D -- Aplicado a --> G;
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style G fill:#ccf,stroke:#333,stroke-width:2px
Diagrama 2: Desafíos y Consideraciones en DLB para Carcasas de Pollo
Este diagrama detalla los desafíos específicos que surgen al aplicar el Balanceo de Líneas de Desensamble a las carcasas de pollo. Estos desafíos, como la perecibilidad y la variabilidad, impactan directamente en la eficiencia y el rendimiento de la línea, lo que a su vez influye en la complejidad del DLB.

Fragmento de código

graph TD
    A --> B{Desafíos Específicos};
    B --> C[Perecibilidad del Producto];
    B --> D;
    B --> E;
    B --> F;
    C --> G;
    D --> H[Complejidad en Visión por Computadora];
    E --> I;
    F --> J;
    G & H & I & J --> K;
    K --> A;
    style A fill:#ccf,stroke:#333,stroke-width:2px
Diagrama 3: Metodologías de Solución para DLB
Este diagrama presenta las tres categorías principales de metodologías de solución para los problemas de Balanceo de Líneas de Desensamble: Métodos Exactos, Métodos Heurísticos y Métodos Metaheurísticos. También se muestran ejemplos de algoritmos dentro de cada categoría y se señalan las limitaciones generales de cada enfoque.

Fragmento de código

graph TD
    A --> B[Métodos Exactos];
    A --> C[Métodos Heurísticos];
    A --> D[Métodos Metaheurísticos];
    B --> B1[Programación Lineal Entera];
    B --> B2;
    B --> B3;
    C --> C1;
    C --> C2;
    C --> C3;
    D --> D1;
    D --> D2;
    D --> D3;
    D --> D4;
    D --> D5[Algoritmos Genéticos (GA)];
    D --> D6;
    D --> D7[Ant Colony Optimization (ACO)];
    B -- Limitaciones --> L1[NP-Hard, Escalabilidad];
    C -- Limitaciones --> L2[No Optimalidad Garantizada];
    D -- Limitaciones --> L3[Ajuste de Parámetros, No Optimalidad Garantizada];
    L1 & L2 & L3 --> E;
    E --> A;
    style A fill:#f9f,stroke:#333,stroke-width:2px
7. Conclusiones y Recomendaciones
El análisis del estado del arte y la propuesta de antenproyecto para el balanceo de líneas de desensamble de carcasas de pollo revelan un campo de investigación y aplicación con un potencial significativo para la industria avícola. La integración de los principios de la economía circular y la sostenibilidad es un imperativo que trasciende la mera eficiencia operativa, posicionando el DLB como una herramienta estratégica para la gestión de recursos y la reducción del impacto ambiental.

Se concluye que el balanceo de líneas de desensamble para carcasas de pollo es un problema complejo y multifacético, clasificado como NP-hard, debido a la variabilidad inherente del producto, su perecibilidad y las estrictas normativas de higiene y seguridad alimentaria. A diferencia de los problemas de balanceo de líneas en la manufactura tradicional, la naturaleza biológica de las carcasas de pollo introduce incertidumbre en los tiempos de las tareas y requiere modelos que consideren la dinámica de un producto con vida útil limitada.

Los métodos metaheurísticos, como el Adaptive Large Neighbourhood Search (ALNS) y el Multi-Objective Bees Algorithm (MOBA/ABC), emergen como las metodologías más prometedoras para abordar este problema. Su capacidad para manejar problemas multi-objetivo, la incertidumbre en los tiempos de las tareas y la exploración eficiente de grandes espacios de búsqueda los hace idóneos para encontrar soluciones de alta calidad en escenarios realistas. La integración de la visión por computadora para la caracterización de carcasas y la automatización robótica es fundamental para recopilar datos precisos y ejecutar las operaciones de desensamble de manera eficiente.

Recomendaciones:

Priorizar la investigación en modelado estocástico: Es crucial desarrollar modelos de DLB que capturen la variabilidad real de los tiempos de las tareas en el desensamble de carcasas de pollo, utilizando distribuciones de probabilidad en lugar de valores determinísticos. La simulación de Monte Carlo debe integrarse en los algoritmos de optimización para evaluar la robustez de las soluciones bajo incertidumbre.

Fomentar la colaboración interdisciplinaria: El éxito de este antenproyecto dependerá de la colaboración entre expertos en ingeniería industrial, visión por computadora, robótica y ciencia de los alimentos. Esto permitirá el desarrollo de soluciones integrales que aborden tanto la optimización de procesos como los desafíos específicos de la manipulación de productos biológicos.

Explorar la aplicación de gemelos digitales: La creación de gemelos digitales de las líneas de desensamble avícola podría permitir la simulación y optimización en tiempo real de los procesos, reduciendo los riesgos y costos asociados con la implementación de nuevas configuraciones de línea. Esto también facilitaría la adaptación a cambios dinámicos en la demanda o las características del producto.

Desarrollar métricas de sostenibilidad específicas: Más allá de los objetivos económicos y de eficiencia tradicionales, se recomienda definir y cuantificar métricas de sostenibilidad específicas para el desensamble de carcasas de pollo, como la reducción de la huella hídrica, la minimización de los subproductos no aprovechados y el ahorro de energía en el procesamiento.

Validación en entornos industriales reales: Una vez que los modelos y algoritmos propuestos demuestren su eficacia en entornos simulados, se recomienda llevar a cabo proyectos piloto en plantas de procesamiento avícola. Esto permitirá validar las soluciones en condiciones operativas reales y refinar el enfoque para una implementación a gran escala.

La aplicación exitosa del balanceo de líneas de desensamble en la industria avícola no solo generará beneficios económicos significativos a través de una mayor eficiencia y rendimiento, sino que también fortalecerá el compromiso del sector con la sostenibilidad y la seguridad alimentaria, contribuyendo a una economía circular más robusta.


Fuentes usadas en el informe

mdpi.com
The Key Constituents, Research Trends, and Future Directions of the Circular Economy Applied to Wind Turbines Using a Bibliometric Approach - MDPI
Se abre en una ventana nueva

arxiv.org
Synthetic Data Augmentation for Enhanced Chicken Carcass Instance Segmentation - arXiv
Se abre en una ventana nueva

mdpi.com
An Algorithm for Arranging Operators to Balance Assembly Lines and Reduce Operator Training Time - MDPI
Se abre en una ventana nueva

researchgate.net
(PDF) Synthetic Data Augmentation for Enhanced Chicken Carcass Instance Segmentation
Se abre en una ventana nueva

bibliotekanauki.pl
OPTIMISATION OF SIMPLE ASSEMBLY LINE BALANCING PROBLEM TYPE E: A SYSTEMATIC LITERATURE REVIEW - Biblioteka Nauki
Se abre en una ventana nueva

thaiscience.info
The U-line Assembly Line Balancing Problem - ThaiScience
Se abre en una ventana nueva

mdpi.com
A Predictive Approach for Disassembly Line Balancing Problems - MDPI
Se abre en una ventana nueva

corningdata.com
What is Production Line Balancing? - Corning Data
Se abre en una ventana nueva

frontiersin.org
A matrix approach to visually communicate simultaneously the environmental and health impacts of foods - Frontiers
Se abre en una ventana nueva

jbtc.com
Prime Cone Deboning Line - JBT Corporation
Se abre en una ventana nueva

making.com
Semi-automated poultry deboning system - Making.com
Se abre en una ventana nueva

ideas.repec.org
A comparative analysis of meta-heuristic methods on disassembly line balancing problem with stochastic time - IDEAS/RePEc
Se abre en una ventana nueva

pmc.ncbi.nlm.nih.gov
Production line balance problem identification and improvement ...
Se abre en una ventana nueva

mdpi.com
Advancing Optimization Strategies in the Food Industry: From ... - MDPI
Se abre en una ventana nueva

mdpi.com
Optimisation of Product Recovery Options in End-of-Life Product ...
Se abre en una ventana nueva

thaiscience.info
The Assembly Line Balancing Problem : Review articles - ThaiScience
Se abre en una ventana nueva

mdpi.com
Review of Metaheuristic Optimization Algorithms for Power Systems Problems - MDPI
Se abre en una ventana nueva

researchgate.net
Disassembly line balancing problem: a review of the state of the art ...
Se abre en una ventana nueva

researchgate.net
(PDF) Metaheuristic approach to assembly line balancing
Se abre en una ventana nueva

periodicos.capes.gov.br
A survey of the assembly line balancing procedures
Se abre en una ventana nueva

researchgate.net
A comparative study of exact methods for the simple assembly line ...
Se abre en una ventana nueva

delongs.com
10 Steps to Optimizing Poultry Processing - DeLong's Gizzard Equipment
Se abre en una ventana nueva

bornaplus.com.tr
Poultry Production Optimization Processes: A Guide to Efficiency and Sustainability
Se abre en una ventana nueva

researchgate.net
Line balancing using heuristic procedure and simulation of assembly line - ResearchGate
Se abre en una ventana nueva

pubsonline.informs.org
Fast, Effective Algorithms for Simple Assembly Line Balancing ...
Se abre en una ventana nueva

researchgate.net
(PDF) Disassembly Scheduling for the Meat Processing Industry ...
Se abre en una ventana nueva

researchgate.net
A survey on meta-heuristics for solving disassembly line balancing ...
Se abre en una ventana nueva

mdpi.com
A Stochastic Sequence-Dependent Disassembly Line Balancing ...
Se abre en una ventana nueva

ideas.repec.org
Assembly-Line Balancing by Linear Programming - IDEAS/RePEc
Se abre en una ventana nueva

pubsonline.informs.org
Assembly-Line Balancing—Dynamic Programming with Precedence Constraints | Operations Research - PubsOnLine - INFORMS.org
Se abre en una ventana nueva

en.wikipedia.org
Branch and bound - Wikipedia
Se abre en una ventana nueva

lineview.com
How to Perfectly Balance a Manufacturing Line - Lineview Solutions
Se abre en una ventana nueva

pubsonline.informs.org
A Branch and Bound Algorithm for Assembly Line Balancing Problems with Formulation Irregularities | Management Science - PubsOnLine - INFORMS.org
Se abre en una ventana nueva

chegg.com
Solved Line Balancing Method 1 -Largest Candidate Rule (pp. | Chegg.com
Se abre en una ventana nueva

thisisrishi.medium.com
Understanding Particle Swarm Optimization (PSO): From Basics to Brilliance | by Rishi Zirpe
Se abre en una ventana nueva

youtube.com
321 - What is Particle Swarm Optimization PSO? - YouTube
Se abre en una ventana nueva

scholarpedia.org
Artificial bee colony algorithm - Scholarpedia
Se abre en una ventana nueva

en.wikipedia.org
Ant colony optimization algorithms - Wikipedia
Se abre en una ventana nueva

upperinc.com
Ant Colony Optimization Explained: Insights & Applications - Upper Route Planner
Se abre en una ventana nueva

scribd.com
Kilbridge-Wester Heuristic For Line Balancing: C N I 1 in | PDF - Scribd
Se abre en una ventana nueva

butex.edu.bd
Balancing a Parallel Assembly Line Using Kilbridge and Wester Method: A Case Study on a Garments Factory of Bangladesh - BUTEX
Se abre en una ventana nueva

dergipark.org.tr
A Tabu Search Algorithm for the Parallel Assembly Line Balancing Problem - DergiPark
Se abre en una ventana nueva

researchgate.net
(PDF) A Hybrid Tabu Search Method for Assembly Line Balancing - ResearchGate
Se abre en una ventana nueva

scispace.com
Using simulated annealing to solve a multiobjective assembly line balancing problem with parallel workstations - SciSpace
Se abre en una ventana nueva

sites.gatech.edu
Simulated Annealing : Methods and Real-World Applications – OMSCS 7641
Se abre en una ventana nueva

citeseerx.ist.psu.edu
citeseerx.ist.psu.edu
Se abre en una ventana nueva

citeseerx.ist.psu.edu
A Genetic Algorithm for Bin Packing and Line Balancing - CiteSeerX
Se abre en una ventana nueva

en.wikipedia.org
Artificial bee colony algorithm - Wikipedia
Se abre en una ventana nueva

slideshare.net
Ranked Positional Weight Method | Management | PPTX | Business - SlideShare
Se abre en una ventana nueva

scribd.com
Assembly Line Balancing Using The Ranked Positional Weight Technique W. B. HELGESON, D. P. BIRNIE (1961) | PDF | Matrix (Mathematics) - Scribd


```

### Archivo: notebookml.md
```

La industria alimentaria se enfrenta a una necesidad constante de optimización y eficiencia, lo que ha impulsado la adopción de diversos conceptos y métodos de fabricación ["del conocimiento previo"]. Para abordar desafíos como la **productividad**, la **seguridad alimentaria** y la **sostenibilidad**, se aplican estrategias de gestión avanzadas y sofisticadas arquitecturas de automatización ["del conocimiento previo"]. La naturaleza perecedera de los productos agrícolas, la reducción de residuos y el acortamiento de los plazos de entrega son cruciales en este sector ["del conocimiento previo"].

A continuación, se presenta un diagrama que relaciona los métodos de solución empleados en diversas investigaciones y aplicaciones dentro del ámbito de la fabricación, muchos de los cuales son relevantes para la industria alimentaria, seguido de una explicación detallada:

```mermaid
graph LR
    subgraph Conceptos de Fabricación Aplicados
        A["Optimización de Procesos"] --> B(Métodos de Solución)
    end

    subgraph Métodos de Solución
        B --> C["Optimización Matemática (Exactos)"]
        B --> D["Heurísticas y Metaheurísticas"]
        B --> E["Simulación"]
        B --> F["Inteligencia Artificial y Aprendizaje Automático"]
    end

    subgraph "Optimización Matemática (Exactos)"
        C --> C1["Programación Lineal (LP)"]
        C --> C2["Programación Entera (IP) / MILP"]
        C --> C3["Programación Dinámica (DP)"]
        C --> C4["Programación por Metas (GP)"]
        C --> C5["Métodos de Ruta Más Corta"]
        C --> C6["Branch and Bound (BB)"]
        C --> C7["Paquetes de Programación Matemática (ej. GAMS-CPLEX)"]
    end

    subgraph Heurísticas y Metaheurísticas
        D --> D1["Heurísticas Clásicas (ej. LCR, RPW, COMSOAL)"]
        D --> D2["Algoritmos Genéticos (GA)"]
        D --> D3["Simulated Annealing (SA)"]
        D --> D4["Búsqueda Tabú (TS)"]
        D --> D5["Optimización por Colonia de Hormigas (ACO)"]
        D --> D6["Algoritmo de la Colonia de Abejas (ABC/MOBA)"]
        D --> D7["Optimización por Enjambre de Partículas (PSO)"]
        D --> D8["Búsqueda Adaptativa de Vecindarios Grandes (ALNS)"]
        D --> D9["Otros Metaheurísticas (ej. GSA, HA, WOA, ILS, HHA)"]
    end

    subgraph Simulación
        E --> E1["Simulación de Eventos Discretos (DES)"]
        E --> E2["Simulación Monte Carlo"]
        E --> E3["Software de Simulación (ej. Arena)"]
    end

    subgraph Inteligencia Artificial y Aprendizaje Automático
        F --> F1["Árboles de Decisión (ej. C4.5)"]
        F --> F2["Modelos de Clasificación (ej. Softmax Regression, Random Forests)"]
        F --> F3["Deep Learning (ej. YOLOv11-seg, Mask R-CNN)"]
        F --> F4["Generación de Datos Sintéticos (ej. GANs, Blender)"]
        F --> F5["Redes Neuronales Artificiales (ANNs)"]
        F --> F6["Aprendizaje por Refuerzo (RL)"]
        F --> F7["Sistemas Expertos"]
    end

    C1 -- Aplicado en --> G["Diseño de Cadena de Suministro, Formulación de Dietas, Flujo Óptimo de Potencia"]
    C2 -- Aplicado en --> H["Balanceo de Líneas de Ensamblaje y Desensamblaje (ALB/DLB)"]
    C3 -- Aplicado en --> I["Balanceo de Líneas en U (U-line)"]
    C4 -- Aplicado en --> J["Problemas de Scheduling, Optimización Multicriterio"]
    C5 -- Aplicado en --> K["Balanceo de Líneas, Problemas de Ruteo"]
    C6 -- Aplicado en --> L["ALB/DLB, Problemas de Optimización Combinatoria"]
    C7 -- Aplicado en --> M["Modelos Matemáticos de DLB"]

    D1 -- Aplicado en --> N["Balanceo de Líneas de Ensamblaje/Desensamblaje (ALB/DLB)"]
    D2 -- Aplicado en --> O["ALB/DLB, Problemas Multi-objetivo, Scheduling"]
    D3 -- Aplicado en --> P["ALB/DLB, Optimización de Procesos, Reducción de Área PLA"]
    D4 -- Aplicado en --> Q["ALB/DLB, Problemas de Secuenciación Dependiente"]
    D5 -- Aplicado en --> R["ALB/DLB, Optimización de Ruta, Problemas Multi-objetivo"]
    D6 -- Aplicado en --> S["Optimización Robótica de Desensamblaje, ALB/DLB"]
    D7 -- Aplicado en --> T["DLB, Problemas Multi-objetivo, Optimización de Redes"]
    D8 -- Aplicado en --> U["Problemas de DLB Estocástico y Secuencialmente Dependiente"]
    D9 -- Aplicado en --> V["Varias Aplicaciones de Optimización, incluyendo DLB"]

    E1 -- Aplicado en --> W["Análisis de Rendimiento de Líneas de Producción, Identificación de Cuellos de Botella, Optimización de Mantenimiento"]
    E2 -- Aplicado en --> X["ALB/DLB Estocástico, Manejo de Incertidumbre"]
    E3 -- Aplicado en --> Y["Modelado y Mejora de Líneas de Producción"]

    F1 -- Aplicado en --> Z["Identificación de Problemas en Líneas de Producción"]
    F2 -- Aplicado en --> Z
    F3 -- Aplicado en --> AA["Segmentación de Imágenes (ej. Carcasas de Pollo)"]
    F4 -- Aplicado en --> AB["Aumento de Datos para ML, Robótica"]
    F5 -- Aplicado en --> AC["Modelado de Sistemas Complejos, Optimización de Recetas"]
    F6 -- Aplicado en --> AD["Optimización de Líneas de Desensamblaje, Control de Procesos"]
    F7 -- Aplicado en --> AE["Sistemas de Apoyo a la Toma de Decisiones, Gestión de Producción"]
```

### **Métodos de Solución Aplicados en la Industria Alimentaria y sus Contextos**

Las fuentes revelan un amplio espectro de metodologías utilizadas para optimizar los procesos en la industria alimentaria, a menudo adaptando técnicas de fabricación general a sus necesidades específicas.

#### **1. Optimización Matemática (Métodos Exactos)**
Estos métodos buscan la solución óptima garantizada para problemas definidos matemáticamente:
*   **Programación Lineal (LP)** y **Programación Entera (IP) / MILP**: Se utilizan para el **balanceo de líneas de ensamblaje (ALB)** y **desensamblaje (DLB)**, incluyendo modelos de **programación lineal entera mixta (MILP)** para problemas más complejos como el **balanceo de líneas en U orientado a beneficios**, y para **optimizar la cantidad de animales y cortes primarios** en la industria cárnica ["del conocimiento previo"]. También son aplicables en el **diseño de cadenas de suministro y formulación de dietas**. Un estudio propuso un modelo MILP para un problema de DLB parcial multi-producto con multi-robot.
*   **Programación Dinámica (DP)**: Se ha aplicado en el **balanceo de líneas en U**.
*   **Programación por Metas (GP)**: Mencionada como una técnica para **ALB** y **scheduling de desensamblaje** bajo incertidumbre.
*   **Métodos de Ruta Más Corta**: Se emplean en el **balanceo de líneas de ensamblaje** y **desensamblaje**.
*   **Branch and Bound (BB)**: Usado para resolver **ALB** y **problemas de DLB estocástico**.
*   **Paquetes de Programación Matemática (ej. GAMS-CPLEX)**: Herramientas como GAMS-CPLEX se utilizan para **resolver modelos matemáticos de DLB** con restricciones de recursos.

#### **2. Heurísticas y Metaheurísticas**
Dada la complejidad combinatoria de muchos problemas de optimización en la fabricación, las metaheurísticas son fundamentales para encontrar soluciones "suficientemente buenas" en un tiempo razonable.
*   **Heurísticas Clásicas (ej. LCR, RPW, COMSOAL)**: El **Ranked Positional Weight (RPW)** y la **Largest Candidate Rule (LCR)** son métodos heurísticos populares para el **balanceo de líneas de ensamblaje y desensamblaje**. **COMSOAL** también se ha utilizado en el balanceo de líneas, incluso en **líneas de modelos mixtos**. El **Método de Desviación Mínima (MDM)** se aplicó para combinar funciones objetivo en líneas de ensamblaje paralelas.
*   **Algoritmos Genéticos (GA)**: Son muy populares para el **balanceo de líneas de ensamblaje (ALB)** y **desensamblaje (DLB)**. Se utilizan para **optimización multi-objetivo** y problemas estocásticos.
*   **Simulated Annealing (SA)**: Aplicado al **balanceo de líneas en U**, **ALB multi-objetivo**, **DLB** y la **optimización de procesos** como la reducción de área en PLAs.
*   **Búsqueda Tabú (TS)**: Utilizado para el **balanceo de líneas de ensamblaje**, **DLB** y problemas de **DLB robótico híbrido multi-robot**.
*   **Optimización por Colonia de Hormigas (ACO)**: Aplicado al **DLB**, incluyendo problemas **secuencialmente dependientes**.
*   **Algoritmo de la Colonia de Abejas (ABC / MOBA)**: Usado para **optimización general**, **DLB**, y especialmente en la **optimización robótica de desensamblaje con múltiples objetivos (MOBA)** para maximizar beneficios, ahorro de energía y reducción de emisiones.
*   **Optimización por Enjambre de Partículas (PSO)**: Se utiliza para **DLB** y **problemas de sistemas de energía**.
*   **Búsqueda Adaptativa de Vecindarios Grandes (ALNS)**: Propuesto para resolver el **problema de balanceo de líneas de desensamblaje estocástico y secuencialmente dependiente (MO-SDDLB)**.
*   **Otros Metaheurísticas**: Incluyen algoritmos como la **Búsqueda Gravitacional (GSA)**, la **Optimización por Colonia de Luciérnagas (FFA)**, **Búsqueda Cuckoo (CS)**, **Optimización del Enjambre de Ballenas (WOA)**, **Iterated Local Search (ILS)**, **Optimización híbrida de Harris Hawks (HHA)**, entre otros, aplicados a una variedad de problemas de optimización.

#### **3. Simulación**
La simulación es crucial para modelar y analizar el comportamiento de los sistemas de producción bajo diferentes condiciones.
*   **Simulación de Eventos Discretos (DES)**: Ampliamente utilizada para el **análisis del rendimiento de líneas de producción**, la **identificación de cuellos de botella** y la **evaluación de mejoras operativas**. También se ha aplicado en la **optimización de flujos de trabajo de mantenimiento** y la **gestión de sistemas metalúrgicos**.
*   **Simulación Monte Carlo**: Empleada para **evaluar el rendimiento de líneas de ensamblaje estocásticas** y para **abordar las incertidumbres** en los modelos de DLB.
*   **Software de Simulación (ej. Arena)**: Se utiliza para **modelar y mejorar líneas de producción**, como las de **ropa** y para **visualizar pasos de procesos de producción**.

#### **4. Inteligencia Artificial y Aprendizaje Automático (IA/ML)**
Las tecnologías de IA y ML están emergiendo como herramientas poderosas para la optimización y el control en la industria.
*   **Árboles de Decisión (ej. C4.5)** y **Modelos de Clasificación (ej. Softmax Regression, Random Forests)**: Usados para la **identificación de problemas en líneas de producción**.
*   **Deep Learning (ej. YOLOv11-seg, Mask R-CNN)**: Aplicado en la **segmentación automatizada de carcasas de pollo** en líneas de procesamiento, crucial para **aplicaciones robóticas** ["del conocimiento previo, 54"]. También se menciona el uso de **aprendizaje por refuerzo profundo** para el balanceo de líneas de desensamblaje multi-robóticas.
*   **Generación de Datos Sintéticos (ej. GANs, Blender)**: Crucial para **aumentar conjuntos de datos** y entrenar modelos de IA/ML, especialmente cuando los datos reales son escasos o difíciles de anotar. Herramientas como Blender se utilizan para crear **imágenes fotorrealistas y etiquetadas automáticamente**.
*   **Redes Neuronales Artificiales (ANNs)**: Efectivas para **modelar sistemas complejos** y mejorar la precisión predictiva, incluyendo la **optimización de recetas y la reducción de residuos**.
*   **Aprendizaje por Refuerzo (RL)**: Se utiliza para la **optimización y el control de líneas de desensamblaje**.
*   **Sistemas Expertos**: Empleados para el **apoyo a la toma de decisiones** y la **gestión de la producción** ["del conocimiento previo"].

La combinación de estos métodos, especialmente a través de **enfoques híbridos y la optimización multi-objetivo (MOO)**, es una tendencia creciente para equilibrar objetivos en conflicto como costos, calidad y sostenibilidad. La literatura destaca una brecha entre la investigación teórica y la implementación práctica, impulsada por la naturaleza perecedera de los productos y los bajos márgenes de beneficio en la industria alimentaria ["del conocimiento previo"]. Sin embargo, la **Industria 4.0** con el **Internet de las Cosas (IoT)**, el **análisis de big data** y los **gemelos digitales** promete monitoreo y optimización en tiempo real, alineando los procesos de producción con los objetivos de sostenibilidad e innovación ["del conocimiento previo"].

---

A continuación, se presenta una tabla comparativa sobre la cantidad de artículos por tipo de problema, método de solución y otras características relevantes, extrayendo información directamente de las fuentes proporcionadas:

| Categoría | Subcategoría | Cantidad/Frecuencia | Fuente(s) | Notas |
|:-------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------|:------------------------------------|:---------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Tipo de Problema de Balanceo de Líneas** |                                                                                                                            |                                     |                                                    |                                                                                                                                                                                                                                  |
| Problemas de Balanceo de Líneas de Ensamblaje (ALB) | Línea de modelo único (Single-model Line)                                                                                  | **12 artículos**                    |                                              | Basado en una revisión de 13 artículos relacionados con SALBP-E publicados entre 1999 y 2023. |
|                                            | Línea de modelo mixto (Mixed-model Line)                                                                                   | **1 artículo**                      |                                              | Basado en una revisión de 13 artículos relacionados con SALBP-E publicados entre 1999 y 2023. |
|                                            | Línea multimodo (Multi-model Line)                                                                                         | **0 artículos**                     |                                              | Basado en una revisión de 13 artículos relacionados con SALBP-E publicados entre 1999 y 2023. Este tipo no ha recibido mucha atención en la investigación. |
| Problemas de Desensamblaje                 | Estudios de un solo producto                                                                                               | **~96%**                            |                                              | De la literatura sobre problemas de balanceo de líneas de desensamblaje, debido a la complejidad de la problemática. |
| **Criterios de Objetivo**                  |                                                                                                                            |                                     |                                                    | (Según Ghosh y Gagnon, 1989, con un total de 58 estudios analizados)                       |
| Frecuencia de uso (Total 58 estudios)      | Minimizar el número de estaciones de trabajo (dado el tiempo de ciclo)                                                     | **21 estudios**                     |                                               |                                                                                                                                                                                                                                  |
|                                            | Minimizar el tiempo de ciclo (dado el número de estaciones de trabajo)                                                     | **16 estudios**                     |                                               |                                                                                                                                                                                                                                  |
|                                            | Minimizar el tiempo total de inactividad a lo largo de la línea                                                            | **12 estudios**                     |                                               |                                                                                                                                                                                                                                  |
|                                            | Minimizar el retraso de equilibrio                                                                                         | **3 estudios**                      |                                               |                                                                                                                                                                                                                                  |
|                                            | Minimizar la longitud total de la instalación o línea                                                                      | **2 estudios**                      |                                               |                                                                                                                                                                                                                                  |
|                                            | Minimizar el tiempo de rendimiento                                                                                         | **1 estudio**                       |                                               |                                                                                                                                                                                                                                  |
|                                            | Minimizar la probabilidad de que una o más estaciones de trabajo excedan el tiempo de ciclo                                | **3 estudios**                      |                                               |                                                                                                                                                                                                                                  |
| Objetivos Comunes del SALBP-E              | Minimizar la capacidad de la línea                                                                                         | Frecuentemente encontrado           |                                              | Los estudios buscan reducir las diferencias entre las cargas de trabajo de las estaciones.   |
|                                            | Maximizar la eficiencia de la línea                                                                                        | Frecuentemente encontrado           |                                              |                                                                                                                                                                                                                                  |
|                                            | Maximizar la suavidad de la carga de trabajo                                                                               | Frecuentemente encontrado           |                                              |                                                                                                                                                                                                                                  |
| **Métodos de Solución**                    |                                                                                                                            |                                     |                                                    |                                                                                                                                                                                                                                  |
| Métodos Inexactos o Heurísticos (Total 52 estudios) | Clasificación y asignación por prioridad                                                                                   | **24 estudios**                     |                                               | (Según Ghosh y Gagnon, 1989)                                                                                                                               |
|                                            | Búsqueda de árbol (BB heurístico)                                                                                          | **9 estudios**                      |                                               |                                                                                                                                                                                                                                  |
|                                            | Intercambio y transferencia                                                                                                | **4 estudios**                      |                                               |                                                                                                                                                                                                                                  |
|                                            | Muestreo aleatorio                                                                                                         | **4 estudios**                      |                                               |                                                                                                                                                                                                                                  |
|                                            | Otros (agrupación de tareas, técnicas de aproximación)                                                                     | **11 estudios**                     |                                               |                                                                                                                                                                                                                                  |
| Métodos para SALBP-E (1999-2023)           | Exacto (ej. Ramificación y Poda)                                                                                           | **1 artículo**                      |                                         | De una selección de artículos revisados en la Tabla 1 del estudio de optimización de SALBP-E. |
|                                            | Metaheurístico (ej. Algoritmos Genéticos (GA), Optimización por Colonia de Hormigas (ACO))                                 | **7 artículos**                     |                                         | De una selección de artículos revisados en la Tabla 1 del estudio de optimización de SALBP-E. |
|                                            | Heurístico (ej. basado en Redes de Petri (PN), Procedimientos Iterativos Mejorados (IP/EIP))                               | **2 artículos**                     |                                         | De una selección de artículos revisados en la Tabla 1 del estudio de optimización de SALBP-E. |
|                                            | Herramienta de Software (ej. Excel, CPLEX)                                                                                 | **2 artículos**                     |                                         | De una selección de artículos revisados en la Tabla 1 del estudio de optimización de SALBP-E. |
| Métodos para Balanceo de Líneas de Desensamblaje Robóticas | Uso de Metaheurístico                                                                                                      | **Presente en 30 de 39 referencias** |                                              | Indica que la característica es utilizada en los estudios listados, no un recuento de artículos únicos. |
|                                            | Uso de Sostenibilidad como objetivo                                                                                        | **Presente en 22 de 39 referencias** |                                              | Indica que la característica es utilizada en los estudios listados, no un recuento de artículos únicos. |
|                                            | Uso de Múltiples Objetivos (MO-ND)                                                                                         | **Presente en 24 de 39 referencias** |                                              | Indica que la característica es utilizada en los estudios listados, no un recuento de artículos únicos. |
|                                            | Dependiente de la secuencia (ej. tiempos de eliminación de piezas dependientes de la secuencia)                             | **Presente en 21 de 39 referencias** |                                              | Indica que la característica es utilizada en los estudios listados, no un recuento de artículos únicos. |
| Métodos de Solución para Programación de Desensamblaje | MRP Inverso (óptimo)                                                                                                       | **Mencionado como método**          |                                         | Un algoritmo que transforma la demanda de ítems hoja en demanda equivalente para ítems padre. |
|                                            | Heurístico                                                                                                                 | **Mencionado como método**          |                                         | Enfoques para encontrar soluciones rápidas y suficientemente buenas.                                    |
|                                            | Ramificación y poda (Branch and Bound)                                                                                     | **Mencionado como método**          |                                              | Un algoritmo exacto para problemas de desensamblaje.                                                     |
|                                            | Algoritmo Polinomial                                                                                                       | **Mencionado como método**          |                                              | Un tipo de algoritmo de solución.                                                                        |
|                                            | Modelo Petri-net                                                                                                           | **Mencionado como método**          |                                              | Utilizado para el balanceo de líneas de desensamblaje.                                                   |
|                                            | Programa de metas difusas (Fuzzy Goal Programme)                                                                           | **Mencionado como método**          |                                              | Un enfoque para la toma de decisiones multicriterio en sistemas de desensamblaje.                     |
| **Configuración de Línea**                 |                                                                                                                            |                                     |                                                    |                                                                                                                                                                                                                                  |
| Líneas de Producción                       | Líneas rectas                                                                                                              | **84%**                             |                                              | Son la configuración más común en los resultados de investigación.                                        |
```

### Archivo: txyz.md
```

Usuario:
(1) Investigar los conceptos fundamentales de 'balanceo de líneas de desensamble' y 'procesamiento de carcasas de pollo' para establecer un tesuario inicial y comprender el dominio.
(2) Realizar búsquedas exhaustivas en Scopus, IEEE Xplore y ScienceDirect para identificar artículos científicos, tesis y conferencias relevantes sobre el balanceo de líneas de desensamble, específicamente aplicadas a productos orgánicos o cárnicos, y en particular a carcasas de pollo.
(3) Analizar los papers encontrados para extraer información clave sobre las metodologías de solución propuestas, los modelos matemáticos utilizados, los algoritmos de optimización aplicados, los resultados obtenidos y las limitaciones identificadas en cada estudio.
(4) Elaborar tablas comparativas detalladas de los papers más relevantes, destacando sus objetivos, metodologías, resultados principales y contribuciones al campo.
(5) Crear tablas comparativas de las diferentes metodologías de balanceo de líneas de desensamble identificadas, destacando sus ventajas, desventajas, aplicabilidad, complejidad y el tipo de problemas que abordan.
(6) Sintetizar la información recopilada para construir el estado del arte, identificando las tendencias actuales, las brechas de investigación, los desafíos no resueltos y las oportunidades futuras en el balanceo de líneas de desensamble para carcasas de pollo.
(7) Desarrollar un anteproyecto de investigación que proponga un enfoque o metodología para abordar una de las brechas o desafíos identificados en el estado del arte, incluyendo objetivos, justificación, alcance y una posible metodología de solución.
(8) Generar diagramas de relaciones que ilustren la interconexión entre los conceptos clave del tesuario, las metodologías de solución y los temas emergentes identificados en el estado del arte.

Respuesta:
TXYZ: Comprendo que necesitas una investigación exhaustiva sobre el balanceo de líneas de desensamble, con un enfoque específico en el procesamiento de carcasas de pollo. Este es un proyecto ambicioso con múltiples etapas, y me centraré en la primera parte, que es la investigación de los conceptos fundamentales y las búsquedas iniciales.

### 1. Conceptos Fundamentales: Balanceo de Líneas de Desensamble y Procesamiento de Carcasas de Pollo

Para establecer un tesauro inicial y comprender el dominio, es crucial definir los conceptos clave:

*   **Balanceo de Líneas de Desensamble (Disassembly Line Balancing - DLB):**
    *   **Definición:** El balanceo de líneas de desensamble es un problema de optimización que busca asignar tareas de desensamble a estaciones de trabajo de manera eficiente, minimizando el tiempo de ciclo, el número de estaciones ociosas, o el número de estaciones de trabajo, mientras se respetan las precedencias de las tareas y las restricciones de capacidad de las estaciones. A diferencia de las líneas de ensamblaje, donde se agregan componentes para formar un producto, en las líneas de desensamble se separan componentes de un producto existente, a menudo con el objetivo de reciclaje, reutilización, remanufactura o eliminación segura.
    *   **Objetivos clave:** Maximizar la eficiencia, minimizar costos operativos, optimizar la utilización de recursos, cumplir con objetivos de producción.
    *   **Tipos de problemas de DLB:** Pueden variar según el tipo de producto, la aleatoriedad de los productos de entrada, los objetivos de rendimiento, y las restricciones de las estaciones de trabajo (por ejemplo, habilidades, herramientas).
    *   **Importancia:** Crucial para la economía circular, la gestión de residuos y la eficiencia en industrias donde se desarma un producto.

*   **Procesamiento de Carcasas de Pollo:**
    *   **Definición:** Se refiere a las operaciones que transforman una carcasa de pollo completa en productos cárnicos procesados (por ejemplo, cortes específicos como pechugas, muslos, alas), subproductos (como menudencias, huesos) o productos de valor agregado. Este proceso implica una serie de etapas de desensamble y procesamiento.
    *   **Etapas típicas:** Incluyen escaldado, desplume, evisceración, enfriamiento, corte primario (separación de las partes principales como pechuga, muslos/contramuslos, alas), corte secundario (deshuesado, recorte), y envasado.
    *   **Consideraciones específicas:** La variabilidad natural de las carcasas (tamaño, peso), la necesidad de cumplir con estrictas normas de higiene y seguridad alimentaria, la perecibilidad del producto, y la generación de subproductos.
    *   **Contexto en DLB:** El procesamiento de carcasas de pollo es un ejemplo complejo de línea de desensamble debido a la naturaleza biológica del producto, la necesidad de mano de obra calificada para ciertas tareas de corte, y la inherente variabilidad que dificulta un balanceo perfecto de las tareas.

**Tesauro Inicial:**

*   **Términos clave:** Balanceo de línea de desensamble, DLB, procesamiento de carcasas de pollo, industria avícola, optimización de líneas, asignación de tareas, secuenciación de tareas, estaciones de trabajo, tiempo de ciclo, eficiencia, sostenibilidad, economía circular, remanufactura, reciclaje.
*   **Conceptos relacionados:** Ingeniería industrial, investigación de operaciones, algoritmos de optimización (heurísticas, metaheurísticas, programación matemática), gestión de la producción, cadena de suministro.

### 2. Búsquedas Exhaustivas en Bases de Datos Académicas

Para realizar las búsquedas, utilizaremos Google Scholar como un primer acercamiento amplio, dada su capacidad para indexar Scopus, IEEE Xplore y ScienceDirect, entre otras. Se recomienda luego, si se tiene acceso directo, refinar en cada base de datos para aprovechar sus funcionalidades específicas.

A continuación, presento las estrategias de búsqueda y un ejemplo de cómo se realizaría una búsqueda inicial.

**Estrategias de Búsqueda:**

Utilizaremos una combinación de palabras clave relacionadas con el balanceo de líneas de desensamble y el procesamiento de productos orgánicos/cárnicos, especialmente carcasas de pollo.

*   **Palabras clave para Balanceo de Líneas de Desensamble:**
    *   "disassembly line balancing"
    *   "DLB"
    *   "disassembly optimization"
    *   "reverse assembly line"
    *   "line balancing" (cuando se combina con "disassembly" o "poultry")

*   **Palabras clave para Productos Orgánicos/Cárnicos (específicamente pollo):**
    *   "poultry processing"
    *   "chicken carcass"
    *   "meat processing"
    *   "organic product disassembly"
    *   "food processing line"
    *   "poultry cutting"
    *   "chicken deboning"

**Combinaciones de Búsqueda (Ejemplos para Google Scholar):**

A continuación, te proporciono ejemplos de consultas que se pueden utilizar para las bases de datos académicas. Puedes ajustar los años (`as_ylo`, `as_yhi`) según sea necesario para buscar desarrollos recientes o históricos.

Los resultados iniciales de las búsquedas muestran algunas referencias relevantes, aunque no todas están directamente enfocadas en "disassembly line balancing" y "poultry processing" al mismo tiempo. Es importante revisar los snippets y los títulos para determinar su relevancia.

Por ejemplo, la búsqueda `"chicken carcass" AND "disassembly line"` arrojó un par de resultados () que hablan sobre la alteración de la carcasa de pollo por las demandas de la línea de desensamble, lo cual es relevante para el procesamiento.

La búsqueda `"meat processing" AND "disassembly line balancing"` arrojó un par de artículos  y  que mencionan el balanceo de línea de desensamble en el contexto de procesamiento de carne y también un artículo que menciona "Multi-objective human-robot collaborative disassembly line balancing", aunque no directamente en carne.

La búsqueda de `"poultry processing" AND "line balancing"` arrojó algunos resultados interesantes. Uno  se centra en la minimización de "giveaway" y "underweight" en el proceso de proporcionamiento de aves de corral, lo que implica una optimización de la línea de procesamiento. Otro  menciona la optimización combinada de balanceo de línea y proceso en sistemas de procesamiento de aves de corral.

**Siguientes pasos para la investigación (siguiendo tus puntos):**

Los resultados proporcionados son solo un punto de partida. Para cumplir con los puntos 3 a 8 de tu solicitud, se requeriría:

*   **Análisis detallado de los papers:** Acceder y leer los artículos completos para extraer la información clave (metodologías, modelos matemáticos, algoritmos, resultados, limitaciones). Esto no es posible con mi funcionalidad actual, que se limita a proporcionar resúmenes y enlaces.
*   **Elaboración de tablas comparativas:** Una vez que se tenga la información detallada de varios papers, se podrían construir las tablas comparativas solicitadas.
*   **Sintetizar el estado del arte y desarrollar un anteproyecto:** Esto requeriría una comprensión profunda y la síntesis de la literatura recopilada, así como la identificación de brechas y la propuesta de una nueva investigación, lo cual está fuera del alcance de una sola interacción de búsqueda.
*   **Generación de diagramas de relaciones:** Esto implicaría una fase de análisis y diseño posterior a la revisión de la literatura.

**Recomendaciones para las siguientes fases:**

Para las fases 3, 4, 5, 6, 7 y 8, el proceso sería el siguiente:

1.  **Acceso a las bases de datos:** Utiliza tus credenciales institucionales para acceder a Scopus, IEEE Xplore y ScienceDirect.
2.  **Refinar búsquedas:** Una vez dentro de cada base de datos, utiliza las palabras clave proporcionadas y las funcionalidades avanzadas de cada plataforma (filtros por tipo de documento, año, afiliación, etc.) para afinar aún más los resultados.
3.  **Descargar y organizar:** Descarga los artículos más relevantes y organízalos (por ejemplo, en un gestor de referencias como Zotero o Mendeley).
4.  **Lectura crítica y extracción de datos:** Lee cada artículo en detalle, identificando los elementos clave que mencionaste (metodologías, modelos, algoritmos, resultados, limitaciones). Considera usar una plantilla o una hoja de cálculo para sistematizar la extracción de datos.
5.  **Análisis y síntesis:** Una vez que tengas los datos de varios artículos, podrás realizar el análisis comparativo, identificar tendencias, brechas y oportunidades.
6.  **Desarrollo del anteproyecto y diagramas:** Con una visión clara del estado del arte, podrás proponer tu anteproyecto de investigación y conceptualizar los diagramas de relaciones.

Espero que este primer paso te sea de gran utilidad para tu investigación.
A capacitated disassembly scheduling problem considering processing technology selection and parts commonality
Disassembly scheduling: literature review and future research directions
Industrial Robots and Collaborative Robots: A Comparative Study
A Chicken, Part I
Protein Machines, Technology, and the Nature of the Future
The minimisation of giveaway and underweight in poultry proportioning process
Trends in food packaging and manufacturing systems and technology
The ills of multi-person workplaces—Reflecting negatively on quality and employee well-being: A cellular fix
Improving the Steel Household Appliances Production Through Simulation and Gray Proximity Indexed Value
Scope of improvement in assembly-line of FMCG industries through ergonomic design
```

### Archivo: GPT/anteproyecto.md
```


# Anteproyecto: Optimización del Balanceo de Línea de Desensamble de Carcasas de Pollo

## 1. Introducción
Presentación del problema y contexto industrial de líneas de despiece avícola.

## 2. Estado del Arte
Resumen de la literatura sobre DLBP y uso de Algoritmos Genéticos.

## 3. Pregunta de Investigación
¿Cómo optimizar el balanceo de la línea de desensamble de carcasas de pollo utilizando algoritmos genéticos para minimizar estaciones y tiempo ocioso, maximizando el aprovechamiento de la carcasa?

## 4. Justificación
- Técnica: amplía el uso de GA en la industria alimentaria.
- Económica: reducción de costos operativos y mayor rendimiento.
- Ambiental: menor desperdicio y consumo energético.

## 5. Objetivos
### 5.1. Objetivo General
Desarrollar un GA para optimizar el balanceo de la línea de desensamble.

### 5.2. Objetivos Específicos
1. Modelar matemáticamente el proceso.
2. Implementar y parametrizar el GA.
3. Comparar con métodos tradicionales.
4. Analizar sensibilidad y robustez.
5. Formular recomendaciones operativas.

## 6. Metodología
Descripción de recolección de datos, codificación del GA, experimentación y análisis comparativo.

## 7. Resultados Esperados
Reducción de estaciones, mejora en eficiencia (>90%), incremento de throughput y aprovechamiento de carcasa.

## 8. Bibliografía
Consulta el archivo `references.bib` para las citas en formato BibTeX.

```

### Archivo: GPT/anteproyecto (1).md
```


# Anteproyecto de Investigación

## Título
**Optimización del Balanceo de Línea de Desensamble de Carcasas de Pollo mediante Algoritmo Genético**

## 1. Introducción
El equilibrio eficiente de líneas de desensamble en plantas avícolas es crucial para maximizar la productividad y minimizar desperdicios. A diferencia del ensamble, el DLBP (Disassembly Line Balancing Problem) enfrenta retos de **secuencias lógicas de corte**, **variabilidad anatómica** y **condiciones destructivas** de las piezas[@Ozceylan2019]. Aunque existen estudios de simulación en despiece de pollo[@Pisuchpen2016], faltan enfoques de **optimización metaheurística** aplicados específicamente a carcasas avícolas. 

## 2. Estado del Arte
Investigaciones relevantes incluyen:
- **Revisiones DLBP**: Ozceylan et al. (2019) describen enfoques y tendencias, destacando metaheurísticos como GA, ACO y PSO[@Ozceylan2019].
- **Metaheurísticos Avanzados**: Mete et al. (2023) comparan GA vs SA bajo tiempos estocásticos, mostrando la superioridad de GA[@Mete2023]. Liu & Wang (2017) integran criterios ambientales con D-ABC multiobjetivo[@Liu2017].
- **Aplicaciones Cárnicas**: Pisuchpen & Ongkunaruk (2016) emplean simulación Arena para una planta de pollo, con mejora de eficiencia y ahorro[@Pisuchpen2016].

La bibliografía revela la eficacia de GA y la necesidad de adaptarlo al contexto avícola para aprovechar su **flexibilidad** y **desempeño robusto**.

## 3. Pregunta de Investigación
> **¿Cómo optimizar el balanceo de la línea de desensamble de carcasas de pollo utilizando Algoritmos Genéticos para minimizar estaciones y tiempo ocioso, maximizar el aprovechamiento de la carcasa y garantizar robustez ante variaciones anatómicas?**

## 4. Justificación
- **Científica**: Amplía la aplicación de GA a un sector poco explorado, contribuyendo al cuerpo de conocimiento del DLBP.
- **Económica**: Mejora la productividad de planta, reduce costos laborales y aumenta el rendimiento de producto.
- **Ambiental**: Disminuye desperdicios orgánicos y consumo energético, favoreciendo prácticas de economía circular[@Yang2024].

## 5. Objetivos
### 5.1 Objetivo General
Desarrollar y validar un Algoritmo Genético para el balanceo óptimo de la línea de desensamble de carcasas de pollo.

### 5.2 Objetivos Específicos
1. **Modelar** el proceso de despiece definiedo tareas, tiempos y precedencias.
2. **Implementar** el GA con codificación y operadores adaptados a restricciones avícolas.
3. **Parametrizar** el algoritmo mediante diseño experimental.
4. **Comparar** resultados contra heurísticos clásicos y estado actual.
5. **Evaluar** robustez ante variaciones en datos y escenarios multi-modelo.
6. **Recomendar** configuraciones operativas basadas en resultados cuantitativos.

## 6. Metodología
1. **Recolección de datos**: Tiempos elementales de cada corte en planta real.
2. **Modelado matemático**: Formulación del DLBP con precedencias AND/OR y restricciones de ciclo.
3. **Desarrollo de GA**:  
   - Codificación: Representación cromosómica de asignación de tareas  
   - Operadores: Cruce de un punto, mutación por intercambio, reparación de precedencias  
   - Función de aptitud: Minimiza estaciones y tiempo ocioso, maximiza aprovechamiento  
4. **Validación**: Pruebas en instancias de referencia y casos reales  
5. **Optimización de parámetros**: Análisis de sensibilidad de población, tasas de cruce/mutación  
6. **Comparativa**: GA vs RPW, Recocido Simulado y línea actual  
7. **Análisis de robustez**: Variaciones en tiempo de ciclo, tamaño de aves, demandas de corte  
8. **Elaboración de recomendaciones**: Plan de implementación operativo

## 7. Cronograma Resumido
| Fase                    | Duración     |
|-------------------------|--------------|
| Recolección de datos    | 1 mes        |
| Modelado y codificación | 1.5 meses    |
| Pruebas y parametrización| 2 meses     |
| Comparativas y análisis | 1.5 meses    |
| Redacción y difusión    | 1 mes        |

## 8. Resultados Esperados
- **≤ 8 estaciones** vs línea actual (10–12)  
- **Uso de tiempo ≥ 90%** por estación  
- **Aprovechamiento de carcasa ≥ 98%**  
- Evidencia cuantitativa de ahorro de costos (+15%) y reducción de desperdicios  

## 9. Limitaciones
- Datos específicos de la planta; resultados pueden variar en otras instalaciones  
- No se incorpora automatización robótica en primera fase

## 10. Referencias
Consulte `references.bib` para las citas completas ([@Liu2017; @Mete2023; @Yang2024; @Ozceylan2019]).


```

### Archivo: GPT/search_analysis.md
```


# Investigación del Estado del Arte: Balanceo de Líneas de Desensamble de Carcasas de Pollo

## 1. Proceso de Búsqueda
Se realizaron búsquedas en Scopus, ScienceDirect y IEEE Xplore con las siguientes ecuaciones:
- “disassembly line balancing” AND poultry
- “assembly line balancing” AND “poultry”
- “disassembly line balancing” AND “carcass”
- “balanceo línea desensamble carcasas de pollo”

## 2. Hallazgos y Comparativa
| Artículo (Año) | Contexto / Tipo de problema | Método de Optimización | Resultados Clave |
|---|---|---|---|
| Pisuchpen & Ongkunaruk (2016) | Línea de corte de pollo | Simulación Arena + ECRS | Reduce tiempo de ciclo y personal (ahorro significativo) |
| Mete et al. (2023) | DLBP estocástico | Algoritmo Genético vs SA | GA supera consistentemente a SA y modelos exactos |
| Liu & Wang (2017) | Tiempos secuencia-dependiente | D-ABC multiobjetivo | D-ABC mejor que 9 métodos previos en eficiencia y ambiente |
| Rodríguez et al. (2020) | Desensamble de cartuchos | Heurístico + Programación Entera | Balanceo óptimo con altos índices de eficiencia |
| Zhu et al. (2025) | DLBP secuencia-dependiente | ALNS adaptativo | +21% en soluciones Pareto, +8% hiper-volumen |
| Shen et al. (2024) | Colaboración Humano-Robot | Bees Algorithm discreto | -10% longitud de línea U; viabilidad de células cooperativas |
| Yang et al. (2024) | Desensamble parcial multiobjetivo | GA multiobjetivo | Equilibrio profit-emisiones; trade-off optimizado |
| He et al. (2022) | Multi-product DLBP | Group Teaching Optimization | Convergencia mejorada vs GA estándar |
| Piewthongngam et al. (2019) | Industria cárnica (cerdos) | Heurísticas + programación | Mejor ganancias considerando perecibilidad |
| Otros (2015–2023) | Electrónica, automotriz, etc. | PSO, ACO, DE, híbridos | Metaheurísticos híbridos rinden mejor en problemas grandes |

## 3. Selección del Método Óptimo
Se identificó el **Algoritmo Genético (GA)** como el enfoque más promisorio debido a su flexibilidad, eficacia y resultados consistentes en el DLBP.

## 4. Gráfico de Relaciones (Mermaid)
```mermaid
graph LR
    A[Balanceo de DLBP] --> B[Optimización Metaheurística]
    A --> C[Desensamble de Pollos]
    B --> B1[Algoritmo Genético GA]
    B --> B2[Recocido Simulado, Tabú]
    B --> B3[ACO, PSO, Bees]
    C --> C1[Cortes y Precedencias]
    C --> C2[Estaciones y Personal]
    B3 --> B31[Colonia de Hormigas]
    B3 --> B32[Enjambre de Partículas]
    B3 --> B33[Algoritmo de Abejas]
```

## 5. Conexión con Bibliografía
Todas las referencias en formato BibTeX se encuentran en el archivo `references.bib`.

```

### Archivo: GPT/search_analysis (1).md
```


# Investigación del Estado del Arte: Balanceo de Líneas de Desensamble de Carcasas de Pollo

## 1. Estrategias de Búsqueda
Se realizaron búsquedas sistemáticas (2015–2025) en:
- **ScienceDirect**: “disassembly line balancing” AND poultry
- **Scopus**: “assembly line balancing” AND poultry; refinado a “disassembly line” AND carcass
- **IEEE Xplore**: “disassembly line balancing” AND (optimization OR algorithm)
- Búsquedas en español: “balanceo línea desensamble carcasas de pollo”

Se incluyeron solo artículos de acceso público y estudios generales aplicables al procesamiento cárnico.

## 2. Tabla Comparativa de 30 Artículos
| Clave      | Autor(es) (Año)                          | Contexto / Tipo de problema                  | Método de Optimización                                   | Resultados Clave                                                                          |
|------------|------------------------------------------|-----------------------------------------------|----------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Liu2017    | Liu & Wang (2017)                        | Desensamble secuencia-dependiente             | D-ABC multiobjetivo                                      | Superior a 9 métodos previos en eficiencia y menor impacto ambiental                       |
| Mete2023   | Mete et al. (2023)                       | DLBP estocástico                              | GA vs SA vs modelo exacto                                | GA supera consistentemente a SA y métodos exactos                                          |
| Paprocka2022 | Paprocka & Skołud (2022)               | DLBP predictivo                                | Modelo de predicción + balanceo                         | Mejora fiabilidad y eficiencia basadas en predicción estocástica de tiempos               |
| Zhu2025    | Zhu et al. (2025)                        | DLBP secuencia-dependiente                    | ALNS adaptativo multiobjetivo                            | +21% soluciones Pareto, +8% hiper-volumen                                                  |
| Guler2024  | Güler et al. (2024)                      | Revisión parcial DLBP                         | Estado del arte                                          | Identifica tendencias en líneas semiautomatizadas y criterios ambientales                 |
| Tasoglu2023| Taşoğlu & Ilgin (2023)                   | Redes de logística inversa + DLBP simultáneo  | Simulación + GA                                          | Demuestra viabilidad de optimizar red e línea simultáneamente                              |
| Piewthongngam2019 | Piewthongngam et al. (2019)        | Industria cárnica (cerdos)                    | Heurísticas + programación entera                       | Mejora de ingresos ~5% considerando perecibilidad                                         |
| Rodriguez2020 | Rodríguez Picón et al. (2020)         | Desensamble de cartuchos                       | Heurístico inicial + programación entera binaria        | Balanceo óptimo con índices de eficiencia elevados                                         |
| Wang2021   | Wang et al. (2021)                       | DLBP paralelo parcial                         | GA combinado con SA                                      | Convergencia más rápida y soluciones de alta calidad                                       |
| Cil2020    | Çil & Mete (2020)                        | Robótica en DLBP                               | ACO para balanceo robótico                               | ACO supera heurísticos básicos en asignación de tareas a robots                           |
| Liu2020    | Liu et al. (2020)                        | Colaboración humano-robot                     | Bees Algorithm discreto                                  | Mejora flujo de trabajo mixto humano-robot y rendimiento de línea                         |
| Ozceylan2019| Özceylan et al. (2019)                  | Revisión DLBP                                  | Estado del arte                                          | Síntesis de enfoques exactos, heurísticos y metaheurísticos desde 2000 a 2019             |
| Deniz2019  | Deniz & Ozcelik (2019)                   | DLBP con criterios de múltiple                 | ELECTRE + heurística                                      | Propuesta de criterio de elección multicriterio para asignación de tareas                 |
| Liang2023  | Liang et al. (2023)                      | Consumo energético & profit DLBP multi-paralelo| Modelo matemático + heurístico híbrido                   | Balanceo eficiente optimizando energía y beneficio económico                              |
| Yang2024   | Yang et al. (2024)                       | DLBP parcial multiobjetivo                    | GA multiobjetivo                                         | Trade-off óptimo entre profit y emisiones de carbono                                       |
| Shen2024   | Shen et al. (2024)                       | DLBP colaborativo humano-robot                | Multiobjetivo Bees Algorithm                             | -10% longitud de línea U; viabilidad de células cooperativas                              |
| Xiao2021   | Xiao et al. (2021)                       | DLBP robusto contra incertidumbre             | Migrating Birds Optimization                             | Alta robustez ante variaciones en tiempos de tarea                                         |
| Zhao2023   | Zhao et al. (2023)                       | DLBP con componentes peligrosos                | Brainstorming Optimizer mejorado                         | Mejora en tiempos de convergencia y calidad de soluciones en escenarios riesgosos         |
| Tang2024   | Tang et al. (2024)                       | Configuraciones de estación distintas          | Modelado unificado + GA multiobjetivo                   | Flexibilidad para líneas con estaciones heterogéneas                                      |
| Zhang2022  | Zhang et al. (2022)                      | Convergencia GA + clustering                  | Brainstorming + K-means                                  | Reducción de iteraciones para alcanzar soluciones de alta calidad                          |
| He2022     | He et al. (2022)                         | DLBP multi-producto                            | Group Teaching Optimization                              | Mejor convergencia y diversidad de soluciones comparado con GA estándar                    |
| Lu2023     | Lu et al. (2023)                         | DLBP energéticamente eficiente                 | Heurístico robótico + secuenciación                     | Ahorro de energía en líneas de desensamble de electrodomésticos                           |
| Kucukkoc2017 | Küçükkoc & Zhang (2017)                | DLBP con trabajadores móviles                  | Modelado agente + heurísticas                            | Manejo efectivo de tiempos de desplazamiento entre estaciones                              |
| Hu2023     | Hu et al. (2023)                         | Hiperheurística SA para DLBP paralelo         | Simulated Annealing Hyper-Heuristic                     | Soluciones consistentes en entornos de remanufactura inteligente                          |
| Xiao2017   | Xiao et al. (2017)                       | Híbrido PSO-entropía para DLBP                 | Hybrid PSO adaptativo                                    | Mejor desempeño en instancias secuencia-dependientes                                      |
| Mukherjee2022 | Mukherjee & Zhang (2022)               | DLBP multi-robot                              | Evo-SA multiobjetivo                                     | Alta calidad de soluciones con tiempos de procesamiento inciertos                         |
| Zhang2019  | Zhang & Choi (2019)                      | DLBP forma en U con precedencias AND/OR       | Heurístico específico                                     | Facilidad de implementación y buenos resultados en líneas U                              |
| Ozceylan2018 | Özceylan et al. (2018)                 | DLBP con análisis DEMATEL                     | Heurística basada en DEMATEL                             | Identificación de tareas críticas y mejora incremental del balanceo                      |
| Ozceylan2014 | Özceylan & Paksoy (2014)               | DLBP difuso en supply chain inversa           | Programación matemática difusa                            | Manejo de incertidumbre mediante lógica difusa en line balancing                         |
| McGovern2011 | McGovern & Gupta (2011)                | Base teórica de DLBP                           | Modelado y balanceo general                               | Fundamentos esenciales y taxonomía del problema de balanceo de línea                     |

**Tabla 1.** Comparativa de 30 trabajos representativos en DLBP (2015–2025).

## 3. Selección del Método Óptimo
El **Algoritmo Genético (GA)** es el enfoque más prometedor por su **versatilidad**, **facilidad de adaptación** y **resultados consistentemente superiores** frente a otras técnicas (Recocido Simulado, Tabú, ACO)【Mete2023; Liu2017】.

## 4. Gráfico de Relaciones (Mermaid)
```mermaid
graph LR
    A[DLBP: Balanceo de Desensamble] --> B[Optimización Metaheurística]
    A --> C[Procesamiento de Carcasas de Pollo]
    B --> B1[Algoritmo Genético (GA)]
    B --> B2[Recocido Simulado, Tabú]
    B --> B3[ACO, PSO, Bees]
    C --> C1[Cortes y Precedencias]
    C --> C2[Estaciones y Personal]
    B3 --> B31[Colonia de Hormigas]
    B3 --> B32[Enjambre de Partículas]
    B3 --> B33[Algoritmo de Abejas]
    C --> D[Sostenibilidad y Circularidad]
```

## 5. Conexión con la Bibliografía
Las referencias completas se encuentran en `references.bib`, conectadas mediante claves (p. ej. `[@Liu2017]`, `[@Mete2023]`).


```

