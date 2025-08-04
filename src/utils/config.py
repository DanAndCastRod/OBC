# src/utils/config.py

import os
from dotenv import load_dotenv

load_dotenv()

def get_sqlite_path() -> str:
    return os.getenv("SQLITE_PATH", "data/papers.db")
