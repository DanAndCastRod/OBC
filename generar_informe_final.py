"""
DLBP Avicola - Generador de Informe Final PDF
==============================================
Genera el PDF del informe de investigacion usando Pandoc
con soporte para graficos y bibliografia.

Autor: Daniel Castaneda
Fecha: Enero 2026
"""

import subprocess
import sys
import os
from pathlib import Path
import shutil


def verificar_dependencias():
    """Verifica que las dependencias esten instaladas."""
    dependencias = {
        'pandoc': 'https://pandoc.org/installing.html',
        'xelatex': 'https://miktex.org/download (MiKTeX) o TeX Live'
    }
    
    todas_ok = True
    
    # Verificar Pandoc
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"   [OK] Pandoc: {version}")
        else:
            print("   [ERROR] Pandoc no funciona correctamente")
            todas_ok = False
    except FileNotFoundError:
        print(f"   [ERROR] Pandoc no encontrado. Instalar desde: {dependencias['pandoc']}")
        todas_ok = False
    
    # Verificar XeLaTeX
    try:
        result = subprocess.run(['xelatex', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   [OK] XeLaTeX encontrado")
        else:
            print("   [ERROR] XeLaTeX no funciona")
            todas_ok = False
    except FileNotFoundError:
        print(f"   [ERROR] XeLaTeX no encontrado. Instalar: {dependencias['xelatex']}")
        todas_ok = False
    
    return todas_ok


def verificar_archivos():
    """Verifica que los archivos necesarios existan."""
    base_dir = Path(__file__).parent
    
    archivos_requeridos = [
        base_dir / 'docs' / 'tesis' / 'INFORME_FINAL_COMPLETO.md',
        base_dir / 'referencias_dlbp.bib',
    ]
    
    archivos_opcionales = [
        base_dir / 'ieee.csl',
        base_dir / 'apa.csl',
        base_dir / 'logo_utp.png',
    ]
    
    # Requeridos
    faltantes = []
    for archivo in archivos_requeridos:
        if archivo.exists():
            print(f"   [OK] {archivo.name}")
        else:
            faltantes.append(archivo.name)
            print(f"   [ERROR] {archivo.name} (REQUERIDO)")
    
    # Opcionales
    for archivo in archivos_opcionales:
        if archivo.exists():
            print(f"   [OK] {archivo.name}")
        else:
            print(f"   [WARN] {archivo.name} (opcional)")
    
    # Verificar figuras
    figuras_dir = base_dir / 'docs' / 'tesis' / 'figuras'
    if figuras_dir.exists():
        n_figuras = len(list(figuras_dir.glob('*.png')))
        print(f"   [OK] {n_figuras} figuras PNG en docs/tesis/figuras/")
    else:
        print("   [WARN] Directorio figuras/ no encontrado")
    
    return len(faltantes) == 0


def generar_pdf():
    """Genera el PDF del informe final usando Pandoc."""
    base_dir = Path(__file__).parent
    
    # Determinar CSL disponible
    csl_file = 'ieee.csl' if (base_dir / 'ieee.csl').exists() else 'apa.csl'
    
    # Archivo de entrada y salida
    input_file = base_dir / 'docs' / 'tesis' / 'INFORME_FINAL_COMPLETO.md'
    output_file = base_dir / 'INFORME_FINAL_INVESTIGACION.pdf'
    
    # Comando Pandoc
    comando = [
        'pandoc',
        str(input_file),
        f'--bibliography={base_dir / "referencias_dlbp.bib"}',
        f'--csl={base_dir / csl_file}',
        '--citeproc',
        '--pdf-engine=xelatex',
        '--variable=geometry:margin=2.5cm',
        '--variable=fontsize=12pt',
        '--variable=documentclass=article',
        '--variable=lang=es',
        '--toc',
        '--toc-depth=3',
        '--highlight-style=tango',
        f'--resource-path={base_dir};{base_dir / "docs" / "tesis"};{base_dir / "docs" / "tesis" / "figuras"}',
        f'--output={output_file}'
    ]
    
    print(f"\n[PDF] Generando PDF del informe...")
    print(f"   Entrada: {input_file.name}")
    print(f"   Salida:  {output_file.name}")
    print(f"   CSL:     {csl_file}")
    
    try:
        result = subprocess.run(comando, capture_output=True, text=True, 
                              cwd=base_dir / 'docs' / 'tesis', encoding='utf-8', errors='replace')
        
        if result.returncode == 0:
            print(f"\n   [OK] PDF generado exitosamente: {output_file.name}")
            return True
        else:
            print(f"\n   [ERROR] Error al generar PDF:")
            if result.stderr:
                # Mostrar solo las ultimas lineas del error
                error_lines = result.stderr.strip().split('\n')
                for line in error_lines[-10:]:
                    print(f"      {line}")
            return False
            
    except Exception as e:
        print(f"\n   [ERROR] Error ejecutando Pandoc: {e}")
        return False


def generar_docx():
    """Genera el documento Word del informe."""
    base_dir = Path(__file__).parent
    
    csl_file = 'ieee.csl' if (base_dir / 'ieee.csl').exists() else 'apa.csl'
    input_file = base_dir / 'docs' / 'tesis' / 'INFORME_FINAL_COMPLETO.md'
    output_file = base_dir / 'INFORME_FINAL_INVESTIGACION.docx'
    
    comando = [
        'pandoc',
        str(input_file),
        f'--bibliography={base_dir / "referencias_dlbp.bib"}',
        f'--csl={base_dir / csl_file}',
        '--citeproc',
        '--toc',
        '--toc-depth=3',
        f'--resource-path={base_dir};{base_dir / "docs" / "tesis"};{base_dir / "docs" / "tesis" / "figuras"}',
        f'--output={output_file}'
    ]
    
    print(f"\n[DOCX] Generando documento Word...")
    
    try:
        result = subprocess.run(comando, capture_output=True, text=True, 
                              cwd=base_dir / 'docs' / 'tesis', encoding='utf-8', errors='replace')
        
        if result.returncode == 0:
            print(f"   [OK] Word generado: {output_file.name}")
            return True
        else:
            print(f"   [ERROR] Error: {result.stderr[-200:] if result.stderr else 'Unknown'}")
            return False
            
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False


def main():
    """Funcion principal."""
    print("=" * 60)
    print("GENERADOR DE INFORME FINAL - DLBP AVICOLA")
    print("   Universidad Tecnologica de Pereira")
    print("   Maestria en Investigacion de Operaciones")
    print("=" * 60)
    
    # Verificar dependencias
    print("\n[CHECK] Verificando dependencias...")
    if not verificar_dependencias():
        print("\n[ERROR] Faltan dependencias. Por favor instalalas antes de continuar.")
        sys.exit(1)
    
    # Verificar archivos
    print("\n[CHECK] Verificando archivos...")
    if not verificar_archivos():
        print("\n[ERROR] Faltan archivos requeridos.")
        sys.exit(1)
    
    # Generar PDF
    print("\n" + "=" * 60)
    pdf_ok = generar_pdf()
    
    # Preguntar por Word
    if pdf_ok:
        print("\nDeseas generar tambien el documento Word? (s/n): ", end="")
        try:
            respuesta = input().lower().strip()
            if respuesta in ['s', 'si', 'y', 'yes']:
                generar_docx()
        except EOFError:
            pass
    
    # Resumen
    print("\n" + "=" * 60)
    print("[RESUMEN]")
    print("=" * 60)
    
    if pdf_ok:
        print("   [OK] Informe PDF generado exitosamente")
        print("\n   Archivos generados:")
        print("      * INFORME_FINAL_INVESTIGACION.pdf")
        print("      * docs/tesis/figuras/*.png (graficos)")
    else:
        print("   [ERROR] Error en la generacion del informe")
        sys.exit(1)
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
