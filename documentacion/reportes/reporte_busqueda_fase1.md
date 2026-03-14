# Reporte de Búsqueda Bibliográfica — Fase 1
**Fecha:** 2026-02-26  
**Sprint:** 1.6 + 1.7  
**Queries ejecutadas:** Q1-Q8 en Scopus (acceso UTP)

---

## 1. Resumen Ejecutivo

Se ejecutaron **8 queries** en Scopus, obteniendo **478 resultados** brutos. Tras clasificación por relevancia (scoring automático + revisión manual de abstracts), se seleccionaron **13 papers** para lectura de texto completo, procesados con `markitdown`. De estos, se identificaron hallazgos que **confirman la complejidad NP-hard** del modelo propuesto y validan el uso de metaheurísticas.

### Hallazgo Principal
> El modelo del Anexo A (CLSP estocástico multi-producto con setup, lote mínimo y perecibilidad) es **NP-hard** por tres vías independientes confirmadas en la literatura:
> 1. El CLSP base es NP-hard (Florian et al. 1980; Bitran & Yanasse 1982) — citado por Goren & Tunali 2016
> 2. Agregar setup crossover + minimum lot size lo hace "computationally even more difficult" — Mahdieh et al. 2018
> 3. Two-stage stochastic capacitated lot-sizing es NP-hard — confirmado explícitamente por Rahmani et al. 2025

---

## 2. Estadísticas de Búsqueda (para Estado del Arte)

| Query | Tema | # Resultados | # Seleccionados |
|:-----:|------|:------------:|:---------------:|
| Q1 | Lot-sizing estocástico + NP-hard | 9 | 0 (cubierto por Q6) |
| Q2 | Metaheurísticas + Setup estocástico | 11 | 2 |
| Q3 | Perecibilidad + Lot-sizing | 20 | 2 |
| Q4 | Optimización avícola/cárnica | 186 | 4 |
| Q5 | 2-Etapas estocástico + Metaheurísticas | 218 | 2 |
| Q6 | CLSP + NP-hard | 30 | 2 |
| Q7 | Reviews multi-product stochastic | 0 | 0 |
| Q8 | Min batch + Setup + IP | 4 | 1 |
| **Total** | | **478** | **13** |

---

## 3. Papers Seleccionados y Hallazgos

### 🔴 Categoría A: Justificación NP-hard (Core)

#### A1. Goren & Tunali (2016) — `Goren2016`
- **Título:** A comparative study of hybrid approaches for solving capacitated lot sizing problem with setup
- **DOI:** 10.1504/EJIE.2016.081019
- **Hallazgo clave:** Cita directamente: *"The single item CLSP is shown to be NP-Hard by Florian et al. (1980) and Bitran and Yanasse (1982)"*. Confirma que CLSP con setup carryover y backordering es **computationally even more difficult**. Usa GA, TS y SA para resolver.
- **Uso en anteproyecto:** Sección 1.2 (justificación de complejidad), Estado del Arte, Anexo A.

#### A2. Rahmani et al. (2025) — `Rahmani2025`
- **Título:** Two-stage stochastic capacitated Lot-Sizing problem by Lot-Size adaptation approach
- **DOI:** 10.22060/AJMC.2023.22698.1184
- **Hallazgo clave:** Modelo de two-stage stochastic capacitated lot-sizing. Afirma explícitamente que es **NP-hard** y lo resuelve con un heurístico híbrido. Usa static y static-dynamic uncertainty strategies.
- **Uso en anteproyecto:** Justificación directa de que nuestro modelo estocástico de 2 etapas + capacitado + setup = NP-hard.

#### A3. Mahdieh et al. (2018) — `Mahdieh2018`
- **Título:** A novel flexible model for lot sizing and scheduling with non-triangular, period-dependent setup
- **DOI:** 10.1007/s10696-017-9279-5
- **Hallazgo clave:** Modela **minimum lot size** con **setup crossover** entre periodos. Demuestra que imponer lote mínimo agrega complejidad considerable al modelo base.
- **Uso en anteproyecto:** Justifica la restricción de lote mínimo ($Q_{min}$) del Anexo A.

#### A4. Roshani et al. (2017) — `Roshani2017`
- **Título:** A relax-and-fix heuristic approach for the capacitated dynamic lot sizing problem in integrated SC
- **DOI:** 10.1016/j.ifacol.2017.08.1580
- **Hallazgo clave:** Confirma NP-hardness del CLSP dinámico integrado en supply chain. Usa simulated annealing + relax-and-fix heuristic.
- **Uso en anteproyecto:** Refuerzo adicional para NP-hardness del CLSP.

---

### 🟠 Categoría B: Metaheurísticas para Lot-Sizing Estocástico

#### B1. Slama et al. (2021) — `Slama2021`
- **Título:** Genetic algorithm and Monte Carlo simulation for a stochastic capacitated disassembly lot-sizing problem under random lead times
- **DOI:** 10.1016/j.cie.2021.107468
- **Hallazgo clave:** Usa **GA + Monte Carlo Simulation** para resolver lot-sizing estocástico capacitado. Compara: (i) MIP exacto para instancias pequeñas, (ii) SAA con Monte Carlo para medianas, (iii) GA para grandes. **Demuestra que GA supera al MIP en instancias medianas y grandes.**
- **Uso en anteproyecto:** Justifica directamente nuestro enfoque GA para lot-sizing estocástico. Sección 5.2 y Fase 2 de metodología.

#### B2. Geiger (2025) — `Geiger2025`
- **Título:** A sample average approximation-based heuristic for the stochastic production routing problem
- **DOI:** 10.1007/s10100-024-00913-4
- **Hallazgo clave:** Usa SAA (Sample Average Approximation) como heurística para un two-stage stochastic programming model que integra producción, inventario y distribución. Demuestra viabilidad del enfoque heurístico para problemas estocásticos de producción.
- **Uso en anteproyecto:** Justifica que resolver modelos de 2 etapas con heurísticas/metaheurísticas es un enfoque establecido.

#### B3. Ghasemi et al. (2024) — `Ghasemi2024`
- **Título:** Model and solution approach to coordinate production-inventory strategies considering nonlinear price-sensitive demand
- **DOI:** 10.1080/00207543.2024.2314712
- **Hallazgo clave:** Two-stage stochastic MINLP para coordinar estrategias de producción-inventario en multi-level supply chain. Usa **progressive hedging algorithm** + decomposition.
- **Uso en anteproyecto:** Referencia metodológica para el enfoque de 2 etapas aplicado a producción.

---

### 🟡 Categoría C: Industria Avícola y Perecibilidad

#### C1. Akbari-Aghghaleh et al. (2025) — `AkbariAghghaleh2025`
- **Título:** Designing a perishable closed-loop poultry supply chain: metaheuristic approaches and model evaluation
- **DOI:** 10.1007/s10668-025-06675-6
- **Hallazgo clave:** **¡Paper más relevante para nuestro proyecto!** Diseña closed-loop poultry supply chain con perecibilidad. Reconoce explícitamente las **"NP-hard characteristics"** del modelo. Usa **DE, SA, GA y 2 híbridos (GA-SA, DE-SA)**. Compara rendimiento de 5 metaheurísticas. El MILP tiene perecibilidad + multi-producto + supply chain avícola.
- **Uso en anteproyecto:** Tabla 3 (estado del arte avícola), justificación del enfoque GA-TS híbrido, sección 5.4.

#### C2. Dadaneh et al. (2024) — `Dadaneh2024`
- **Título:** A stochastic chance-constraint framework for poultry planning and egg inventory management
- **DOI:** 10.1007/s12063-024-00507-y
- **Hallazgo clave:** Aplica **capacitated lot-sizing** directamente a **industria avícola** (egg production). Señala "high complexity" del problema. Usa **chance-constraint** bajo demand uncertainty.
- **Uso en anteproyecto:** Tabla 3, justifica aplicación de lot-sizing en avicultura, validación de relevancia sectorial.

#### C3. González-Neira et al. (2025) — `GonzalezNeira2025`
- **Título:** A novel MILP model for the operation of the poultry supply chain
- **DOI:** 10.1016/j.ifacol.2025.09.391
- **Hallazgo clave:** MILP para scheduling + transporte en supply chain avícola. Modelo complejo: "model complexity prevents from obtaining feasible solutions in some cases". **Paper colombiano** (Universidad Javeriana).
- **Uso en anteproyecto:** Tabla 3 (referencia colombiana reciente), complementa con scheduling.

#### C4. Juwitaa et al. (2024) — `Juwitaa2024`
- **Título:** Optimizing Broiler Chicken Supply Chains Under Uncertain Average Growth Rate Acceleration
- **DOI:** 10.1109/ICELTICs62730.2024.10776298
- **Hallazgo clave:** Usa **two-stage stochastic programming** para broiler chicken supply chain con incertidumbre en crecimiento. Aborda directamente la incertidumbre en producción avícola.
- **Uso en anteproyecto:** Tabla 3 (modelo estocástico en avicultura), sección 5.4.

#### C5. Claassen (2016) — `Claassen2016`
- **Título:** On production planning and scheduling in food processing industry: Modelling non-triangular setups and product decay
- **DOI:** 10.1016/j.cor.2016.06.017
- **Hallazgo clave:** Modela **non-triangular setups** (setup que no cumple desigualdad triangular, típico de limpieza profunda en industria alimentaria) + **product decay** (perecibilidad). Formulación MIP para food processing industry.
- **Uso en anteproyecto:** Justifica la restricción de setup dependiente de secuencia en el modelo, y la necesidad de modelar perecibilidad en FPI. Secciones 5.1, 5.3.

#### C6. Stefánsdóttir et al. (2017) — `Stefansdottir2017`
- **Título:** Classifying and modeling setups and cleanings in lot sizing and scheduling
- **DOI:** 10.1016/j.ejor.2017.03.023
- **Hallazgo clave:** Clasificación taxonómica de tipos de setup y limpieza en lot-sizing + scheduling. Define formalmente setups triangulares vs. non-triangulares y su impacto en la complejidad computacional.
- **Uso en anteproyecto:** Referencia taxonómica para categorizar nuestro tipo de setup. Sección 5.1.

---

## 4. Decisiones para la Fase 2

Basado en los hallazgos:

| Decisión | Sustento | Referencia |
|----------|----------|------------|
| ✅ Mantener restricción de setup ($s_p$) | Non-triangular setups son la norma en FPI | Claassen 2016, Stefánsdóttir 2017 |
| ✅ Activar restricción de vida útil ($L_p$) | Product decay es restricción obligatoria en FPI | Claassen 2016, Akbari-Aghghaleh 2025 |
| ✅ Mantener lote mínimo ($Q_{min}$) | Minimum lot size agrega complejidad NP-hard | Mahdieh 2018 |
| ✅ Modelo estocástico de 2 etapas | Enfoque establecido para lot-sizing bajo incertidumbre | Rahmani 2025, Slama 2021 |
| ✅ Usar GA como metaheurística principal | GA supera MIP exacto en instancias medianas/grandes | Slama 2021, Akbari-Aghghaleh 2025 |
| ⚠️ Considerar GA-SA híbrido | Mejores resultados que GA puro en poultry supply chain | Akbari-Aghghaleh 2025 |

---

## 5. Próximos Pasos

1. **Sprint 1.7 (restante):** Integrar los papers seleccionados a `referencias_coproductos.bib`
2. **Fase 2:** Aplicar correcciones al modelo (Anexo A) usando las decisiones de arriba
3. **Fase 3:** Actualizar estado del arte con estadísticas y papers de este reporte
