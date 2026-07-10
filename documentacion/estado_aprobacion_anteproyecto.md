# Estado de Aprobación del Anteproyecto — Registro Documental

**Fecha de este registro:** 2026-07-09
**Documento evaluado:** `anteproyecto/anteproyecto_coproductos.pdf`
**Formato de evaluación:** `docs/Formato Evaluacion Anteproyectos MIOE (1).pdf`

---

## 1. Veredicto oficial del formato MIOE

| Campo | Valor |
|---|---|
| Título evaluado | Modelo de Optimización para la Planificación de Coproductos con Metaheurísticas en la Industria Avícola |
| Estudiante | Daniel Andrés Castañeda Rodríguez |
| Directora sugerida | PhD. Eliana Mirledy Ocampo Toro |
| Evaluador | John Andrés Muñoz Guevara |
| Fecha de firma (digital) | 2026-03-09 |
| **Evaluación global** | **Aceptado** ✅ (no "Devuelto para modificaciones" ni "Rechazado") |

## 2. Aspectos calificados "Medio" (los demás fueron "Alto")

1. Relevancia del problema/objetivo(s)
2. Consistencia entre la hipótesis y el problema
3. Cobertura y adecuación de la revisión bibliográfica *(con observación textual, ver §3)*
4. Pertinencia del diseño metodológico a emplear

## 3. Observación textual del evaluador (pendiente de blindar en la tesis)

> "En el documento se afirma que el problema abordado es de tipo NP-hard; sin embargo, las referencias citadas corresponden a problemas diferentes que incluyen variables de distribución, tiempos de setup, tiempos de entrega variables y aprovisionamiento, aspectos que no son considerados en esta investigación. Por lo tanto, sería conveniente justificar o demostrar la complejidad del problema objeto de estudio. Por otro lado, las referencias más actuales muestran que abordan el problema con un enfoque multiobjetivo; por tal motivo, las metaheurísticas podrían emplearse principalmente en un contexto de optimización multiobjetivo. No es claro que el problema objeto de estudio sea un problema de optimización combinatoria, ya que solo se habla de un solo producto."

**Implicaciones para la tesis:**
- Justificar/demostrar la NP-hardness del problema específico (lot-sizing estocástico con setup y perecibilidad), no solo por analogía con problemas distintos.
- Anticipar la pregunta sobre enfoque multiobjetivo (hoy la tesis lo lista como trabajo futuro — NSGA-II).
- Aclarar la naturaleza combinatoria: el problema es multi-producto (coproductos) con decisiones binarias de setup, no mono-producto.

## 4. Discrepancia con la instrucción de la directora (2026-06-24)

La directora indicó el 24/06/2026 que "el anteproyecto no quedó aprobado" y solicitó dos versiones del documento (una sin la estrategia de solución + cronograma de actividades, y un mes después el documento completo), con plazo antes del 09/07/2026 para el comité curricular.

**Estado:** El 2026-07-09 Daniel consultó a la directora si el formato MIOE del 09/03/2026 (Aceptado) no constituye ya la aprobación formal del anteproyecto. **Respuesta pendiente.** Mientras se aclara, el trabajo se enfoca en los pendientes críticos del documento de tesis.

## 5. Cronología documental

| Fecha | Evento |
|---|---|
| 2026-01-19 | Aprobación del anteproyecto de la era DLBP (`documentacion/CHECKPOINT_01_ANTEPROYECTO_APROBADO.md` — proyecto anterior) |
| 2026-03-09 | Formato MIOE firma "Aceptado" para el anteproyecto de coproductos |
| 2026-03-13 | Commit de la presentación de sustentación (`sustentacion_coproductos`) |
| 2026-06-24 | Directora comunica que el anteproyecto "no quedó aprobado" y pide dos versiones |
| 2026-07-09 | Consulta a la directora sobre el formato de aprobación; se prioriza corrección de la tesis |
