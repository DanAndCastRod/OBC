# Pseudocodigo y Flujos del Modelo MILP

**Sprint:** 1.3  
**Fecha:** 2026-02-27

---

## 1. Decoder Greedy (decoder.py)

El decoder transforma las decisiones de primera etapa (y, q) en una
solucion completa con variables de segunda etapa (v, I, u).

### Pseudocodigo

```
FUNCION decode(y[T], q[T], instancia) -> Solucion:
    alpha_f = composition @ alpha    // alpha efectivo por forma de corte

    PARA CADA escenario w:
        inventario_capas[f] = []     // FIFO: lista de (cantidad, edad)

        PARA CADA periodo t:
            // 1. PRODUCCION
            PARA CADA forma f:
                prod_f = alpha_f[f] * W * q[t]
                SI prod_f > 0:
                    inventario_capas[f].agregar((prod_f, edad=0))

            // 2. ENVEJECER + DESCARTAR PERECIDOS
            PARA CADA forma f:
                PARA CADA capa EN inventario_capas[f]:
                    capa.edad += 1
                    SI capa.edad > L[f]:
                        ELIMINAR capa    // Eq. 7: perecibilidad

            // 3. CALCULAR DISPONIBLE
            disponible[f] = SUMA(capas de f)

            // 4. ASIGNAR VENTAS (greedy por rentabilidad)
            orden = ORDENAR formas POR precio DESCENDENTE
            PARA CADA f EN orden:
                venta = MIN(disponible[f], demanda[f,t,w])
                v[f,t,w] = venta
                u[f,t,w] = demanda[f,t,w] - venta
                DESCONTAR venta del inventario (FIFO: las mas viejas primero)

            // 5. REGISTRAR INVENTARIO FINAL
            I[f,t,w] = SUMA(capas de f)

    RETORNAR Solucion(y, q, v, I, u)
```

### Diagrama de flujo

```
[y_t, q_t] ──> [Produccion por forma: alpha_f * W * q_t]
                          |
                          v
              [Agregar al inventario FIFO]
                          |
                          v
              [Envejecer capas (+1 dia)]
                          |
                          v
              [Descartar si edad > L_f]  ──> (Eq. 7)
                          |
                          v
              [Asignar ventas (greedy)]   ──> v[f,t,w]
                  por precio desc.              |
                          |                     v
                          v              [Insatisfaccion]
              [Descontar FIFO]            u = d - v  (Eq. 3)
                          |
                          v
              [Inventario final]  ──> I[f,t,w]  (Eq. 2)
```

---

## 2. Funcion Objetivo (objective.py)

### Pseudocodigo

```
FUNCION evaluar(solucion, instancia) -> Desglose:
    revenue   = 0
    prod_cost = 0
    setup_cost = 0
    inv_cost  = 0
    pen_cost  = 0

    PARA CADA escenario w CON probabilidad pi[w]:
        PARA CADA periodo t:
            // Ingresos
            PARA CADA forma f:
                revenue += pi[w] * r[f] * v[f,t,w]

            // Costos (no dependen del escenario)
            prod_cost  += c_prod * q[t] / n_scenarios
            setup_cost += F * y[t] / n_scenarios

            // Costos de inventario y penalizacion
            PARA CADA forma f:
                inv_cost += pi[w] * c_inv[f] * I[f,t,w]
                pen_cost += pi[w] * c_pen[f] * u[f,t,w]

    Z = revenue - prod_cost - setup_cost - inv_cost - pen_cost
    RETORNAR Desglose(Z, revenue, prod_cost, setup_cost, inv_cost, pen_cost)
```

### Version vectorizada (np.einsum)

```python
revenue   = einsum('w,f,ftw->', pi, prices, v)
inv_cost  = einsum('w,f,ftw->', pi, cost_inv, I)
pen_cost  = einsum('w,f,ftw->', pi, cost_pen, u)
prod_cost = cost_prod * sum(q)
setup_cost = cost_setup * sum(y)
```

---

## 3. Verificador de Restricciones (constraints.py)

### Flujo de verificacion completa

```
check_all(solucion, instancia)
    |
    ├── Eq.2: Balance materiales
    |     I[f,t,w] == I[f,t-1,w] + alpha_f*W*q[t] - v[f,t,w]
    |
    ├── Eq.3: Satisfaccion demanda
    |     v[f,t,w] + u[f,t,w] == d[f,t,w]
    |
    ├── Eq.4: Capacidad maxima
    |     q[t] <= Q_max * y[t]
    |
    ├── Eq.5: Lote minimo
    |     q[t] >= Q_min * y[t]
    |
    ├── Eq.6: Limite de ventas
    |     v[f,t,w] <= I[f,t-1,w] + alpha_f*W*q[t]
    |
    ├── Eq.7: Perecibilidad
    |     I[f,t,w] = 0 si sin produccion en L_f periodos
    |
    └── Eq.8: Dominios
          y in {0,1}, q in Z+, v,I,u >= 0
```

### Calculo de alpha efectivo (_get_effective_alpha)

```
FUNCION alpha_efectivo(instancia) -> alpha_f[F]:
    // composition[F x A] @ alpha[A] = alpha_f[F]
    alpha_f = MULTIPLICAR_MATRICES(composition, alpha)

    SI config_corte_fija:
        alpha_f = alpha_f * mascara_config    // desactivar formas no usadas

    RETORNAR alpha_f
```

---

## 4. Pipeline Completo

```
                    PRIMERA ETAPA              SEGUNDA ETAPA
                  (var. de decision)         (calculada por decoder)

Metaheuristica ──> [y, q] ──> decoder.decode() ──> [v, I, u]
                                                       |
                                                       v
                                              objective.evaluate()
                                                       |
                                                       v
                                                    Z (fitness)
                                                       |
                                                       v
                                              constraints.check_all()
                                                       |
                                                       v
                                                  {factible?}
```

La metaheuristica solo manipula (y, q). El decoder calcula (v, I, u).
El evaluador calcula Z. El verificador confirma factibilidad.

---

## 5. Solver Exacto MILP (solver.py)

Construye el modelo completo en PuLP y lo resuelve con CBC/HiGHS/Gurobi.

### Pseudocodigo

```
FUNCION solve_exact(instancia, time_limit, solver) -> SolverResult:
    alpha_f = composition @ alpha    // alpha efectivo

    // === CONSTRUIR MODELO ===
    modelo = MAXIMIZAR

    // Variables de primera etapa
    y[t] in {0,1}           para t in T
    q[t] in Z+              para t in T

    // Variables de segunda etapa
    v[f,t,w] >= 0           para f,t,w
    I[f,t,w] >= 0           para f,t,w
    u[f,t,w] >= 0           para f,t,w

    // Funcion objetivo (Eq. 1)
    Max Z = sum_w pi[w] * sum_t (
        sum_f r[f]*v[f,t,w]
        - c_prod*q[t] - c_setup*y[t]
        - sum_f c_inv[f]*I[f,t,w]
        - sum_f c_pen[f]*u[f,t,w]
    )

    // Restricciones
    PARA CADA w, t, f:
        I[f,t,w] = I[f,t-1,w] + alpha_f[f]*W*q[t] - v[f,t,w]    (Eq. 2)
        v[f,t,w] + u[f,t,w] = d[f,t,w]                           (Eq. 3)
        v[f,t,w] <= I[f,t-1,w] + alpha_f[f]*W*q[t]               (Eq. 6)

    PARA CADA t:
        q[t] <= Q_max * y[t]                                       (Eq. 4)
        q[t] >= Q_min * y[t]                                       (Eq. 5)

    // Perecibilidad linealizada (Eq. 7)
    PARA CADA w, f, t:
        M = Q_max * W * alpha_f[f] * L[f]    // big-M
        I[f,t,w] <= M * SUM(y[s] para s en [t-L[f]+1, t])

    // === RESOLVER ===
    status = modelo.resolver(solver, time_limit)
    RETORNAR SolverResult(solucion, status, gap, tiempo)
```

### Linealizacion de la Perecibilidad (Eq. 7)

La perecibilidad no es directamente lineal. Se linealiza con big-M:

```
SI no hubo produccion (y=0) en los ultimos L_f periodos:
    ENTONCES I[f,t,w] debe ser 0

Linealizacion:
    I[f,t,w] <= M * SUM(y[s], s = max(0,t-L+1) ... t)

Donde M = Q_max * W * alpha_f * L_f (cota superior del inventario)
```

Esto permite que:
- Si al menos un y[s]=1 en la ventana: I puede ser positivo
- Si todos y[s]=0 en la ventana: I forzado a 0

---

## 6. Actualizacion Post-validacion (2026-02-28)

Se incorporaron controles estructurales para evitar sobreconteo de masa
anatomica cuando hay formas de corte superpuestas.

### Nuevas variables y restricciones clave

```text
p[f,t]   = produccion por forma y periodo
z[f,t]   = activacion de forma (si cut_config es variable)
```

Asignacion anatomica:

```text
sum_f composition[f,a] * p[f,t] <= alpha[a] * W * q[t]   para toda pieza a, periodo t
```

Balance y limite de ventas:

```text
I[f,t,w] = I[f,t-1,w] + p[f,t] - v[f,t,w]
v[f,t,w] <= I[f,t-1,w] + p[f,t]
```

Exclusividad (si aplica):

```text
sum_{f in grupo_g} z[f,t] <= 1   para todo grupo g, periodo t
p[f,t] <= M_f * z[f,t]
```

Perecibilidad (formulacion lineal por ventana de produccion):

```text
I[f,t,w] <= sum_{s=max(0,t-L[f]+1)}^t p[f,s]
```

Nota: para detalle completo de la correccion, ver `docs/sprint1_4_correcciones.md`.

