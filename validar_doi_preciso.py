#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Validación Preciso de DOI
Valida DOI usando la API de CrossRef y compara metadatos
"""

import re
import json
import time
import requests
from typing import Dict, List, Tuple, Optional
from difflib import SequenceMatcher

class DOIValidator:
    """Validador de DOI usando API de CrossRef"""
    
    def __init__(self, bib_file: str):
        self.bib_file = bib_file
        self.crossref_api = "https://api.crossref.org/works/"
        self.headers = {
            'User-Agent': 'DOI-Validator/1.0 (mailto:usuario@ejemplo.com)',
            'Accept': 'application/json'
        }
        
    def parse_bib_file(self) -> List[Dict]:
        """Parsea el archivo .bib y extrae referencias con DOI"""
        with open(self.bib_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        references = []
        # Patrón para extraer entradas BibTeX
        pattern = r'@(\w+)\{(\w+),(.*?)(?=@|\Z)'
        
        for match in re.finditer(pattern, content, re.DOTALL):
            entry_type = match.group(1)
            entry_key = match.group(2)
            entry_body = match.group(3)
            
            # Extraer campos
            doi_match = re.search(r'doi\s*=\s*\{([^}]+)\}', entry_body)
            if not doi_match:
                continue
            
            doi = doi_match.group(1).strip()
            
            # Extraer otros campos
            author_match = re.search(r'author\s*=\s*\{([^}]+)\}', entry_body)
            title_match = re.search(r'title\s*=\s*\{([^}]+)\}', entry_body)
            journal_match = re.search(r'journal\s*=\s*\{([^}]+)\}', entry_body)
            year_match = re.search(r'year\s*=\s*\{(\d+)\}', entry_body)
            
            ref = {
                'key': entry_key,
                'type': entry_type,
                'doi': doi,
                'author': author_match.group(1).strip() if author_match else '',
                'title': title_match.group(1).strip() if title_match else '',
                'journal': journal_match.group(1).strip() if journal_match else '',
                'year': year_match.group(1).strip() if year_match else '',
                'raw_body': entry_body
            }
            
            references.append(ref)
        
        return references
    
    def normalize_text(self, text: str) -> str:
        """Normaliza texto para comparación"""
        if not text:
            return ""
        # Convertir a minúsculas, eliminar espacios extra, normalizar caracteres
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)  # Eliminar puntuación
        return text.strip()
    
    def similarity(self, text1: str, text2: str) -> float:
        """Calcula similitud entre dos textos (0-1)"""
        if not text1 or not text2:
            return 0.0
        return SequenceMatcher(None, 
                              self.normalize_text(text1), 
                              self.normalize_text(text2)).ratio()
    
    def extract_first_author(self, author_string: str) -> str:
        """Extrae el primer autor de una cadena de autores"""
        if not author_string:
            return ""
        # Separar por 'and' o ','
        authors = re.split(r'\s+and\s+|\s*,\s*', author_string)
        if authors:
            first_author = authors[0].strip()
            # Extraer apellido
            parts = first_author.split(',')
            if len(parts) > 1:
                return parts[0].strip()
            else:
                # Si no hay coma, tomar la última palabra como apellido
                words = first_author.split()
                return words[-1] if words else first_author
        return ""
    
    def validate_doi_with_crossref(self, doi: str) -> Optional[Dict]:
        """Valida DOI usando la API de CrossRef"""
        url = f"{self.crossref_api}{doi}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'message' in data:
                    return data['message']
            elif response.status_code == 404:
                return None  # DOI no encontrado
            else:
                return {'error': f'HTTP {response.status_code}'}
                
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
        
        return None
    
    def compare_metadata(self, bib_ref: Dict, crossref_data: Dict) -> Dict:
        """Compara metadatos de la referencia BibTeX con datos de CrossRef"""
        comparisons = {
            'title_match': 0.0,
            'author_match': 0.0,
            'year_match': False,
            'journal_match': 0.0,
            'overall_confidence': 0.0
        }
        
        # Comparar título
        if 'title' in crossref_data and crossref_data['title']:
            title_crossref = crossref_data['title'][0] if isinstance(crossref_data['title'], list) else crossref_data['title']
            comparisons['title_match'] = self.similarity(bib_ref['title'], title_crossref)
        
        # Comparar autores
        if 'author' in crossref_data and crossref_data['author']:
            if bib_ref['author']:
                # Obtener primer autor de BibTeX
                first_author_bib = self.extract_first_author(bib_ref['author'])
                # Obtener primer autor de CrossRef
                first_author_cr = ""
                if crossref_data['author'] and len(crossref_data['author']) > 0:
                    first_author_cr = crossref_data['author'][0].get('family', '')
                
                if first_author_bib and first_author_cr:
                    comparisons['author_match'] = self.similarity(first_author_bib, first_author_cr)
        
        # Comparar año
        if 'published-print' in crossref_data:
            year_parts = crossref_data['published-print'].get('date-parts', [])
            if year_parts and len(year_parts[0]) > 0:
                year_crossref = str(year_parts[0][0])
                comparisons['year_match'] = (bib_ref['year'] == year_crossref)
        
        # Comparar journal
        if 'container-title' in crossref_data and crossref_data['container-title']:
            journal_crossref = crossref_data['container-title'][0] if isinstance(crossref_data['container-title'], list) else crossref_data['container-title']
            if bib_ref['journal']:
                comparisons['journal_match'] = self.similarity(bib_ref['journal'], journal_crossref)
        
        # Calcular confianza general (promedio ponderado)
        weights = {'title': 0.4, 'author': 0.3, 'journal': 0.2, 'year': 0.1}
        comparisons['overall_confidence'] = (
            comparisons['title_match'] * weights['title'] +
            comparisons['author_match'] * weights['author'] +
            comparisons['journal_match'] * weights['journal'] +
            (1.0 if comparisons['year_match'] else 0.0) * weights['year']
        )
        
        return comparisons
    
    def validate_reference(self, ref: Dict) -> Dict:
        """Valida una referencia completa"""
        result = {
            'key': ref['key'],
            'doi': ref['doi'],
            'status': 'unknown',
            'doi_exists': False,
            'metadata_match': False,
            'confidence': 0.0,
            'details': {}
        }
        
        # Validar DOI en CrossRef
        crossref_data = self.validate_doi_with_crossref(ref['doi'])
        
        if crossref_data is None:
            result['status'] = 'not_found'
            result['details']['error'] = 'DOI no encontrado en CrossRef'
            return result
        
        if 'error' in crossref_data:
            result['status'] = 'error'
            result['details']['error'] = crossref_data['error']
            return result
        
        result['doi_exists'] = True
        
        # Comparar metadatos
        comparisons = self.compare_metadata(ref, crossref_data)
        result['confidence'] = comparisons['overall_confidence']
        result['details']['comparisons'] = comparisons
        result['details']['crossref_title'] = crossref_data.get('title', [''])[0] if crossref_data.get('title') else ''
        
        # Determinar si el DOI es correcto
        if comparisons['overall_confidence'] >= 0.7:
            result['status'] = 'valid'
            result['metadata_match'] = True
        elif comparisons['overall_confidence'] >= 0.4:
            result['status'] = 'uncertain'
        else:
            result['status'] = 'mismatch'
        
        return result
    
    def validate_all(self, delay: float = 0.5) -> List[Dict]:
        """Valida todas las referencias"""
        references = self.parse_bib_file()
        results = []
        
        print(f"Validando {len(references)} referencias...")
        print("=" * 70)
        
        for i, ref in enumerate(references, 1):
            print(f"[{i}/{len(references)}] Validando {ref['key']}...", end=' ', flush=True)
            
            result = self.validate_reference(ref)
            results.append(result)
            
            status_icons = {
                'valid': '✓',
                'uncertain': '?',
                'mismatch': '✗',
                'not_found': '✗',
                'error': '!'
            }
            
            icon = status_icons.get(result['status'], '?')
            confidence_str = f"{result['confidence']:.2f}" if result['doi_exists'] else "N/A"
            
            print(f"{icon} {result['status'].upper()} (confianza: {confidence_str})")
            
            # Pausa para no sobrecargar la API
            if i < len(references):
                time.sleep(delay)
        
        return results
    
    def generate_report(self, results: List[Dict], output_file: str = None):
        """Genera un reporte detallado"""
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append("REPORTE DE VALIDACIÓN DE DOI")
        report_lines.append("=" * 70)
        report_lines.append("")
        
        # Estadísticas generales
        total = len(results)
        valid = sum(1 for r in results if r['status'] == 'valid')
        uncertain = sum(1 for r in results if r['status'] == 'uncertain')
        mismatch = sum(1 for r in results if r['status'] == 'mismatch')
        not_found = sum(1 for r in results if r['status'] == 'not_found')
        errors = sum(1 for r in results if r['status'] == 'error')
        
        report_lines.append("ESTADÍSTICAS GENERALES:")
        report_lines.append(f"  Total de referencias: {total}")
        report_lines.append(f"  ✓ Válidas (confianza ≥ 0.7): {valid} ({valid/total*100:.1f}%)")
        report_lines.append(f"  ? Inciertas (confianza 0.4-0.7): {uncertain} ({uncertain/total*100:.1f}%)")
        report_lines.append(f"  ✗ No coinciden (confianza < 0.4): {mismatch} ({mismatch/total*100:.1f}%)")
        report_lines.append(f"  ✗ No encontradas: {not_found} ({not_found/total*100:.1f}%)")
        report_lines.append(f"  ! Errores: {errors} ({errors/total*100:.1f}%)")
        report_lines.append("")
        
        # Referencias válidas
        report_lines.append("=" * 70)
        report_lines.append("REFERENCIAS VÁLIDAS (Confianza ≥ 0.7)")
        report_lines.append("=" * 70)
        for r in sorted(results, key=lambda x: -x['confidence']):
            if r['status'] == 'valid':
                report_lines.append(f"\n{r['key']}:")
                report_lines.append(f"  DOI: {r['doi']}")
                report_lines.append(f"  Confianza: {r['confidence']:.2%}")
                comps = r['details'].get('comparisons', {})
                report_lines.append(f"    - Título: {comps.get('title_match', 0):.2%}")
                report_lines.append(f"    - Autor: {comps.get('author_match', 0):.2%}")
                report_lines.append(f"    - Revista: {comps.get('journal_match', 0):.2%}")
                report_lines.append(f"    - Año: {'✓' if comps.get('year_match') else '✗'}")
        
        # Referencias problemáticas
        report_lines.append("\n" + "=" * 70)
        report_lines.append("REFERENCIAS PROBLEMÁTICAS")
        report_lines.append("=" * 70)
        
        # No encontradas
        if not_found > 0:
            report_lines.append("\n❌ DOI NO ENCONTRADOS EN CROSSREF:")
            for r in results:
                if r['status'] == 'not_found':
                    report_lines.append(f"  - {r['key']}: {r['doi']}")
        
        # No coinciden
        if mismatch > 0:
            report_lines.append("\n⚠️  DOI CON METADATOS NO COINCIDENTES:")
            for r in sorted(results, key=lambda x: x['confidence']):
                if r['status'] == 'mismatch':
                    report_lines.append(f"\n  {r['key']}: {r['doi']}")
                    report_lines.append(f"    Confianza: {r['confidence']:.2%}")
                    if 'comparisons' in r['details']:
                        comps = r['details']['comparisons']
                        report_lines.append(f"    Título BibTeX: {comps.get('title_match', 0):.2%}")
                        report_lines.append(f"    Título CrossRef: {r['details'].get('crossref_title', 'N/A')[:80]}")
        
        # Inciertas
        if uncertain > 0:
            report_lines.append("\n❓ DOI CON BAJA CONFIANZA (0.4-0.7):")
            for r in sorted(results, key=lambda x: x['confidence']):
                if r['status'] == 'uncertain':
                    report_lines.append(f"  - {r['key']}: {r['doi']} (confianza: {r['confidence']:.2%})")
        
        # Errores
        if errors > 0:
            report_lines.append("\n❗ ERRORES EN LA VALIDACIÓN:")
            for r in results:
                if r['status'] == 'error':
                    report_lines.append(f"  - {r['key']}: {r['doi']}")
                    report_lines.append(f"    Error: {r['details'].get('error', 'Desconocido')}")
        
        report = "\n".join(report_lines)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\nReporte guardado en: {output_file}")
        else:
            print("\n" + report)
        
        return report


def main():
    """Función principal"""
    import sys
    
    bib_file = 'referencias_dlbp.bib'
    output_file = 'validacion_doi_report.txt'
    
    if len(sys.argv) > 1:
        bib_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    print("=" * 70)
    print("VALIDADOR PRECISO DE DOI")
    print("Usando API de CrossRef para verificación de metadatos")
    print("=" * 70)
    print()
    
    validator = DOIValidator(bib_file)
    results = validator.validate_all(delay=0.5)
    validator.generate_report(results, output_file)


if __name__ == '__main__':
    main()