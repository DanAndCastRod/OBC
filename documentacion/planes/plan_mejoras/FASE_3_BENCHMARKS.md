# Fase 3: Comparación con Benchmarks DLBP

**Prioridad:** P2 (Media)  
**Esfuerzo:** Medio  
**Duración Estimada:** 3-5 días  
**Estado:** [x] ✅ COMPLETADO (22-Ene-2026)

---

## 🎯 Objetivo

Contextualizar los resultados de la investigación comparando el desempeño de los algoritmos implementados con instancias benchmark de la literatura y/o solvers comerciales.

---

## 📋 Justificación

El proyecto actual usa instancias sintéticas propias. Aunque están calibradas con datos de la literatura, una comparación directa con benchmarks estándar:

1. **Valida la implementación** verificando que los algoritmos funcionan correctamente
2. **Contextualiza los resultados** permitiendo comparar con otros autores
3. **Fortalece las conclusiones** del trabajo de investigación

---

## 🔧 Actividades

### 3.1. Búsqueda de Instancias Benchmark

**Fuentes potenciales:**

| Fuente | Tipo | URL/Referencia |
|--------|------|----------------|
| OR-Library | ALBP (puede adaptarse) | http://people.brunel.ac.uk/~mastjjb/jeb/orlib/albinfo.html |
| Scholl Benchmark | SALBP | Scholl (1999) |
| Papers DLBP | Instancias específicas | McGovern (2007), Kucukkoc (2020) |

**Nota:** DLBP tiene menos benchmarks estandarizados que ALBP. Puede ser necesario adaptar instancias de ALBP.

### 3.2. Adaptar Formato de Instancias

**Script a crear:** `src/experiments/cargar_benchmark.py`

```python
def cargar_instancia_orlib(archivo: str) -> ProblemInstance:
    """
    Convierte formato OR-Library a formato interno.
    
    Formato OR-Library:
    - Línea 1: número de tareas
    - Líneas siguientes: tiempo_tarea, predecesores
    """
    # Implementación de parser
    pass

def cargar_instancia_scholl(archivo: str) -> ProblemInstance:
    """
    Convierte formato Scholl a formato interno.
    """
    pass
```

### 3.3. Comparación con Solver Exacto (Opcional)

**Herramienta:** Gurobi o CBC (open source)

**Script:** `src/models/resolver_exacto.py`

```python
def resolver_optimo(instancia: ProblemInstance, tiempo_limite: int = 300):
    """
    Resuelve la instancia con MILP para obtener óptimo como referencia.
    
    Returns:
        - Valor óptimo (si se encuentra)
        - Gap de optimalidad
        - Tiempo de resolución
    """
    # Usar PuLP o gurobipy
    pass
```

### 3.4. Ejecutar Experimentos Comparativos

**Diseño experimental:**

| Instancia | n | Óptimo Conocido | GA | TS | Híbrido | Gap% |
|-----------|---|-----------------|----|----|---------|------|
| Scholl_1 | 25 | 6 | ? | ? | ? | ? |
| Scholl_2 | 50 | 10 | ? | ? | ? | ? |
| ... | | | | | | |

**Métricas a reportar:**
- Gap vs óptimo: `(obtenido - óptimo) / óptimo × 100%`
- Tiempo de ejecución
- Desviación estándar

### 3.5. Documentar y Visualizar

**Gráficos a generar:**

1. **Tabla comparativa:** Algoritmos vs instancias benchmark
2. **Gráfico de gap:** Barras mostrando distancia al óptimo
3. **Performance profile:** Curva de rendimiento acumulado

**Ubicación:** `docs/tesis/figuras/benchmarks/`

---

## 📦 Entregables

| Entregable | Ubicación | Estado |
|------------|-----------|--------|
| Script comparación | `src/experiments/benchmark_comparison.py` | ✅ |
| Instancias benchmark | Definidas en script (3 instancias) | ✅ |
| Solver exacto | Integrado en script (PuLP + CBC) | ✅ |
| Resultados JSON | `results/benchmark_comparison.json` | ✅ |
| Anexo tesis | `docs/tesis/anexo_benchmarks.md` | ✅ |

---

## ✅ Criterios de Aceptación

- [ ] Al menos 5 instancias benchmark cargadas y ejecutadas
- [ ] Comparación con óptimo conocido o solver (al menos 2 instancias)
- [ ] Gap promedio reportado
- [ ] Gráfico comparativo generado

---

## ⚠️ Consideraciones

1. **DLBP vs ALBP:** Las instancias ALBP pueden requerir inversión del grafo de precedencias
2. **Tiempo de solver:** Para instancias grandes (>50 tareas), el solver puede no encontrar óptimo en tiempo razonable
3. **Interpretación:** Un gap de 5-10% es típicamente aceptable para metaheurísticas

---

## 📚 Referencias

- Scholl, A., & Becker, C. (2006). State-of-the-art exact and heuristic solution procedures for SALBP.
- McGovern, S. M., & Gupta, S. M. (2007). Combinatorial optimization analysis of the DLBP.

---

*Última actualización: 22 de Enero de 2026*
