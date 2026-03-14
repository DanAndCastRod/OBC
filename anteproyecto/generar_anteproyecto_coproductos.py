import subprocess
import sys
import os
from pathlib import Path


def verificar_dependencias():
    """Verifica que Pandoc esté instalado"""
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Pandoc encontrado")
            return True
        else:
            print("✗ Pandoc no encontrado")
            return False
    except FileNotFoundError:
        print("✗ Pandoc no está instalado")
        return False


def verificar_archivos():
    """Verifica que los archivos necesarios existan"""
    archivos_requeridos = [
        'anteproyecto_coproductos.md',
        'referencias_coproductos.bib',
        'ieee.csl'
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if not Path(archivo).exists():
            archivos_faltantes.append(archivo)
    
    if archivos_faltantes:
        print(f"✗ Archivos faltantes: {', '.join(archivos_faltantes)}")
        return False
    else:
        print("✓ Todos los archivos requeridos están presentes")
        return True


def generar_pdf():
    """Genera el PDF del anteproyecto usando Pandoc"""
    
    comando = [
        'pandoc',
        'anteproyecto_coproductos.md',
        '--bibliography=referencias_coproductos.bib',
        '--csl=ieee.csl',
        '--citeproc',
        '--pdf-engine=xelatex',
        '--variable=geometry:margin=2.5cm',
        '--variable=fontsize=12pt',
        '--variable=documentclass=article',
        '--variable=lang=es',
        '--highlight-style=tango',
        '--include-in-header=header_mermaid.tex',
        '--output=anteproyecto_coproductos.pdf'
    ]
    
    # Add mermaid filter if available
    # On Windows, Pandoc can't execute .cmd files directly, so we create a .bat wrapper
    import shutil
    mermaid_path = shutil.which('mermaid-filter')
    if mermaid_path:
        if sys.platform == 'win32':
            wrapper = Path('_mermaid_wrapper.bat')
            bat_content = '@echo off\r\ncall "' + mermaid_path + '" %*\r\n'
            wrapper.write_text(bat_content)
            comando.insert(2, '--filter=' + str(wrapper.resolve()))
        else:
            comando.insert(2, '--filter=mermaid-filter')
        print("✓ mermaid-filter disponible (" + mermaid_path + ")")
        # Set mermaid filter width for smaller images
        os.environ['MERMAID_FILTER_WIDTH'] = '800'
    else:
        print("⚠ mermaid-filter no encontrado. Los diagramas se renderizarán como bloques de código.")
        print("  Instalar con: npm install -g mermaid-filter")
    
    print("\nGenerando PDF del anteproyecto...")
    print(f"Comando: {' '.join(comando)}")
    
    try:
        result = subprocess.run(comando, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ PDF generado exitosamente: anteproyecto_coproductos.pdf")
            return True
        else:
            print(f"✗ Error al generar PDF:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Error ejecutando Pandoc: {e}")
        return False


def generar_docx():
    """Genera el documento Word del anteproyecto"""
    
    comando = [
        'pandoc',
        'anteproyecto_coproductos.md',
        '--bibliography=referencias_coproductos.bib',
        '--csl=ieee.csl',
        '--citeproc',
        '--number-sections',
        '--output=anteproyecto_coproductos.docx'
    ]
    
    print("Generando documento Word...")
    
    try:
        result = subprocess.run(comando, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Documento Word generado: anteproyecto_coproductos.docx")
            return True
        else:
            print(f"✗ Error al generar Word: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Error ejecutando Pandoc: {e}")
        return False


def main():
    """Función principal"""
    print("=== Generador de Anteproyecto — Optimización de Coproductos ===\n")
    
    # Verificar dependencias
    if not verificar_dependencias():
        print("\nPor favor instala Pandoc desde: https://pandoc.org/installing.html")
        sys.exit(1)
    
    # Verificar archivos
    if not verificar_archivos():
        print("\nPor favor asegúrate de que todos los archivos requeridos estén presentes")
        sys.exit(1)
    
    print("\n=== Generando documentos ===\n")
    
    # Generar PDF
    pdf_exitoso = generar_pdf()
    
    # Opcionalmente generar Word
    if pdf_exitoso:
        print("\n¿Deseas generar también el documento Word? (s/n): ", end="")
        respuesta = input().lower().strip()
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            generar_docx()
    
    print("\n=== Proceso completado ===")
    
    if pdf_exitoso:
        print("✓ Anteproyecto generado exitosamente")
        print("📄 Archivo PDF: anteproyecto_coproductos.pdf")
        print("📚 Bibliografía: referencias_coproductos.bib")
        print("📊 Estilo de citas: ieee.csl")
    else:
        print("✗ Error en la generación del anteproyecto")
        sys.exit(1)


if __name__ == "__main__":
    main()
