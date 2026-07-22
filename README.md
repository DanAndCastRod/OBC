# OBC — Optimización de Coproductos en la Industria Avícola

**Tesis de Maestría en Investigación de Operaciones y Estadística (MIOE)**  
Universidad Tecnológica de Pereira, 2026

**Autor:** Daniel Andrés Castañeda Rodríguez  
**Directora:** Ing. Eliana Mirledy Ocampo Toro, PhD.

---

## Descripción

Modelo de optimización para la planificación de coproductos en la industria avícola colombiana, resuelto mediante metaheurísticas (GA, SA, DE, GA-SA). Aborda el desbalance estructural entre la oferta rígida de coproductos —determinada por la anatomía del ave— y la demanda estocástica del mercado.

Se formula un modelo de **Programación Lineal Entera Mixta (MILP)** multi-periodo con estructura de **lot-sizing estocástico**, incluyendo decisiones binarias de setup, lote mínimo y restricciones de perecibilidad. El problema se resuelve mediante cuatro metaheurísticas calibradas con **Optuna/TPE** y evaluadas en **dos campañas experimentales** (1,098 ejecuciones diagnósticas + 780 confirmatorias) sobre **39 instancias** calibradas con datos del sector avícola colombiano (FENAVI, DANE).

## Resultados Principales

El hallazgo central es que **el valor de la optimización depende del régimen económico**:

- **Campaña diagnóstica (v1):** con demanda por encima de la capacidad y costo de setup marginal, el problema degenera y una regla trivial (producir a capacidad máxima) queda casi óptima — H1 y H3 no se soportan. Un análisis de potencia muestra que ese diseño no podía detectar los umbrales declarados.
- **Campaña confirmatoria (v2):** con setup costoso, holgura de capacidad y demanda volátil (el régimen operativo real), las metaheurísticas **mejoran el beneficio ~20% y reducen el inventario 28–31%** frente al baseline ($p<10^{-4}$, potencia 1.000). Con las cuatro metaheurísticas **re-calibradas para el régimen** y presupuesto igualado, todas convergen a gaps de **4.6–5.9%** frente al óptimo certificado por CBC:

| Algoritmo | Gap vs óptimo (v2) | Rango Nemenyi |
|-----------|:------------------:|:-------------:|
| **DE** | 4.6–8.4% | 🥇 1.77 |
| GA | 4.8–6.6% | 2.73 |
| SA | 4.7–6.8% | 2.73 |
| GA-SA | 4.8–5.9% | 2.77 |

**Nota metodológica:** el ranking observado depende de qué algoritmos estén calibrados. Con calibración justa (los cuatro tuneados para v2) la diferencia entre ellos es estadísticamente marginal — **calibrar para el régimen pesa más que elegir el algoritmo**. CBC alcanza optimalidad certificada en todos los tamaños (best bound; 1.4–191 s). Fuente: `experiments/results_v2/`.

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
# Campaña diagnóstica v1 (1,098 ejecuciones)
python experiments/scripts/run_comparison.py

# Campaña confirmatoria v2 (780 ejecuciones, presupuesto igualado, --workers N)
python experiments/scripts/run_comparison.py --config experiments/config/comparison_v2.yaml --workers 12

# Re-calibración de metaheurísticas para el régimen v2 (Optuna/TPE)
python experiments/scripts/tune_mh_v2.py --algo ga_sa --n-trials 40 --max-evaluations 6000

# Análisis de sensibilidad multi-instancia (v2: 225 ejecuciones, 3 bases)
python experiments/scripts/run_sensitivity.py --config experiments/config/sensitivity_v2.yaml --workers 7

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
