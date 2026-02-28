# Stock Data Pipeline (ETL) — Stooq or Local CSV/Excel → PostgreSQL → KPI Views → CSV Exports

An end-to-end **data pipeline** that:
1. Extracts daily stock prices from **Stooq (online)** or **local files (offline)**,
2. Transforms raw data into a clean OHLCV format,
3. Loads the data into **PostgreSQL** (`stg_prices`) using **UPSERT**,
4. Builds **KPI SQL views** (last close, daily returns, moving averages),
5. Exports KPI datasets to `data/processed/` (via pgAdmin).

---

## Tech Stack
- Python (venv)
- pandas, requests
- PostgreSQL 16 (Docker Compose)
- SQLAlchemy + psycopg2
- pgAdmin 4 (GUI)

---

## Repository Structure

```text
.
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── generate_fake_aapl.py
├── generate_fake_msft.py
├── sql/
│   ├── 01_create_tables.sql
│   └── 02_kpi_views.sql
└── src/
    └── pipeline/
        ├── config.py
        ├── extract.py          # Stooq extractor (online)
        ├── extract_local.py    # Local CSV/XLSX extractor (offline)
        ├── transform.py
        ├── load.py             # UPSERT into Postgres
        └── run_pipeline.py
```

---

## Screenshots

> Put your screenshots in: `docs/screenshots/`

- Docker running: `docs/screenshots/01_docker_running.png`  
- pgAdmin connected: `docs/screenshots/02_pgadmin_connection.png`  
- `stg_prices` sample: `docs/screenshots/03_stg_prices_sample.png`  
- KPI `v_last_close`: `docs/screenshots/04_kpi_last_close.png`  
- Exported CSV files: `docs/screenshots/05_export_csv_folder.png`  
- Pipeline logs: `docs/screenshots/06_pipeline_run_logs.png`

![Docker running](docs/screenshots/01_docker_running.png)
![pgAdmin connected](docs/screenshots/02_pgadmin_connection.png)
![stg_prices sample](docs/screenshots/03_stg_prices_sample.png)
![KPI v_last_close](docs/screenshots/04_kpi_last_close.png)
![CSV exports](docs/screenshots/05_export_csv_folder.png)
![Pipeline logs](docs/screenshots/06_pipeline_run_logs.png)

---

## Prerequisites
- Python 3.10+ recommended
- Docker Desktop + Docker Compose
- (Optional) pgAdmin 4

---

## Setup

### 1) Create & activate a virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If you plan to load `.xlsx` files (Excel):
```powershell
pip install openpyxl
```

### 2) Configure environment variables
Copy `.env.example` to `.env` and update passwords:

```powershell
Copy-Item .env.example .env
```

Example `.env`:
```dotenv
# PostgreSQL (Docker)
POSTGRES_USER=user
POSTGRES_PASSWORD=user123
POSTGRES_DB=stock_db
DB_PORT=5432

# SQLAlchemy connection string used by Python
DATABASE_URL=postgresql+psycopg2://user:user123@localhost:5432/stock_db

# Pipeline
TICKERS=AAPL,MSFT
DATA_SOURCE=local
LOCAL_DATA_DIR=data/raw
```

> Note: `http://localhost:5432/` will NOT work in a browser. Port **5432 is PostgreSQL**, not HTTP.

### 3) Start PostgreSQL with Docker
```powershell
docker compose up -d
```

---

## Initialize Database (tables + KPI views)

Run these SQL files in order using **pgAdmin** (Query Tool):
1. `sql/01_create_tables.sql` (creates `stg_prices`)
2. `sql/02_kpi_views.sql` (creates KPI views)

---

## Run the ETL Pipeline

### Option A — Offline mode (Local CSV/Excel)
1. Put one file per ticker in `data/raw/`:
   - `data/raw/AAPL.csv` or `data/raw/AAPL.xlsx`
   - `data/raw/MSFT.csv` or `data/raw/MSFT.xlsx`

2. Required columns (case-insensitive):
   - `Date, Open, High, Low, Close, Volume`

3. Run:
```powershell
python -m src.pipeline.run_pipeline
```

### Option B — Online mode (Stooq)
Set in `.env`:
```dotenv
DATA_SOURCE=stooq
```

Run:
```powershell
python -m src.pipeline.run_pipeline
```

---

## Generate Fake Data (Offline Demo)

Generate fake AAPL (CSV):
```powershell
python .\generate_fake_aapl.py
```

Generate fake MSFT (XLSX + CSV):
```powershell
python .\generate_fake_msft.py
```

Then run ETL:
```powershell
python -m src.pipeline.run_pipeline
```

---

## KPI Views (SQL)

KPI views on top of `stg_prices`:
- `v_last_close`: latest close per ticker
- `v_daily_returns`: daily close-to-close returns
- `v_moving_averages`: SMA(5) and SMA(20)

Example queries:
```sql
SELECT * FROM v_last_close ORDER BY ticker;

SELECT ticker, date, daily_return
FROM v_daily_returns
WHERE daily_return IS NOT NULL
ORDER BY date DESC
LIMIT 10;

SELECT * FROM v_moving_averages
ORDER BY ticker, date DESC
LIMIT 10;
```

---

## Export KPI datasets to CSV (pgAdmin)

1. In pgAdmin → Query Tool, run for example:
```sql
SELECT * FROM v_last_close ORDER BY ticker;
```

2. Use the results grid **Download/Export → CSV**
3. Save to: `data/processed/v_last_close.csv`

Repeat for:
- `v_daily_returns` → `data/processed/v_daily_returns.csv`
- `v_moving_averages` → `data/processed/v_moving_averages.csv`

---

## Data Quality Checks (recommended)

```sql
-- duplicates (should be empty due to PK)
SELECT ticker, date, COUNT(*) AS n
FROM stg_prices
GROUP BY ticker, date
HAVING COUNT(*) > 1;

-- basic OHLC consistency
SELECT *
FROM stg_prices
WHERE high < low
   OR close < low OR close > high
   OR open < low OR open > high
LIMIT 50;
```

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'dotenv'`
You are likely running the **system Python** instead of the venv.
Activate the venv and reinstall dependencies:
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### `FileNotFoundError` for local tickers
- Ensure the file exists in `data/raw/` and is named exactly like the ticker: `AAPL.csv`, `MSFT.xlsx`, etc.
- Ensure `LOCAL_DATA_DIR=data/raw`

### `EmptyDataError: No columns to parse from file`
- The file is empty or has no header row.
- Ensure your file contains columns: `Date,Open,High,Low,Close,Volume`

### Browser can’t open `localhost:5432`
- Use pgAdmin/psql; do not open `http://localhost:5432/` in a browser.

---

## Future Improvements
- Automatic KPI export to `data/processed/` via a Python script (no manual pgAdmin export)
- Add unit tests for transformations
- Add CI (GitHub Actions) to run linting/tests
- Optional: expose KPIs via a small FastAPI service
