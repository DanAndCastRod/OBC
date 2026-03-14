# Correcciones Sprint 1.4 (Post-validacion)

**Fecha:** 2026-02-28  
**Alcance:** `src/model`, `tests`, `docs`

## Resumen ejecutivo

Se corrigieron tres riesgos detectados en la validacion del Sprint 1.4:

1. Sobreconteo de masa anatomica cuando existen formas de corte superpuestas.
2. Ausencia de control explicito de exclusividad en ejecucion/solver.
3. Tests no reproducibles sin configurar `PYTHONPATH`.

## Cambios implementados

### 1) Produccion explicita por forma (`p[f,t]`)

- Se agrego `p` a `Solution` como produccion por forma y periodo.
- `decoder.decode()` ahora calcula `p[f,t]` con asignacion explicita desde un pool anatomico:
  - pool por pieza: `alpha[a] * weight * q[t]`
  - consumo por forma segun `composition[f,a]`
- Esto evita duplicar masa de una misma pieza entre varias formas.

Archivos:
- `src/model/solution.py`
- `src/model/decoder.py`

### 2) Activacion de formas (`z[f,t]`) y exclusividad

- Se agrego `z` a `Solution` (activacion por forma/periodo).
- En decoder:
  - si `cut_config` es fija, se respeta directamente.
  - si `cut_config` es variable, se aplica seleccion por grupos de exclusividad.
- En constraints:
  - nuevo check `check_exclusivity`.
  - validacion de `cut_config=0 -> p=0`.
- En `ProblemInstance.validate()`:
  - validacion de dominio de `cut_config` (solo 0/1 y longitud correcta).
  - validacion de conflictos de `cut_config` contra `exclusivity_groups`.

Archivos:
- `src/model/parameters.py`
- `src/model/constraints.py`
- `src/model/decoder.py`

### 3) Solver MILP con asignacion anatomica

Se actualizo la formulacion en `solve_exact()`:

- Nueva variable `p[f,t]` (produccion por forma, primera etapa extendida).
- Nueva variable `z[f,t]` cuando `cut_config` es variable.
- Restriccion de asignacion anatomica:
  - `sum_f composition[f,a] * p[f,t] <= alpha[a] * weight * q[t]`
- Restriccion de activacion:
  - `p[f,t] <= M_f * z[f,t]` y `p[f,t] <= M_f * y[t]`
- Restricciones de exclusividad:
  - `sum_{f in grupo} z[f,t] <= 1`
- Balance/sales actualizados a `p[f,t]`:
  - `I[f,t,w] = I[f,t-1,w] + p[f,t] - v[f,t,w]`
  - `v[f,t,w] <= I[f,t-1,w] + p[f,t]`
- Perishability lineal sin big-M (ventana de produccion reciente):
  - `I[f,t,w] <= sum_{s=t-L_f+1..t} p[f,s]`

Archivo:
- `src/model/solver.py`

### 4) Robustez de ejecucion de tests

- Se agrego `tests/conftest.py` para incluir la raiz del proyecto en `sys.path`.
- Ahora `pytest` funciona sin exportar variables manuales.

Archivo:
- `tests/conftest.py`

## Nuevas pruebas agregadas

Se agregaron tests especificos para la correccion del sobreconteo:

- `tests/test_constraints.py`
  - `test_decoder_respects_part_pool_with_overlap`
  - `test_part_allocation_detects_legacy_overcount`
- `tests/test_solver.py`
  - `test_solver_respects_part_allocation_overlap`

## Evidencia de validacion

Comando ejecutado:

```bash
pytest tests/test_parameters.py tests/test_constraints.py tests/test_solver.py -q
```

Resultado:

- **41 tests passed**
- Sin necesidad de `PYTHONPATH` manual.

## Compatibilidad

- El verificador mantiene compatibilidad con soluciones legacy sin `p`:
  - si `sol.p` no existe, usa la produccion implicita historica como fallback.
- Las soluciones nuevas (decoder/solver) ya incluyen `p` y `z` para trazabilidad completa.
