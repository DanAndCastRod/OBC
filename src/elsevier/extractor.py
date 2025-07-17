# src/elsevier/extractor.py

import requests
from urllib.parse import quote
from src.utils.config import ELSEVIER_KEY

# Endpoint base para Scopus Search API
BASE_URL = "https://api.elsevier.com/content/search/scopus"

def buscar_papers(query: str, start: int = 0, count: int = 25):
    """
    Realiza una llamada a Scopus Search API.
    :param query: término de búsqueda (p.ej. "optimization balance carcass")
    :param start: registro inicial (paginación)
    :param count: número de resultados a obtener
    :return: JSON con resultados
    """
    headers = {
        "Accept": "application/json",
        "X-ELS-APIKey": ELSEVIER_KEY
    }
    params = {
        "query": quote(query),
        "start": start,
        "count": count
    }
    resp = requests.get(BASE_URL, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()

def extraer_metadatos(item: dict) -> dict:
    """
    Mapea un registro JSON de Scopus a un dict de campos útiles.
    """
    return {
        "title":       item.get("dc:title"),
        "authors":     item.get("dc:creator"),
        "year":        item.get("prism:coverDate", "")[:4],
        "doi":         item.get("prism:doi"),
        "scopus_id":   item.get("dc:identifier", "").split(":")[-1],
        "journal":     item.get("prism:publicationName")
    }
