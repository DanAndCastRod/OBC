import re
import bibtexparser

def load_bibtex(bib_path):
    with open(bib_path, 'r', encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    return {entry['ID']: entry for entry in bib_database.entries}

def extract_citations_with_context(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex to capture "Name et al. [@Key]" or "Name (Year) [@Key]" or "Name [@Key]"
    # Captures: 1=Name, 2=Connector(et al/and), 3=CitationKey
    # This is a heuristic; it won't catch everything but should catch explicit attributions.
    pattern = re.compile(r'([A-Z][a-z\u00C0-\u00FF]+(?:-[A-Z][a-z\u00C0-\u00FF]+)?)\s+(?:et al\.|and\s+[A-Z][a-z\u00C0-\u00FF]+)?\s*(?:\(\d{4}\))?\s*\[@([a-zA-Z0-9_-]+)(?:;\s*@[a-zA-Z0-9_-]+)*\]')
    
    matches = []
    lines = content.split('\n')
    for line_num, line in enumerate(lines):
        for match in pattern.finditer(line):
            text_name = match.group(1)
            citation_key = match.group(2)
            matches.append({
                'line': line_num + 1,
                'text_name': text_name,
                'citation_key': citation_key,
                'context': line.strip()
            })
    return matches

def audit_citations(md_path, bib_path):
    bib_data = load_bibtex(bib_path)
    citations_in_text = extract_citations_with_context(md_path)
    
    issues = []
    
    print(f"Auditing {len(citations_in_text)} explicit author mentions...")
    
    for item in citations_in_text:
        key = item['citation_key']
        text_name = item['text_name']
        
        if key not in bib_data:
            issues.append(f"[MISSING KEY] Line {item['line']}: Cited @{key} but key not found in .bib")
            continue
            
        bib_author_field = bib_data[key].get('author', '').lower()
        # Clean up bib author (remove weird chars, simplify)
        bib_authors_normalized = bib_author_field.replace('{', '').replace('}', '').replace('\n', ' ')
        
        # Check if the text name appears in the bib author list
        # We do a loose check: is "smith" in "smith, j. and doe, a."?
        if text_name.lower() not in bib_authors_normalized:
            issues.append(f"[MISMATCH] Line {item['line']}: Text mentions '{text_name}' but citation @{key} has authors: '{bib_author_field}'")

    if not issues:
        print("\n✅ No obvious Author-Citation mismatches found in explicit mentions.")
    else:
        print(f"\n⚠️ Found {len(issues)} potential issues:")
        for issue in issues:
            print(issue)

if __name__ == "__main__":
    try:
        audit_citations('anteproyecto_dlbp_coproductos.md', 'referencias_dlbp.bib')
    except Exception as e:
        print(f"Error running audit: {e}")
