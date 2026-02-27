from __future__ import annotations

import io
from dataclasses import dataclass

import pandas as pd
import requests


@dataclass(frozen=True)
class ExtractResult:
    ticker: str
    df: pd.DataFrame


def fetch_daily_prices_stooq(ticker: str) -> ExtractResult:
    """
    Stooq endpoint commonly works like:
    https://stooq.com/q/d/l/?s=aapl.us&i=d

    Returns CSV with columns:
    Date, Open, High, Low, Close, Volume
    """
    url = f"https://stooq.com/q/d/l/?s={ticker.lower()}.us&i=d"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    df = pd.read_csv(io.StringIO(resp.text))
    # If ticker is invalid, Stooq may return empty CSV with headers only
    return ExtractResult(ticker=ticker, df=df)