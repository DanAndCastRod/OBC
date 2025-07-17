# src/utils/config.py

import os
from dotenv import load_dotenv

load_dotenv()

SQLITE_PATH = os.getenv("SQLITE_PATH", "data/papers.db")
ELSEVIER_KEY = os.getenv("ELSEVIER_API_KEY")
