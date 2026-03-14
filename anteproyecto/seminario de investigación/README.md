# Entregables - Seminario de Investigación I

Este directorio contiene los entregables principales para el **Seminario de Investigación I** según los requisitos del curso.

> [!WARNING]
> **CRÍTICO - Referencias Bibliográficas**: El protocolo contiene referencias que están **PENDIENTES DE VALIDACIÓN**. Consulta `guia_revision_bibliografica.md` para el proceso sistemático de validación antes de usar los datos cuantitativos.

## 📋 Estructura de Evaluación

Según el programa del curso, la evaluación se distribuye así:

| Componente | Peso | Entregable |
|------------|------|------------|
| Protocolo de Investigación | 40% | `protocolo_investigacion.md` |
| Presentación Oral | 40% | `presentacion_oral_protocolo.pptx` |
| Participación y Coevaluación | 20% | Durante clases |

---

## 📁 Archivos en Este Directorio

### Documentos Principales

1. **`protocolo_investigacion.md`** 📄
   - Protocolo de investigación completo en formato Markdown
   - Diseñado para co-creación colaborativa
   - **Secciones marcadas con 🔄**: Requieren completado conjunto
   - **Secciones marcadas con 📚**: Requieren validación bibliográfica
   - Incluye: título, problema, justificación, objetivos, marco teórico, metodología, cronograma, presupuesto

2. **`guia_revision_bibliografica.md`** 📚 **[DOCUMENTO CRÍTICO]**
   - Metodología sistemática para validar referencias bibliográficas
   - Ecuaciones de búsqueda para bases de datos académicas (Scopus, WoS, IEEE, etc.)
   - Plantillas de documentación y fichas bibliográficas
   - Checklist de validación
   - Lista de las 14 referencias a validar del anteproyecto
   - **USAR ANTES de confiar en datos cuantitativos del protocolo**

3. **`presentacion_oral_protocolo.pptx`** 🎤
   - Presentación PowerPoint profesional (15 diapositivas)
   - Cubre todos los puntos clave del protocolo
   - Lista para defender en clase
   - Diseño moderno y consistente

4. **`crear_presentacion.py`** 🐍
   - Script Python para generar/regenerar la presentación
   - Útil si necesitas modificar el diseño o contenido
   - Requiere: `python-pptx`

---

## 📄 1. Protocolo de Investigación (40%)

### Contenido del Protocolo

✅ **Secciones incluidas:**
1. Título de la investigación
2. Planteamiento del problema
3. Justificación
4. Objetivos (general y específicos)
5. Marco teórico
6. Metodología completa (5 fases)
7. Cronograma (26 semanas)
8. Presupuesto
9. Resultados esperados
10. Bibliografía (integrada con BibTeX)

### ⚠️ IMPORTANTE: Estado de Referencias

El protocolo incluye datos cuantitativos y referencias que provienen del anteproyecto preliminar y **NO HAN SIDO VALIDADOS**. 

**Acción Requerida:**
- [ ] Consultar `guia_revision_bibliografica.md`
- [ ] Validar sistemáticamente las 14 referencias listadas
- [ ] Actualizar protocolo con datos verificados
- [ ] Eliminar o marcar datos que no puedan validarse

### Cómo Trabajar con el Protocolo

1. **Revisar el documento completo**
   ```bash
   code protocolo_investigacion.md
   ```

2. **Identificar secciones pendientes**
   - **🔄**: Requieren co-creación
   - **📚**: Requieren validación bibliográfica
   - Lee las guías de "PARA COMPLETAR JUNTOS"

3. **Prioridad #1: Revisión Bibliográfica**
   - Seguir metodología en `guia_revision_bibliografica.md`
   - Validar referencias antes de confiar en datos numéricos
   - Documentar hallazgos

4. **Renderizar a PDF (opcional)**
   ```bash
   pandoc protocolo_investigacion.md -o protocolo_investigacion.pdf \
     --bibliography=../referencias_dlbp.bib \
     --csl=../apa.csl \
     --pdf-engine=xelatex
   ```

---

## 📚 2. Guía de Revisión Bibliográfica (**NUEVO**)

### Propósito

Este documento es **CRÍTICO** porque:
- Las referencias del anteproyecto no han sido validadas
- Los datos cuantitativos necesitan verificación
- Es necesario realizar búsqueda sistemática en bases académicas

### Contenido de la Guía

1. **Metodología PRISMA adaptada** para revisión sistemática
2. **Ecuaciones de búsqueda** para:
   - Scopus
   - Web of Science
   - IEEE Xplore
   - ScienceDirect
   - Google Scholar
3. **Tracking de 14 referencias a validar**:
   - @AltairOptimization2019
   - @PoultryEfficiencyStudy2022
   - Solano-Blanco et al. (2022)
   - Becker & Scholl (1998)
   - Y más...
4. **Plantillas de documentación**:
   - Fichas bibliográficas
   - Tablas de evidencia
   - Tracking de validación
5. **Fuentes de datos industriales**:
   - FENAVI
   - FAO
   - DANE
   - ICA
6. **Cronograma de 6 semanas** para completar revisión

### Cómo Usar la Guía

```bash
# 1. Abrir la guía
code guia_revision_bibliografica.md

# 2. Seguir Fase 1: Validación de referencias existentes

# 3. Configurar Zotero (sección 9.1)

# 4. Ejecutar búsquedas sistemáticas (sección 2)

# 5. Documentar hallazgos con plantillas (sección 5)
```

---

## 🎤 3. Presentación Oral (40%)

### Estructura de la Presentación (15 diapositivas)

1. Portada
2. Agenda
3. Contexto  
4. Planteamiento del Problema
5. Pregunta de Investigación
6. Justificación
7. Objetivos
8. Marco Teórico: DLBP
9. Metaheurísticas
10. Metodología
11. Cronograma
12. Resultados Esperados
13. Contribuciones
14. Referencias Clave
15. Cierre

### Características de Diseño

- ✅ Paleta profesional (azules corporativos)
- ✅ Fuentes optimizadas para proyección
- ✅ Estructura consistente
- ✅ Fondos suaves RGB(245, 248, 250)

### Duración Sugerida

- **Total**: 15-20 minutos
- **Por diapositiva**: ~1-1.5 minutos
- **Preguntas**: 5 minutos

---

## 🔧 4. Scripts Auxiliares

### `crear_presentacion.py`

Genera la presentación automáticamente.

**Uso:**
```bash
python crear_presentacion.py
```

**Dependencias:**
```bash
pip install python-pptx
```

---

## 🎯 Próximos Pasos Prioritarios

### 1. PRIORIDAD MÁXIMA: Revisión Bibliográfica

- [ ] Abrir `guia_revision_bibliografica.md`
- [ ] Configurar Zotero o Mendeley
- [ ] Validar Top 3 referencias:
  1. Solano-Blanco et al. (2022) - Fundamental
  2. Becker & Scholl (1998) - Base teórica
  3. @AltairOptimization2019 - Caso colombiano
- [ ] Ejecutar primera búsqueda sistemática en Scopus
- [ ] Documentar hallazgos

### 2. Completar Secciones del Protocolo

Después de validar referencias, completar secciones con 🔄:
- [ ] Sección 2.2: Contexto industrial específico
- [ ] Sección 3.2: Casos adicionales validados
- [ ] Sección 5.2: Estado del arte con literatura validada
- [ ] Sección 6.3: Datos reales de calibración
- [ ] Sección 7.3: Ajuste de presupuesto

### 3. Preparar Presentación

- [ ] Revisar cada diapositiva
- [ ] Practicar (cronometrar)
- [ ] Preparar notas del presentador
- [ ] Ensayar respuestas a preguntas

---

## 📚 Recursos Adicionales

### Archivos de Referencia

- **Anteproyecto**: `../anteproyecto_dlbp_coproductos.md`
- **Descripción problema**: `../descripcion_problema.md`
- **Referencias BibTeX**: `../referencias_dlbp.bib`
- **Estilo APA**: `../apa.csl`

### Enlaces Útiles

- [Zotero](https://www.zotero.org/) - Gestor de referencias (recomendado)
- [Scopus](https://www.scopus.com/) - Base de datos académica
- [Web of Science](https://www.webofscience.com/)
- [Python-PPTX Docs](https://python-pptx.readthedocs.io/)
- [Pandoc Manual](https://pandoc.org/MANUAL.html)

### Fuentes de Datos Industriales

- [FENAVI](https://fenavi.org/) - Federación Nacional de Avicultores
- [FAO Poultry](https://www.fao.org/poultry-production-products/)
- [DANE](https://www.dane.gov.co/)

---

## ✅ Checklist de Entrega

### Antes de Entregar el Protocolo

- [ ] **CRÍTICO**: Referencias bibliográficas validadas
- [ ] Todas las secciones principales completadas
- [ ] Secciones 🔄 co-creadas
- [ ] Datos cuantitativos verificados (o eliminados si no validados)
- [ ] Referencias en formato APA correctamente citadas
- [ ] Tablas y figuras numeradas
- [ ] Cronograma alineado con fechas del curso
- [ ] Presupuesto realista
- [ ] Documento revisado por tutor/pares

### Antes de la Presentación Oral

- [ ] 15 diapositivas completas
- [ ] Diseño profesional y consistente
- [ ] Texto legible sin sobrecarga
- [ ] Duración ensayada (15-20 min)
- [ ] Notas del presentador preparadas
- [ ] Respuestas a preguntas potenciales listas
- [ ] Probada en equipo de presentación

---

## 📞 Soporte y Co-creación

Cuando necesites ayuda:

1. **Identifica la sección específica**
2. **Prepara información relevante** (referencias leídas, datos encontrados)
3. **Solicita co-creación** con contexto

**Ejemplo:**
> "Validé la referencia Solano-Blanco et al. (2022) en IJPE. Encontré que los datos de 7-57% mejora en utilidad son correctos. ¿Podemos actualizar la Sección 2.3.1 del protocolo con esta información validada?"

---

## 📝 Historial de Cambios

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| 0.1 | 2025-11-21 | Creación inicial de protocolo y presentación |
| 0.2 | 2025-11-21 | Ajuste para reflejar necesidad de validación bibliográfica. Creación de `guia_revision_bibliografica.md` |

---

## ⚠️ Recordatorio Importante

> [!CAUTION]
> **NO USES datos cuantativos del protocolo en tu entrega final hasta que hayas validado las referencias fuente**. Es preferible tener MENOS datos pero VERIFICADOS que muchos datos sin sustento académico.

**¡Éxito en tu Seminario de Investigación I!** 🎓
