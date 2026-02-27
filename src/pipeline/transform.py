from __future__ import annotations

import pandas as pd


def transform_prices(ticker: str, df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["ticker", "date", "open", "high", "low", "close", "volume"])

    # Normalize column names
    df = df.rename(
        columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
    ).copy()

    df["ticker"] = ticker.upper()

    # Parse date + types
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    for c in ["open", "high", "low", "close"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0).astype("int64")

    # Drop bad rows
    df = df.dropna(subset=["date", "close"])
    df = df[df["close"] > 0]

    # Remove duplicates, keep last
    df = df.sort_values(["ticker", "date"]).drop_duplicates(subset=["ticker", "date"], keep="last")

    return df[["ticker", "date", "open", "high", "low", "close", "volume"]].reset_index(drop=True)