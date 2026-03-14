
import pypdf
import os

pdf_path = "anteproyecto_dlbp_coproductos.pdf"
output_path = "validation_render.txt"

def extract_text(pdf_path, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"--- START FILE: {pdf_path} ---\n")
        try:
            reader = pypdf.PdfReader(pdf_path)
            text = ""
            for i, page in enumerate(reader.pages):
                try:
                    text += page.extract_text() + "\n"
                except Exception as e:
                    text += f"[Error extracting page {i}: {e}]\n"
            f.write(text)
        except Exception as e:
            f.write(f"Error opening PDF: {e}\n")
        f.write(f"--- END FILE: {pdf_path} ---\n")

if __name__ == "__main__":
    if os.path.exists(pdf_path):
        extract_text(pdf_path, output_path)
        print(f"Extracted content to {output_path}")
    else:
        print(f"File not found: {pdf_path}")
