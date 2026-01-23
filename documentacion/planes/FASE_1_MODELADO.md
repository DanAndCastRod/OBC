# Fase 1: Fundamentación y Modelado Matemático

**Duración Estimada:** Mes 1-2
**Objetivo Principal:** Traducir la problemática operativa del desensamble avícola a un modelo matemático formal (MILP) y redactar el capítulo correspondiente de la tesis.

**Estado:** ✅ Completado (100%)
**Ultima Actualización:** 19 de Enero de 2026

---

## 1. Definición Formal del Problema
El primer paso es formalizar el problema de balanceo de línea de desensamble (DLBP) con las particularidades avícolas.

### 1.1. Conjuntos
*   $T$: Conjunto de tareas de despiece.
*   $S$: Conjunto de estaciones de trabajo disponibles.
*   $P$: Conjunto de coproductos (partes).
*   $D$: Conjunto de períodos de demanda.

### 1.2. Parámetros
*   $t_i$: Tiempo de procesamiento de la tarea $i$ (estocástico/variable).
*   $d_{pt}$: Demanda del coproducto $p$ en el período $t$.
*   $c_p$: Precio de venta del coproducto $p$.
*   $h_p$: Costo de mantener inventario del coproducto $p$.
*   Precedencias: Grafo dirigido acíclico de tareas.

### 1.3. Variables de Decisión
*   $x_{is}$: Asignación de tarea $i$ a estación $s$ (binaria).
*   $y_{pt}$: Cantidad producida del coproducto $p$ en período $t$.
*   $I_{pt}$: Inventario del coproducto $p$ al final del período $t$.

---

## 2. Actividades de Modelado

### 2.1. Levantamiento de Restricciones
Se deben modelar matemáticamente las siguientes restricciones críticas:
1.  **Precedencia AND/OR:** Algunas tareas requieren que *todas* las predecesoras estén listas (ej. no se puede deshuesar el muslo sin separarlo de la carcasa).
2.  **Zonificación:** Tareas "sucias" (evisceración) no pueden estar en la misma estación que tareas "limpias" (fileteado) por normas sanitarias.
3.  **Capacidad de Estación:** La suma de tiempos en una estación no puede exceder el tiempo de ciclo $C$.

### 2.2. Formulación MILP (Mixed-Integer Linear Programming)
*   **Herramienta de Prototipado:** Python + `PuLP` o `Gurobi` (licencia académica).
*   **Entregable:** Script `src/models/milp_validation.py` que resuelva instancias pequeñas (5-10 tareas) para verificar que la lógica de precedencia y tiempos es correcta.

---

## 3. Revisión Bibliográfica Específica
Actualizar el estado del arte con enfoque en **formulaciones matemáticas**:
*   Buscar papers que modelen "Sequence Dependent Setup Times" en DLBP.
*   Revisar modelos de "Stochastic DLBP" para ver cómo manejan la varianza de tiempos.

---


### 🛠️ Técnico
*   [x] Script de validación `src/models/milp_validation.py` (✅ 11 tareas, precedencia, ciclo, **zonificación**).
*   [x] Script de beneficio `src/models/dlbp_profit.py` (✅ 12 áreas, demanda, inventario, penalizaciones).
*   [x] **Restricciones de Zonificación:** Separación sucias/limpias implementada y validada.
*   [x] **Tiempos Estocásticos:** Simulación Monte Carlo en `src/models/stochastic_dlbp.py` (✅ 100 runs, 92% con 4 estaciones).

### 📘 Académico (Escritura)
*   [x] **Borrador Capítulo 3 (Formulación):** `docs/tesis/cap3_formulacion.md`.
*   [x] **Borrador Capítulo 4 (Metodología):** `docs/tesis/cap4_metodologia.md`.
*   [x] **Actualizar Estado del Arte:** Papers estocásticos (Hu, Liu, Fang) ya integrados en `cap3_formulacion.md` (secciones 2.2 y 7).
