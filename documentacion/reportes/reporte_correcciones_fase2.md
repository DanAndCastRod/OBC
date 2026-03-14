# Reporte de Fase 2: Correcciones al Modelo Matemático
**Fecha:** 2026-02-26  
**Sprint:** 2.1 + 2.2  
**Documento modificado:** `anteproyecto_coproductos.md`

---

## 1. Resumen Ejecutivo

Se aplicaron **8 correcciones** al anteproyecto basadas en los hallazgos de la Fase 1 (búsqueda bibliográfica). Las correcciones abarcan: eliminación de elementos sin sustento (canales de venta), fortalecimiento de la justificación NP-hard con citas formales, ampliación del marco de metaheurísticas, y adición de la restricción de perecibilidad al modelo.

---

## 2. Decisiones Tomadas

| # | Decisión | Resultado | Referencia |
|:-:|----------|-----------|------------|
| 1 | Restricción de vida útil ($L_p$) | **Opción A: Restricción dura** — $I_{pt\omega} = 0$ si supera $L_p$ | Claassen 2016 |
| 2 | Canales de venta | **Eliminados** — sin sustento en la literatura | Q2/Q4 sin resultados |
| 3 | Setup + lote mínimo | **Formulación validada** como estándar | Mahdieh 2018, Goren 2016 |
| 4 | Metaheurísticas | **4 seleccionadas:** GA, SA, DE, GA-SA | Akbari-Aghghaleh 2025 |

---

## 3. Correcciones Aplicadas al Anteproyecto

| # | Línea(s) | Cambio | Tipo |
|:-:|:--------:|--------|:----:|
| 1 | L143 | Eliminado "canal de venta" | 🗑️ |
| 2 | L146 | NP-hard con citas: Florian 1980, Bitran & Yanasse 1982, Goren 2016, Rahmani 2025, Mahdieh 2018 | 📚 |
| 3 | L150 | Meta ampliadas: GA+SA+DE+GA-SA (antes GA+TS) | 🧬 |
| 4 | L461 | "canales de venta" → "decisiones de activación de línea" | 🗑️ |
| 5 | L475-479 | TS+GA-TS → SA+DE+GA-SA con citas | 🧬 |
| 6 | L497 | "canales de venta" → "escenarios estocásticos" + "vidas útiles" | 🗑️ |
| 7 | L607 | Intro Anexo A con cadena de citas NP-hard | 📚 |
| 8 | L671+ | **Nueva Eq. 7:** Restricción perecibilidad $L_p$ | ➕ |

---

## 4. Metaheurísticas: Selección Final

### Confirmadas (4 algoritmos)

| Algoritmo | Paradigma | Justificación |
|-----------|-----------|---------------|
| **GA** | Evolutivo poblacional | Más citado en lot-sizing. Exploración global | 
| **SA** | Trayectoria | Metropolis para escapar óptimos locales |
| **DE** | Evolutivo diferencial | Dinámica distinta al GA; efectivo en mixtos |
| **GA-SA** | Híbrido memético | Mejor rendimiento en benchmark avícola |

### Excluidos

| Algoritmo | Razón |
|-----------|-------|
| TS | SA cubre el paradigma trayectoria con mejor sustento avícola |
| DE-SA | Excede alcance de maestría → **propuesto como trabajo futuro** |

### Criterios de selección
1. **Diversidad de paradigmas:** 2 evolutivos + 1 trayectoria + 1 híbrido
2. **Sustento bibliográfico:** ≥1 referencia por algoritmo en lot-sizing/avicultura
3. **Replicabilidad:** Alineado con Akbari-Aghghaleh 2025

---

## 5. Estado del Modelo Post-Correcciones

### Inventario del Anexo A

| Componente | Cantidad | Detalle |
|------------|:--------:|---------|
| Conjuntos | 3 | $P, T, \Omega$ |
| Parámetros | 11 | $\alpha_p, W, d_{pt\omega}, r_p, c^{prod}, F, c^{inv}_p, c^{pen}_p, Q^{max}, Q^{min}, L_p, \pi_\omega$ |
| Variables | 5 | $y_t, q_t, v_{pt\omega}, I_{pt\omega}, u_{pt\omega}$ |
| Ecuaciones | 7 | FO + Balance + Demanda + Cap. Máx. + Lote Mín. + Ventas + **Perecibilidad** |

### Verificación de consistencia

- ✅ Todo parámetro definido se usa en ≥1 ecuación (incluyendo $L_p$)
- ✅ Toda variable aparece en FO o ≥1 restricción
- ✅ No hay símbolos "fantasma"
- ✅ 0 menciones a "canales de venta"
- ✅ Metaheurísticas consistentes entre sección 6.2 Fase 2 y resumen (GA, SA, DE, GA-SA)

---

## 6. Trabajo Futuro Sugerido

Para incluir en la sección "¿Qué sigue después de esta investigación?" del anteproyecto:

- **Híbrido DE-SA:** Evaluar Differential Evolution con Simulated Annealing como búsqueda local (Akbari-Aghghaleh 2025 lo evaluó positivamente)
- **Tabu Search (TS):** Comparar con SA como algoritmo de trayectoria alternativo
- **Multi-objetivo:** Extender a optimización bi-objetivo (costo vs. nivel de servicio)
- **Datos reales:** Validar con datos de planta de beneficio avícola colombiana real

---

## 7. Próximos Pasos → Fase 3

1. Ampliar el Estado del Arte con los papers encontrados (estadísticas de búsqueda, Tabla 3 actualizada)
2. Agregar sección "Trabajo Futuro" con DE-SA
3. Agregar entradas BibTeX de los nuevos papers a `referencias_coproductos.bib`
4. Verificar compilación del documento completo
