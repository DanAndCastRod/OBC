# Bitácora del proyecto OBC

Registro cronológico de decisiones, hallazgos y acciones sobre el repositorio.
Las entradas más recientes van arriba.

---

## 2026-07-10 (noche) — Bloques C y D: decodificador, algoritmos e instancias

**Bloque C — decodificador y algoritmos:**
- **C#10 tope de demanda (`demand_cap`)**: el decoder puede limitar la
  producción de cada forma a la demanda esperada en su ventana de vida útil
  (newsvendor). Impacto medido en small/medium: Z sube (gap vs CBC de 3.4% a
  **0.8%**) y el inventario baja de ~2,970 a **~756** (CBC ~158). Flag apagado
  por defecto (preserva comportamiento histórico).
- **C#12 presupuesto igualado**: `max_evaluations`/`max_seconds` en la clase
  base cortan los 4 algoritmos por presupuesto común; SA encadena **restarts**
  hasta agotarlo (antes terminaba al enfriarse la primera cadena, compitiendo
  con ~14x menos presupuesto que GA).
- **C#13 segunda etapa vectorizada**: la simulación FIFO con caducidad se
  reescribió en NumPy (cubetas por periodo [W,F,T]); **~12x más rápida** en
  large, con test de equivalencia exacto contra la versión de bucles (que se
  conserva como referencia).

**Bloque D — diseño de instancias y experimento:**
- **D#16 economía v2**: setup 50M COP/día, capacidad con holgura (10–12k),
  demanda volátil. Validado con CBC: el óptimo **apaga la línea 1–5 días** y el
  baseline queda **11–28% por debajo** (en v1 quedaba a ~3%). Prueba ácida:
  GA-SA supera al baseline en **+5.2% a +7.6%** en las instancias v2.
- **D#17 set v2** (`data/instances_v2/`, 30 instancias = 10 por tamaño,
  pensadas para ~6 seeds): la unidad estadística pasa de n=9 a n=30. `medium`
  ahora usa 18 periodos (en v1 era idéntica a small). Generador:
  `experiments/scripts/generate_instances_v2.py --validate`.
- **Config `comparison_v2.yaml`**: 780 corridas (vs 1098), presupuesto
  igualado (20k evals), `demand_cap` activo, salidas en `experiments/results_v2/`.
  Smoke end-to-end (2 instancias, budget reducido): las metaheurísticas se
  **diferencian del baseline** (baseline 11.17% vs GA-SA 5.70%), 12/12 corridas,
  0 errores.

**Pendiente de este bloque:** la sensibilidad multi-instancia (#18) requiere
refactorizar el flujo de `run_sensitivity.py` (hoy toma una sola
`base_instance`); no se hizo para no dejarlo a medias. Cambio necesario: aceptar
`base_instances` (lista) y envolver el cuerpo en un bucle por instancia,
etiquetando el CSV con la instancia base.

Tests: 254 en verde (nuevos: tope de demanda ×3, equivalencia de segunda etapa
×3, restarts de SA por presupuesto ×1).

---

## 2026-07-10 (tarde) — Bloque B: valor estadístico de los datos ya corridos

Implementado sin ejecutar ninguna corrida nueva (todo sobre `comparison.csv` y
`comparison_traces.csv` existentes):

- **Análisis anytime** (`experiments/scripts/analyze_traces.py`, nuevo): curvas
  de calidad best-so-far vs tiempo por tamaño (`tesis/figuras/anytime_curves.png`)
  y tabla time-to-target (`experiments/results/time_to_target.csv`). Hallazgos:
  DE alcanza el 99% del mejor Z conocido en ~5–11 s en small/medium; GA-SA es el
  único que alcanza el 99% en el 100% de las corridas large (mediana 231 s); SA
  se estanca en ~93% de la calidad en small/medium (no llega nunca al 99%).
  Convierte el "52.5x el tiempo de CBC" en un argumento anytime defendible.
- **Estadística corregida** (`run_statistical_tests.py`, protocolo v2.2):
  - `effect_size_dz` pareado en H1/H2/H3: la d agrupada usada antes diluía el
    efecto con la varianza entre instancias (H3 pasaba de d≈0.4 "small" a
    dz=0.67–0.95 "medium/large").
  - Ranking **estratificado por tamaño** (Friedman por estrato); el ANOVA/Tukey
    global queda marcado como pseudoreplicación (solo trazabilidad histórica).
  - **Diagrama de diferencia crítica de Nemenyi** (`tesis/figuras/nemenyi_cd.png`):
    rangos GA-SA 1.33 < GA 2.33 < DE 2.67 < SA 3.67, CD=1.563 → GA-SA
    significativamente mejor que SA; el resto sin diferencia significativa.
  - **Potencia a priori** para H1/H3: con n=9 instancias, H1 tenía potencia ≈0
    (efecto observado 0.6–1.1% < umbral 5%) y H3 entre 0.02–0.10; para 80% de
    potencia se necesitarían cientos de instancias. Conclusión honesta para la
    tesis: el diseño no podía detectar los umbrales declarados; reportar
    estimación con IC en lugar de veredicto binario.
- Verificado: los 15 tests de hipótesis del JSON conservan exactamente los
  mismos p-valores/métricas (0 cambios); solo se añaden secciones nuevas.
  Suite completa: 247 tests en verde.

---

## 2026-07-10 — Recomendaciones para mejorar resultados y arranque del Bloque A

**Análisis:** se ejecutó un análisis multi-agente por lentes (medición de gap,
decodificador, estadística, instancias, algoritmos) con verificación contra el
código. Informe completo: `recomendaciones_mejora_resultados.md` (18
recomendaciones en 4 bloques).

**Hallazgo crítico:** `experiments/results/comparison.csv` muestra que
`cbc_exact` terminó las 3 instancias **large en 25–35 s** (límite: 300 s), lo
que sugiere que CBC resolvió a optimalidad — contradice §5.5 de la tesis ("CBC
no logra converger en large"). El CSV no registra el estatus del solver y
`run_comparison.py` fuerza `gap_percent=0.0` para CBC, así que los datos no
permiten distinguirlo. → Ver resolución al final de esta entrada.

**Decisión (Daniel):** proceder con el **Bloque A** — medición honesta del gap:
1. Extraer `best_bound` y `mip_gap` reales de CBC (`SolverResult`).
2. Registrar `solver_status`, `solver_best_bound` y `gap_vs_bound_percent` en el
   CSV de comparación; dejar de forzar `gap_percent=0.0` para cbc_exact.
3. Unificar el criterio del caché de referencia CBC (fresco vs `--resume`).
4. Tabla de resultados desagregada por tamaño de instancia.

**Resolución del hallazgo (ejecutado 2026-07-10):** se corrió cbc_exact en las 3
instancias large con el solver instrumentado. Resultado:

| Instancia | Estatus | Z | Best bound | MIP gap | Tiempo |
|---|---|---|---|---|---|
| large_seed42 | **optimal** | 1,995,008,340 | 1,995,008,340 | 0.0% | 16.8 s |
| large_seed123 | **optimal** | 1,982,131,972 | 1,982,131,972 | 0.0% | 19.3 s |
| large_seed456 | **optimal** | 1,993,154,118 | 1,993,154,118 | 0.0% | 18.1 s |

**CBC resuelve las 3 large a OPTIMALIDAD PROBADA en 17–19 s** (57,840 variables,
no 72,060 como dice la tesis). Consecuencias:
1. §5.5 de la tesis debe corregirse: con las instancias actuales, los métodos
   exactos NO son intratables. Los gaps de 17–19% de las metaheurísticas en
   large son contra el óptimo verdadero.
2. La justificación de las metaheurísticas debe reformularse (p. ej. escalar a
   instancias genuinamente grandes — perfil `industrial` de 52 periodos × 500
   escenarios está definido y sin usar — o replantearla como comparación
   metodológica) y/o rediseñar las instancias (recomendación #16-17 del informe).
3. La comparación por tamaño (nueva `size_results_table.csv`) muestra además la
   disparidad de presupuesto: en large GA tarda ~1,238 s/corrida y SA ~61 s.

**Implementado (Bloque A completo):**
- `SolverResult` ahora expone `best_bound` y calcula `gap` como el MIP gap real
  (0.0 solo con optimalidad probada) — `src/model/solver.py`.
- CSV de comparación con columnas nuevas `gap_vs_bound_percent`,
  `solver_status`, `solver_best_bound`; se eliminó el `gap_percent=0.0` forzado
  para cbc_exact — `experiments/scripts/run_comparison.py`.
- Caché de referencia unificado: la referencia primal solo se toma de corridas
  OPTIMAL (fresco y `--resume` por igual); la cota se acepta de cualquier corrida.
- Nueva tabla `size_results_table.csv` desagregada por tamaño
  (`generate_results_tables.py::generate_size_table`).
- Tests: 247 en verde (nuevo: `test_best_bound_at_optimality`).

---

## 2026-07-09 (tarde) — Perfiles de pollo, despiece, paralelismo y perecibilidad

- **Perecibilidad del decoder corregida**: las capas FIFO ahora caducan según
  `shelf_life`, igual que la restricción Eq.7 del MILP; `check_perishability`
  usa la misma cota. Impacto: inventario del baseline decodificado baja de
  ~34k–50k a ~3k (orden de CBC). Cambia H3 si se re-ejecuta.
- **Módulo de despiece** (`src/planning/`): decisión de despiece de un periodo
  con perfiles de pollo, LP exacto, CLI `despiece_decision.py`. Ver
  `aplicabilidad_despiece.md`.
- **Perfiles de pollo en el pipeline**: `flock_mix` en `InstanceGenerator`
  (liviano 2.0 kg / estándar 2.5 kg / pesado 3.0 kg, mezclables), con round-trip
  YAML. Smoke run: Z escala 276M→782M liviano→pesado; el gap vs CBC baja
  4.79%→3.12%; servicio 46%→66%.
- **Paralelismo** en `run_comparison.py` (`--workers N`): CBC secuencial
  primero (caché de gap), metaheurísticas en ProcessPoolExecutor. Validado 8/8.
- Commit `48389ac` en rama `feat/perfiles-pollo-y-correcciones-tesis`;
  246 tests en verde.

## 2026-07-09 (mañana) — Auditoría, aprobación del anteproyecto y reparación del PDF

- **Formato MIOE**: el anteproyecto de coproductos fue **Aceptado** el
  2026-03-09 (evaluador John Andrés Muñoz Guevara). Registrado en
  `estado_aprobacion_anteproyecto.md`. Discrepancia con la instrucción de la
  directora del 24/06 ("no quedó aprobado", pidió dos versiones) — consulta
  elevada a la directora, respuesta pendiente. Observación técnica del
  evaluador por blindar: justificar NP-hardness del problema específico.
- **Pipeline del PDF de la tesis reparado**: la causa raíz de los captions
  corruptos era que citeproc interpretaba los marcadores `@@SHORT@@` como citas.
  Solución: pandoc-crossref v0.3.19 + filtro `short-captions.lua`, 9 diagramas
  Mermaid pre-renderizados a PNG, Unicode a modo matemático, "Tabla/Lista de"
  en español. PDF verificado: 58 págs, 26/26 figuras, 0 refs rotas.
- **Cifras corregidas**: gap real vs CBC 8.12–13.11% (el "≤2%" del README/
  Resumen confundía H2, que es vs mejor metaheurística). **H2 reclasificada a
  "parcialmente soportada"** (tiempo 52.5x CBC vs umbral 50%).
- Tests: 234/234 en verde tras instalar dependencias faltantes (auditoría de
  junio no había podido ejecutarlos).
