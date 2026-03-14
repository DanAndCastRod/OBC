import PyPDF2
import re

pdf_path = r'c:\Users\facem\OneDrive\Documentos\Maestría\OBC\data\DANE-2024pr.pdf'

with open(pdf_path, 'rb') as file:
    pdf = PyPDF2.PdfReader(file)
    print(f'Total páginas: {len(pdf.pages)}\n')
    
    # Primera página
    print('='*80)
    print('PÁGINA 1 - METADATA:')
    print('='*80)
    page1_text = pdf.pages[0].extract_text()
    print(page1_text[:1000])
    
    # Buscar dato "1.7" o "1,7"
    print('\n' + '='*80)
    print('BÚSQUEDA DE "1.7" o "1,7":')
    print('='*80)
    
    found = False
    for i in range(min(10, len(pdf.pages))):
        text = pdf.pages[i].extract_text()
        if '1.7' in text or '1,7' in text:
            print(f'\n✅ ENCONTRADO en página {i+1}')
            # Buscar contexto
            idx17 = text.find('1.7') if '1.7' in text else text.find('1,7')
            start = max(0, idx17-300)
            end = min(len(text), idx17+300)
            print(f'\nContexto:\n{text[start:end]}')
            found = True
    
    if not found:
        print('\n❌ NO encontrado "1.7" o "1,7" en primeras 10 páginas')
    
    # Buscar datos de producción general
    print('\n' + '='*80)
    print('DATOS DE PRODUCCIÓN EN PÁGINA 1:')
    print('='*80)
    
    lines = page1_text.split('\n')
    for line in lines:
        if any(word in line.lower() for word in ['producción', 'tonelada', 'mill', 'pollo', 'carne']):
            print(f'  {line}')
