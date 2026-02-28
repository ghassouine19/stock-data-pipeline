from sqlalchemy import create_engine, text
from src.pipeline.config import DATABASE_URL

print("DATABASE_URL =", DATABASE_URL)

engine = create_engine(DATABASE_URL, future=True)

with engine.connect() as conn:
    value = conn.execute(text("SELECT 1")).scalar()
    print("SELECT 1 =>", value)