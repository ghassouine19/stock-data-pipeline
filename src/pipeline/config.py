import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root (2 levels up from this file: src/pipeline/config.py -> project root)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", "")
TICKERS = [t.strip().upper() for t in os.getenv("TICKERS", "AAPL,MSFT").split(",") if t.strip()]
DATA_SOURCE = os.getenv("DATA_SOURCE", "stooq")