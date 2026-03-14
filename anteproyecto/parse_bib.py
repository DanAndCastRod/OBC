import os
import re
import sys

def parse_bib(filepath, outpath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    entries = re.findall(r'@(?:article|inproceedings|book|misc|conference)\{([^,]+),\s*(.*?)(?=\n@|\Z)', content, re.DOTALL | re.IGNORECASE)
    
    with open(outpath, 'w', encoding='utf-8') as out:
        out.write(f"# Analysis of {os.path.basename(filepath)}\n")
        out.write(f"- Total Entries: {len(entries)}\n\n")
        
        for key, data in entries:
            title_match = re.search(r'title\s*=\s*[\{"](.*?)(?:[\}"]\s*,|\n)', data, re.IGNORECASE | re.DOTALL)
            author_match = re.search(r'author\s*=\s*[\{"](.*?)(?:[\}"]\s*,|\n)', data, re.IGNORECASE | re.DOTALL)
            year_match = re.search(r'year\s*=\s*[\{"]?(\d+)[\}"]?,', data, re.IGNORECASE)
            abstract_match = re.search(r'abstract\s*=\s*[\{"](.*?)(?:[\}"]\s*,|\n)', data, re.IGNORECASE | re.DOTALL)
            
            title = title_match.group(1).replace('\n', ' ').strip() if title_match else "No title"
            author = author_match.group(1).replace('\n', ' ').strip() if author_match else "No author"
            year = year_match.group(1) if year_match else "No year"
            abstract = abstract_match.group(1).replace('\n', ' ').strip() if abstract_match else "No abstract"
            
            # Simple relevance scoring
            keywords = ['lot sizing', 'setup', 'np-hard', 'metaheuristic', 'poultry', 'two-stage', 'stochastic', 'sequence', 'batch']
            score = sum(1 for kw in keywords if kw.lower() in title.lower() or kw.lower() in abstract.lower())
            
            out.write(f"### {title} ({year})\n")
            out.write(f"**Key:** `{key}`\n")
            out.write(f"**Authors:** {author}\n")
            out.write(f"**Relevance Score:** {score}/9\n")
            out.write(f"**Abstract:** {abstract[:500]}...\n" if len(abstract) > 500 else f"**Abstract:** {abstract}\n")
            out.write("\n---\n\n")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        parse_bib(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python parse_bib.py <filepath> <outpath>")
