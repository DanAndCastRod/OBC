"""
Generador de Tesis — Optimización de Coproductos con Metaheurísticas
Pipeline: Markdown → PDF (Pandoc + XeLaTeX + citeproc + mermaid-filter)

Basado en: anteproyecto/generar_anteproyecto_coproductos.py
"""

import subprocess
import sys
import os
from pathlib import Path


THESIS_MD = "tesis_coproductos.md"
THESIS_PDF = "tesis_coproductos.pdf"
THESIS_DOCX = "tesis_coproductos.docx"
BIB_FILE = "referencias_coproductos.bib"
CSL_FILE = "ieee.csl"
HEADER_TEX = "header_mermaid.tex"


def verificar_dependencias():
    """Verifica que Pandoc y XeLaTeX estén instalados."""
    ok = True

    # Pandoc
    try:
        result = subprocess.run(
            ["pandoc", "--version"], capture_output=True, text=True, encoding="utf-8"
        )
        if result.returncode == 0:
            version = result.stdout.split("\n")[0]
            print(f"  ✓ {version}")
        else:
            print("  ✗ Pandoc no encontrado")
            ok = False
    except FileNotFoundError:
        print("  ✗ Pandoc no está instalado")
        print("    → https://pandoc.org/installing.html")
        ok = False

    # XeLaTeX
    try:
        result = subprocess.run(
            ["xelatex", "--version"], capture_output=True, text=True, encoding="utf-8"
        )
        if result.returncode == 0:
            version = result.stdout.split("\n")[0]
            print(f"  ✓ {version}")
        else:
            print("  ✗ XeLaTeX no encontrado")
            ok = False
    except FileNotFoundError:
        print("  ✗ XeLaTeX no está instalado")
        print("    → https://miktex.org/download")
        ok = False

    return ok


def verificar_archivos():
    """Verifica que los archivos necesarios existan."""
    archivos_requeridos = [THESIS_MD, BIB_FILE, CSL_FILE, HEADER_TEX]

    archivos_faltantes = [a for a in archivos_requeridos if not Path(a).exists()]

    if archivos_faltantes:
        print(f"  ✗ Archivos faltantes: {', '.join(archivos_faltantes)}")
        return False

    print("  ✓ Todos los archivos requeridos están presentes")

    # Contar referencias en .bib
    bib_content = Path(BIB_FILE).read_text(encoding="utf-8")
    import re
    n_refs = len(re.findall(r"^@\w+{", bib_content, re.MULTILINE))
    print(f"  ✓ {n_refs} entradas en {BIB_FILE}")

    # Contar figuras
    n_figs = len(list(Path("figuras").glob("*.png")))
    print(f"  ✓ {n_figs} figuras PNG en figuras/")

    return True


def generar_pdf():
    """Genera el PDF de la tesis usando Pandoc + XeLaTeX."""

    comando = [
        "pandoc",
        THESIS_MD,
        f"--bibliography={BIB_FILE}",
        f"--csl={CSL_FILE}",
        "--citeproc",
        "--pdf-engine=xelatex",
        "--variable=geometry:margin=2.5cm",
        "--variable=fontsize=12pt",
        "--variable=documentclass=article",
        "--variable=lang=es",
        "--highlight-style=tango",
        f"--include-in-header={HEADER_TEX}",
        f"--output=tesis_coproductos.tex",
    ]

    # Mermaid filter (optional)
    import shutil
    import re

    mermaid_path = shutil.which("mermaid-filter")
    if mermaid_path:
        if sys.platform == "win32":
            wrapper = Path("_mermaid_wrapper.bat")
            bat_content = '@echo off\r\ncall "' + mermaid_path + '" %*\r\n'
            wrapper.write_text(bat_content)
            comando.insert(2, "--filter=" + str(wrapper.resolve()))
        else:
            comando.insert(2, "--filter=mermaid-filter")
        print(f"  ✓ mermaid-filter disponible ({mermaid_path})")
        os.environ["MERMAID_FILTER_WIDTH"] = "800"
    else:
        print(
            "  ⚠ mermaid-filter no encontrado — los diagramas se renderizarán como código"
        )
        print("    → npm install -g mermaid-filter")

    print(f"\n  Generando código LaTeX...")
    print(f"  Comando: {' '.join(comando)}")

    try:
        result = subprocess.run(comando, capture_output=True, text=True, encoding="utf-8")

        if result.returncode == 0:
            print("  ✓ LaTeX generado. Ajustando captions cortos...")
            tex_file = "tesis_coproductos.tex"
            with open(tex_file, "r", encoding="utf-8") as f:
                tex_content = f.read()
            
            # Buscar y reemplazar captions
            # Busca \caption{@@SHORT@@(corto)@@ENDSHORT@@ (largo)} y lo vuelve \caption[corto]{largo}
            tex_content = re.sub(
                r"\\caption(?:\[.*?\])?\{@@SHORT@@(.*?)@@ENDSHORT@@\s*(.*?)\}",
                r"\\caption[\1]{\2}",
                tex_content,
                flags=re.DOTALL
            )
            with open(tex_file, "w", encoding="utf-8") as f:
                f.write(tex_content)
                
            print("  Compilando a PDF con XeLaTeX (paso 1/2)...")
            subprocess.run(["xelatex", "-interaction=nonstopmode", tex_file], capture_output=True)
            print("  Compilando a PDF con XeLaTeX (paso 2/2)...")
            result_pdf = subprocess.run(["xelatex", "-interaction=nonstopmode", tex_file], capture_output=True)
            
            if result_pdf.returncode == 0:
                size_kb = Path(THESIS_PDF).stat().st_size / 1024
                print(f"  ✓ PDF generado: {THESIS_PDF} ({size_kb:.0f} KB)")
                return True
            else:
                print("  ✗ Error al generar PDF con XeLaTeX.")
                return False
        else:
            print(f"  ✗ Error al procesar Pandoc:")
            if result.stdout:
                print(f"  STDOUT: {result.stdout[:500]}")
            if result.stderr:
                print(f"  STDERR: {result.stderr[:1000]}")
            return False

    except Exception as e:
        print(f"  ✗ Error ejecutando Pandoc/XeLaTeX: {e}")
        return False


def generar_docx():
    """Genera el documento Word de la tesis."""

    import re
    # Limpiar los marcadores cortos para docx
    tmp_md = "tesis_coproductos_temp.md"
    with open(THESIS_MD, "r", encoding="utf-8") as f:
        md_content = f.read()
    md_content = re.sub(r"@@SHORT@@.*?@@ENDSHORT@@\s*", "", md_content)
    with open(tmp_md, "w", encoding="utf-8") as f:
        f.write(md_content)

    comando = [
        "pandoc",
        tmp_md,
        f"--bibliography={BIB_FILE}",
        f"--csl={CSL_FILE}",
        "--citeproc",
        f"--output={THESIS_DOCX}",
    ]

    print("  Generando documento Word...")

    try:
        result = subprocess.run(comando, capture_output=True, text=True, encoding="utf-8")

        if result.returncode == 0:
            size_kb = Path(THESIS_DOCX).stat().st_size / 1024
            print(f"  ✓ Word generado: {THESIS_DOCX} ({size_kb:.0f} KB)")
            return True
        else:
            print(f"  ✗ Error al generar Word: {result.stderr[:500]}")
            return False

    except Exception as e:
        print(f"  ✗ Error ejecutando Pandoc: {e}")
        return False


def main():
    """Función principal."""
    print("=" * 60)
    print("  Generador de Tesis — Coproductos con Metaheurísticas")
    print("=" * 60)

    # 1. Verificar dependencias
    print("\n[1/3] Verificando dependencias...")
    if not verificar_dependencias():
        print("\n✗ Dependencias faltantes. Instálalas antes de continuar.")
        sys.exit(1)

    # 2. Verificar archivos
    print("\n[2/3] Verificando archivos...")
    if not verificar_archivos():
        print("\n✗ Archivos faltantes. Verifica la estructura del directorio.")
        sys.exit(1)

    # 3. Generar PDF
    print("\n[3/3] Generando documentos...")
    pdf_ok = generar_pdf()

    # Opcionalmente generar Word
    if pdf_ok:
        print("\n¿Generar también Word? (s/n): ", end="")
        try:
            respuesta = input().lower().strip()
            if respuesta in ["s", "si", "sí", "y", "yes"]:
                generar_docx()
        except EOFError:
            pass

    print("\n" + "=" * 60)
    if pdf_ok:
        print("  ✓ Tesis generada exitosamente")
        print(f"  📄 PDF:          {THESIS_PDF}")
        print(f"  📚 Bibliografía: {BIB_FILE}")
        print(f"  📊 Figuras:      figuras/")
    else:
        print("  ✗ Error en la generación")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()
