# 🐔 DLBP Avícola - Optimización del Balanceo de Carcasa

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Tests](https://img.shields.io/badge/Tests-50%20passing-brightgreen.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> **Modelo de Optimización DLBP con Metaheurísticas para la Industria Avícola Colombiana**

- Documentos en formato Markdown que describen el problema, la metodología de investigación y las guías de implementación.
- Código en `src/` para gestionar referencias bibliográficas de forma manual mediante un módulo de base de datos SQLite.
- Pruebas automáticas en `test/` que verifican la inserción de artículos en la base de datos.
- Guía consolidada en `development_guide.md` con pasos de investigación, implementación y recomendaciones para el anteproyecto.
## 📋 Descripción

Este proyecto desarrolla un modelo de optimización para el **Problema de Balanceo de Líneas de Desensamble (DLBP)** aplicado a la industria avícola colombiana. Implementa tres técnicas metaheurísticas (Algoritmo Genético, Búsqueda Tabú, y un Híbrido) para minimizar el número de estaciones de trabajo respetando restricciones de precedencia y tiempo de ciclo.

### 📊 Resultados Principales

| Algoritmo | Eficiencia Línea | Tiempo Promedio | Recomendación |
|-----------|------------------|-----------------|---------------|
| **Híbrido** | 89.1% | 3.41s | ⭐ Mejor calidad |
| GA | 87.5% | 2.34s | Balance calidad/tiempo |
| TS | 84.3% | 0.89s | Menor tiempo |

**Hallazgo clave:** Gap = 0% vs óptimo exacto en instancias probadas.

---

## 🚀 Quick Start

### Prerrequisitos
- Python 3.10 o superior
- PuLP (para solver MILP)

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/usuario/OBC.git
cd OBC

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecución Rápida

```bash
# Ejecutar algoritmo genético
python src/algorithms/genetic_algorithm.py

# Ejecutar comparación de algoritmos
python src/experiments/comparar_algoritmos.py

# Ejecutar experimento completo (30 réplicas × 4 instancias × 3 algoritmos)
python src/experiments/experimento_final.py

# Comparar con benchmarks (vs solver exacto MILP)
python src/experiments/benchmark_comparison.py
```

### Ejecutar Tests

```bash
# Ejecutar todos los tests
python -m unittest discover -s tests -v

# Resultado esperado: 50 tests, 50 passed
```

---

## 📁 Estructura del Repositorio

Este repositorio contiene tanto el **código fuente reutilizable** como los **entregables académicos** de la maestría.

```
OBC/
├── src/                      # 🛠️ CÓDIGO FUENTE (Framework DLBP)
│   ├── algorithms/           # Implementación de metaheurísticas (GA, TS, Híbrido, NSGA-II)
│   ├── models/               # Modelos matemáticos (MILP)
│   └── experiments/          # Scripts de experimentación
│
├── tests/                    # ✅ SUITE DE TESTS (Validación del código)
│
├── docs/                     # 📚 DOCUMENTACIÓN
│   ├── GUIA_USO_CODIGO.md    # -> Manual Técnico para desarrolladores
│   ├── tesis/                # -> Informe Final de Investigación (LaTeX/Markdown)
│   ├── presentacion/         # -> Diapositivas de Sustentación
│   └── planes/               # -> Planes de trabajo y bitácoras
│
└── results/                  # 📊 RESULTADOS EXPERIMENTALES
```

---

## 📚 Documentación Disponible

### Para Desarrolladores / Reutilización
*   **[Manual Técnico de Uso](docs/GUIA_USO_CODIGO.md):** Guía práctica para importar los algoritmos, configurar instancias y extender el framework para nuevos problemas. Lee esto si quieres usar el código.

### Entregables Académicos
*   **[Informe Final de Investigación](docs/tesis/INFORME_FINAL_COMPLETO.md):** Documento completo de la tesis.
*   **[Diapositivas de Sustentación](docs/presentacion/sustentacion_dlbp.html):** Presentación interactiva Reveal.js.
*   **Anexos Técnicos:**
    * [Anexo E: Sensibilidad](docs/tesis/anexo_sensibilidad.md)
    * [Anexo F: Tests](docs/tesis/anexo_tests.md)
    * [Anexo G: Benchmarks](docs/tesis/anexo_benchmarks.md)
    * [Anexo H: Extensiones](docs/tesis/anexo_extensiones.md)

---

---

## 🔧 Configuración de Algoritmos

### Parámetros Calibrados (Optuna, 30 trials)

```yaml
GA:
  poblacion_size: 75
  prob_cruce: 0.93
  prob_mutacion: 0.20
  tamano_torneo: 4

TS:
  tamano_lista_tabu: 15
  tamano_vecindario: 49

Hybrid:
  generaciones_ga: 100
  aplicar_ts_cada: 24
```

---

## 📊 Validación con Benchmarks

| Instancia | n | Óptimo | GA | TS | Gap |
|-----------|---|--------|----|----|-----|
| demo_15t | 15 | 5 | 5.0 | 5.0 | **0%** |
| lineal_10t | 10 | 4 | 4.0 | 4.0 | **0%** |
| paralelo_12t | 12 | 4 | 4.0 | 4.0 | **0%** |

---

## 👨‍🎓 Información Académica

**Programa:** Maestría en Investigación de Operaciones y Estadística  
**Institución:** Universidad Tecnológica de Pereira  
**Autor:** Daniel Castañeda  
**Directora:** Eliana Mirledy Ocampo Toro, PhD.  
**Fecha:** Enero 2026

---

## 📄 Citación

```bibtex
@mastersthesis{castaneda2026dlbp,
  author = {Castañeda, Daniel},
  title = {Modelo de Optimización DLBP con Metaheurísticas para la Industria Avícola Colombiana},
  school = {Universidad Tecnológica de Pereira},
  year = {2026},
  type = {Tesis de Maestría}
}
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

*Desarrollado como parte de la investigación de maestría en Investigación de Operaciones y Estadística.*
