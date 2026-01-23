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
        'anteproyecto_dlbp_coproductos.md',
        'referencias_dlbp.bib',
        'apa.csl'
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
    
    # Comando de Pandoc
    comando = [
        'pandoc',
        'anteproyecto_dlbp_coproductos.md',
        '--bibliography=referencias_dlbp.bib',
        '--csl=apa.csl',
        '--citeproc',
        '--pdf-engine=xelatex',
        '--variable=geometry:margin=2.5cm',
        '--variable=fontsize=12pt',
        '--variable=documentclass=article',
        '--variable=lang=es',
        # '--toc',
        # '--toc-depth=3',
        # '--number-sections',
        '--highlight-style=tango',
        '--output=anteproyecto.pdf'
    ]
    
    print("Generando PDF del anteproyecto...")
    print(f"Comando: {' '.join(comando)}")
    
    try:
        result = subprocess.run(comando, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ PDF generado exitosamente: anteproyecto.pdf")
            return True
        else:
            print(f"✗ Error al generar PDF:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Error ejecutando Pandoc: {e}")
        return False

# def generar_docx():
#     """Genera el documento Word del anteproyecto"""
    
#     comando = [
#         'pandoc',
#         'anteproyecto_dlbp_coproductos.md',
#         '--bibliography=referencias_dlbp.bib',
#         '--csl=apa.csl',
#         '--citeproc',
#         '--reference-doc=template.docx',
#         # '--toc',
#         # '--toc-depth=3',
#         '--number-sections',
#         '--output=anteproyecto_dlbp_coproductos.docx'
#     ]
    
#     print("Generando documento Word...")
    
#     try:
#         result = subprocess.run(comando, capture_output=True, text=True)
        
#         if result.returncode == 0:
#             print("✓ Documento Word generado: anteproyecto_dlbp_coproductos.docx")
#             return True
#         else:
#             print(f"✗ Error al generar Word: {result.stderr}")
#             return False
            
#     except Exception as e:
#         print(f"✗ Error ejecutando Pandoc: {e}")
#         return False

def generar_descripcion_problema():
    """Genera el documento de descripción del problema"""
    comando = [
        'pandoc',
        'descripcion_problema.md',
        '--bibliography=referencias_dlbp.bib',
        '--csl=apa.csl',
        '--citeproc',
        '--pdf-engine=xelatex',
        '--variable=geometry:margin=2.5cm',
        '--variable=fontsize=12pt',
        '--variable=documentclass=article',
        '--variable=lang=es',
        '--number-sections',
        '--highlight-style=tango',
        '--output=descripcion_problema.pdf'
    ]
    print("Generando PDF de descripción del problema...")
    print(f"Comando: {' '.join(comando)}")
    try:
        result = subprocess.run(comando, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ PDF de descripción del problema generado exitosamente: descripcion_problema.pdf")
            return True
        else:
            print(f"✗ Error al generar PDF de descripción del problema: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error ejecutando Pandoc: {e}")
        return False

def main():
    """Función principal"""
    print("=== Generador de Anteproyecto DLBP ===\n")
    
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
    # pdf_exitoso = generar_descripcion_problema()
    # Generar Word (opcional)
    if pdf_exitoso:
        print("\n¿Deseas generar también el documento de descripción del problema? (s/n): ", end="")
        respuesta = input().lower().strip()
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            generar_descripcion_problema()
    
    print("\n=== Proceso completado ===")
    
    if pdf_exitoso:
        print("✓ Anteproyecto generado exitosamente")
        print("📄 Archivo PDF: anteproyecto_dlbp_coproductos.pdf")
        print("📄 Archivo PDF: descripcion_problema.pdf")
        print("📚 Bibliografía: referencias_dlbp.bib")
        print("⚙️  Configuración: config_anteproyecto.yaml")
    else:
        print("✗ Error en la generación del anteproyecto")
        sys.exit(1)

if __name__ == "__main__":
    main()
