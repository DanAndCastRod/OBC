# Fase 3: Generación de Datos y Calibración

**Duración Estimada:** Mes 5
**Objetivo Principal:** Crear un banco de pruebas robusto y ajustar los hiperparámetros de los algoritmos.

**Estado:** ✅ Completado (100%)
**Ultima Actualización:** 21 de Enero de 2026

---

## 1. Generación de Instancias Sintéticas

### 1.1. Implementación Actual ✅

**Archivo:** `src/experiments/generar_instancias.py` (243 lines)

El generador crea instancias sintéticas con propiedades controladas:

| Tamaño | N Tareas | N Áreas | Ciclo | Densidad |
|--------|----------|---------|-------|----------|
| Pequeña | 20 | 4 | 30s | 0.30 |
| Mediana | 40 | 6 | 40s | 0.25 |
| Grande | 70 | 10 | 45s | 0.20 |
| Muy Grande | 100 | 12 | 50s | 0.15 |

**Características del generador:**
- Grafo DAG aleatorio dividido en áreas con cadenas secuenciales
- Tiempos de procesamiento uniformes (min-max configurable)
- Exportación a JSON en `data/instancias_sinteticas/`

### 1.2. Factores de Diseño Experimental

1. **Tamaño del Problema ($N$):** 20, 40, 70, 100 tareas
2. **Densidad de Precedencia:** Controlada por n_areas y densidad
3. **Variabilidad de Tiempos ($\sigma^2$):** Rango tiempo_min/tiempo_max

---

## 2. Comparación de Algoritmos ✅

**Archivo:** `src/experiments/comparar_algoritmos.py` (253 lines)

Framework completo para experimentación:

```
ejecutar_bateria_experimentos()
├── Por cada instancia
│   ├── Por cada algoritmo (GA, TS, Hybrid)
│   │   └── N repeticiones con semillas diferentes
└── Genera reporte estadístico (media, std, min, max)
```

**Métricas capturadas:**
- Número de estaciones
- Fitness
- Tiempo de ejecución
- Factibilidad
- Historial de convergencia

**Salida:** `src/experiments/resultados_comparacion.json`

---

## 3. Calibración de Parámetros (Tuning) 🟡

### 3.1. Enfoque Propuesto

**Herramienta:** `Optuna` (Python nativo) o `irace` (R package)

**Parámetros a calibrar:**

| Algoritmo | Parámetro | Rango |
|-----------|-----------|-------|
| **GA** | poblacion_size | [30, 100, 200] |
| | prob_cruce | [0.7, 0.8, 0.9] |
| | prob_mutacion | [0.05, 0.1, 0.2] |
| **TS** | tamano_lista_tabu | [10, 20, sqrt(N)] |
| | tamano_vecindario | [20, 30, 50] |
| **Hybrid** | aplicar_ts_cada | [10, 20, 30] gen |

### 3.2. Implementación ✅

**Archivo:** `src/experiments/tuning_optuna.py`

- Calibra GA, TS e Híbrido automáticamente
- Exporta a `config/algorithm_params.yaml`

---

## 4. Entregables de la Fase

### 🛠️ Técnico
*   [x] Generador de instancias `src/experiments/generar_instancias.py` ✅
*   [x] Framework de comparación `src/experiments/comparar_algoritmos.py` ✅
*   [x] Carpeta `data/instancias_sinteticas/` con 4 instancias JSON ✅
*   [x] Script de tuning `src/experiments/tuning_optuna.py` ✅
*   [ ] Ejecutar tuning para generar `config/algorithm_params.yaml` (requiere Optuna instalado)

### 📘 Académico (Escritura)
*   [x] **Capítulo 5: Diseño Experimental** `docs/tesis/cap5_experimentos.md` ✅
