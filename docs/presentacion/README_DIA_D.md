# README — Día D (sustentación)

Guía de arranque y operación para defender **`sustentacion_coproductos.html`**
(Reveal.js 4.5.0, 35 láminas, tema "tinta institucional"). Todo el material es
**100% offline** (~10 MB): fuentes, Chart.js, Reveal y el plugin de notas están en
`libs/`. No requiere internet.

---

## 1. Checklist de arranque (5 min antes)

- [ ] Copiar la carpeta `docs/presentacion/` completa al equipo de sustentación
      (o a una USB de respaldo). Debe incluir `libs/`, `figuras/`,
      `presentation_data.js` y `sustentacion_coproductos.html`.
- [ ] Abrir **`sustentacion_coproductos.html`** en **Google Chrome** (recomendado)
      con doble clic. Esperar a que carguen las gráficas (1–2 s).
- [ ] Verificar que el logo UTP y las 4 animaciones (GA/SA/DE/GA-SA) se ven.
- [ ] Pulsar **F** para pantalla completa.
- [ ] Pulsar **S** para abrir la **vista de orador** (speaker view) en una segunda
      ventana: allí verás las notas, el cronómetro y la lámina siguiente.
      Colócala en la pantalla del portátil y proyecta solo la ventana principal.
- [ ] Tener listo el **PDF de respaldo** (ver §4) por si falla el navegador.
- [ ] **NO abrir** `sustentacion_dlbp_LEGACY.html` — es una versión antigua obsoleta.
      Tampoco tocar `presentation_data.js` ni las figuras.

---

## 2. Atajos de teclado de Reveal

| Tecla | Acción |
|-------|--------|
| **→ / Espacio** | Avanzar (revela fragmentos uno a uno y luego pasa de lámina) |
| **←** | Retroceder |
| **S** | Abrir **vista de orador** (notas + cronómetro + próxima lámina) |
| **F** | Pantalla completa |
| **B** o **.** | **Pantalla negra** (para hacer una pausa y captar la atención) |
| **O** o **ESC** | Vista general (**overview**) de todas las láminas — útil para saltar |
| **Alt + clic** | Zoom sobre un punto (detalle de una gráfica) |
| **Inicio / Fin** | Ir a la primera / última lámina |

> Las láminas con contenido dosificado por **fragmentos** (4 Hipótesis,
> 16 Campaña v2, 22 Conclusiones) requieren pulsar **→** varias veces antes de
> pasar a la siguiente. No te adelantes con clic.

---

## 3. Contador de láminas

El contador muestra **solo el número actual** (`slideNumber:'c'`), no `26/35`.
Es deliberado: **9 de las 35 láminas son material de respaldo** (después de
"¿Preguntas?") y no forman parte de la exposición. Así el jurado no percibe que
"faltan" láminas al llegar al cierre.

Estructura: 26 láminas de exposición (portada → contribuciones → ¿Preguntas?) +
1 divisoria "Material de respaldo" + 8 láminas de respaldo para el turno de preguntas.

---

## 4. Exportar el PDF de respaldo (hazlo la víspera)

1. En Chrome, abrir el archivo con el parámetro de impresión:
   **`sustentacion_coproductos.html?print-pdf`**
   (arrastra el archivo y añade `?print-pdf` al final de la URL).
2. **Ctrl + P** (Imprimir).
3. Destino: **Guardar como PDF**.
4. Diseño: **Horizontal**.
5. Márgenes: **Ninguno**.
6. Activar **"Gráficos de fondo"** (Background graphics) — imprescindible para
   que se vean los fondos azules de las divisorias y los callouts.
7. Guardar como `sustentacion_coproductos_RESPALDO.pdf` junto al HTML.

> El PDF congela las gráficas y los fragmentos en su estado final; es solo un
> plan B. La versión viva es el HTML.

---

## 5. Presupuesto de tiempo (exposición ≈ 39–40 min + preguntas)

Ajustado a las láminas reales. Cada acto abre con su divisoria azul.

| Bloque | Láminas | Tiempo |
|--------|---------|--------|
| **Apertura** | Portada + Agenda | **2.5 min** |
| **Acto I — El problema** | Divisoria I + láminas 1–7 (contexto, problema, justificación, hipótesis, objetivos, marco teórico, estado del arte) | **11 min** |
| **Acto II — Modelo y algoritmos** | Divisoria II + láminas 8–11 (MILP, 4 estrategias, codificación, vecindades) | **7 min** |
| **Acto III — La evidencia** | Divisoria III + láminas 12–20 (diseño, análisis v1, resultados, inferencia, **campaña v2**, escalabilidad, convergencia, Pareto, sensibilidad) | **12 min** |
| **Acto IV — Qué significa** | Divisoria IV + láminas 21–23 (limitaciones, conclusiones, contribuciones) + ¿Preguntas? | **7 min** |
| **Preguntas del jurado** | Material de respaldo (8 láminas) | *sin límite* |

**Momentos clave donde bajar el ritmo:** lámina 14 (el empate del baseline *es*
un hallazgo) y lámina 16 (campaña v2: +20% beneficio, −30% inventario). Son el
giro argumental de la tesis.

---

## 6. Qué NO hacer

- **No** abrir `sustentacion_dlbp_LEGACY.html` (versión vieja).
- **No** editar `presentation_data.js` ni las figuras PNG/GIF (otro proceso las
  regenera).
- **No** depender de internet: todo es local. Si una gráfica no carga, recarga
  con **Ctrl + Shift + R**.
- **No** proyectar la vista de orador: esa ventana (con las notas) va solo en tu
  portátil.
