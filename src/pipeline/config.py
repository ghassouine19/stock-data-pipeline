from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

DATABASE_URL = os.getenv("DATABASE_URL", "")

TICKERS = [t.strip().upper() for t in os.getenv("TICKERS", "AAPL").split(",") if t.strip()]

# Which extractor to use: "stooq" (online) or "local" (offline)
DATA_SOURCE = os.getenv("DATA_SOURCE", "stooq")

# Directory containing <TICKER>.csv files when DATA_SOURCE=local
LOCAL_DATA_DIR = os.getenv("LOCAL_DATA_DIR", "data/raw")