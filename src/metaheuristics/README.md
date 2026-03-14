# src/metaheuristics — Algoritmos de Optimización

## Arquitectura

Todos los algoritmos heredan de `MetaheuristicBase` y comparten:

- **Codificación:** cromosoma $(y_t, q_t)$ con variables mixtas (binarias + continuas)
- **Decodificador greedy:** asignación FIFO de la 2ª etapa por escenario $\omega$
- **Calibración:** Optuna/TPE con 50 trials por algoritmo

## Algoritmos Implementados

| Archivo | Algoritmo | Clase | Descripción |
|---------|-----------|-------|-------------|
| `ga.py` | Algoritmo Genético | `GeneticAlgorithm` | Cruce 2 puntos, mutación gaussiana, elitismo |
| `sa.py` | Recocido Simulado | `SimulatedAnnealing` | Enfriamiento geométrico, vecindarios mixtos, reheating |
| `de.py` | Evolución Diferencial | `DifferentialEvolution` | DE/best/1/bin, codificación continua discretizada |
| `ga_sa.py` | Híbrido GA-SA | `HybridGASA` | GA global + SA local cada k generaciones |
| `base.py` | Clase base | `MetaheuristicBase` | Interfaz común, logging, criterio de parada |
| `encoding.py` | Codificación | — | Reparación, discretización, conversión |

## Hiperparámetros Calibrados (Optuna/TPE)

| Parámetro | GA | SA | DE | GA-SA |
|-----------|:--:|:--:|:--:|:-----:|
| `pop_size` | 80 | — | 51 | 39 |
| `mutation_rate` | 0.068 | — | — | 0.156 |
| `crossover_rate` | 0.833 | — | — | 0.694 |
| `T_initial` | — | 203,952 | — | — |
| `cooling_rate` | — | 0.782 | — | — |
| `F` (escala) | — | — | 0.317 | — |
| `CR` (cruce) | — | — | 0.511 | — |
| `local_search_freq` | — | — | — | 9 |

## Uso

```python
from src.metaheuristics.ga_sa import HybridGASA
from src.model.parameters import ProblemInstance

instance = ProblemInstance.from_yaml("data/instances/medium_seed42.yaml")
algo = HybridGASA(instance, pop_size=39, max_evals=5000)
best = algo.run()
print(f"Best Z = {best.objective:,.0f}")
```

## Resultados

Ranking final (1,098 ejecuciones): **GA-SA > DE > GA > SA**

ANOVA: $F = 0.259$, $p = 0.855$ — diferencias no estadísticamente significativas.
