# DLBP Avícola - Código Fuente

Este directorio contiene la implementación del proyecto de optimización DLBP.

## Estructura

```
src/
├── models/
│   ├── dlbp_completo.py    # Modelo MILP (minimiza estaciones)
│   ├── dlbp_profit.py      # Modelo MILP profit-oriented
│   └── milp_validation.py  # Script de validación inicial
├── algorithms/
│   ├── base.py             # Clases base: ProblemInstance, Solution, Optimizer
│   ├── genetic_algorithm.py # Algoritmo Genético (OX, swap, elitismo)
│   ├── tabu_search.py      # Búsqueda Tabú (lista tabú, aspiración)
│   └── hybrid.py           # Híbrido Memetic (GA + TS)
├── utils/                  # Funciones auxiliares
└── experiments/            # Scripts de experimentación
```

## Scripts Disponibles

### Modelos Exactos (MILP)
```bash
python src/models/dlbp_completo.py   # Min estaciones
python src/models/dlbp_profit.py     # Max beneficio
```

### Metaheurísticas
```bash
python src/algorithms/genetic_algorithm.py  # Algoritmo Genético
python src/algorithms/tabu_search.py        # Búsqueda Tabú
python src/algorithms/hybrid.py             # Híbrido (GA+TS)
```

## Dependencias

```bash
pip install pulp numpy
```

## Referencias

| Paper | Concepto |
|-------|----------|
| Liang et al. (2023) | Función objetivo profit-oriented |
| Wang et al. (2021) | GA para DLBP paralelo |
| Hu et al. (2023) | Hyper-heurísticas para DLBP estocástico |
| Tian et al. (2023) | Híbrido evolutivo multi-objetivo |

---
*Fases 1-2 Completadas | Enero 2026*
