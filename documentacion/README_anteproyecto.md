# Anteproyecto DLBP - Coproductos con Metaheurísticas

## Descripción

Este repositorio contiene el anteproyecto completo para el desarrollo de un **modelo de Disassembly Line Balancing Problem (DLBP)** específicamente diseñado para optimizar el aprovechamiento de coproductos en la industria avícola mediante técnicas metaheurísticas.

## Estructura del Proyecto

```
├── anteproyecto_dlbp_coproductos.md    # Documento principal del anteproyecto
├── referencias_dlbp.bib                # Base de datos bibliográfica en BibTeX
├── config_anteproyecto.yaml            # Configuración del proyecto
├── generar_anteproyecto.py             # Script para generar documentos
├── apa.csl                             # Estilo de citación APA
└── README_anteproyecto.md              # Este archivo
```

## Características del Anteproyecto

### 🎯 **Enfoque Metodológico**
- **Modelo DLBP** para coproductos avícolas
- **Metaheurísticas**: Algoritmo Genético, PSO, Búsqueda Tabú
- **Pronóstico de demanda** integrado
- **Validación empírica** con datos reales

### ⏱️ **Cronograma**
- Se sugiere presentar un cronograma por fases (alto nivel), alineado con la rúbrica institucional MIOE. La duración total y fechas específicas dependen del plan aprobado por el programa.

### 📊 **Resultados Esperados**
- Reducción del 15-25% en desviación del mix objetivo
- Mejora del 10-20% en utilización de recursos
- Disminución del 5-15% en costos operativos

## Instalación y Uso

### Prerrequisitos

1. **Pandoc** (versión 2.0 o superior)
   ```bash
   # Windows (con Chocolatey)
   choco install pandoc
   
   # macOS (con Homebrew)
   brew install pandoc
   
   # Linux (Ubuntu/Debian)
   sudo apt-get install pandoc
   ```

2. **Python 3.7+** (para el script de generación)
3. **LaTeX** (para generación de PDF)

### Generación de Documentos

#### Opción 1: Script Automático (Recomendado)
```bash
python generar_anteproyecto.py
```

#### Opción 2: Comando Pandoc Manual
```bash
# Generar PDF
pandoc anteproyecto_dlbp_coproductos.md \
  --bibliography=referencias_dlbp.bib \
  --csl=apa.csl \
  --citeproc \
  --pdf-engine=xelatex \
  --toc \
  --number-sections \
  --output=anteproyecto_dlbp_coproductos.pdf

# Generar Word
pandoc anteproyecto_dlbp_coproductos.md \
  --bibliography=referencias_dlbp.bib \
  --csl=apa.csl \
  --citeproc \
  --output=anteproyecto_dlbp_coproductos.docx
```

## Contenido del Anteproyecto

### 📋 **Secciones Principales (según plantilla institucional)**

0. **Datos generales** (estudiante, programa, director, fechas)
1. **Introducción** (contexto y motivación)
2. **Planteamiento del problema** (incluye pregunta de investigación)
3. **Objetivos** (general y específicos)
4. **Marco teórico y estado del arte** (incluye PRISMA/tablas si aplica)
5. **Metodología** (diseño, datos, modelado, solución, validación, métricas)
6. **Delimitación del alcance**
7. **Cronograma** (alto nivel)
8. **Recursos**
9. **Resultados esperados**
10. **Referencias**
11. **Anexos (opcional)**

### 🔬 **Metodología Técnica (resumen)**

#### Modelo Matemático
- **Variables**: Asignación de tareas, utilización de estaciones
- **Función objetivo**: Minimizar desviación del mix + costos
- **Restricciones**: Precedencia, capacidad, balanceo

#### Metaheurísticas Implementadas
- **Algoritmo Genético**: Población=100, generaciones=500
- **PSO**: Enjambre=50, iteraciones=300
- **Búsqueda Tabú**: Lista tabú=20, iteraciones=200

#### Sistema de Pronóstico
- **ARIMA**: Para patrones estacionales
- **Prophet**: Para eventos especiales
- **Validación cruzada**: 70% entrenamiento, 30% validación

## Bibliografía

El archivo `referencias_dlbp.bib` contiene referencias organizadas en categorías (ejemplos):

- **Fundamentos DLBP**: @AssemblyLineSurvey1998, @Minegishi2000
- **Metaheurísticas**: @MetaheuristicApproach2018, @HybridTabuSearch2019
- **Aplicaciones Avícolas**: @PoultryProportioning2023, @Altair2019
- **Modelos Matemáticos**: @DynamicLotSizing2011, @DisassemblySetupTimes2016

## Personalización

### Modificar el Documento
1. Edita `anteproyecto_dlbp_coproductos.md`
2. Actualiza `config_anteproyecto.yaml` si es necesario
3. Regenera con `python generar_anteproyecto.py`

### Agregar Referencias
1. Añade entradas al archivo `referencias_dlbp.bib`
2. Usa el formato BibTeX estándar
3. Cita en el texto con `[@ClaveReferencia]`

### Cambiar Estilo de Citas
1. Reemplaza `apa.csl` con otro archivo CSL
2. Actualiza la configuración en el script

## Solución de Problemas

### Error: "Pandoc no encontrado"
```bash
# Verificar instalación
pandoc --version

# Reinstalar si es necesario
# Windows: choco reinstall pandoc
# macOS: brew reinstall pandoc
# Linux: sudo apt-get --reinstall install pandoc
```

### Error: "LaTeX no encontrado"
```bash
# Instalar LaTeX
# Windows: MiKTeX o TeX Live
# macOS: MacTeX
# Linux: texlive-full
```

### Error: "Archivo CSL no encontrado"
- Descarga `apa.csl` desde el repositorio oficial de estilos CSL y colócalo en el directorio del proyecto.

## Relación con plantillas institucionales
- Revise `plantillas/Doc_Anteproyecto_RicardoS_DEF_REV_aprob.docx` y `plantillas/Formato Evaluacion Anteproyectos MIOE.pdf` para asegurar que cada sección requerida esté cubierta.
- La plantilla guía de este repo está en `anteproyecto_plantilla.md` e incluye el apartado 0 (Datos generales) y Anexos opcionales para PRISMA, tablas y rúbrica MIOE.

## Contribuciones

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Realiza los cambios
4. Envía un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## Contacto

Para preguntas sobre el anteproyecto:
- **Email**: [tu-email@universidad.edu.co]
- **Institución**: Universidad Tecnológica de Pereira
- **Programa**: Maestría en Ingeniería de Operaciones y Estadística

---

**Nota**: Este anteproyecto está diseñado para ser completado en 8 semanas y se enfoca específicamente en la optimización de coproductos avícolas mediante técnicas de balanceo de líneas de desensamble con metaheurísticas.
