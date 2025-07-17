# src/myloft/client.py

import requests
from src.utils.config import MYLOFT_URL, MYLOFT_KEY

def insertar_paper_en_loft(metadatos: dict) -> bool:
    """
    Inserta un paper en la base de datos a través de MyLoft.
    :param metadatos: diccionario con campos title, authors, year, doi, etc.
    :return: True si se insertó correctamente
    """
    headers = {
        "Authorization": f"Bearer {MYLOFT_KEY}",
        "Content-Type":  "application/json"
    }
    resp = requests.post(
        f"{MYLOFT_URL}/papers",
        headers=headers,
        json=metadatos
    )
    resp.raise_for_status()
    return resp.status_code == 201
