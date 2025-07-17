#!/usr/bin/env python
# scripts/elsevier_to_sqlite.py

from src.elsevier.extractor import buscar_papers, extraer_metadatos
from src.db.sqlite        import init_db, insertar_paper_db
import bibtexparser
from src.utils.config     import SQLITE_PATH

def main():
    # 1) Inicializar SQLite
    init_db()

    query = "optimization AND carcass"
    todos = []
    start = 0

    # 2) Paginación
    while True:
        data    = buscar_papers(query, start=start, count=25)
        entries = data["search-results"]["entry"]
        if not entries:
            break

        for raw in entries:
            meta = extraer_metadatos(raw)
            # 3) Insertar en SQLite
            if insertar_paper_db(meta):
                todos.append(meta)
        start += 25

    # 4) Actualizar references.bib
    generar_bibtex(todos)
    print(f"Insertados {len(todos)} nuevos papers en {SQLITE_PATH} y actualizado references.bib")

def generar_bibtex(lista_metadatos):
    """
    Añade cada paper a docs/references.bib en formato BibTeX.
    """
    bib_path = "docs/references.bib"
    bib_db   = bibtexparser.load(open(bib_path, encoding="utf-8"))
    ids_existentes = {e["ID"] for e in bib_db.entries}

    for m in lista_metadatos:
        key = m["doi"].replace("/", "_") if m.get("doi") else m["scopus_id"]
        if key in ids_existentes:
            continue

        entry = {
            "ENTRYTYPE": "article",
            "ID":        key,
            "title":     m["title"],
            "author":    m.get("authors", ""),
            "year":      m.get("year", ""),
            "journal":   m.get("journal", ""),
            "doi":       m.get("doi", "")
        }
        bib_db.entries.append(entry)

    with open(bib_path, "w", encoding="utf-8") as bibfile:
        bibtexparser.dump(bib_db, bibfile)

if __name__ == "__main__":
    main()
