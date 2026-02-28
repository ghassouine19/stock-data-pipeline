from __future__ import annotations

from pathlib import Path
import random

import pandas as pd


def generate_fake_ohlcv(
    start: str = "2025-01-01",
    end: str = "2025-12-31",
    start_price: float = 350.0,
    seed: int = 42,
) -> pd.DataFrame:
    random.seed(seed)

    dates = pd.bdate_range(pd.Timestamp(start), pd.Timestamp(end))  # business days
    price = start_price

    rows: list[dict] = []
    for d in dates:
        # random walk day-to-day
        price *= (1 + random.uniform(-0.02, 0.02))

        open_ = price * (1 + random.uniform(-0.005, 0.005))
        close = price * (1 + random.uniform(-0.005, 0.005))
        high = max(open_, close) * (1 + random.uniform(0, 0.01))
        low = min(open_, close) * (1 - random.uniform(0, 0.01))
        volume = random.randint(8_000_000, 70_000_000)

        rows.append(
            {
                "Date": d.date().isoformat(),
                "Open": round(open_, 4),
                "High": round(high, 4),
                "Low": round(low, 4),
                "Close": round(close, 4),
                "Volume": volume,
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)

    df = generate_fake_ohlcv(start_price=350.0, seed=123)

    # Write Excel (recommended since you said "en exel")
    xlsx_path = out_dir / "MSFT.xlsx"
    df.to_excel(xlsx_path, index=False)

    # Also write CSV (optional, handy for debugging)
    csv_path = out_dir / "MSFT.csv"
    df.to_csv(csv_path, index=False)

    print(f"Wrote {xlsx_path} rows={len(df)}")
    print(f"Wrote {csv_path} rows={len(df)}")


if __name__ == "__main__":
    main()