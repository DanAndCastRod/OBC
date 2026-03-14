import os
import re
import json
import time
import pathlib
from typing import Optional

import requests


BIB_PATH = "referencias_dlbp.bib"
OUT_DIR = pathlib.Path("data")
CHECKLIST_PATH = pathlib.Path("referencias_pendientes.md")

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "OBC-PDF-Fetcher/1.0 (contact: local-user)"
})


def read_bib_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_bib_entries(content: str):
    entries = []
    for block in re.findall(r"@(\w+)\s*\{([^,]+),([\s\S]*?)\n\}", content):
        entry_type, key, body = block
        fields = dict(re.findall(r"(\w+)\s*=\s*\{([\s\S]*?)\}", body))
        norm = {k.lower(): v.strip() for k, v in fields.items()}
        entries.append({"type": entry_type.lower(), "key": key.strip(), **norm})
    return entries


def sanitize_filename(name: str) -> str:
    name = re.sub(r"[^\w\-. ]+", "_", name)
    return re.sub(r"\s+", " ", name).strip()


def save_pdf(resp: requests.Response, default_name: str) -> pathlib.Path:
    OUT_DIR.mkdir(exist_ok=True)
    filename = pathlib.Path(resp.url).name or default_name
    if not filename.lower().endswith(".pdf"):
        filename = f"{filename}.pdf"
    path = OUT_DIR / sanitize_filename(filename)
    with open(path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=32768):
            if chunk:
                f.write(chunk)
    return path


def try_direct_url(url: str) -> Optional[pathlib.Path]:
    try:
        r = SESSION.get(url, allow_redirects=True, timeout=30, stream=True)
        ct = (r.headers.get("Content-Type") or "").lower()
        if "application/pdf" in ct or r.url.lower().endswith(".pdf"):
            return save_pdf(r, "document.pdf")
        # buscar enlace a PDF en el HTML
        text = r.text
        m = re.search(r'href=["\']([^"\']+\.pdf)["\']', text, flags=re.I)
        if m:
            pdf_url = requests.compat.urljoin(r.url, m.group(1))
            r2 = SESSION.get(pdf_url, allow_redirects=True, timeout=30, stream=True)
            ct2 = (r2.headers.get("Content-Type") or "").lower()
            if "application/pdf" in ct2 or r2.url.lower().endswith(".pdf"):
                return save_pdf(r2, "document.pdf")
    except Exception:
        return None
    return None


def try_unpaywall(doi: str) -> Optional[pathlib.Path]:
    email = os.getenv("UNPAYWALL_EMAIL")
    if not email:
        return None
    url = f"https://api.unpaywall.org/v2/{requests.utils.quote(doi)}?email={requests.utils.quote(email)}"
    try:
        r = SESSION.get(url, timeout=30)
        if r.status_code != 200:
            return None
        data = r.json()
        candidates = []
        best = data.get("best_oa_location") or {}
        candidates += [best.get("url_for_pdf"), best.get("url")]
        for loc in data.get("oa_locations") or []:
            candidates += [loc.get("url_for_pdf"), loc.get("url")]
        for cand in [c for c in candidates if c]:
            p = try_direct_url(cand)
            if p:
                return p
    except Exception:
        return None
    return None


def try_doi_resolution(doi: str) -> Optional[pathlib.Path]:
    # resolver en doi.org
    for base in ("https://doi.org/", "https://dx.doi.org/"):
        try:
            r = SESSION.get(base + requests.utils.quote(doi), allow_redirects=True, timeout=30, stream=True)
            ct = (r.headers.get("Content-Type") or "").lower()
            if "application/pdf" in ct or r.url.lower().endswith(".pdf"):
                return save_pdf(r, f"{doi.replace('/', '_')}.pdf")
        except Exception:
            continue
    return None


def desired_filename(entry: dict) -> str:
    title = entry.get("title") or entry.get("key")
    year = entry.get("year") or ""
    return f"{sanitize_filename(title)}_{year}.pdf"


def update_checklist_status(checklist_text: str, key: str, success: bool) -> str:
    pattern = re.compile(rf"- \[ \]\s*{re.escape(key)}(.*)")
    if success:
        return pattern.sub(r"- [x] " + key + r"\1", checklist_text)
    return checklist_text


def main():
    bib_text = read_bib_text(BIB_PATH)
    entries = parse_bib_entries(bib_text)
    checklist_text = CHECKLIST_PATH.read_text(encoding="utf-8") if CHECKLIST_PATH.exists() else ""

    report = []
    for e in entries:
        key = e["key"]
        title = e.get("title", "")
        doi = e.get("doi", "")
        url = e.get("url", "")

        # solo actuar sobre entradas que figuran en el checklist (pendientes)
        if checklist_text and f"- [ ] {key}" not in checklist_text:
            continue

        status = {"key": key, "title": title, "doi": doi, "url": url, "saved": None, "note": ""}

        saved_path: Optional[pathlib.Path] = None

        if url:
            saved_path = try_direct_url(url)
        if not saved_path and doi:
            saved_path = try_unpaywall(doi)
        if not saved_path and doi:
            saved_path = try_doi_resolution(doi)

        if saved_path:
            # renombrar por título
            target = OUT_DIR / desired_filename(e)
            try:
                os.replace(saved_path, target)
                saved_path = target
            except Exception:
                pass
            status["saved"] = str(saved_path)
            status["note"] = "descargado"
            # marcar checklist
            if checklist_text:
                checklist_text = update_checklist_status(checklist_text, key, True)
        else:
            status["note"] = "no encontrado"

        report.append(status)
        time.sleep(0.5)

    # guardar checklist actualizado
    if checklist_text:
        CHECKLIST_PATH.write_text(checklist_text, encoding="utf-8")

    # guardar reporte JSON en UTF-8 y notificar en consola
    with open("reporte_descargas.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    success = sum(1 for r in report if r.get("note") == "descargado")
    total = len(report)
    print(f"Descargas exitosas: {success}/{total}")


if __name__ == "__main__":
    main()


