# src/db/sqlite.py

from sqlalchemy import (
    create_engine, Column, Integer, String, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, sessionmaker
from src.utils.config import get_sqlite_path

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

def get_engine():
    return create_engine(f"sqlite:///{get_sqlite_path()}", echo=False)

def init_db():
    """
    Inicializa la base de datos creando tablas si no existen.
    """
    engine = get_engine()
    Base.metadata.create_all(engine)

def insertar_paper_db(metadatos: dict) -> bool:
    """
    Inserta un paper en SQLite si no existe.
    :param metadatos: dict con keys 'scopus_id', 'doi', 'title', 'authors', 'journal', 'year'
    :return: True si se insertó, False si ya existía.
    """
    engine = get_engine()
    Session = sessionmaker(bind=engine)
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
