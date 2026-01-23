# Anexo F: Suite de Tests Unitarios

## F.1. Introducción

Este anexo documenta la suite de tests unitarios desarrollada para validar la correcta implementación de los algoritmos metaheurísticos y módulos auxiliares del proyecto DLBP Avícola.

## F.2. Resumen de Cobertura

| Módulo | Archivo de Test | Tests | Estado |
|--------|-----------------|-------|--------|
| **Algoritmos Base** | `test_algorithms.py` | 22 | ✅ Pasaron |
| **Modelos DLBP** | `test_models.py` | 13 | ✅ 7 pasaron, 6 skipped* |
| **Experimentos** | `test_experiments.py` | 15 | ✅ Pasaron |
| **TOTAL** | | **50** | **44 pasaron, 6 skipped** |

*Tests skipped requieren la biblioteca `pulp` para modelos MILP.

## F.3. Categorías de Tests

### F.3.1. Tests de Clases Base

| Test | Descripción | Resultado |
|------|-------------|-----------|
| `test_n_tareas` | Verifica conteo de tareas | ✅ |
| `test_tiempo_total` | Verifica suma de tiempos | ✅ |
| `test_precedencia_valida` | Valida orden correcto | ✅ |
| `test_precedencia_invalida` | Detecta violaciones | ✅ |

### F.3.2. Tests de Soluciones

| Test | Descripción | Resultado |
|------|-------------|-----------|
| `test_decodificacion` | Asigna tareas a estaciones | ✅ |
| `test_factibilidad` | Marca soluciones válidas | ✅ |
| `test_fitness_estaciones` | Calcula fitness correctamente | ✅ |
| `test_clonacion` | Crea copias independientes | ✅ |

### F.3.3. Tests de Algoritmos

| Algoritmo | Tests | Resultado |
|-----------|-------|-----------|
| Algoritmo Genético | 3 tests | ✅ |
| Búsqueda Tabú | 3 tests | ✅ |
| Algoritmo Híbrido | 2 tests | ✅ |
| Integración | 1 test | ✅ |

### F.3.4. Tests de Edge Cases

| Test | Escenario | Resultado |
|------|-----------|-----------|
| `test_instancia_una_tarea` | Solo 1 tarea | ✅ |
| `test_instancia_sin_precedencias` | Sin dependencias | ✅ |
| `test_tiempos_iguales` | Todas las tareas = mismo tiempo | ✅ |
| `test_tiempo_ciclo_muy_grande` | Todo cabe en 1 estación | ✅ |
| `test_tiempo_ciclo_muy_pequeno` | 1 tarea por estación | ✅ |

### F.3.5. Tests de Generador de Instancias

| Test | Descripción | Resultado |
|------|-------------|-----------|
| `test_genera_dict_para_todas_tareas` | Cobertura de tareas | ✅ |
| `test_primera_tarea_sin_predecesoras` | Tarea inicial válida | ✅ |
| `test_grafo_sin_ciclos` | DAG válido | ✅ |
| `test_tiempos_en_rango` | Tiempos dentro de límites | ✅ |
| `test_instancia_reproducible` | Misma semilla = mismo resultado | ✅ |
| `test_exportar_json_valido` | Exporta JSON correcto | ✅ |

## F.4. Comando de Ejecución

```bash
# Ejecutar todos los tests
python -m unittest discover -s tests -v

# Resultado esperado:
# Ran 50 tests in 0.430s
# OK (skipped=6)
```

## F.5. Configuración

**Archivo:** `pytest.ini`

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
filterwarnings = 
    ignore::DeprecationWarning
```

## F.6. Conclusiones

1. **Cobertura ampliada:** La suite pasó de 17 tests a 50 tests (+194%)
2. **Validación robusta:** Tests cubren casos normales, límites y errores
3. **Reproducibilidad:** Todas las pruebas son determinísticas con semillas fijas
4. **Documentación:** Cada test tiene docstring explicativo

---

*Suite de tests ejecutada: 22 de Enero de 2026*
