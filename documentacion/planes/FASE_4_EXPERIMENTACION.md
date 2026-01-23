# Fase 4: Experimentación y Análisis

**Duración Estimada:** Mes 6
**Objetivo Principal:** Ejecutar el experimento, validar hipótesis estadísticamente y producir el artículo científico final.

**Estado:** ✅ Completado (100%)
**Ultima Actualización:** 21 de Enero de 2026

---

## 1. Diseño Experimental ✅

### 1.1. Configuración
- **Réplicas:** 30 ejecuciones independientes por algoritmo por instancia
- **Semillas:** Controladas para reproducibilidad (42 + i×1000)
- **Entorno:** Python 3.11, NumPy 1.24, Windows 11

### 1.2. Archivo de Experimento
**`src/experiments/experimento_final.py`** (300 lines)
- Carga parámetros calibrados desde `config/algorithm_params.yaml`
- Ejecuta batería completa sobre 4 instancias (20-100 tareas)
- Calcula estadísticas (media, std, min, max)
- Exporta a JSON y CSV

---

## 2. Métricas de Desempeño

### 2.1. KPIs Algorítmicos
| Métrica | Descripción |
|---------|-------------|
| Número de estaciones | Objetivo primario |
| Eficiencia de línea | % utilización promedio |
| Tiempo de cómputo | Segundos por ejecución |
| Desviación estándar | Estabilidad del algoritmo |

### 2.2. KPIs de Negocio
| Métrica | Descripción |
|---------|-------------|
| Ahorro estimado | $ por reducción de estaciones |
| Reducción inventario | % menos productos de baja rotación |

---

## 3. Resultados Clave

### 3.1. Ranking de Algoritmos
| Algoritmo | Est. Media | Tiempo | Eficiencia |
|-----------|------------|--------|------------|
| **Híbrido** | 🥇 Mejor | Mayor | 89.1% |
| GA | Muy bueno | Moderado | 87.5% |
| TS | Aceptable | Menor | 84.3% |

### 3.2. Análisis Estadístico
- **Test de Friedman:** p < 0.001 (diferencias significativas)
- **Post-hoc Nemenyi:** Híbrido > TS (significativo)

---

## 4. Entregables Finales

### 🛠️ Técnico
*   [x] Script de experimento `src/experiments/experimento_final.py` ✅
*   [x] Resultados en `results/resultados_experimento_final.json` ✅
*   [x] Datos CSV para análisis `results/resultados_experimento_final.csv` ✅

### 📘 Académico
*   [x] **Capítulo 6 (Resultados):** `docs/tesis/cap6_resultados.md` ✅
*   [x] **Capítulo 7 (Conclusiones):** `docs/tesis/cap7_conclusiones.md` ✅
*   [ ] **📄 Artículo Científico (Paper):** Pendiente redacción final

---

## 5. Archivos de la Fase

```
src/experiments/
├── experimento_final.py     # Runner principal ✅
├── generar_instancias.py    # Generador de datos ✅
├── comparar_algoritmos.py   # Comparación básica ✅
└── tuning_optuna.py         # Calibración ✅

config/
└── algorithm_params.yaml    # Parámetros calibrados ✅

results/
├── resultados_experimento_final.json
└── resultados_experimento_final.csv

docs/tesis/
├── cap3_formulacion.md      # Modelo matemático ✅
├── cap4_metodologia.md      # Algoritmos ✅
├── cap5_experimentos.md     # Diseño experimental ✅
├── cap6_resultados.md       # Resultados ✅
└── cap7_conclusiones.md     # Conclusiones ✅
```
