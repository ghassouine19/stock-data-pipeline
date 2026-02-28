from __future__ import annotations

from pathlib import Path
import random
import pandas as pd


def main() -> None:
    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)

    start = pd.Timestamp("2025-01-01")
    end = pd.Timestamp("2025-12-31")
    dates = pd.bdate_range(start, end)  # business days

    price = 200.0
    rows = []
    for d in dates:
        # random walk
        price *= (1 + random.uniform(-0.02, 0.02))
        open_ = price * (1 + random.uniform(-0.005, 0.005))
        close = price * (1 + random.uniform(-0.005, 0.005))
        high = max(open_, close) * (1 + random.uniform(0, 0.01))
        low = min(open_, close) * (1 - random.uniform(0, 0.01))
        volume = random.randint(5_000_000, 50_000_000)

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

    df = pd.DataFrame(rows)
    df.to_csv(out_dir / "AAPL.csv", index=False)
    print("Wrote", out_dir / "AAPL.csv", "rows=", len(df))


if __name__ == "__main__":
    main()