# OBC — Optimización de Coproductos en la Industria Avícola

**Tesis de Maestría en Investigación de Operaciones y Estadística (MIOE)**  
Universidad Tecnológica de Pereira, 2026

**Autor:** Daniel Andrés Castañeda Rodríguez  
**Directora:** Ing. Eliana Mirledy Ocampo Toro, PhD.

---

## Descripción

Modelo de optimización para la planificación de coproductos en la industria avícola colombiana, resuelto mediante metaheurísticas (GA, SA, DE, GA-SA). Aborda el desbalance estructural entre la oferta rígida de coproductos —determinada por la anatomía del ave— y la demanda estocástica del mercado.

Se formula un modelo de **Programación Lineal Entera Mixta (MILP)** multi-periodo con estructura de **lot-sizing estocástico**, incluyendo decisiones binarias de setup, lote mínimo y restricciones de perecibilidad. El problema se resuelve mediante cuatro metaheurísticas calibradas con **Optuna/TPE** y evaluadas en un diseño experimental de **1,098 ejecuciones** sobre **9 instancias** calibradas con datos del sector avícola colombiano (FENAVI, DANE).

## Resultados Principales

| Algoritmo | Rank | Gap vs CBC (Small/Medium) | Gap vs CBC (promedio global) |
|-----------|:----:|:-------------------------:|:----------------------------:|
| **GA-SA** (híbrido) | 🥇 1 | 3.4% | 8.12% |
| DE | 🥈 2 | 3.4% | 8.14% |
| GA | 🥉 3 | 3.4% | 8.52% |
| SA | 4 | 10.4% | 13.11% |

**Notas:** (1) El promedio global está dominado por las instancias Large (~17.6–18.8% para todos los algoritmos), en las que CBC no converge al óptimo dentro del límite de 300 s, por lo que el gap allí es frente al incumbente de CBC. (2) El criterio de la hipótesis H2 (gap ≤ 2%) se evalúa frente a la **mejor metaheurística individual**, no frente a CBC; su resultado fue −0.02% (componente de calidad soportado). Fuente: `experiments/results/main_results_table.csv` e `instance_results_table.csv`.

## Estructura del Repositorio

```
OBC/
├── src/                   # Código fuente principal
│   ├── model/             # Modelo MILP estocástico (PuLP/CBC)
│   │   ├── parameters.py  # ProblemInstance y datos de entrada
│   │   ├── decoder.py     # Decodificador greedy FIFO
│   │   ├── solver.py      # Solver exacto (CBC)
│   │   ├── objective.py   # Función objetivo Z
│   │   └── constraints.py # Restricciones del modelo
│   ├── metaheuristics/    # GA, SA, DE, GA-SA
│   │   ├── ga.py          # Algoritmo Genético
│   │   ├── sa.py          # Recocido Simulado
│   │   ├── de.py          # Evolución Diferencial
│   │   ├── ga_sa.py       # Híbrido GA-SA
│   │   ├── base.py        # Clase base MetaheuristicBase
│   │   └── encoding.py    # Codificación de soluciones
│   ├── instances/         # Generación de instancias sintéticas
│   │   ├── generator.py   # InstanceGenerator
│   │   ├── calibration.py # Calibración FENAVI/DANE
│   │   └── distributions.py
│   └── utils/             # Utilidades compartidas
├── experiments/           # Diseño experimental
│   ├── config/            # Configuraciones YAML
│   ├── scripts/           # Scripts de ejecución
│   │   ├── run_comparison.py
│   │   ├── run_sensitivity.py
│   │   └── run_complexity_analysis.py
│   └── results/           # Resultados (CSV, JSON, PNG)
├── tests/                 # Tests unitarios (pytest)
├── tesis/                 # Documento de tesis (Markdown → PDF)
├── anteproyecto/          # Documento del anteproyecto
├── docs/presentacion/     # Presentación de sustentación (Reveal.js)
├── data/                  # Papers e instancias
│   ├── instances/
│   └── references/
├── documentacion/         # Planes y reportes
└── LEGACY/                # Código del proyecto anterior (DLBP)
```

## Reproducción Rápida

### Requisitos Previos

- Python 3.11+
- Pandoc 3.x + XeLaTeX (para compilar tesis)
- mermaid-filter (opcional, para diagramas)

### Instalación

```bash
git clone https://github.com/DanAndCastRod/OBC.git
cd OBC
pip install -r requirements.txt
```

### Ejecución de Tests

```bash
pytest tests/ -v
```

### Reproducción Completa

```bash
# Verificación rápida de reproducibilidad (GA-SA sobre una instancia small)
python experiments/scripts/reproduce.py
```

### Ejecución Individual

```bash
# Comparación de algoritmos (1,098 ejecuciones)
python experiments/scripts/run_comparison.py

# Análisis de sensibilidad (450 ejecuciones)
python experiments/scripts/run_sensitivity.py

# Análisis de complejidad
python experiments/scripts/run_complexity_analysis.py
```

### Compilación de la Tesis

```bash
cd tesis
python generar_tesis.py
# Genera: tesis_coproductos.pdf
```

### Presentación de Sustentación

Abrir directamente en el navegador:

```
docs/presentacion/sustentacion_coproductos.html
```

## Stack Tecnológico

| Herramienta | Versión | Uso |
|-------------|---------|-----|
| Python | 3.11+ | Lenguaje principal |
| PuLP | 2.7.0 | Solver exacto (CBC) |
| NumPy | 1.26.0 | Operaciones numéricas |
| Pandas | 2.3.2 | Manejo de datos |
| SciPy | 1.11.2 | Tests estadísticos |
| Optuna | 4.7.0 | Calibración de hiperparámetros |
| Matplotlib | 3.8.0 | Visualización |
| Seaborn | 0.13.0 | Gráficos estadísticos |
| Pytest | 8.4.1 | Testing |

Las versiones exactas están fijadas en [requirements.txt](requirements.txt).

## Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENCE](LICENCE) para más detalles.
