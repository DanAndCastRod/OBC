# Protocolo de Búsqueda Bibliográfica - DLBP Avícola

## 🎯 Objetivo
Ampliar el estado del arte con **10-15 papers relevantes** enfocados en:
1. DLBP estocástico (tiempos variables)
2. Metaheurísticas híbridas para balanceo de líneas
3. Optimización en industria alimentaria/avícola

---

## 📚 Bases de Datos a Consultar

| Base | URL | Acceso | Prioridad |
| :--- | :--- | :--- | :---: |
| **Scopus** | scopus.com | Institucional UTP | ⭐⭐⭐ |
| **Web of Science** | webofscience.com | Institucional UTP | ⭐⭐⭐ |
| **Google Scholar** | scholar.google.com | Libre | ⭐⭐ |
| **IEEE Xplore** | ieeexplore.ieee.org | Institucional | ⭐⭐ |
| **ScienceDirect** | sciencedirect.com | Institucional | ⭐⭐ |

---

## 🔍 Términos de Búsqueda (Queries)

### Query 1: DLBP Estocástico
```
("disassembly line balancing" OR "DLBP") AND ("stochastic" OR "uncertain" OR "probabilistic")
```

### Query 2: Metaheurísticas para DLBP
```
("disassembly line balancing") AND ("genetic algorithm" OR "tabu search" OR "memetic" OR "hybrid metaheuristic")
```

### Query 3: Optimización en Industria Alimentaria
```
("food processing" OR "poultry" OR "meat processing") AND ("optimization" OR "scheduling" OR "line balancing")
```

### Query 4: Balanceo Multi-objetivo
```
("assembly line balancing" OR "ALBP" OR "DLBP") AND ("multi-objective" OR "pareto" OR "NSGA")
```

### Query 5: Reciente (2020-2025)
```
("disassembly line balancing") AND (year >= 2020)
```

---

## 📋 Lo que necesito que hagas

### Paso 1: Ejecutar Búsquedas
Para cada Query, necesito que me reportes:

| Query | Base de Datos | # Resultados | Top 5 Títulos Relevantes |
| :--- | :--- | :--- | :--- |
| Q1 | Scopus | 59 | [Q1-1] "10.3390/s23031652", [Q1-2] "10.1080/00207543.2021.1881648", [Q1-3] "10.1016/j.jmsy.2025.09.018", [Q1-4] "10.1007/s11356-023-27081-3", [Q1-5] "10.1080/00207543.2019.1659520"|
| Q2 | Scopus | 69 | [Q2-1]"10.1016/j.asoc.2021.107404",[Q2-2]"10.1016/j.ejor.2005.03.055", [Q2-3]"10.1016/j.ijpe.2023.108928", [Q2-4] "10.1007/s11081-021-09696-y", [Q2-5] "10.1016/j.cor.2020.105064"|
| Q3 | Scopus | 3466 | [Q3-1] "10.1016/j.compchemeng.2011.12.015", [Q3-2] "10.1007/s10111-007-0107-7", [Q3-3] "10.1142/S0219686719500240", [Q3-4] "10.1111/jfs.12315", [Q3-5] "10.12133/j.smartag.2020.2.4.202011-SA006"|
| Q4 | Scopus | 258 | [Q4-1] "10.1016/j.cie.2014.07.009", [Q4-2] "10.1016/j.cie.2018.06.014", [Q4-3] "10.1007/s10845-020-01598-7", [Q4-4] "10.1016/j.cie.2017.08.029", [Q4-5] "10.1007/s00500-018-3457-6"|
| Q5 | Scopus | 0 ||
### Paso 2: Descargar PDFs
- Descargar los PDFs de los papers seleccionados
- Guardarlos en: `data/papers_nuevos/`
- Nombrarlos como: `Autor_Año_TituloCorto.pdf`

### Paso 3: Extraer Metadatos
Para cada paper, necesito:
```
Título:
Autores:
Año:
Journal/Conferencia:
DOI:
Abstract (resumen breve):
¿Por qué es relevante para DLBP avícola?:
```

### Paso 4: Yo me encargo de...
- Generar las entradas BibTeX
- Integrar al archivo `referencias_dlbp.bib`
- Citar en el documento de formulación
- Validar con el script de consistencia

---

## 🛠️ Herramientas que puedo usar

1. **DOI → BibTeX automático:** Si me das el DOI, puedo generar la entrada BibTeX automáticamente.
2. **Validación de referencias:** Script PowerShell para verificar que todas las citas tienen entrada en .bib.
3. **Búsqueda web:** Puedo buscar información general, pero NO tengo acceso a bases de datos institucionales.

---

## ⚡ Flujo Rápido (Si tienes poco tiempo)

1. Ve a **Scopus** con tu cuenta UTP
2. Ejecuta Query 1 y Query 2
3. Filtra: Últimos 5 años, Artículos de revista
4. Selecciona los 5 más citados de cada query
5. Exporta como **BibTeX** (Scopus tiene esa opción)
6. Pégame el archivo BibTeX y yo lo integro

---

## 📤 ¿Cómo me pasas la info?

**Opción A (Rápida):** Exportar BibTeX desde Scopus → Pegar en chat
**Opción B (Detallada):** Lista de DOIs → Yo genero el BibTeX
**Opción C (Manual):** Tabla con Título/Autor/Año/DOI → Yo proceso

---

*Documento generado para agilizar la colaboración en la Fase 1*
