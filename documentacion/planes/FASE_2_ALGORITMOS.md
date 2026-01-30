# Fase 2: Implementación Algorítmica

**Duración Estimada:** Mes 3-4
**Objetivo Principal:** Construir el motor de optimización metaheurístico y documentar su diseño lógico en el capítulo de Metodología.

**Estado:** ✅ Completado (100%)
**Ultima Actualización:** 20 de Enero de 2026

---

## 1. Arquitectura de Software

### 1.1. Estructura de Clases (POO)
Se recomienda un diseño modular para facilitar la hibridación:

*   **`ProblemInstance`**: Clase inmutable que carga y almacena la matriz de tiempos, precedencias y demanda.
*   **`Solution`**: Clase que representa una asignación específica (cromosoma). Debe tener métodos para calcular su propio `fitness` (makespan, balance, costo).
*   **`Optimizer`** (Clase Abstracta): Interfaz base.
    *   `GeneticAlgorithm(Optimizer)`
    *   `TabuSearch(Optimizer)`
    *   `HybridGATS(Optimizer)`

### 1.2. Librerías a Utilizar
*   **DEAP (Distributed Evolutionary Algorithms in Python):** Framework robusto para GA. Facilita la paralelización y manejo de poblaciones.
*   **NumPy:** Para operaciones matriciales rápidas en el cálculo de tiempos.

---

## 2. Diseño de Metaheurísticas

### 2.1. Algoritmo Genético (GA)
*   **Representación:** Permutación de tareas (como en el TSP) transformada a asignación de estaciones mediante un decodificador voraz.
*   **Población Inicial:** Generada aleatoriamente con heurísticas constructivas (ej. LPT - Longest Processing Time) para mejorar la calidad inicial.
*   **Cruce (Crossover):** Order Crossover (OX) o PMX para respetar precedencias.
*   **Mutación:** Swap (intercambio de dos tareas) o Insertion (mover una tarea).

### 2.2. Búsqueda Tabú (TS)
*   **Vecindario:** Definido por movimientos `Swap` y `Insert`.
*   **Lista Tabú:** Memoria de corto plazo para evitar ciclos.
*   **Criterio de Aspiración:** Permitir movimientos tabú si mejoran la mejor solución histórica.

### 2.3. Híbrido (Memetic Algorithm)
*   Estrategia: Usar GA para exploración global y aplicar TS a los mejores individuos de cada generación para refinamiento local (intensificación).

---

## 3. Estrategia de Desarrollo
1.  **Semana 1-2:** Implementar `ProblemInstance` y decodificadores. Tests unitarios para asegurar que las soluciones generadas son factibles (respetan precedencia).
2.  **Semana 3-4:** Implementar GA básico con DEAP.
3.  **Semana 5-6:** Implementar TS y validar contra resultados pequeños del MILP (Fase 1).
4.  **Semana 7-8:** Implementar Híbrido y optimización de código (profiling).

---

## 4. Entregables de la Fase

### 🛠️ Técnico
*   [x] Framework en Python funcional (`src/algorithms/`).
    *   `base.py`: Clases `ProblemInstance`, `Solution`, `Optimizer` (12.6KB)
    *   `genetic_algorithm.py`: GA con OX, swap, torneo (12.6KB, 333 lines) ✅
    *   `tabu_search.py`: TS con swap/insert, aspiración (11.6KB, 305 lines) ✅
    *   `hybrid.py`: Memetic GA+TS (7.4KB) ✅
*   [x] Tests unitarios pasando al 100% (`tests/test_algorithms.py`: 17 tests OK).

### 📘 Académico (Escritura)
*   [x] **Borrador Capítulo 4 (Metodología de Solución):** `docs/tesis/cap4_metodologia.md` (321 lines).
    *   Diagramas Mermaid de flujo (GA, TS, Híbrido).
    *   Pseudocódigo de OX, First-Fit, Memetic.
    *   Análisis de complejidad O(G·P·n).
