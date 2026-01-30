# Guía de Desarrollo del Anteproyecto y Proyecto

Esta guía centraliza el plan de trabajo, las recomendaciones de implementación
y la ruta de investigación para elaborar el anteproyecto y el proyecto final
sobre optimización del balanceo de carcasa. La búsqueda de documentación se
realiza de forma manual y los resultados relevantes se registran en los
archivos del repositorio.

---

## 1. Organización del repositorio y entorno

- **Estructura recomendada**
  - `README.md`, `LICENSE`, `CONTRIBUTING.md` en la raíz.
  - `src/` para código fuente y utilidades.
  - `data/` para metadatos y bases de prueba (sin PDFs cerrados).
  - `test/` para pruebas automatizadas.
  - `docs/` o `planning/` para cronogramas, figuras y actas.
- **Dependencias y reproducibilidad**
  - Gestionar paquetes con `requirements.txt` y entornos virtuales.
  - Usar `python-dotenv` para cargar rutas o claves desde un archivo `.env`.
  - Opcional: contenedor de desarrollo o `Dockerfile` para ambientes coherentes.
- **Calidad y automatización**
  - Incluir pruebas (`pytest`) y, si es posible, _pre-commit hooks_ para linting.
  - Configurar flujos de integración continua cuando el proyecto crezca.

---

## 2. Proceso de investigación y redacción

1. **Preparación (Sem. 0‑1)**
   - Crear repositorio con la estructura mínima.
   - Reunión inicial con el director para alinear alcance y métricas.
   - Copiar plantillas básicas y definir gestor de referencias.
2. **Definición del problema (Sem. 1‑2)**
   - Redactar contexto, pregunta de investigación y objetivos.
   - Validar coherencia con el director.
3. **Búsqueda sistemática manual (Sem. 2‑4)**
   - Construir tesauro y cadenas de búsqueda.
   - Registrar cada consulta y almacenar metadatos en el gestor de referencias.
4. **Screening (Sem. 4‑6)**
   - Aplicar criterios de inclusión/exclusión sobre título, resumen y texto completo.
   - Mantener un registro transparente de decisiones y duplicados.
5. **Extracción y síntesis (Sem. 6‑8)**
   - Completar la tabla comparativa del estado del arte.
   - Elaborar conteos PRISMA y narrativa crítica de vacíos.
6. **Metodología preliminar (Sem. 8‑10)**
   - Definir paradigma de modelado, datos requeridos y esquema de validación.
7. **Cronograma y recursos (Sem. 10‑11)**
   - Construir el plan temporal y asignar responsables.
8. **Redacción del anteproyecto (Sem. 11‑13)**
   - Integrar secciones revisadas en la plantilla oficial.
   - Insertar tabla comparativa y diagrama PRISMA.
9. **Revisión y ajustes (Sem. 13‑14)**
   - Incorporar comentarios del director y generar versión final.
10. **Resumen ejecutivo y defensa (Sem. 14)**
    - Preparar un resumen de una página y diapositivas de presentación.

---

## 3. Recomendaciones para agilizar el anteproyecto

- Mantener **reuniones periódicas** y registrar acuerdos en `planning/`.
- Trabajar con **Issues o tareas pequeñas** para avanzar de forma incremental.
- Automatizar tareas repetitivas (generación de tablas, conteos PRISMA) con
  scripts en `src/`.
- Llevar un **checklist** de entregables para evitar olvidos.
- Hacer commits frecuentes y descriptivos; ejecutar las pruebas antes de cada
  cambio significativo.
- Utilizar este asistente para revisar texto, generar código auxiliar o
  proponer mejoras metodológicas.

---

## 4. Colaboración con el asistente

- Describe con claridad la tarea o problema a resolver.
- Comparte fragmentos de código o secciones del documento que quieras mejorar.
- Solicita ejemplos o plantillas cuando necesites inspiración.
- Revisa y ejecuta siempre los comandos y pruebas que el asistente sugiera.

Con esta guía unificada se dispone de un recorrido claro desde la organización
del repositorio hasta la redacción y defensa del anteproyecto, facilitando la
colaboración continua con el asistente.

