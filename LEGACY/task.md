# Lista de Tareas - Fase 1: Modelado Matemático (MILP)

## 🎯 Objetivo Inmediato
Implementar el script de validación `milp_validation.py` para resolver una instancia pequeña del DLBP avícola usando Python + PuLP/Gurobi.

## 📝 Actividades
- [ ] **Configuración de Entorno**
    - [ ] Crear estructura de directorios `src/models`, `data/processed`
    - [ ] Instalar dependencias (`pulp`, `pandas`, `matplotlib`)
- [ ] **Prototipado del Modelo**
    - [ ] Definir clases de datos (Data Classes) para `Task`, `Station`, `Coproduct`
    - [ ] Implementar carga de datos desde JSON/CSV
    - [ ] Traducir formulación matemática del Anexo A a código PuLP
- [ ] **Validación**
    - [ ] Crear instancia de juguete (10 tareas, 3 estaciones)
    - [ ] Ejecutar solver y validar precedencias
    - [ ] Visualizar diagrama de Gantt simple de la solución
- [ ] **Documentación**
    - [ ] Actualizar `FASE_1_MODELADO.md` con hallazgos del prototipo
