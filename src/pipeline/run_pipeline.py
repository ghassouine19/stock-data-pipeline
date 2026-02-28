from __future__ import annotations

from src.pipeline.config import DATABASE_URL, TICKERS, DATA_SOURCE, LOCAL_DATA_DIR
from src.pipeline.extract import fetch_daily_prices_stooq
from src.pipeline.extract_local import fetch_daily_prices_local
from src.pipeline.transform import transform_prices
from src.pipeline.load import upsert_prices


def main() -> None:
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is empty. Check your .env file.")

    total_loaded = 0

    for ticker in TICKERS:
        print(f"[ETL] Extracting {ticker} ...")

        if DATA_SOURCE.lower() == "local":
            df = fetch_daily_prices_local(ticker, LOCAL_DATA_DIR)
        else:
            result = fetch_daily_prices_stooq(ticker)
            df = result.df

        print(f"[ETL] Transforming {ticker} ... rows={len(df)}")
        clean = transform_prices(ticker, df)

        print(f"[ETL] Loading {ticker} ... clean_rows={len(clean)}")
        loaded = upsert_prices(DATABASE_URL, clean, DATA_SOURCE)
        total_loaded += loaded

    print(f"[ETL] Done. Loaded/Upserted rows: {total_loaded}")


if __name__ == "__main__":
    main()