
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

