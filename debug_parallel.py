
import sys
import os
import pytest
sys.path.insert(0, os.path.abspath('src'))

from algorithms.base import Solution, cargar_instancia_demo
from algorithms.parallel import ParallelNeighborhoodGenerator

def test_debug():
    instancia = cargar_instancia_demo()
    orden = list(instancia.tareas)
    solucion = Solution(instancia=instancia, cromosoma=orden)
    
    gen = ParallelNeighborhoodGenerator(n_workers=2)
    print("Running generated_vecindario...")
    try:
        vecinos = gen.generar_vecindario(solucion, tamano=10, tipo_movimiento="swap")
        print(f"Success! Generated {len(vecinos)} neighbors.")
    except Exception as e:
        print("caught exception:")
        print(e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_debug()
