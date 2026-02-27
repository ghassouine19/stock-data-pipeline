CREATE TABLE IF NOT EXISTS stg_prices (
  ticker TEXT NOT NULL,
  date DATE NOT NULL,
  open DOUBLE PRECISION,
  high DOUBLE PRECISION,
  low DOUBLE PRECISION,
  close DOUBLE PRECISION,
  volume BIGINT,
  source TEXT NOT NULL DEFAULT 'stooq',
  ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (ticker, date)
);

CREATE INDEX IF NOT EXISTS idx_stg_prices_date ON stg_prices(date);