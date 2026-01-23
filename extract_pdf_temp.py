
import pypdf
import os


files = [
    r"anteproyecto_dlbp_coproductos.pdf"
]


def extract_text(pdf_path, output_file):
    output_file.write(f"--- START FILE: {pdf_path} ---\n")
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            try:
                text += page.extract_text() + "\n"
            except:
                pass
        output_file.write(text)
    except Exception as e:
        output_file.write(f"Error extracting {pdf_path}: {e}\n")
    output_file.write(f"--- END FILE: {pdf_path} ---\n")

if __name__ == "__main__":
    with open("extraction_result_utf8.txt", "w", encoding="utf-8") as f:
        for file_path in files:
            if os.path.exists(file_path):
                extract_text(file_path, f)
            else:
                f.write(f"File not found: {file_path}\n")
