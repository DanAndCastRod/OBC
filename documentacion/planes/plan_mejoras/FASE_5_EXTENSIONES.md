# Fase 5: Extensiones Técnicas Avanzadas

**Prioridad:** P4+ (Baja / Trabajo Futuro)  
**Esfuerzo:** Alto  
**Duración Estimada:** Variable (semanas-meses)  
**Estado:** ⏳ Documentado (Enero 2026)

---

## 🎯 Objetivo

Documentar las extensiones técnicas avanzadas que pueden desarrollarse como trabajo futuro, incluyendo estimaciones de complejidad y requerimientos.

---

## 📊 Visualizaciones Generadas

Se han generado las siguientes figuras para ilustrar las extensiones:

| Figura | Descripción | Ubicación |
|--------|-------------|-----------|
| `roadmap_extensiones.png` | Matriz impacto vs complejidad | docs/tesis/figuras/ |
| `timeline_proyecto.png` | Timeline del proyecto completo | docs/tesis/figuras/ |
| `resumen_proyecto.png` | Dashboard con métricas clave | docs/tesis/figuras/ |
| `arquitectura_nsga2.png` | Diagrama conceptual NSGA-II | docs/tesis/figuras/ |

---

## 📋 Extensiones Identificadas

| Extensión | Complejidad | Impacto | Prerrequisitos |
|-----------|-------------|---------|----------------|
| Optimización Multi-Objetivo (NSGA-II) | Alta | Alto | Fases 1-4 completas |
| Robustez Estocástica | Alta | Alto | Modelo estocástico existente |
| Paralelización | Media | Medio | Ninguno |
| Interfaz Web (Dashboard) | Media | Bajo | Ninguno |
| Aprendizaje por Refuerzo | Muy Alta | Alto | Investigación adicional |

---

## 🔧 Detalle por Extensión

### 5.1. Optimización Multi-Objetivo (NSGA-II)

**Descripción:**  
Implementar el algoritmo NSGA-II para optimizar simultáneamente múltiples objetivos.

**Objetivos a considerar:**
1. Minimizar número de estaciones
2. Minimizar desbalance de carga (smooth load)
3. Minimizar costo de inventario
4. Maximizar utilización de mano de obra

**Implementación sugerida:**

```python
# Estructura básica
from deap import tools, algorithms

def evaluar_multiobjetivo(individuo, instancia):
    """
    Retorna tupla de objetivos (todos a minimizar).
    """
    solucion = decodificar(individuo, instancia)
    
    obj1 = solucion.n_estaciones
    obj2 = calcular_desbalance(solucion)
    obj3 = calcular_costo_inventario(solucion, demanda)
    
    return (obj1, obj2, obj3)

# NSGA-II con DEAP
toolbox.register("evaluate", evaluar_multiobjetivo)
toolbox.register("select", tools.selNSGA2)
```

**Entregables:**
- `src/algorithms/nsga2_dlbp.py`
- Visualización de frente de Pareto
- Análisis de trade-offs entre objetivos

**Tiempo estimado:** 2-3 semanas

---

### 5.2. Optimización Robusta bajo Incertidumbre

**Descripción:**  
Extender el modelo para manejar incertidumbre en tiempos de procesamiento de manera robusta.

**Enfoques a considerar:**

| Enfoque | Descripción | Complejidad |
|---------|-------------|-------------|
| Worst-case | Optimizar el peor escenario | Media |
| CVaR | Conditional Value at Risk | Alta |
| Chance-constrained | Restricciones probabilísticas | Alta |

**Implementación sugerida:**

```python
def evaluar_robusto(individuo, instancia, n_escenarios=100, alpha=0.05):
    """
    Evalúa el CVaR (peor alpha% de escenarios).
    """
    resultados = []
    
    for _ in range(n_escenarios):
        tiempos = generar_tiempos_estocasticos(instancia)
        solucion = decodificar(individuo, instancia, tiempos)
        resultados.append(solucion.n_estaciones)
    
    # CVaR: promedio del peor alpha%
    resultados.sort(reverse=True)
    n_peores = max(1, int(alpha * n_escenarios))
    cvar = sum(resultados[:n_peores]) / n_peores
    
    return cvar
```

**Tiempo estimado:** 2-3 semanas

---

### 5.3. Paralelización de Algoritmos

**Descripción:**  
Acelerar la ejecución de algoritmos mediante paralelización.

**Oportunidades de paralelización:**

| Componente | Técnica | Speedup Esperado |
|------------|---------|------------------|
| Evaluación de población (GA) | `multiprocessing.Pool` | 2-4x |
| Ejecución de réplicas | `joblib.Parallel` | Nx (N=cores) |
| Generación de vecindario (TS) | `concurrent.futures` | 2-3x |

**Implementación sugerida:**

```python
from multiprocessing import Pool
from functools import partial

def evaluar_poblacion_paralelo(poblacion, instancia, n_procesos=4):
    """
    Evalúa la población en paralelo.
    """
    evaluar_func = partial(evaluar_individuo, instancia=instancia)
    
    with Pool(n_procesos) as pool:
        fitnesses = pool.map(evaluar_func, poblacion)
    
    return fitnesses
```

**Tiempo estimado:** 1 semana

---

### 5.4. Interfaz Web (Dashboard)

**Descripción:**  
Crear una interfaz web interactiva para visualizar y ejecutar los algoritmos.

**Herramientas sugeridas:**
- **Streamlit** (más simple)
- **Gradio** (alternativa)
- **Dash** (más complejo pero flexible)

**Funcionalidades:**

```python
# streamlit_app.py
import streamlit as st

st.title("DLBP Avícola - Dashboard")

# Sidebar para configuración
algoritmo = st.sidebar.selectbox("Algoritmo", ["GA", "TS", "Híbrido"])
n_tareas = st.sidebar.slider("Número de tareas", 10, 100, 40)

# Botón de ejecución
if st.button("Ejecutar Optimización"):
    resultado = ejecutar_algoritmo(algoritmo, n_tareas)
    st.success(f"Estaciones: {resultado.n_estaciones}")
    
    # Visualización
    fig = crear_grafico_convergencia(resultado.historial)
    st.pyplot(fig)
```

**Tiempo estimado:** 1-2 semanas

---

### 5.5. Aprendizaje por Refuerzo (RL)

**Descripción:**  
Explorar el uso de RL para balanceo dinámico basado en demanda en tiempo real.

**Estado:** Investigación preliminar requerida

**Componentes:**
- **Agente:** Red neuronal que decide asignaciones
- **Ambiente:** Simulación de planta avícola
- **Reward:** -estaciones + bonus_balance

**Referencia:**  
Luo et al. (2020). Reinforcement learning for assembly line balancing.

**Tiempo estimado:** 1-2 meses (investigación + implementación)

---

## 📊 Roadmap Visual

```
                      Complejidad vs Impacto
Impacto
   ▲
   │     ★ NSGA-II        ★ RL
   │                      
   │ ★ Robustez
   │
   │         ★ Paralelización
   │                         ★ Dashboard
   │
   └──────────────────────────────────────▶ Complejidad
         Bajo   Medio   Alto   Muy Alto
```

---

## ✅ Criterios para Iniciar

Antes de iniciar cualquier extensión de Fase 5:

- [ ] Fases 1-4 completadas satisfactoriamente
- [ ] Proyecto con cobertura de tests ≥60%
- [ ] Documentación al día
- [ ] Tiempo disponible según estimación
- [ ] Recursos de cómputo necesarios disponibles

---

## 📚 Referencias Adicionales

- Deb, K. (2002). *Multi-Objective Optimization Using Evolutionary Algorithms*. Wiley.
- Ben-Tal, A., & Nemirovski, A. (2002). *Robust optimization*. Princeton University Press.
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction*. MIT Press.

---

*Última actualización: 22 de Enero de 2026*
