# Organización y Depuración de Archivos del Proyecto OBC

## Resumen de la Reorganización

Este documento explica la estructura optimizada del proyecto después de la depuración de archivos redundantes, basándose en los cambios recientes y la necesidad de evitar duplicaciones.

## Archivos Principales a Mantener

### 📋 Documentación Principal
- **`anteproyecto_dlbp_coproductos.md`** - Anteproyecto definitivo y actualizado (746 líneas)
- **`anteproyecto_dlbp_coproductos.pdf`** - Versión PDF del anteproyecto
- **`resumen_ejecutivo_dlbp.md`** - Resumen ejecutivo del proyecto
- **`cronograma_12_semanas.md`** - Cronograma detallado del proyecto

### 📚 Referencias Bibliográficas
- **`referencias_dlbp.bib`** - Referencias principales del proyecto DLBP (577 líneas, actualizado)
- **`apa.csl`** - Estilo de citación APA para documentos

### ⚙️ Configuración y Scripts
- **`config_anteproyecto.yaml`** - Configuración del proyecto
- **`generar_anteproyecto.py`** - Script para generar documentos
- **`fetch_pdfs_from_bib.py`** - Script para descargar PDFs desde bibliografía
- **`requirements.txt`** - Dependencias del proyecto

### 📊 Datos y Reportes
- **`data/`** - Carpeta con PDFs de referencias (mantener todos los archivos)
- **`reporte_descargas.json`** - Reporte de descargas de PDFs
- **`referencias_pendientes.md`** - Referencias por procesar
- **`referencias_urls_a_corregir.md`** - URLs que necesitan corrección

## Archivos Redundantes Identificados para Eliminación

### ❌ Anteproyectos Obsoletos
- **`anteproyecto (1).md`** - Versión anterior, reemplazada por `anteproyecto_dlbp_coproductos.md`
- **`anteproyecto_plantilla.md`** - Plantilla genérica, ya no necesaria
- **`Optimización del balanceo de carcasa.md`** - Documento duplicado

### ❌ Referencias Obsoletas
- **`references.bib`** - Reemplazado por `referencias_dlbp.bib`
- **`referencias.bib`** - Archivo duplicado

### ❌ Documentos de Desarrollo
- **`descripcion_problema.md`** - Contenido integrado en anteproyecto principal
- **`descripcion_problema.pdf`** - PDF obsoleto
- **`doc.pdf`** - Documento genérico sin contenido específico

### ❌ Carpetas de Respuestas Temporales
- **`respuestas/`** - Carpeta completa con respuestas de diferentes IA (temporal)
  - `gemini.md`
  - `notebookml.md`
  - `txyz.md`
  - `GPT/` (subcarpeta completa)

### ❌ Documentos Previos
- **`previousmd/`** - Versiones anteriores de guías ya actualizadas
  - `implementation_guide.md`
  - `investigation_guide.md`  
  - `pasoapaso.md`

### ❌ Archivos de Configuración Temporal
- **`prisma_conteos_template.csv`** - Plantilla temporal
- **`anteproyecto_balanceo_avicola_revision_sistematica.xlsx`** - Hoja de cálculo temporal

## Estructura Final Recomendada

```
OBC/
├── README.md                           # README mejorado
├── ORGANIZACION_ARCHIVOS.md            # Este documento
├── CONTRIBUTING.md                     # Guía de contribución
├── LICENCE                            # Licencia
│
├── 📋 DOCUMENTACIÓN PRINCIPAL/
│   ├── anteproyecto_dlbp_coproductos.md
│   ├── anteproyecto_dlbp_coproductos.pdf
│   ├── resumen_ejecutivo_dlbp.md
│   └── cronograma_12_semanas.md
│
├── 📚 REFERENCIAS/
│   ├── referencias_dlbp.bib
│   ├── apa.csl
│   ├── referencias_pendientes.md
│   └── referencias_urls_a_corregir.md
│
├── ⚙️ SCRIPTS Y CONFIG/
│   ├── config_anteproyecto.yaml
│   ├── generar_anteproyecto.py
│   ├── fetch_pdfs_from_bib.py
│   ├── requirements.txt
│   └── reporte_descargas.json
│
├── 📊 DATOS/
│   └── data/                          # PDFs de referencias
│
└── 📁 PLANTILLAS/                     # Mantener como referencia
    ├── 3. Formulación_.docx.pdf
    ├── Doc_Anteproyecto_RicardoS_DEF_REV_aprob.docx
    └── Formato Evaluacion Anteproyectos MIOE.pdf
```

## Integración en la Documentación Global

### Flujo de Trabajo Principal
1. **`anteproyecto_dlbp_coproductos.md`** es el documento central del proyecto
2. **`config_anteproyecto.yaml`** define los parámetros de configuración
3. **`generar_anteproyecto.py`** automatiza la generación del PDF
4. **`referencias_dlbp.bib`** alimenta las citas del documento principal

### Referencias Cruzadas
- El anteproyecto principal referencia el cronograma y resumen ejecutivo
- Las referencias bibliográficas están centralizadas en `referencias_dlbp.bib`
- Los scripts utilizan la configuración de `config_anteproyecto.yaml`

### Mantenimiento
- Nuevas referencias se agregan a `referencias_dlbp.bib`
- Cambios en el proyecto se reflejan en `config_anteproyecto.yaml`
- El README principal documenta el uso de todos los componentes

## Beneficios de la Reorganización

1. **Eliminación de Redundancia**: Se eliminan ~15 archivos duplicados
2. **Claridad Documental**: Un solo anteproyecto definitivo
3. **Referencias Centralizadas**: Una sola fuente de verdad bibliográfica
4. **Flujo Automatizado**: Scripts optimizados para generar documentación
5. **Mantenimiento Simplificado**: Estructura clara y documentada

## Próximos Pasos

1. Ejecutar la eliminación de archivos redundantes
2. Actualizar el README principal
3. Verificar que todos los scripts funcionen con la nueva estructura
4. Documentar el flujo de trabajo en el README actualizado
