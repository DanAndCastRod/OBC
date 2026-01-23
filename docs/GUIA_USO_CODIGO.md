# 🛠️ Guía de Uso del Código (Manual Técnico)

Esta guía explica cómo utilizar el framework de optimización DLBP de forma independiente, para aplicarlo a nuevos problemas o extenderlo en futuros proyectos.

## 📦 Estructura de Módulos

El núcleo del código reutilizable se encuentra en `src/algorithms/`. Los componentes principales son:

- `base.py`: Define el contrato de los algoritmos y las estructuras de datos (`ProblemInstance`, `Solution`).
- `genetic_algorithm.py`: Implementación flexible de GA.
- `tabu_search.py`: Implementación de Búsqueda Tabú.
- `hybrid.py`: El optimizador maestro (GA + TS).
- `nsga2.py`: Extensión multi-objetivo.

---

## 🚀 Cómo usar el Framework en tu Proyecto

### 1. Definir una Instancia
Puedes cargar una instancia desde un archivo o crearla manualmente:

```python
from src.algorithms.base import ProblemInstance

# Opción A: Crear manualmente
instancia = ProblemInstance(
    tareas=['T1', 'T2', 'T3'],
    tiempos={'T1': 5, 'T2': 3, 'T3': 4},
    precedencias={'T1': ['T2'], 'T2': ['T3']},
    tiempo_ciclo=10
)

# Opción B: Cargar demo
from src.algorithms.base import cargar_instancia_demo
instancia = cargar_instancia_demo()
```

### 2. Ejecutar un Algoritmo

#### Algoritmo Genético (Básico)
```python
from src.algorithms.genetic_algorithm import GeneticAlgorithm, GAConfig

config_ga = GAConfig(
    poblacion_size=50,
    max_generaciones=100,
    prob_cruce=0.9
)

ga = GeneticAlgorithm(instancia, config_ga)
mejor_solucion = ga.optimizar(verbose=True)

print(f"Estaciones: {mejor_solucion.n_estaciones}")
```

#### Algoritmo Híbrido (Recomendado)
El híbrido ofrece el mejor balance calidad/tiempo.

```python
from src.algorithms.hybrid import HybridAlgorithm, HybridConfig

config_hibrido = HybridConfig(
    poblacion_size=40,
    generaciones_ga=100,
    aplicar_ts_cada=20  # Frecuencia de búsqueda local
)

optimizador = HybridAlgorithm(instancia, config_hibrido)
solucion = optimizador.optimizar()
```

#### Multi-Objetivo (NSGA-II)
Para minimizar estaciones y desbalance simultáneamente.

```python
from src.algorithms.nsga2 import NSGA2, NSGA2Config

nsga2 = NSGA2(instancia, NSGA2Config(poblacion_size=100))
pareto_front = nsga2.optimizar()

# Obtener solución de compromiso
mejor = nsga2.obtener_mejor_compromiso()
```

### 3. Interpretar Resultados

Todas las soluciones devuelven objetos `Solution` (o `MultiObjectiveSolution`) con atributos útiles:

```python
sol = mejor_solucion

# Atributos clave
print(sol.n_estaciones)      # Número total de estaciones
print(sol.fitness)           # Valor de la función objetivo
print(sol.asignacion)        # Diccionario {estacion: [tareas]}
print(sol.tiempos_estacion)  # Diccionario {estacion: tiempo_total}

# Validar validez
assert sol.es_factible       # Debe ser True
```

---

## 🔧 Extender el Framework

### Crear un Nuevo Algoritmo
Para crear un nuevo método (ej. Simulated Annealing), hereda de `Optimizer`:

```python
from src.algorithms.base import Optimizer, ProblemInstance, Solution

class SimulatedAnnealing(Optimizer):
    def __init__(self, instancia, temp_inicial=100, cooling_rate=0.95, seed=42):
        super().__init__(instancia, seed)
        self.temp = temp_inicial
        self.alpha = cooling_rate
    
    def optimizar(self, max_iter=1000, verbose=False):
        actual = self.generar_solucion_inicial()
        mejor = actual.clonar()
        
        while self.temp > 0.1:
            # Lógica del algoritmo...
            pass
            
        return mejor
```

---

## 🧪 Validar Cambios

Antes de hacer commit de nuevas funcionalidades, ejecuta la suite de tests unitarios que cubre el 100% del core:

```bash
# Desde la raíz del proyecto
python -m pytest tests/ -v
```
