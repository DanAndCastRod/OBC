# Capítulo 7: Conclusiones y Trabajo Futuro

## 7.1. Conclusiones Generales

Esta investigación abordó el Problema de Balanceo de Líneas de Desensamble (DLBP) aplicado a la industria avícola colombiana, desarrollando y evaluando tres algoritmos metaheurísticos para optimizar la asignación de tareas a estaciones de trabajo.

### 7.1.1. Respecto a los Objetivos

| Objetivo | Estado | Evidencia |
|----------|--------|-----------|
| Formular modelo MILP para DLBP avícola | ✅ Cumplido | Capítulo 3: Formulación con zonificación y estocasticidad |
| Implementar GA, TS e Híbrido | ✅ Cumplido | Capítulo 4: Framework modular en Python |
| Evaluar comparativamente los algoritmos | ✅ Cumplido | Capítulo 6: Experimento con 30 réplicas y tests estadísticos |
| Generar recomendaciones para la industria | ✅ Cumplido | Sección 7.3: Implicaciones gerenciales |

### 7.1.2. Hallazgos Principales

1. **El Algoritmo Híbrido (GA+TS) ofrece la mejor calidad de solución:** Con una eficiencia de línea promedio del 89.1% y la menor variabilidad (σ menor), el enfoque memético demostró ser el más robusto para el DLBP avícola.

2. **El GA puro ofrece un buen balance calidad-tiempo:** Con resultados solo 1.6% inferiores al Híbrido pero tiempos de ejecución significativamente menores, GA es recomendable para aplicaciones en tiempo real.

3. **La Búsqueda Tabú es la más rápida pero menos estable:** Aunque TS converge más rápido, presenta mayor variabilidad en la calidad de las soluciones, especialmente en instancias grandes.

4. **Las restricciones de zonificación son críticas:** La separación de tareas "sucias" y "limpias" añade complejidad al problema pero refleja las condiciones reales de una planta avícola.

5. **La calibración de parámetros mejora significativamente el desempeño:** El uso de Optuna para calibrar automáticamente los hiperparámetros resultó en una mejora del 8-12% respecto a configuraciones por defecto.

---

## 7.2. Contribuciones de la Investigación

### 7.2.1. Contribuciones Teóricas

1. **Extensión del DLBP al sector alimentario:** Se propuso una formulación matemática específica para el desensamble de productos biológicos, incorporando incertidumbre en tiempos de procesamiento y restricciones sanitarias de zonificación.

2. **Validación empírica de metaheurísticas híbridas:** Se demostró que la combinación sinérgica de exploración (GA) e intensificación (TS) supera a los enfoques puros en el contexto del DLBP.

### 7.2.2. Contribuciones Prácticas

1. **Framework de software reutilizable:** El código desarrollado es modular, documentado y puede adaptarse a otras plantas de procesamiento de alimentos.

2. **Generador de instancias sintéticas:** Permite a investigadores futuros evaluar nuevos algoritmos sin requerir datos confidenciales de plantas reales.

3. **Guía de calibración:** La metodología de calibración automática con Optuna es transferible a otros problemas de optimización combinatoria.

---

## 7.3. Implicaciones Gerenciales

### 7.3.1. Recomendaciones para la Industria Avícola

1. **Adoptar herramientas de balanceo automatizado:** Los métodos manuales o basados en experiencia pueden estar dejando un 5-10% de eficiencia sobre la mesa.

2. **Considerar el rebalanceo periódico:** Dado que la demanda de coproductos fluctúa, se recomienda re-ejecutar el algoritmo de balanceo mensualmente o ante cambios significativos en el mix de productos.

3. **Integrar con sistemas de información existentes:** El framework puede conectarse a ERPs (SAP, Oracle) para alimentarse de datos reales de demanda y capacidad.

### 7.3.2. Ahorro Potencial

Basándose en los parámetros de @SolanoBlanco2022 y nuestros resultados:

| Concepto | Valor Estimado |
|----------|----------------|
| Reducción de estaciones ociosas | 2-3 estaciones |
| Ahorro mensual en mano de obra | $1.5M - $2M COP |
| Reducción en inventario de baja rotación | 15-20% |
| Mejora en nivel de servicio | +5% pedidos completos |

---

## 7.4. Limitaciones del Estudio

1. **Datos sintéticos:** Aunque calibrados con literatura, los datos no provienen de una planta real específica.

2. **Tiempos deterministas en experimentos finales:** A pesar de modelar la estocasticidad, los experimentos se ejecutaron con tiempos fijos para asegurar comparabilidad.

3. **Monoobjetivo:** El modelo optimiza número de estaciones; versiones multi-objetivo (costos, balance ergonómico) quedan para trabajo futuro.

4. **Sin validación de campo:** Los resultados no han sido validados en una planta avícola real en operación.

---

## 7.5. Trabajo Futuro

### 7.5.1. Extensiones Inmediatas

1. **Optimización Multi-Objetivo:** Incorporar objetivos adicionales como minimización de costos energéticos, balance de carga entre estaciones, y reducción del inventario.

2. **Robustez bajo incertidumbre:** Desarrollar una versión estocástica que optimice el valor esperado y el peor caso simultáneamente.

3. **Validación industrial:** Realizar un estudio piloto en una planta avícola colombiana para validar los ahorros proyectados.

### 7.5.2. Líneas de Investigación a Largo Plazo

1. **Aprendizaje por refuerzo:** Explorar agentes RL que aprendan políticas de balanceo dinámico basándose en la demanda en tiempo real.

2. **Digital Twin:** Desarrollar un gemelo digital de la planta que permita simular diferentes configuraciones antes de implementarlas.

3. **Integración con IoT:** Usar sensores para capturar tiempos reales de procesamiento y retroalimentar el modelo continuamente.

---

## 7.6. Reflexión Final

El Problema de Balanceo de Líneas de Desensamble en la industria avícola representa un desafío real con impacto económico significativo. Esta investigación demostró que las técnicas metaheurísticas modernas, adecuadamente calibradas, pueden ofrecer soluciones de alta calidad en tiempos razonables. La combinación de rigor académico (formulación matemática, análisis estadístico) con aplicabilidad práctica (código reproducible, recomendaciones gerenciales) constituye el aporte central de este trabajo.

El sector avícola colombiano, con su volumen de 1.7 millones de toneladas anuales, tiene la oportunidad de adoptar estas herramientas para mejorar su competitividad en un mercado cada vez más exigente. Esperamos que los resultados presentados aquí sirvan como punto de partida para futuras investigaciones y aplicaciones en la industria de procesamiento de alimentos.

---

## Referencias

Las referencias citadas en este capítulo se encuentran en el archivo `referencias_dlbp.bib` del proyecto.
