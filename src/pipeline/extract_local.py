from __future__ import annotations

from pathlib import Path
import pandas as pd


def fetch_daily_prices_local(ticker: str, data_dir: str | Path) -> pd.DataFrame:
    """
    Load daily prices for `ticker` from a local CSV or Excel file.

    Accepted files (first one found):
      <data_dir>/<TICKER>.csv
      <data_dir>/<TICKER>.xlsx
      <data_dir>/<TICKER>.xls
    """
    project_root = Path(__file__).resolve().parents[2]

    data_dir = Path(data_dir)
    if not data_dir.is_absolute():
        data_dir = project_root / data_dir

    base = data_dir / ticker.upper()
    candidates = [base.with_suffix(".csv"), base.with_suffix(".xlsx"), base.with_suffix(".xls")]

    path = next((p for p in candidates if p.exists()), None)
    if path is None:
        raise FileNotFoundError(
            f"Local price file not found for ticker={ticker}. Tried: "
            + ", ".join(str(p) for p in candidates)
        )

    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        # For xlsx support: pip install openpyxl
        df = pd.read_excel(path)

    df.columns = [c.strip().lower() for c in df.columns]

    required = ["date", "open", "high", "low", "close", "volume"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            f"{path} is missing required columns: {missing}. Found columns: {list(df.columns)}"
        )

    return df[required]