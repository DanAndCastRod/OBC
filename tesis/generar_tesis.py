"""
Generador de Tesis — Optimización de Coproductos con Metaheurísticas
Pipeline: Markdown → PDF (Pandoc + pandoc-crossref + XeLaTeX + citeproc)

Notas de diseño:
- Los diagramas Mermaid están pre-renderizados como PNG en figuras/
  (fuentes .mmd en figuras/mermaid_src/). Para regenerarlos:
      mmdc -i figuras/mermaid_src/fig_N.mmd -o figuras/mermaid_fig_N.png \
           -w 1600 -b white --scale 2
  (mmdc: npm install -g @mermaid-js/mermaid-cli)
- Los captions cortos usan el atributo short-caption="..." en el markdown;
  el filtro short-captions.lua los convierte al ShortCaption nativo del AST
  (\caption[corto]{largo} en LaTeX). No hay post-procesamiento del .tex.
- pandoc-crossref numera figuras/tablas y resuelve referencias [@fig:]/[@tbl:].
  Debe ir ANTES de --citeproc en la línea de comandos.

Uso:
    python generar_tesis.py [--docx]
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

THESIS_MD = "tesis_coproductos.md"
THESIS_TEX = "tesis_coproductos.tex"
THESIS_PDF = "tesis_coproductos.pdf"
THESIS_DOCX = "tesis_coproductos.docx"
BIB_FILE = "referencias_coproductos.bib"
CSL_FILE = "ieee.csl"
HEADER_TEX = "header_mermaid.tex"
LUA_FILTER = "short-captions.lua"

XELATEX_PASSES = 3  # TOC/LOF/LOT + referencias cruzadas necesitan 3 pasadas


def _run(cmd, **kwargs):
    return subprocess.run(cmd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kwargs)


def verificar_dependencias():
    """Verifica que Pandoc, pandoc-crossref y XeLaTeX estén instalados."""
    ok = True
    for exe, url in [
        ("pandoc", "https://pandoc.org/installing.html"),
        ("pandoc-crossref", "https://github.com/lierdakil/pandoc-crossref/releases (usar la versión compilada para tu Pandoc)"),
        ("xelatex", "https://miktex.org/download"),
    ]:
        path = shutil.which(exe)
        if path:
            result = _run([exe, "--version"])
            version = result.stdout.split("\n")[0] if result.returncode == 0 else path
            print(f"  ✓ {version}")
        else:
            print(f"  ✗ {exe} no está instalado → {url}")
            ok = False
    return ok


def verificar_archivos():
    """Verifica que los archivos necesarios existan."""
    requeridos = [THESIS_MD, BIB_FILE, CSL_FILE, HEADER_TEX, LUA_FILTER]
    faltantes = [a for a in requeridos if not Path(a).exists()]
    if faltantes:
        print(f"  ✗ Archivos faltantes: {', '.join(faltantes)}")
        return False
    print("  ✓ Todos los archivos requeridos están presentes")

    bib_content = Path(BIB_FILE).read_text(encoding="utf-8")
    n_refs = len(re.findall(r"^@\w+{", bib_content, re.MULTILINE))
    print(f"  ✓ {n_refs} entradas en {BIB_FILE}")

    n_figs = len(list(Path("figuras").glob("*.png")))
    print(f"  ✓ {n_figs} figuras PNG en figuras/")

    # Los marcadores del mecanismo antiguo no deben reaparecer: citeproc los
    # interpreta como citas (@SHORT) y corrompe todos los captions del PDF.
    md = Path(THESIS_MD).read_text(encoding="utf-8")
    if "@@SHORT@@" in md:
        print("  ✗ El markdown contiene marcadores @@SHORT@@ (mecanismo obsoleto);")
        print("    usar el atributo short-caption=\"...\" en su lugar.")
        return False
    if "```mermaid" in md:
        print("  ✗ El markdown contiene bloques mermaid sin renderizar;")
        print("    pre-renderizarlos a PNG (ver encabezado de este script).")
        return False
    return True


def _comando_pandoc(salida):
    return [
        "pandoc",
        THESIS_MD,
        "--filter=pandoc-crossref",
        f"--lua-filter={LUA_FILTER}",
        "--citeproc",
        f"--bibliography={BIB_FILE}",
        f"--csl={CSL_FILE}",
        "--variable=geometry:margin=2.5cm",
        "--variable=fontsize=12pt",
        "--variable=documentclass=article",
        "--variable=lang=es",
        "--highlight-style=tango",
        f"--include-in-header={HEADER_TEX}",
        f"--output={salida}",
    ]


def _revisar_log():
    """Analiza el log de XeLaTeX en busca de problemas silenciosos."""
    log_file = Path(THESIS_PDF).with_suffix(".log")
    if not log_file.exists():
        return
    log = log_file.read_text(encoding="utf-8", errors="replace")

    problemas = []
    missing = sorted(set(re.findall(r"Missing character: There is no (\S+)", log)))
    if missing:
        problemas.append(f"caracteres sin glifo (se pierden en el PDF): {' '.join(missing[:10])}")
    if re.search(r"Rerun to get", log):
        problemas.append("referencias aún inestables (aumentar XELATEX_PASSES)")
    undef = re.findall(r"Reference `([^']+)' on page \d+ undefined", log)
    if undef:
        problemas.append(f"referencias indefinidas: {', '.join(sorted(set(undef))[:10])}")
    n_overfull = len(re.findall(r"Overfull \\hbox \((\d+(?:\.\d+)?)pt", log))
    if n_overfull:
        problemas.append(f"{n_overfull} overfull hbox (revisar tablas anchas)")

    if problemas:
        print("  ⚠ Advertencias del log de XeLaTeX:")
        for p in problemas:
            print(f"    - {p}")
    else:
        print("  ✓ Log de XeLaTeX sin problemas detectables")


def generar_pdf():
    """Genera el PDF de la tesis: Pandoc → .tex → XeLaTeX (3 pasadas)."""
    print("\n  Generando código LaTeX (pandoc-crossref + citeproc)...")
    result = _run(_comando_pandoc(THESIS_TEX))
    if result.returncode != 0:
        print("  ✗ Error de Pandoc:")
        print(f"  STDERR: {result.stderr[:1000]}")
        return False

    for i in range(1, XELATEX_PASSES + 1):
        print(f"  Compilando con XeLaTeX (pasada {i}/{XELATEX_PASSES})...")
        result_pdf = _run(["xelatex", "-interaction=nonstopmode", THESIS_TEX])

    if result_pdf.returncode != 0 or not Path(THESIS_PDF).exists():
        print("  ✗ Error al generar PDF con XeLaTeX (ver "
              f"{Path(THESIS_PDF).with_suffix('.log')}).")
        return False

    _revisar_log()
    size_kb = Path(THESIS_PDF).stat().st_size / 1024
    print(f"  ✓ PDF generado: {THESIS_PDF} ({size_kb:.0f} KB)")
    return True


def generar_docx():
    """Genera el documento Word de la tesis (mismos filtros que el PDF)."""
    print("  Generando documento Word...")
    result = _run(_comando_pandoc(THESIS_DOCX))
    if result.returncode != 0:
        print(f"  ✗ Error al generar Word: {result.stderr[:500]}")
        return False
    size_kb = Path(THESIS_DOCX).stat().st_size / 1024
    print(f"  ✓ Word generado: {THESIS_DOCX} ({size_kb:.0f} KB)")
    return True


def main():
    parser = argparse.ArgumentParser(description="Genera el PDF (y opcionalmente DOCX) de la tesis")
    parser.add_argument("--docx", action="store_true", help="generar también el .docx")
    args = parser.parse_args()

    os.chdir(SCRIPT_DIR)

    print("=" * 60)
    print("  Generador de Tesis — Coproductos con Metaheurísticas")
    print("=" * 60)

    print("\n[1/3] Verificando dependencias...")
    if not verificar_dependencias():
        print("\n✗ Dependencias faltantes. Instálalas antes de continuar.")
        sys.exit(1)

    print("\n[2/3] Verificando archivos...")
    if not verificar_archivos():
        print("\n✗ Verificación de archivos falló.")
        sys.exit(1)

    print("\n[3/3] Generando documentos...")
    pdf_ok = generar_pdf()

    if pdf_ok and args.docx:
        generar_docx()

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
