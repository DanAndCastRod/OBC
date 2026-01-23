
import os
import codecs

def convert_to_utf8(filename):
    try:
        # Try reading as utf-8 first
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"{filename} is already valid UTF-8.")
        # We rewrite it just to be sure (e.g. normalizing line endings)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except UnicodeDecodeError:
        print(f"{filename} is NOT valid UTF-8. Attempting to convert...")
        # Try reading with different encodings
        encodings = ['latin-1', 'cp1252', 'iso-8859-1']
        for enc in encodings:
            try:
                with open(filename, 'r', encoding=enc) as f:
                    content = f.read()
                # Rewrite as utf-8
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Converted {filename} from {enc} to UTF-8.")
                return
            except UnicodeDecodeError:
                continue
        print(f"Failed to convert {filename}.")

if __name__ == "__main__":
    convert_to_utf8("anteproyecto_dlbp_coproductos.md")
    convert_to_utf8("referencias_dlbp.bib")
