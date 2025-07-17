# src/db/sqlite.py

from sqlalchemy import (
    create_engine, Column, Integer, String, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.utils.config import SQLITE_PATH

# Base para definir modelos
Base = declarative_base()

class Paper(Base):
    __tablename__ = "papers"
    id        = Column(Integer, primary_key=True, autoincrement=True)
    scopus_id = Column(String, nullable=False)
    doi       = Column(String, nullable=True)
    title     = Column(String, nullable=False)
    authors   = Column(String, nullable=True)
    journal   = Column(String, nullable=True)
    year      = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint("scopus_id", name="uq_papers_scopus_id"),
    )

# Crear engine y sesión
engine = create_engine(f"sqlite:///{SQLITE_PATH}", echo=False)
Session = sessionmaker(bind=engine)

def init_db():
    """
    Inicializa la base de datos creando tablas si no existen.
    """
    Base.metadata.create_all(engine)

def insertar_paper_db(metadatos: dict) -> bool:
    """
    Inserta un paper en SQLite si no existe.
    :param metadatos: dict con keys 'scopus_id', 'doi', 'title', 'authors', 'journal', 'year'
    :return: True si se insertó, False si ya existía.
    """
    session = Session()
    existe = session.query(Paper).filter_by(scopus_id=metadatos["scopus_id"]).first()
    if existe:
        session.close()
        return False

    # Crear instancia y guardar
    paper = Paper(
        scopus_id=metadatos["scopus_id"],
        doi       =metadatos.get("doi"),
        title     =metadatos["title"],
        authors   =metadatos.get("authors"),
        journal   =metadatos.get("journal"),
        year      =metadatos.get("year")
    )
    session.add(paper)
    session.commit()
    session.close()
    return True
