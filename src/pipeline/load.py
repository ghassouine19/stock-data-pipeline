from __future__ import annotations

from sqlalchemy import create_engine, text

import pandas as pd


UPSERT_SQL = """
INSERT INTO stg_prices (ticker, date, open, high, low, close, volume, source)
VALUES (:ticker, :date, :open, :high, :low, :close, :volume, :source)
ON CONFLICT (ticker, date) DO UPDATE SET
  open = EXCLUDED.open,
  high = EXCLUDED.high,
  low  = EXCLUDED.low,
  close = EXCLUDED.close,
  volume = EXCLUDED.volume,
  source = EXCLUDED.source,
  ingested_at = NOW()
"""


def upsert_prices(database_url: str, df: pd.DataFrame, source: str) -> int:
    if df.empty:
        return 0

    engine = create_engine(database_url)

    rows = df.to_dict(orient="records")
    for r in rows:
        r["source"] = source

    with engine.begin() as conn:
        conn.execute(text(UPSERT_SQL), rows)

    return len(rows)