# Rúbrica para la Investigación sobre Balanceo de Carcasa de Pollo

Esta rúbrica orienta la preparación de un **anteproyecto** y un **proyecto de sistema de balanceo** enfocado en líneas de desensamble de pollo. Se sugiere seguir cada etapa de manera secuencial.

## 1. Anteproyecto con estado del arte y análisis de papers

1. **Delimitación del problema y objetivos.**
   - Plantear la situación actual del desbalance de carcasa.
   - Definir objetivo general y específicos.
2. **Identificación de palabras clave.**
   - "carcass balancing", "poultry", "chicken", "disassembly line", "line balancing", "optimization".
3. **Ecuaciones de búsqueda.**
   - **Scopus**
     ```
     TITLE-ABS-KEY(("carcass balancing" OR "disassembly line" OR "poultry") AND
                   ("optimization" OR "line balancing") AND (chicken OR broiler))
     ```
   - **IEEE Xplore**
     ```
     ("disassembly line" OR "carcass" OR "poultry") AND
     ("optimization" OR "line balancing") AND (chicken OR broiler)
     ```
4. **Recolección y organización de literatura.**
   - Exportar resultados en formato BibTeX.
   - Clasificar artículos por enfoque (modelos matemáticos, heurísticas, casos de estudio).
5. **Lectura crítica y análisis.**
   - Resumir contribuciones, datos utilizados y brechas identificadas.
6. **Estado del arte.**
   - Redactar síntesis integrando los hallazgos más relevantes.
7. **Cronograma preliminar y recursos.**
   - Estimar tiempos de revisión, modelado y validación.

## 2. Proyecto de sistema de balanceo de línea de desensamble

1. **Diseño conceptual del sistema.**
   - Describir flujo de despiece y variables de decisión.
2. **Formulación del modelo de optimización.**
   - Definir función objetivo y restricciones (demanda, proporciones de carcasa, capacidades de línea).
3. **Estrategia de solución.**
   - Seleccionar herramientas (por ejemplo, PuLP o Gurobi) y algoritmos.
4. **Obtención y depuración de datos.**
   - Compilar información de pesos, rendimientos y demanda histórica.
5. **Experimentación y validación.**
   - Ejecutar pruebas piloto, análisis de sensibilidad y comparación con métodos actuales.
6. **Documentación y conclusiones.**
   - Registrar resultados, recomendaciones y oportunidades de mejora.

Esta guía proporciona un marco claro para avanzar desde la revisión inicial hasta la propuesta técnica del sistema de balanceo.