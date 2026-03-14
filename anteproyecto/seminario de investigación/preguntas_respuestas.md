# Preguntas y Respuestas (Q&A) - Defensa de Protocolo

## Categoría 1: Justificación y Relevancia

**P: ¿Por qué eligió el 8.6% como meta de reducción de costos? ¿No es muy ambicioso?**
**R:** "Esa cifra no es arbitraria. Proviene del estudio de Solano-Blanco (2022), realizado en una empresa avícola de Santa Marta con condiciones muy similares a las que modelaremos. Representa un benchmark realista de lo que se puede lograr pasando de una planificación manual a una optimizada. Incluso si logramos la mitad (4-5%), el impacto en una industria de alto volumen sería millonario."

**P: ¿Por qué es necesario usar metaheurísticas? ¿Por qué no programación lineal simple?**
**R:** "El problema DLBP es clasificado como **NP-Hard**. A medida que aumentamos el número de cortes y escenarios de demanda, el tiempo de cómputo para encontrar una solución *exacta* crece exponencialmente. Las metaheurísticas (GA, Tabú) nos permiten encontrar soluciones 'suficientemente buenas' (cuasi-óptimas) en tiempos operativos viables para la toma de decisiones diaria."

## Categoría 2: Metodología y Datos

**P: ¿Cómo va a validar su modelo si no tiene acceso a una planta real mañana?**
**R:** "La validación se hará mediante **simulación con datos sintéticos calibrados**. Utilizaré parámetros de la literatura (rendimientos de carcasa estándar, costos promedio del sector) para crear un 'gemelo digital' del proceso. Esto es estándar en investigación de operaciones cuando el acceso a datos privados es restringido."

**P: ¿Qué pasa si la demanda cambia drásticamente de un día para otro?**
**R:** "Precisamente por eso el modelo es estocástico. No asumimos una demanda fija. El modelo evaluará múltiples escenarios de demanda posibles y buscará una solución que sea robusta frente a esas variaciones, minimizando el riesgo de faltantes o sobrantes extremos."

## Categoría 3: Impacto

**P: ¿Este modelo sirve para cualquier empresa avícola?**
**R:** "La estructura matemática es generalizable porque la anatomía del pollo es la misma en todas partes. Lo que cambia son los parámetros (precios, capacidades). El modelo está diseñado para ser flexible: si una empresa cambia sus costos o sus cortes, solo debe actualizar los parámetros de entrada."

**P: ¿Cuál es la diferencia entre su propuesta y lo que ya hizo Solano-Blanco?**
**R:** "Solano-Blanco se enfocó en la **planificación agregada** de la cadena de suministro (mes a mes). Mi propuesta baja al nivel operativo de la **línea de desensamble** (día a día, turno a turno), optimizando la asignación específica de cortes en la planta. Son complementarios, pero mi enfoque ataca la ineficiencia operativa directa en el piso de producción."
