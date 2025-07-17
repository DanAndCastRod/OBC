# tests/test_sqlite_integration.py
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.sqlite import Base, Paper, insertar_paper_db, init_db
from src.utils.config import SQLITE_PATH

TEST_DB = "data/test_papers.db"

@pytest.fixture(scope="module", autouse=True)
def setup_sqlite():
    # Configurar DB de prueba
    os.environ["SQLITE_PATH"] = TEST_DB
    engine = create_engine(f"sqlite:///{TEST_DB}")
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    yield
    # Limpieza
    os.remove(TEST_DB)

def test_insertar_y_duplicados():
    datos = {
        "scopus_id": "12345",
        "doi":       "10.1000/test",
        "title":     "Título Test",
        "authors":   "Autor A",
        "journal":   "Journal Test",
        "year":      "2025"
    }
    # Primera inserción debe ser True
    assert insertar_paper_db(datos) is True
    # Segunda inserción idéntica debe ser False
    assert insertar_paper_db(datos) is False
