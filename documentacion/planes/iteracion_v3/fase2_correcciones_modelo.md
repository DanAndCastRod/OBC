# Fase 2: Correcciones al Modelo Matemático (Anexo A)

> **Estado:** ✅ Completada (2026-02-26)  
> **Prioridad:** ALTA — El modelo debe ser coherente antes de corregir el texto  
> **Duración real:** < 1 día

---

## Objetivo General de la Fase

Aplicar al modelo matemático del Anexo A las correcciones identificadas en la evaluación Y los ajustes informados por la literatura encontrada en la Fase 1. El modelo resultante debe ser:
1. **Formalmente NP-hard** — sustentado por la referencia clásica encontrada (ej. Bitran & Yanasse 1982)
2. **Internamente coherente** — todo parámetro definido debe usarse en al menos una restricción
3. **Narrativamente consistente** — lo que describe la metodología debe coincidir exactamente con lo que formula el Anexo A

---

## Dependencias de Fase 1 ✅ RESUELTAS

| Hallazgo requerido | Resultado | Referencia |
|-------------------|-----------|------------|
| Paper con prueba NP-hard del CLSP | ✅ Confirmado: CLSP es NP-hard | Goren 2016 (cita Florian 1980, Bitran & Yanasse 1982) |
| Formulación de restricción de vida útil | ✅ Product decay + non-triangular setups en FPI | Claassen 2016, Stefánsdóttir 2017 |
| ¿Canales de venta en lot-sizing avícola? | ❌ Ningún paper los modela → **eliminar del documento** | Búsqueda Q2/Q4 sin resultados |
| ¿Lote mínimo diferente? | ✅ Formulación estándar validada con crossover | Mahdieh 2018 |
| Two-stage stochastic lot-sizing es NP-hard | ✅ Confirmado explícitamente | Rahmani 2025 |
| Metaheurísticas apropiadas para poultry SC | ✅ **5 metaheurísticas evaluadas:** GA, SA, DE, GA-SA, DE-SA | Akbari-Aghghaleh 2025 |

---

## 📑 Tabla Contextual: Papers → PDFs

> Usar esta tabla como referencia rápida cuando la lectura del `.md` procesado falle (imágenes, fórmulas rotas, etc.).

| CiteKey | Autor principal | Año | PDF en `data/papers_nuevos/` | MD procesado en `data/papers_procesados/` |
|---------|----------------|:---:|------------------------------|-------------------------------------------|
| `Goren2016` | Goren, H. G. | 2016 | `Goren_2016_CLSPSetupHybrid.pdf` | `Goren_2016.md` |
| `Roshani2017` | Roshani, A. | 2017 | `Roshani_2017_CLSPRelaxFix.pdf` | `Roshani_2017.md` |
| `Mahdieh2018` | Mahdieh, M. | 2018 | `Mahdieh_2018_MinLotSetup.pdf` | `Mahdieh_2018.md` |
| `Rahmani2025` | Rahmani, A. | 2025 | `Rahmani_2025_TwoStageLotSizing.pdf` | `Rahmani_2025.md` |
| `Slama2021` | Slama, I. | 2021 | `Slama_2021_GADisassemblyLotSizing.pdf` | `Slama_2021.md` |
| `AkbariAghghaleh2025` | Akbari-Aghghaleh, Z. | 2025 | `Akbari-Aghghaleh_2025_PerishablePoultry.pdf` | `Akbari-Aghghaleh_2025.md` |
| `Dadaneh2024` | Dadaneh, D. Z. | 2024 | `Dadaneh_2024_PoultryLotSizing.pdf` | `Dadaneh_2024.md` |
| `GonzalezNeira2025` | González-Neira, E. M. | 2025 | `Gonzalez-Neira_2025_PoultryMILP.pdf` | `Gonzalez-Neira_2025.md` |
| `Juwitaa2024` | Juwitaa, R. | 2024 | `Juwitaa_2024_BroilerStochastic.pdf` | `Juwitaa_2024.md` |
| `Claassen2016` | Claassen, G. D. H. | 2016 | `Claassen_2016_NonTriangularSetups.pdf` | `Claassen_2016.md` |
| `Stefansdottir2017` | Stefánsdóttir, B. G. | 2017 | `Stefansdottir_2017_SetupsCleanings.pdf` | `Stefansdottir_2017.md` |
| `Geiger2025` | Geiger, A. | 2025 | `Geiger_2025_SAAProductionRouting.pdf` | `Geiger_2025.md` |
| `Ghasemi2024` | Ghasemi, E. | 2024 | `Ghasemi_2024_ProductionInventory.pdf` | `Ghasemi_2024.md` |

---

## 🧬 Metaheurísticas — Decisión Final ✅

### Seleccionadas (4 algoritmos)

| # | Algoritmo | Sigla | Tipo | Justificación |
|:-:|-----------|:-----:|------|---------------|
| 1 | **Genetic Algorithm** | GA | Evolutivo | Más citado en lot-sizing estocástico. Exploración global poblacional | Slama 2021, Goren 2016 |
| 2 | **Simulated Annealing** | SA | Trayectoria | Criterio Metropolis para escapar óptimos locales en vecindarios de toggle/ajuste | Roshani 2017, Akbari-Aghghaleh 2025 |
| 3 | **Differential Evolution** | DE | Evolutivo | Dinámica diferencial distinta al GA; efectivo en espacios mixtos continuo/entero | Akbari-Aghghaleh 2025 |
| 4 | **Híbrido GA-SA** | GA-SA | Híbrido memético | **Mejor rendimiento** en perishable poultry SC (benchmark más cercano) | Akbari-Aghghaleh 2025 |

### Criterios de selección

1. **Diversidad de paradigmas:** 2 evolutivos (GA, DE) + 1 trayectoria (SA) + 1 híbrido (GA-SA)
2. **Sustento bibliográfico:** Cada algoritmo tiene ≥1 referencia aplicada a lot-sizing/producción/avicultura
3. **Replicabilidad comparativa:** Alineado con el marco de Akbari-Aghghaleh 2025

### Excluidos (con justificación)

| Algoritmo | Razón de exclusión | Trabajo futuro |
|-----------|-------------------|----------------|
| **TS** (Tabu Search) | Sin sustento en poultry/perishable SC. SA cubre el paradigma de trayectoria con mejor evidencia | No |
| **DE-SA** (Híbrido) | Excede el alcance de maestría (5 algoritmos). GA-SA ya cubre el concepto híbrido y tuvo mejor rendimiento | ✅ **Propuesto como trabajo futuro** |

---

## 🏃 Sprint 2.1: Decisiones Informadas por la Literatura ✅

### 📋 Checklist

- [x] **2.1.1 Decisión sobre la restricción $L_p$ (vida útil):**
  - [x] Revisar cómo los papers modelan la perecibilidad → Claassen 2016: "product decay", Akbari-Aghghaleh 2025: perecibilidad en poultry SC
  - [x] **✅ Opción A seleccionada:** Restricción dura — $I_{pt\omega} = 0$ si el inventario excede $L_p$ periodos (alineada con Claassen 2016)
  - [x] Documentada con referencia a Claassen 2016

- [x] **2.1.2 Decisión sobre "canales de venta":** → **ELIMINADOS** (sin sustento en literatura)
  - [x] Verificado: ningún paper de Q2/Q4 modela canales en lot-sizing avícola
  - [x] Decisión: Eliminar todas las menciones a "canales" del documento

- [x] **2.1.3 Validación de la estructura setup + batch mínimo:**
  - [x] Confirmado: Mahdieh 2018 usa $Q^{min}$ con setup crossover, formulación estándar
  - [x] Goren 2016 confirma CLSP con setup como NP-hard

- [x] **2.1.4 Decisión sobre metaheurísticas a implementar:**
  - [x] Seleccionados **4 de 6**: GA, SA, DE, GA-SA
  - [x] Excluidos: TS (sin sustento avícola), DE-SA (alcance de maestría → trabajo futuro)
  - [x] Justificación: diversidad de paradigmas + sustento bibliográfico + replicabilidad

---

## 🏃 Sprint 2.2: Implementación de Correcciones al Anexo A ✅

### 📋 Checklist

- [x] **2.2.1 Agregar restricción de vida útil:**
  - [x] Insertada nueva ecuación (Eq. 7) — restricción dura $I_{pt\omega} = 0$ si $t' - t > L_p$
  - [x] Texto explicativo incluido
  - [x] Citado Claassen 2016 como sustento

- [x] **2.2.2 Actualizar introducción del Anexo A:**
  - [x] Agregada cadena de citas: Florian 1980 → Bitran & Yanasse 1982 → Goren 2016 → Rahmani 2025 → Mahdieh 2018
  - [x] Descripción consistente como "lot-sizing estocástico"

- [x] **2.2.3 Limpieza de inconsistencias narrativas:**
  - [x] Eliminadas 3 menciones a "canales de venta" (L143, L461, L497)
  - [x] Reemplazadas por: "decisiones de activación", "escenarios estocásticos", "vidas útiles"
  - [x] Metaheurísticas actualizadas: GA+TS+GA-TS → GA+SA+DE+GA-SA
  - [x] $L_p$ ya estaba definido como parámetro (L627) → ahora se usa en restricción nueva

- [x] **2.2.4 Verificación de consistencia:**
  - [x] 7 ecuaciones en el modelo (FO + 6 restricciones, incluyendo nueva Eq. perecibilidad)
  - [x] Conjuntos: $P, T, \Omega$ | Parámetros: $\alpha_p, W, d, r, c's, F, Q's, L_p, \pi_\omega$ | Variables: $y_t, q_t, v, I, u$
  - [x] $L_p$ ahora se usa en la restricción de perecibilidad ✅
  - [x] Todas las variables aparecen en FO o restricciones ✅

---

## Criterio de Salida de la Fase 2

✅ La fase se considera **COMPLETA**:
1. ✅ La restricción de $L_p$ está implementada y sustentada con referencia (Claassen 2016)
2. ✅ No existen inconsistencias entre metodología y modelo (canales eliminados, metaheurísticas consistentes)
3. ✅ Todo parámetro y variable definido se usa en al menos una ecuación ($L_p$ ahora activo)
4. ✅ La introducción del Anexo A cita la prueba formal de NP-hardness (Florian 1980, Bitran & Yanasse 1982)
5. ✅ El modelo tiene: 1 variable binaria ($y_t$), 1 variable entera ($q_t$), variables continuas ($v, I, u$), y restricciones de setup + batch + perecibilidad
