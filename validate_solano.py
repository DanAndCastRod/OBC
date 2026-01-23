
import pypdf
import os

pdf_path = r"data/Integrated planning decisions in the broiler chicken supply chain.pdf"
output_path = "validation_result_solano.txt"

def extract_text(pdf_path, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"--- START FILE: {pdf_path} ---\n")
        try:
            reader = pypdf.PdfReader(pdf_path)
            text = ""
            # Read first few pages and discussion/results (usually enough)
            # Or just read all
            for i, page in enumerate(reader.pages):
                try:
                    content = page.extract_text()
                    text += f"--- PAGE {i+1} ---\n{content}\n"
                except Exception as e:
                    text += f"Error on page {i+1}: {e}\n"
            f.write(text)
        except Exception as e:
            f.write(f"Error opening PDF: {e}\n")
        f.write(f"--- END FILE ---\n")

if __name__ == "__main__":
    if os.path.exists(pdf_path):
        extract_text(pdf_path, output_path)
        print(f"Extraction complete to {output_path}")
    else:
        print(f"File not found: {pdf_path}")
