"""
Extrae referencias mensuales desde PDF FENAVI escaneado.

Tablas objetivo:
  - Tabla 5.5.3 (Precio corriente promedio mensual de la carne de pollo en canal)
  - Tabla 5.3.1 (Produccion mensual de pollo)
  - Fuente: Avicultura en Cifras 2024 (FENAVI/FONAV)

Dependencias (entorno virtual recomendado):
  pip install pymupdf rapidocr-onnxruntime opencv-python<4.11

Uso:
  python experiments/scripts/extract_fenavi_pdf_reference.py
  python experiments/scripts/extract_fenavi_pdf_reference.py --pdf-path data/Avicultura-en-Cifras-2024_17-09-2024.pdf
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import fitz
import numpy as np
import pandas as pd
from rapidocr_onnxruntime import RapidOCR

MONTHS_ORDER = [
    "Ene",
    "Feb",
    "Mar",
    "Abr",
    "May",
    "Jun",
    "Jul",
    "Ago",
    "Sep",
    "Oct",
    "Nov",
    "Dic",
    "Promedio",
]

MONTH_TO_NUM = {
    "Ene": 1,
    "Feb": 2,
    "Mar": 3,
    "Abr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Ago": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dic": 12,
}


def _ocr_page_text(
    pdf_path: Path,
    page_number_1_based: int,
    dpi: int = 170,
    score_threshold: float = 0.45,
) -> str:
    if not pdf_path.exists():
        raise FileNotFoundError(f"No existe el PDF: {pdf_path}")

    with fitz.open(pdf_path) as doc:
        if page_number_1_based < 1 or page_number_1_based > doc.page_count:
            raise ValueError(
                f"Pagina invalida {page_number_1_based}; rango valido: 1..{doc.page_count}"
            )
        page = doc[page_number_1_based - 1]
        pix = page.get_pixmap(dpi=dpi)

    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    if pix.n == 4:
        img = img[:, :, :3]

    ocr = RapidOCR()
    result, _ = ocr(img)
    texts: list[str] = []
    if result:
        for line in result:
            txt = (line[1] or "").strip()
            score = float(line[2]) if len(line) > 2 else 0.0
            if txt and score >= score_threshold:
                texts.append(txt)
    return " ".join(texts)


def _extract_table_553(section_text: str) -> dict[str, list[str]]:
    txt = section_text
    txt = txt.replace("inr", "Jul")
    txt = txt.replace("Mes / Anio", " ")
    txt = txt.replace("Mes I AKo", " ")
    txt = re.sub(r"\s+", " ", txt).strip()

    start = txt.find("Tabla5.5.3")
    end = txt.find("Tabla5.5.4")
    if start == -1:
        raise ValueError("No se encontro 'Tabla5.5.3' en el texto OCR")
    if end == -1:
        end = len(txt)
    body = txt[start:end]

    labels: list[tuple[int, str]] = []
    for label in MONTHS_ORDER:
        for m in re.finditer(rf"\b{label}\b", body):
            labels.append((m.start(), label))
    labels.sort(key=lambda x: x[0])
    if not labels:
        raise ValueError("No se detectaron etiquetas de mes en la tabla 5.5.3")

    rows: dict[str, list[str]] = {}

    for i, (pos, label) in enumerate(labels):
        label_idx = MONTHS_ORDER.index(label)
        j = i + 1
        while j < len(labels) and MONTHS_ORDER.index(labels[j][1]) <= label_idx:
            j += 1

        next_pos = labels[j][0] if j < len(labels) else len(body)
        segment = body[pos:next_pos]
        row_gap = (
            MONTHS_ORDER.index(labels[j][1]) - label_idx
            if j < len(labels)
            else len(MONTHS_ORDER) - label_idx
        )

        # La tabla usa formato de miles con punto (ej. 5.673).
        values = re.findall(r"\d{1,3}(?:\.\d{3})+", segment)
        needed = 11 * row_gap  # 11 anios: 2013..2023
        values = values[:needed]

        # OCR puede omitir "Oct", por eso se rellena por bloques de 11 valores.
        for k in range(row_gap):
            target_label = MONTHS_ORDER[label_idx + k]
            chunk = values[k * 11 : (k + 1) * 11]
            if len(chunk) == 11:
                rows[target_label] = chunk

    missing = [m for m in MONTHS_ORDER if m not in rows]
    if missing:
        raise ValueError(
            f"No se pudieron extraer todas las filas de la tabla 5.5.3. Faltan: {missing}"
        )
    return rows


def _extract_table_531(section_text: str) -> dict[int, list[str]]:
    txt = section_text
    txt = txt.replace("Inr", "jul")
    txt = txt.replace(" inr ", " jul ")
    txt = re.sub(r"\s+", " ", txt).strip()

    start = txt.find("Tabla5.3.1")
    if start == -1:
        start = txt.find("Tabla 5.3.1")
    if start == -1:
        raise ValueError("No se encontro 'Tabla5.3.1' en el texto OCR")

    # El texto de la pagina contiene una grafica previa con anios; por eso
    # se localiza el primer inicio de fila real: "2010 <valor mensual>".
    body = txt[start:]
    row_start = re.search(r"\b2010\s+\d{1,3}\.\d{3}", body)
    if row_start is None:
        raise ValueError("No se encontro el inicio de filas para la tabla 5.3.1")
    rows_txt = body[row_start.start() :]

    years = list(range(2010, 2024))
    year_pos: list[tuple[int, int]] = []
    for y in years:
        m = re.search(rf"\b{y}\b", rows_txt)
        if m is not None:
            year_pos.append((m.start(), y))
    year_pos.sort(key=lambda x: x[0])

    parsed: dict[int, list[str]] = {}
    for i, (pos, year) in enumerate(year_pos):
        nxt = year_pos[i + 1][0] if i + 1 < len(year_pos) else len(rows_txt)
        seg = rows_txt[pos:nxt]
        # Captura valores mensuales tipo 87.496 y omite el total anual.
        vals = re.findall(r"\d{1,3}\.\d{3}", seg)
        monthly = vals[:12]
        parsed[year] = monthly

    missing_years = [y for y in years if y not in parsed]
    if missing_years:
        raise ValueError(
            f"No se extrajeron todos los anios de tabla 5.3.1. Faltan: {missing_years}"
        )

    bad = [y for y in years if len(parsed.get(y, [])) != 12]
    if bad:
        raise ValueError(
            f"No se extrajeron 12 meses para los anios: {bad} (tabla 5.3.1)"
        )
    return parsed


def _value_to_float_cop_kg(value_str: str) -> float:
    # En las tablas FENAVI/DANE la notacion esta en miles con punto (ej. 5.673).
    # Se conserva esta convencion para mantener consistencia con CSV historicos
    # ya cargados en data/references.
    return float(value_str.replace(",", "."))


def _build_long_df_from_553(rows: dict[str, list[str]], source_pdf: str, page: int) -> pd.DataFrame:
    years = list(range(2013, 2024))
    out: list[dict] = []
    for month_label in MONTHS_ORDER:
        if month_label == "Promedio":
            continue
        month_num = MONTH_TO_NUM[month_label]
        for year, raw_val in zip(years, rows[month_label]):
            out.append(
                {
                    "product": "medio_pollo",
                    "date": f"{year}-{month_num:02d}-01",
                    "month": month_num,
                    "year": year,
                    "value": _value_to_float_cop_kg(raw_val),
                    "variable_type": "price_cop_kg",
                    "source_file": source_pdf,
                    "source_table": "Tabla 5.5.3",
                    "source_page": page,
                }
            )
    df = pd.DataFrame(out).sort_values(["year", "month"]).reset_index(drop=True)
    return df


def _build_long_df_from_531(
    rows: dict[int, list[str]], source_pdf: str, page: int
) -> pd.DataFrame:
    out: list[dict] = []
    for year in sorted(rows):
        monthly = rows[year]
        for month_num, raw_val in enumerate(monthly, start=1):
            out.append(
                {
                    "product": "medio_pollo",
                    "date": f"{year}-{month_num:02d}-01",
                    "month": month_num,
                    "year": year,
                    "value": float(raw_val),
                    "variable_type": "production_tons",
                    "source_file": source_pdf,
                    "source_table": "Tabla 5.3.1",
                    "source_page": page,
                }
            )
    return pd.DataFrame(out).sort_values(["year", "month"]).reset_index(drop=True)


def _merge_with_existing(existing_csv: Path, extracted: pd.DataFrame) -> pd.DataFrame:
    if not existing_csv.exists():
        return extracted.copy()

    base = pd.read_csv(existing_csv)
    req_cols = {"product", "month", "year", "value"}
    missing = req_cols - set(base.columns)
    if missing:
        raise ValueError(
            f"{existing_csv} no contiene columnas requeridas para merge: {sorted(missing)}"
        )

    merged_base = base.copy()
    if "variable_type" not in merged_base.columns:
        merged_base["variable_type"] = ""
    if "source_file" not in merged_base.columns:
        merged_base["source_file"] = ""
    if "date" not in merged_base.columns:
        merged_base["date"] = pd.to_datetime(
            dict(year=merged_base["year"], month=merged_base["month"], day=1),
            errors="coerce",
        ).dt.strftime("%Y-%m-%d")

    key_cols = ["product", "year", "month", "variable_type"]
    base_keys = {
        tuple(x)
        for x in merged_base[key_cols].astype(
            {"product": str, "year": int, "month": int, "variable_type": str}
        ).itertuples(index=False, name=None)
    }
    add_mask = [
        (
            str(r.product),
            int(r.year),
            int(r.month),
            str(r.variable_type),
        )
        not in base_keys
        for r in extracted.itertuples(index=False)
    ]
    to_add = extracted.loc[add_mask].copy()

    final_cols = list(dict.fromkeys(list(merged_base.columns) + list(to_add.columns)))
    merged = pd.concat(
        [merged_base.reindex(columns=final_cols), to_add.reindex(columns=final_cols)],
        ignore_index=True,
    )
    merged = merged.sort_values(["product", "year", "month"]).reset_index(drop=True)
    return merged


def run(
    pdf_path: str,
    output_price_csv: str,
    output_production_csv: str,
    output_extended_csv: str,
    existing_reference_csv: str,
    page_553: int = 101,
    page_531: int = 95,
    dpi_553: int = 170,
    dpi_531: int = 190,
) -> tuple[Path, Path, Path]:
    pdf = Path(pdf_path)
    out_price = Path(output_price_csv)
    out_prod = Path(output_production_csv)
    out_ext = Path(output_extended_csv)
    existing_csv = Path(existing_reference_csv)

    out_price.parent.mkdir(parents=True, exist_ok=True)
    out_prod.parent.mkdir(parents=True, exist_ok=True)
    out_ext.parent.mkdir(parents=True, exist_ok=True)

    text_553 = _ocr_page_text(pdf, page_number_1_based=page_553, dpi=dpi_553)
    rows_553 = _extract_table_553(text_553)
    extracted_price = _build_long_df_from_553(
        rows_553, source_pdf=pdf.name, page=page_553
    )
    extracted_price.to_csv(out_price, index=False, encoding="utf-8")

    text_531 = _ocr_page_text(pdf, page_number_1_based=page_531, dpi=dpi_531)
    rows_531 = _extract_table_531(text_531)
    extracted_prod = _build_long_df_from_531(
        rows_531, source_pdf=pdf.name, page=page_531
    )
    extracted_prod.to_csv(out_prod, index=False, encoding="utf-8")

    extracted_all = pd.concat([extracted_price, extracted_prod], ignore_index=True)
    merged = _merge_with_existing(existing_csv, extracted_all)
    merged.to_csv(out_ext, index=False, encoding="utf-8")

    return out_price, out_prod, out_ext


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Extrae tablas 5.5.3 (precio) y 5.3.1 (produccion) "
            "de Avicultura en Cifras 2024 (PDF escaneado)."
        )
    )
    parser.add_argument(
        "--pdf-path",
        type=str,
        default="data/Avicultura-en-Cifras-2024_17-09-2024.pdf",
    )
    parser.add_argument(
        "--output-price-csv",
        type=str,
        default="data/references/fenavi_price_pollo_en_canal_2013_2023.csv",
    )
    parser.add_argument(
        "--output-production-csv",
        type=str,
        default="data/references/fenavi_production_pollo_2010_2023.csv",
    )
    parser.add_argument(
        "--existing-reference-csv",
        type=str,
        default="data/references/fenavi_monthly_reference.csv",
    )
    parser.add_argument(
        "--output-extended-csv",
        type=str,
        default="data/references/fenavi_monthly_reference_extended.csv",
    )
    parser.add_argument(
        "--page-553",
        type=int,
        default=101,
        help="Pagina (1-based) donde se ubica la Tabla 5.5.3",
    )
    parser.add_argument(
        "--page-531",
        type=int,
        default=95,
        help="Pagina (1-based) donde se ubica la Tabla 5.3.1",
    )
    parser.add_argument(
        "--dpi-553",
        type=int,
        default=170,
        help="Resolucion OCR para tabla 5.5.3",
    )
    parser.add_argument(
        "--dpi-531",
        type=int,
        default=190,
        help="Resolucion OCR para tabla 5.3.1",
    )
    args = parser.parse_args()

    price_csv, prod_csv, extended_csv = run(
        pdf_path=args.pdf_path,
        output_price_csv=args.output_price_csv,
        output_production_csv=args.output_production_csv,
        output_extended_csv=args.output_extended_csv,
        existing_reference_csv=args.existing_reference_csv,
        page_553=args.page_553,
        page_531=args.page_531,
        dpi_553=args.dpi_553,
        dpi_531=args.dpi_531,
    )

    df_price = pd.read_csv(price_csv)
    df_prod = pd.read_csv(prod_csv)
    print("=" * 80)
    print("EXTRACCION FENAVI PDF COMPLETADA")
    print("=" * 80)
    print(f"CSV tabla 5.5.3: {price_csv}")
    print(f"CSV tabla 5.3.1: {prod_csv}")
    print(f"CSV extendido: {extended_csv}")
    print(f"Filas extraidas (tabla 5.5.3): {len(df_price)}")
    print(f"Filas extraidas (tabla 5.3.1): {len(df_prod)}")
    print(
        f"Rango fechas precio: {df_price['date'].min()} -> {df_price['date'].max()}"
    )
    print(
        f"Rango fechas produccion: {df_prod['date'].min()} -> {df_prod['date'].max()}"
    )


if __name__ == "__main__":
    main()
