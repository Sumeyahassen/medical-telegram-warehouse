from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from api.database import SessionLocal   # make sure api/__init__.py exists
import sqlalchemy as sa

app = FastAPI(title="Medical Telegram Warehouse API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint: fact_messages with optional filters
@app.get("/fact_messages")
def get_fact_messages(
    channel: str | None = Query(None, description="Filter by channel name"),
    day: str | None = Query(None, description="Filter by day (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    base_query = "SELECT * FROM raw.fact_messages WHERE 1=1"
    params = {}

    if channel:
        base_query += " AND channel_name = :channel"
        params["channel"] = channel
    if day:
        base_query += " AND day = :day"
        params["day"] = day

    query = sa.text(base_query)
    result = db.execute(query, params).fetchall()
    return [dict(row._mapping) for row in result]

# Endpoint: dim_channels
@app.get("/dim_channels")
def get_dim_channels(db: Session = Depends(get_db)):
    query = sa.text("SELECT * FROM raw.dim_channels")
    result = db.execute(query).fetchall()
    return [dict(row._mapping) for row in result]
