# Decisiones de Diseño — Modelo de Optimizacion de Coproductos

**Sprint:** 1.1  
**Fecha:** 2026-02-27  
**Autor:** Daniel Andres Castaneda Rodriguez

---

## DD-01: Modelado de Perecibilidad

**Pregunta:** ¿Como modelar la vida util ($L_p$) de los coproductos?

**Opciones consideradas:**

| Opcion | Descripcion | Complejidad | Papers |
|--------|-------------|:-----------:|--------|
| A. Descarte total | $I_{pt\omega} = 0$ cuando $t' - t > L_p$ | Baja | Claassen 2016, Eq. 7 del anteproyecto |
| B. FIFO tracking | Rastrear la edad de cada unidad en inventario | Alta | Entrup 2005 |
| C. Deterioro continuo | Valor decrece con funcion exponencial | Media | Rong 2011 |

**Decision:** **Opcion A (Descarte total)** — Es la formulacion adoptada en el anteproyecto (Eq. 7) y la mas comun en lot-sizing con perecibilidad (Claassen 2016). Simplifica la implementacion sin perder realismo: en la industria avicola, los productos refrigerados se descartan al superar su vida util regulatoria.

**Implementacion:** Restriccion $I_{pt\omega} = 0$ para $t' > t + L_p$. En el decoder greedy, el inventario se resetea a 0 al exceder $L_p$ periodos.

---

## DD-02: Granularidad Temporal

**Pregunta:** ¿Cual es la unidad de los periodos $t \in T$?

**Opciones consideradas:**

| Opcion | Unidad | $L_p$ tipico (refrigerado) | Papers |
|--------|--------|:------------:|--------|
| A. Dias | 1 dia | 5-7 | Tahraoui 2025, Gonzalez-Neira 2025 |
| B. Semanas | 1 semana | 1 | Solano-Blanco 2022 |
| C. Turnos | 8 horas | 15-21 | N/A |

**Decision:** **Opcion A (Dias)** — La granularidad diaria permite modelar con mayor precision la perecibilidad de los productos frescos ($L_p = 5$-$7$ dias) y captura mejor la dinamica operativa real de las plantas de beneficio, que toman decisiones de produccion a nivel diario. Tahraoui 2025 y Gonzalez-Neira 2025 usan este nivel de detalle.

**Consecuencia:**
- $L_p$ se expresa en dias. Refrigerado fresco: $L_p = 5$-$7$ dias. Congelado: $L_p \geq 30$ dias.
- $n_t$ sera mayor (e.g. $n_t = 30$ dias = 1 mes), lo que incrementa la complejidad pero es mas realista.
- Las instancias toy pueden usar $n_t = 7$ dias, las industriales $n_t = 60$-$90$.

---

## DD-03: Estructura de Coproductos (3 Capas de Abstraccion)

**Pregunta:** ¿Como modelar la relacion entre lo que produce la carcasa y lo que se vende al mercado?

### Contexto industrial

Una planta de beneficio avicola tipica (caso de referencia: ~65,000 aves/dia) maneja ~350 referencias comerciales (SKUs). Estas referencias son el resultado de la combinacion factorialz de tres dimensiones:

```
SKU = Pieza anatomica x Forma de corte x Presentacion
        (~8 piezas)      (~5-6 formas)    (empaque + proceso)
```

Ejemplos:
- Muslo x individual x bandeja x 10 = 1 SKU
- Muslo x individual x bolsa granel = otro SKU
- Pechuga x filete x bolsa adobada = otro SKU
- Muslo+Contramuslo x pernil completo x canasta = otro SKU

### Decision: modelar a 3 capas con agregacion

```
         Capa 1                Capa 2                    Capa 3
    PIEZAS ANATOMICAS  -->  FORMAS DE CORTE  -->  REFERENCIAS COMERCIALES
      (biologia)          (planta de beneficio)       (ventas/marketing)
     ~8 piezas fijas       ~12-15 familias              ~350 SKUs
     Parametro alpha_a     VARIABLE DE DECISION         Se AGREGA a Capa 2
```

El modelo optimiza en **Capa 1 + Capa 2**. La demanda de Capa 3 (350 SKUs) se agrega hacia Capa 2.

### Capa 1: Piezas Anatomicas $A = \{a_1, ..., a_{n_a}\}$

Partes fijas determinadas por la anatomia del ave. Cada carcasa produce exactamente estas piezas en proporciones $\alpha_a$ (invariantes biologicas):

| ID | Pieza anatomica | $\alpha_a$ | Cantidad/ave | Notas |
|:--:|----------------|:----------:|:------------:|-------|
| a1 | Pechuga | 0.28 | 1 (entera) o 2 (mitades) | Pieza de mayor valor |
| a2 | Muslo | 0.12 | 2 | Par izq/der |
| a3 | Contramuslo | 0.10 | 2 | Par izq/der |
| a4 | Rabadilla | 0.04 | 1 | Puede ir con pernil o aparte |
| a5 | Ala | 0.06 | 2 | Par izq/der |
| a6 | Costillar (espalda) | 0.08 | 1 | Puede ir unido a alas |
| a7 | Menudencias (higado, molleja, corazon) | 0.07 | 1 set | |
| a8 | Otros (grasa, hueso, piel sobrante) | 0.25 | Variable | Subproducto industrial |
| | **Total** | **1.00** | | |

### Capa 2: Formas de Corte $F = \{f_1, ..., f_{n_f}\}$

Las formas de corte representan las **maneras en que las piezas anatomicas se combinan o separan** en la planta de beneficio. Son las familias de producto a nivel de planificacion tactica.

**Restricciones anatomicas clave:**
- Un ave tiene **1 pechuga** (puede venderse entera o en 2 mitades)
- Un ave tiene **2 perniles**. Cada pernil = muslo + contramuslo. El pernil puede ir con o sin rabadilla. La rabadilla es una sola, asi que solo 1 pernil puede llevarla.
- Un ave tiene **2 alas**. Pueden venderse individuales o unidas en una pieza con el costillar.

| ID | Forma de corte | Composicion anatomica | Restricciones |
|:--:|---------------|----------------------|---------------|
| f1 | Pechuga entera | a1 (completa) | Excluye f2 |
| f2 | Media pechuga | a1 / 2 | Excluye f1, genera 2 unidades |
| f3 | Pernil completo con rabadilla | a2 + a3 + a4 | Max 1 ave (1 rabadilla), excluye f4-f7 para esas piezas |
| f4 | Pernil sin rabadilla | a2 + a3 | Excluye f5, f6 para esas piezas |
| f5 | Muslo individual | a2 | Excluye f3, f4 |
| f6 | Contramuslo individual | a3 | Excluye f3, f4 |
| f7 | Rabadilla suelta | a4 | Solo si no va en pernil |
| f8 | Alas unidas con costillar | a5 + a6 (las 2 alas + costillar) | Excluye f9 |
| f9 | Ala individual | a5 | Excluye f8, genera 2 unidades |
| f10 | Costillar suelto | a6 | Solo si alas se venden individuales |
| f11 | Menudencias | a7 | Sin exclusividad |
| f12 | Subproducto industrial | a8 | Sin exclusividad |

### Grupos de exclusividad

Las piezas anatomicas compartidas generan restricciones de exclusividad:

```
Grupo 1 (Pechuga):    f1 XOR f2
Grupo 2 (Pierna izq): f3 XOR f4 XOR (f5 + f6)   [cada pierna]
Grupo 3 (Pierna der): f3 XOR f4 XOR (f5 + f6)   [cada pierna]
Grupo 4 (Rabadilla):  incluida en f3 XOR f7 XOR descarte
Grupo 5 (Alas):       f8 XOR (f9 + f10)
```

La **decision de configuracion de corte** es que combinacion de formas se produce cada dia. Esto es una variable de optimizacion que impacta directamente la rentabilidad.

### Capa 3: Referencias Comerciales (SKUs) — Agregacion

Las ~350 referencias comerciales se clasifican por forma de corte y se agrega su demanda:

```
SKU "Bandeja muslos x10"      --\
SKU "Bolsa muslos granel"     ----> Demanda total: forma f5 (muslo individual)
SKU "Muslo marinado bandeja"  --/

SKU "Pernil entero bolsa"     --\
SKU "Pernil con rabadilla"    ----> Demanda total: forma f3 (pernil con rabadilla)
SKU "Pernil adobado canasta"  --/
```

La demanda agregada $d_{ft\omega}$ se obtiene sumando la demanda de todos los SKUs que corresponden a la forma $f$:

$$d_{ft\omega} = \sum_{s \in SKU(f)} d_{st\omega}$$

Los precios de venta se calculan como promedio ponderado de los SKUs por forma.

**Decision:** El modelo opera a nivel de **Capa 2 (formas de corte, ~12 familias)**. La Capa 3 (350 SKUs) se agrega a Capa 2 como paso de preprocesamiento. No se modifica el anteproyecto; esta decision se documenta en el Capitulo 3 de la tesis (seccion "Supuestos y simplificaciones").

---

## DD-04: Estructura de Escenarios Estocasticos

**Pregunta:** ¿Como generar y manejar los escenarios de demanda $\omega \in \Omega$?

**Decision:** **Muestreo Monte Carlo** con distribuciones calibradas.

- Demanda base por forma de corte: $\mu_f$ (media diaria en kg, agregada desde SKUs)
- Variabilidad: $d_{ft\omega} \sim \text{LogNormal}(\mu_{ft}, \sigma_f)$
- Estacionalidad: factor multiplicativo $s_t$ (mayor en dic, menor en feb)
- Probabilidad: $\pi_\omega = 1/n_\omega$ (equiprobables)
- Referencia: Slama 2021 (GA + Monte Carlo para lot-sizing estocastico)

**Perfiles de variabilidad:**

| Perfil | $\sigma / \mu$ | Uso  |
|--------|:---------:|------|
| Estable | 0.10 | Formas de corte maduras (pechuga) |
| Moderado | 0.25 | Formas estandar (muslo, pernil) |
| Volatil | 0.40 | Formas nicho (menudencias, subproducto) |

---

## DD-05: Formato de Datos

**Pregunta:** YAML o JSON para archivos de instancias?

**Decision:** **YAML** — mas legible para humanos, soporta comentarios, y es estandar en configuracion cientifica. JSON como formato de salida para resultados (facil de parsear programaticamente).

**Estructura de una instancia:**

```yaml
# Instancia: small_seed42.yaml
metadata:
  name: "small_seed42"
  profile: "small"
  seed: 42
  generated_at: "2026-03-15T10:00:00"

problem:
  n_products: 6
  n_periods: 12
  n_scenarios: 20

  # Proporciones anatomicas (sum = 1.0)
  alpha: [0.30, 0.18, 0.14, 0.10, 0.08, 0.20]

  # Peso promedio carcasa (kg)
  weight: 2.3

  # Precios de venta (COP/kg)
  prices: [14000, 9000, 7500, 7000, 3000, 1500]

  # Costos
  cost_prod: 2000        # COP/carcasa
  cost_setup: 1000000    # COP/periodo (costo fijo activacion)
  cost_inv: [300, 250, 250, 200, 150, 100]   # COP/kg/periodo
  cost_pen: [5000, 3500, 3000, 2500, 1000, 500]  # COP/kg penalizacion

  # Capacidad
  capacity_max: 10000    # carcasas/periodo
  capacity_min: 1000     # lote minimo

  # Vida util (periodos = semanas)
  shelf_life: [1, 1, 1, 2, 1, 4]

  # Escenarios
  scenario_probs: null   # null = equiprobable (1/n_scenarios)

  # Demanda: array 3D [n_products x n_periods x n_scenarios]
  # Almacenada como lista de matrices (un bloque por producto)
  demand:
    - # Producto 0 (Pechuga): [periodos x escenarios]
      [[1200, 1150, ...], [1300, 1250, ...], ...]
    - # Producto 1 (Muslo): [periodos x escenarios]
      [[800, 780, ...], [850, 820, ...], ...]
    # ... (6 productos en total)
```

**Estructura de una solucion:**

```yaml
# Solucion: small_seed42_ga.yaml
metadata:
  instance: "small_seed42"
  algorithm: "GA"
  timestamp: "2026-03-20T14:30:00"
  elapsed_seconds: 12.5

solution:
  objective_value: 45000000.0
  is_feasible: true

  # Primera etapa
  setup: [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1]
  quantity: [8000, 7500, 9000, 0, 6000, 7000, 8500, 0, 9500, 8000, 10000, 9000]

  # Segunda etapa (promedios sobre escenarios)
  avg_sales: [[...], ...]       # n_products x n_periods
  avg_inventory: [[...], ...]   # n_products x n_periods
  avg_unmet: [[...], ...]       # n_products x n_periods

  # Desglose del objetivo
  breakdown:
    revenue: 52000000.0
    prod_cost: 4500000.0
    setup_cost: 1000000.0
    inv_cost: 800000.0
    pen_cost: 700000.0
```

---

## DD-06: Solver Exacto

**Pregunta:** ¿Que solver usar como baseline?

**Decision:** Estrategia multi-solver con prioridad en herramientas open-source:

| Prioridad | Solver | Via | Uso |\n|:---------:|--------|-----|-----|\n| 1 | **Google OR-Tools CP-SAT** | `ortools` | Solver principal — excelente para variables enteras/binarias y restricciones de exclusividad (constraint programming nativo). Gratis, paraleliza en multi-core. |\n| 2 | **HiGHS** | PuLP / `highspy` | Alternativa MILP clasica — sucesor moderno de CBC, ~3-5x mas rapido. Integrado en SciPy 1.9+. |\n| 3 | **CBC** | PuLP | Fallback — estable, integrado en PuLP por defecto. |\n| 4 | **Gurobi** | `gurobipy` / PuLP | Benchmark comercial — licencia academica UTP. Solo para validar que la solucion open-source es competitiva. |\n\n**Justificacion:** OR-Tools CP-SAT es ideal porque las restricciones de exclusividad de formas de corte (DD-03) son naturalmente un problema de constraint programming. HiGHS cubre el caso MILP puro si se necesita comparar formulaciones. PuLP abstrae la interfaz para CBC/HiGHS/Gurobi, permitiendo cambiar con un parametro.

---

## DD-07: Codificacion de Soluciones para Metaheuristicas

**Pregunta:** ¿Como codificar una solucion para las metaheuristicas?

**Decision:** **Cromosoma de dos vectores** (primera etapa only):

```
Cromosoma = [y_1, ..., y_T, q_1, ..., q_T]
             |--- setup ---|--- cantidades ---|
             |-- binario --|---- entero ------|
```

- $y_t \in \{0, 1\}$: activacion de linea (setup)
- $q_t \in [Q^{min}, Q^{max}]$: cantidad si $y_t = 1$, else $q_t = 0$

**Variables de segunda etapa** ($v$, $I$, $u$) se calculan via **decoder greedy**:
1. Para cada escenario $\omega$:
   a. Calcular produccion de cada coproducto: $\alpha_p \cdot W \cdot q_t$
   b. Actualizar inventario: $I_{pt\omega} = I_{p,t-1,\omega} + \text{produccion} - v_{pt\omega}$
   c. Asignar ventas en orden de rentabilidad ($r_p$ descendente): $v_{pt\omega} = \min(\text{disponible}, d_{pt\omega})$
   d. Calcular insatisfaccion: $u_{pt\omega} = d_{pt\omega} - v_{pt\omega}$
   e. Aplicar perecibilidad: $I_{pt\omega} = 0$ si edad > $L_p$

**Referencia:** Akbari-Aghghaleh 2025 usa codificacion similar para variables mixtas.

---

## DD-08: Escenarios de Prueba Escalonados

**Pregunta:** ¿Que niveles de complejidad debe cubrir el banco de instancias?

**Decision:** **6 niveles** progresivos, de lo mas simple a lo mas robusto:

| Nivel | Nombre | $n_a$ | $n_f$ | $n_t$ | $n_\omega$ | Config. corte | Uso |
|:-----:|--------|:-----:|:-----:|:-----:|:----------:|-------|-----|
| 0 | Trivial | 3 | 3 | 3 | 1 | Fija | Verificacion manual con calculadora |
| 1 | Toy | 4 | 4 | 7 | 5 | Fija | Debug, tests unitarios |
| 2 | Small | 8 | 8 | 14 | 20 | Fija | Validacion con solver exacto (CBC) |
| 3 | Medium | 8 | 12 | 30 | 50 | Variable | Calibracion hiperparametros (Optuna) |
| 4 | Large | 8 | 12 | 60 | 100 | Variable | Comparacion de metaheuristicas |
| 5 | Industrial | 8 | 12 | 90 | 500 | Variable | Test de escalabilidad (ref: 65K aves/dia) |

**Notas:**
- $n_a$: piezas anatomicas, $n_f$: formas de corte, $n_t$: periodos (dias), $n_\omega$: escenarios
- **Config. fija:** una sola configuracion de corte para todo el horizonte (simplifica)
- **Config. variable:** la decision de corte (pernil completo vs piezas) varia por dia
- Niveles 0-1: verifican correctitud del codigo
- Niveles 2-3: validan contra solver exacto y calibran
- Niveles 4-5: evaluan rendimiento y escalabilidad (CBC probablemente falle en timeout)
- Se generan **3 seeds** por nivel = 18 instancias total

---

## DD-09: Calibracion Industrial

**Pregunta:** ¿Que valores de referencia usar para calibrar las instancias?

**Fuente:** Planta de beneficio avicola colombiana (datos del investigador).

| Parametro | Valor real | Uso en el modelo |
|-----------|:----------:|------------------|
| Aves procesadas/dia | ~65,000 | $Q^{max}$ en instancias Industrial |
| Peso promedio carcasa | ~2.3-2.5 kg | Parametro $W$ |
| Produccion diaria total | ~150 ton | Validacion de volumenes |
| SKUs comerciales | ~350 | Se agregan a ~12 formas de corte |
| Dias laborables/semana | 5-6 | Horizonte de planificacion |

**Produccion diaria por pieza anatomica (estimado):**

| Pieza | $\alpha_a$ | Produccion (ton/dia) |
|-------|:----------:|:--------------------:|
| Pechuga | 0.28 | 42 |
| Muslo | 0.12 | 18 |
| Contramuslo | 0.10 | 15 |
| Rabadilla | 0.04 | 6 |
| Ala | 0.06 | 9 |
| Costillar | 0.08 | 12 |
| Menudencias | 0.07 | 10.5 |
| Otros | 0.25 | 37.5 |
| **Total** | **1.00** | **150** |

**Nota:** Estos valores se usan como referencia para instancias de nivel Industrial. En instancias Toy/Small, se escalan proporcionalmente (e.g. 5,000 aves/dia).

**Seccion sugerida para la tesis (Capitulo 3):**
> "El modelo opera a nivel de familia de producto (formas de corte), no a nivel de SKU comercial. La planta de referencia procesa ~65,000 aves/dia generando ~350 referencias comerciales, las cuales se agregan en ~12 familias de producto segun la composicion anatomica. Esta agregacion es consistente con la practica estandar en planificacion tactica (Solano-Blanco et al., 2022)."

---

## Registro de Decisiones

| ID | Tema | Decision | Justificacion clave |
|----|------|----------|---------------------|
| DD-01 | Perecibilidad | Descarte total | Eq. 7 anteproyecto, Claassen 2016 |
| DD-02 | Granularidad | **Dias** | Tahraoui 2025, mayor precision perecibilidad |
| DD-03 | Coproductos | **3 capas:** 8 anatomicas + 12 formas + ~350 SKUs (agregados) | Realidad industrial, exclusividad anatomica |
| DD-04 | Escenarios | Monte Carlo + LogNormal | Slama 2021 |
| DD-05 | Formato datos | YAML (in) / JSON (out) | Legibilidad + comentarios |
| DD-06 | Solver | CBC (PuLP) + Gurobi backup | Open-source, licencia acad. |
| DD-07 | Codificacion | 2 vectores (y, q) + decoder | Akbari-Aghghaleh 2025 |
| DD-08 | Escenarios prueba | 6 niveles (Trivial → Industrial) | Validacion progresiva |
| DD-09 | Calibracion | 65K aves/dia, 350 SKUs, ~150 ton/dia | Datos reales del investigador |
