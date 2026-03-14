# src/model — Modelo MILP Estocástico

## Módulos

| Archivo | Descripción |
|---------|-------------|
| `parameters.py` | `ProblemInstance`: encapsula datos de entrada (partes anatómicas, costos, demanda, vida útil) |
| `decoder.py` | `decode()`: decodificador greedy FIFO para la 2ª etapa estocástica |
| `solver.py` | `solve_exact()`: formulación PuLP para solver CBC (instancias pequeñas) |
| `objective.py` | `compute_objective()`: función objetivo Z (ingresos − costos − penalizaciones) |
| `constraints.py` | Restricciones del modelo (balance, setup, perecibilidad) |
| `solution.py` | `Solution`: estructura de datos para almacenar soluciones evaluadas |

## Formulación

$$\max Z = \sum_{\omega} \pi_\omega \left[ \sum_t \left( \sum_p r_p v_{pt\omega} - c^{prod} q_t - F y_t - \sum_p c^{inv}_p I_{pt\omega} - \sum_p c^{pen}_p u_{pt\omega} \right) \right]$$

**Variables de decisión:**
- **1ª etapa (here-and-now):** $y_t \in \{0,1\}$ (setup), $q_t \in [Q^{min}, Q^{max}]$ (lote)
- **2ª etapa (wait-and-see):** $v_{pt\omega}$ (ventas), $I_{pt\omega}$ (inventario), $u_{pt\omega}$ (demanda insatisfecha)

## Uso

```python
from src.model.parameters import ProblemInstance
from src.model.decoder import decode

instance = ProblemInstance.from_yaml("data/instances/medium_seed42.yaml")
y = [1, 1, 0, 1, 1, 0]  # setup decisions
q = [500, 480, 0, 520, 490, 0]  # lot sizes
solution = decode(instance, y, q)
print(f"Z = {solution.objective:,.0f}")
```
