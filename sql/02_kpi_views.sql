-- KPI views for analytics on top of stg_prices
-- Assumes table: stg_prices(ticker, date, open, high, low, close, volume)

CREATE OR REPLACE VIEW v_last_close AS
SELECT DISTINCT ON (ticker)
    ticker,
    date AS last_date,
    close AS last_close,
    volume AS last_volume
FROM stg_prices
ORDER BY ticker, date DESC;

CREATE OR REPLACE VIEW v_daily_returns AS
SELECT
    ticker,
    date,
    close,
    LAG(close) OVER (PARTITION BY ticker ORDER BY date) AS prev_close,
    CASE
        WHEN LAG(close) OVER (PARTITION BY ticker ORDER BY date) IS NULL THEN NULL
        WHEN LAG(close) OVER (PARTITION BY ticker ORDER BY date) = 0 THEN NULL
        ELSE (close / LAG(close) OVER (PARTITION BY ticker ORDER BY date)) - 1
    END AS daily_return
FROM stg_prices;

CREATE OR REPLACE VIEW v_moving_averages AS
SELECT
    ticker,
    date,
    close,
    AVG(close) OVER (
        PARTITION BY ticker
        ORDER BY date
        ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
    ) AS sma_5,
    AVG(close) OVER (
        PARTITION BY ticker
        ORDER BY date
        ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
    ) AS sma_20
FROM stg_prices;