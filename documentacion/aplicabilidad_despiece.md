# Aplicabilidad práctica: decisión de despiece por lote

**Fecha:** 2026-07-09
**Módulo:** `src/planning/despiece.py` · CLI: `experiments/scripts/despiece_decision.py`

Este documento responde a la pregunta operativa que motiva la tesis y aterriza
su aplicabilidad: *dado un lote de pollo y un mix comercial, ¿cómo despiezar la
carcasa para maximizar la utilidad?*

## 1. Qué resuelve

El modelo de la tesis (`src/model/`) es multi-periodo, estocástico y se resuelve
con metaheurísticas — apropiado para planeación táctica bajo incertidumbre. Pero
la decisión de planta de **un día con pedidos conocidos** es un problema pequeño
y determinista que se resuelve de forma exacta al instante. Ese es el alcance de
`src/planning`:

- **Entrada:** el lote de pollo (perfiles + cantidades) y el mix comercial
  (cortes vendibles, precio por kg y demanda/pedido).
- **Salida:** el plan de despiece óptimo — cuánto producir y vender de cada
  corte, qué demanda queda sin cubrir, y el porcentaje de aprovechamiento de
  cada pieza anatómica, con la utilidad total.

## 2. Perfil del pollo (liviano / estándar / pesado)

A diferencia del pipeline experimental —que usa un peso único por instancia—,
aquí el lote puede ser una **mezcla de perfiles**, cada uno con su propio peso y
sus propias proporciones anatómicas (`alpha`). La masa disponible de cada pieza
es la mezcla ponderada:

    masa_pieza = Σ_perfil  n_carcasas_perfil · peso_perfil · alpha_perfil[pieza]

Los perfiles por defecto (`PERFILES_ESTANDAR`) son:

| Perfil    | Peso (kg) | Pechuga | Muslo | Contramuslo | Ala | Menud. | Otros |
|-----------|:---------:|:-------:|:-----:|:-----------:|:---:|:------:|:-----:|
| liviano   | 2.0       | 0.28    | 0.18  | 0.14        | 0.09| 0.06   | 0.25  |
| estándar  | 2.5       | 0.30    | 0.18  | 0.14        | 0.08| 0.05   | 0.25  |
| pesado    | 3.0       | 0.32    | 0.18  | 0.13        | 0.08| 0.05   | 0.24  |

> **Estos rendimientos son un punto de partida calibrable.** El perfil estándar
> usa las proporciones canónicas de `calibration.py` (USDA/FAO, Ross 308). El
> liviano y el pesado desplazan el rendimiento en la dirección reportada por las
> guías de manejo (un ave más pesada rinde proporcionalmente más pechuga). Para
> uso real, reemplácelos con los rendimientos medidos en su planta.

## 3. Cómo se modela el balance

Es un problema de mezcla de productos bajo producción conjunta:

    max  Σ  precio · venta
    s.a. uso de cada pieza ≤ masa disponible de esa pieza   (no doble conteo)
         venta ≤ producción ;  venta ≤ demanda

La competencia entre cortes que comparten pieza (p. ej. pernil entero vs muslo +
contramuslo) la resuelve automáticamente la restricción de disponibilidad: no se
puede usar más muslo del que hay, lo use el pernil o el muslo individual. Con los
precios FENAVI por defecto, deshuesar (muslo + contramuslo) rinde más que vender
el pernil entero, y el óptimo lo refleja. Si por una razón comercial se quiere
ofrecer *o* pernil *o* individuales (no ambos), se asigna el mismo
`exclusivity_group`.

## 4. Uso

```bash
# Lote de 10.000 pollos estándar, catálogo y demanda por defecto (sin tope)
python experiments/scripts/despiece_decision.py --carcasas 10000

# Mezcla de parvada + pedidos reales (kg)
python experiments/scripts/despiece_decision.py --carcasas 10000 \
    --mezcla "liviano=0.3,estándar=0.5,pesado=0.2" \
    --demanda "Pechuga=6000,Pernil completo=4000,Ala=1500,Menudencias=800"
```

Desde Python:

```python
from src.planning import FlockMix, PERFILES_ESTANDAR, catalogo_despiece_default, optimizar_despiece

flock = FlockMix.from_fractions(10000, {"liviano": 0.3, "estándar": 0.5, "pesado": 0.2})
plan = optimizar_despiece(flock, catalogo_despiece_default())
print(plan.resumen())
```

## 5. Cómo hacer pruebas con datos reales

1. **Rendimientos reales:** medir el `alpha` (proporción de cada pieza) de una
   muestra de canales por perfil de peso en su planta, y reemplazar
   `PERFILES_ESTANDAR`.
2. **Precios reales:** actualizar los precios del catálogo con su lista vigente.
3. **Libro de pedidos:** pasar la demanda real (kg por corte) de un día vía
   `--demanda` o construyendo los `CommercialItem`.
4. **Validación:** comparar el plan que recomienda el modelo contra el despiece
   que la planta realizó ese día, y medir la diferencia de utilidad. Esa
   comparación —sobre varios días— es la evidencia de aplicabilidad que el
   modelo sintético no puede dar por sí solo.

## 6. Relación con la tesis

Este módulo **no modifica** el pipeline experimental ni los resultados de la
tesis. Es una capa de decisión operativa construida sobre la misma estructura de
producción conjunta (piezas anatómicas → formas de corte). Puede presentarse
como evidencia de aplicabilidad práctica y como base para el trabajo futuro de
"validación con datos operativos reales" ya identificado en el Capítulo 8.
