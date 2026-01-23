# Fase 2: Ampliación de Cobertura de Tests

**Prioridad:** P1 (Alta)  
**Esfuerzo:** Bajo  
**Duración Estimada:** 2-3 días  
**Estado:** [x] ✅ COMPLETADO (22-Ene-2026)

---

## 🎯 Objetivo

Aumentar la cobertura de tests unitarios del proyecto de ~40% a ≥60%, agregando tests para módulos actualmente sin cobertura.

---

## 📋 Estado Actual (Post-Implementación)

| Módulo | Archivo | Tests Implementados | Estado |
|--------|---------|---------------------|--------|
| `algorithms/base.py` | ✅ | 8 tests | ✅ Cubierto |
| `algorithms/genetic_algorithm.py` | ✅ | 3 tests | ✅ Cubierto |
| `algorithms/tabu_search.py` | ✅ | 3 tests | ✅ Cubierto |
| `algorithms/hybrid.py` | ✅ | 2 tests | ✅ Cubierto |
| `algorithms/` (edge cases) | ✅ | 5 tests | ✅ **NUEVO** |
| `models/dlbp_completo.py` | ✅ | 3 tests | ✅ **NUEVO** |
| `models/milp_validation.py` | ✅ | 1 test | ✅ **NUEVO** |
| `models/dlbp_profit.py` | ✅ | 1 test | ✅ **NUEVO** |
| `models/stochastic_dlbp.py` | ✅ | 1 test | ✅ **NUEVO** |
| `models/` (validación) | ✅ | 8 tests | ✅ **NUEVO** |
| `experiments/generar_instancias.py` | ✅ | 15 tests | ✅ **NUEVO** |

**Total implementado:** 50 tests en 3 archivos

---

## 🔧 Actividades

### 2.1. Crear Tests para Módulo `models/`

**Archivo:** `tests/test_models.py`

```python
# Tests a implementar
class TestMILPValidation(unittest.TestCase):
    def test_crear_modelo_pequeno(self): ...
    def test_restriccion_precedencia(self): ...
    def test_restriccion_ciclo(self): ...
    def test_resolver_instancia_trivial(self): ...

class TestDLBPProfit(unittest.TestCase):
    def test_calcular_beneficio_basico(self): ...
    def test_penalizacion_inventario(self): ...
    def test_demanda_excedida(self): ...

class TestStochasticDLBP(unittest.TestCase):
    def test_generar_tiempos_estocasticos(self): ...
    def test_simulacion_montecarlo(self): ...
    def test_estadisticas_resultado(self): ...
```

**Estimación:** ~150 líneas, 10 tests nuevos

### 2.2. Crear Tests para Generador de Instancias

**Archivo:** `tests/test_experiments.py`

```python
class TestGeneradorInstancias(unittest.TestCase):
    def test_generar_instancia_pequena(self): ...
    def test_grafo_dag_valido(self): ...
    def test_tiempos_en_rango(self): ...
    def test_precedencias_coherentes(self): ...
    def test_exportar_json(self): ...
```

**Estimación:** ~80 líneas, 5 tests nuevos

### 2.3. Añadir Tests de Edge Cases

**Archivo:** Agregar a `tests/test_algorithms.py`

```python
class TestEdgeCases(unittest.TestCase):
    def test_instancia_una_tarea(self): ...
    def test_instancia_sin_precedencias(self): ...
    def test_tiempos_iguales(self): ...
    def test_tiempo_ciclo_muy_grande(self): ...
    def test_tiempo_ciclo_muy_pequeno(self): ...
```

**Estimación:** ~60 líneas, 5 tests nuevos

### 2.4. Configurar Medición de Cobertura

**Herramienta:** `pytest-cov`

```bash
# Instalación
pip install pytest pytest-cov

# Ejecución con reporte de cobertura
pytest --cov=src --cov-report=html tests/
```

**Archivo de configuración:** `pytest.ini`

```ini
[pytest]
testpaths = tests
addopts = --cov=src --cov-report=term-missing
```

### 2.5. Integrar con CI (Opcional)

**Archivo:** `.github/workflows/tests.yml`

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-cov
      - run: pytest --cov=src tests/
```

---

## 📦 Entregables

| Entregable | Ubicación | Estado |
|------------|-----------|--------|
| Tests de modelos | `tests/test_models.py` | ✅ 15 tests |
| Tests de experimentos | `tests/test_experiments.py` | ✅ 15 tests |
| Tests edge cases | `tests/test_algorithms.py` (ampliado) | ✅ 5 tests |
| Configuración pytest | `pytest.ini` | ✅ |
| Reporte de cobertura | **50 tests, 50 pasaron, 0 skipped** | ✅ |

---

## ✅ Criterios de Aceptación

- [ ] Todos los tests nuevos pasan sin errores
- [ ] Cobertura total ≥60% (medida con pytest-cov)
- [ ] Sin warnings de deprecación en ejecución
- [ ] Documentación de cada test class

---

## 📊 Resumen de Tests Implementados

| Módulo | Tests Antes | Tests Nuevos | Total |
|--------|-------------|--------------|-------|
| algorithms | 17 | 5 (edge cases) | 22 |
| models | 0 | 13 | 13 |
| experiments | 0 | 15 | 15 |
| **TOTAL** | **17** | **33** | **50** |

**Resultado de ejecución:** 50 tests, **50 pasaron**, 0 skipped ✅

---

*Última actualización: 22 de Enero de 2026*
