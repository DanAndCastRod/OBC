# Recomendaciones adicionales para mejorar los resultados experimentales

**Fecha:** 2026-07-10
**Método:** análisis multi-agente por lentes (medición de gap, decodificador,
estadística, instancias, algoritmos) con verificación de evidencia contra el
código y los datos del repo. Excluye lo ya decidido: re-ejecución con el decoder
de perecibilidad corregido, perfiles de pollo como factor, datos reales de
planta, y paralelización (ya implementada).

---

## ⚠️ Hallazgo previo que condiciona todo (verificado en los datos)

**`experiments/results/comparison.csv` muestra que CBC terminó las 3 instancias
large en 25–35 segundos** (large_seed42: 34.9 s; seed123: 25.1 s; seed456: 26.9 s),
muy por debajo del límite de 300 s — lo que sugiere que **CBC sí resolvió large a
optimalidad**, contradiciendo §5.5 de la tesis ("CBC no logra converger dentro del
límite de tiempo... confirmando la necesidad de métodos metaheurísticos").
Como el CSV no registra el estatus del solver (columnas: algorithm...is_feasible,
sin `solver_status`) y `run_comparison.py` fuerza `gap_percent = 0.0` para
cbc_exact incondicionalmente, hoy es imposible saber desde los datos si esos Z
son óptimos probados o incumbentes. **Cualquiera de las dos ramas exige acción**:
si CBC resolvió a óptimo, hay que corregir la justificación de la tesis (y los
gaps de 17–19% de las metaheurísticas en large son contra el óptimo verdadero);
si no, hay que registrar el estatus para poder afirmarlo.

---

## Bloque A — Medición honesta del gap (sin re-ejecutar metaheurísticas)

1. **[ALTA/medio] Extraer la best bound y el MIP gap real de CBC** y reportar el
   gap de las metaheurísticas contra la COTA, no contra el incumbente.
   *Evidencia:* `src/model/solver.py:326` (`gap = 0.0 if OPTIMAL else NaN` — nunca
   se lee el gap real), `solver.py:247` (CBC sin `logPath`), `metrics.py:85-99`
   (compara contra Z incumbente). El código legado ya leía `prob.bestBound`
   (`LEGACY/src/experiments/benchmark_milp_completo.py:103-104`), así que es viable
   con PuLP 2.7. *Única recomendación verificada adversarialmente: CONFIRMED.*
   *Impacto:* "a lo sumo X% del óptimo" es defendible ante el jurado aunque CBC
   no converja.

2. **[ALTA/bajo] Registrar `solver_status`, `mip_gap` y `best_bound` en el CSV**
   y dejar de forzar `gap_percent=0.0` para cbc_exact
   (`run_comparison.py:367-368`). Resuelve el hallazgo ⚠️ de arriba.

3. **[ALTA/bajo] Unificar el criterio del caché de referencia CBC**: en fresco
   solo cachea OPTIMAL (`run_comparison.py:322-323`), al reanudar acepta
   cualquier z del CSV (`:216-237`). El gap puede diferir según cómo se ejecutó.

4. **[ALTA/bajo] Reportar el gap desagregado por tamaño** en la tabla principal
   (`generate_results_tables.py:57` promedia gaps contra óptimo con gaps contra
   incumbente en un solo número). La historia honesta — empate con baseline en
   small/medium, diferenciación en large — hoy queda oculta en el promedio.

5. **[MEDIA/bajo] Referencia más fuerte para large**: subir `time_limit` solo
   para cbc_exact en large (corre 1 vez por instancia: son 3 corridas extra) y/o
   probar HiGHS (`solver.py:242-243` ya lo soporta, pero requiere instalar el
   binario: `pulp.HiGHS_CMD().available()` da False en este entorno).

## Bloque B — Más valor estadístico con los datos YA corridos (costo ~cero)

6. **[ALTA/bajo] Explotar los traces guardados**: `comparison_traces.csv` tiene
   317,152 filas con `best_fitness` y `elapsed_seconds` por iteración — da para
   curvas anytime, time-to-target y "alcanza el 99% de su calidad final en X s"
   sin una sola corrida nueva. Convierte el punto más débil (tiempo, 52.5x CBC)
   en un análisis rico.

7. **[ALTA/bajo] Análisis estratificado por tamaño y eliminar el ANOVA agrupado**:
   `run_statistical_tests.py:594-599` aplica `f_oneway` sobre las 270 corridas
   agrupadas (pseudoreplicación: réplicas de la misma instancia tratadas como
   independientes y tamaños mezclados — por eso z_std ≈ 5.2e8, es varianza entre
   instancias, no entre algoritmos).

8. **[MEDIA/bajo] Corregir los tamaños de efecto**: `cohens_d` usa desviación
   agrupada de muestras independientes (`run_statistical_tests.py:91-100`) pero
   se aplica a datos PAREADOS por instancia (`:258,324,371,503`) — por eso todo
   sale "negligible" (d=0.018). Usar d pareado (dz) y añadir diagrama de
   diferencia crítica de Nemenyi.

9. **[ALTA/bajo] Potencia a priori para H1/H3 e IC en vez de veredicto binario**:
   con n=9 instancias y la sd observada, detectar la reducción del 15% de H3
   requeriría ~100 instancias — el diseño nunca tuvo potencia para H3. Decirlo
   explícitamente (y reportar la estimación con IC) es más defendible que
   "no soportada".

## Bloque C — Mejoras al decodificador y algoritmos (requieren re-ejecutar)

10. **[ALTA/medio] Limitar la producción por forma a la demanda residual esperada
    en su ventana de vida útil** (estilo newsvendor): hoy el decoder produce el
    máximo posible de cada forma en orden de precio bruto sin mirar
    `instance.demand` (`decoder.py:65-71`), y la Z sí cobra ese exceso (inventario
    + merma). Beneficia a los 4 algoritmos a la vez y ataca directamente H3.

11. **[ALTA/medio] Pulido matheurístico**: con (y,q) fijos, el subproblema
    restante del MILP es un LP puro (las únicas enteras son y, q —
    `solver.py:82-83`). Resolver ese LP para los cromosomas élite y la solución
    final elimina la suboptimalidad del decoder donde más se ve (gap small/medium
    debería caer de ~3.4% hacia 0–1%).

12. **[ALTA/medio] Igualar el presupuesto entre algoritmos**: SA corre ~28 s
    frente a 456 s de GA (16x menos, `main_results_table.csv`), con
    `max_iterations: 27` heredado de la calibración; la rama de metaheurísticas
    de `_run_single` no impone tope de tiempo/evaluaciones. Igualar por
    evaluaciones o por tiempo hace la comparación publicable — y probablemente
    SA deje de perder contra el baseline.

13. **[MEDIA/medio] Vectorizar la segunda etapa del decoder** (buckets de edad
    [W,L] en NumPy en vez de listas Python por capa): 10–50x más evaluaciones
    por segundo → más presupuesto real para todos con el mismo tiempo.

14. **[MEDIA/alto] Activar la dimensión z (elección de cortes)**: hoy es código
    muerto — el generador siempre fija `cut_config` (`generator.py`), así que ni
    el MILP ni el decoder optimizan qué cortes activar, y en large la config fija
    bloquea el filete premium. Meter z al cromosoma crea la diferenciación
    estructural entre algoritmos que hoy no existe.

15. **[MEDIA/medio] Re-calibrar Optuna tras los cambios**: los hiperparámetros
    actuales se calibraron con el decoder viejo (sin perecibilidad); tras el
    arreglo, el paisaje de fitness cambió.

## Bloque D — Diseño de instancias y del experimento (rediseño)

16. **[ALTA/medio] Hacer que las decisiones de setup importen**: con la economía
    actual el baseline es casi óptimo por construcción — la demanda supera a la
    oferta (nivel de servicio ~56% en estándar), el costo de setup (500k COP/día)
    es ~1% del margen diario, y el inventario es barato frente a los precios.
    Recalibrar: capacidad ≥ demanda esperada (holgura), setup 10–50x más caro,
    estacionalidad `volatile`, vidas útiles cortas frente al horizonte. Y
    diferenciar `medium` de `small` estructuralmente (hoy `medium()` retorna
    `small()`, solo cambian los escenarios).

17. **[ALTA/medio] Más instancias, menos seeds**: la unidad estadística es la
    instancia (n=9), no la réplica (30 seeds). Con el mismo presupuesto, 30
    instancias × 6–9 seeds dan mucha más potencia (la distancia crítica de
    Nemenyi baja de 1.56 a 0.86 rangos). Los perfiles `toy` e `industrial` del
    generador están definidos y sin usar.

18. **[MEDIA/medio] Rediseñar la sensibilidad**: hoy son 30 seeds sobre UNA sola
    instancia (`sensitivity.yaml:34`, `base_instance: medium_seed42`); repartir
    las 450 corridas entre ≥3 instancias base con menos réplicas hace las
    conclusiones replicadas en vez de anecdóticas.

---

### Orden sugerido de ejecución

- **Antes de re-ejecutar nada:** Bloque A completo + hallazgo ⚠️ (cambia cómo se
  mide todo lo demás) → luego Bloque B sobre los datos existentes.
- **En la re-ejecución ya planeada** (decoder de perecibilidad + perfiles): sumar
  #10, #12 y #15, que comparten la misma corrida.
- **Si hay tiempo/alcance:** #11 y #16-17 son los que más pueden cambiar la
  historia de la tesis (metaheurísticas que sí se diferencian del baseline).

*Nota de verificación: la recomendación #1 pasó verificación adversarial completa
(CONFIRMED). Los datos citados de #2, #6, #7, #8, #12, #16 (CSV de CBC, columnas,
traces, código de estadística, tiempos, configs) fueron verificados directamente
contra el repo el 2026-07-10. El resto cita file:line reportados por los agentes
de análisis cuya verificación quedó interrumpida por errores de red; verificar el
punto concreto antes de implementar.*
