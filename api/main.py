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

# Endpoint: fact_messages with filters + pagination + error handling
@app.get("/fact_messages")
def get_fact_messages(
    channel: str | None = Query(None, description="Filter by channel name"),
    day: str | None = Query(None, description="Filter by day (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Number of records per page"),
    db: Session = Depends(get_db)
):
    try:
        base_query = "SELECT * FROM raw.fact_messages WHERE 1=1"
        params = {}

        if channel:
            base_query += " AND channel_name = :channel"
            params["channel"] = channel
        if day:
            base_query += " AND day = :day"
            params["day"] = day

        base_query += " ORDER BY day DESC LIMIT :limit OFFSET :offset"
        params["limit"] = limit
        params["offset"] = (page - 1) * limit

        query = sa.text(base_query)
        result = db.execute(query, params).fetchall()
        return [dict(row._mapping) for row in result]
    except Exception as e:
        return {"error": f"Failed to fetch fact_messages: {str(e)}"}

# Endpoint: dim_channels with error handling
@app.get("/dim_channels")
def get_dim_channels(db: Session = Depends(get_db)):
    try:
        query = sa.text("SELECT * FROM raw.dim_channels")
        result = db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]
    except Exception as e:
        return {"error": f"Failed to fetch dim_channels: {str(e)}"}
@app.get("/top_channels")
def get_top_channels(
    limit: int = Query(10, ge=1, le=50, description="Number of top channels to return"),
    db: Session = Depends(get_db)
):
    try:
        query = sa.text("""
            SELECT channel_name, COUNT(*) AS message_count
            FROM raw.fact_messages
            GROUP BY channel_name
            ORDER BY message_count DESC
            LIMIT :limit
        """)
        result = db.execute(query, {"limit": limit}).fetchall()
        return [dict(row._mapping) for row in result]
    except Exception as e:
        return {"error": f"Failed to fetch top channels: {str(e)}"}
@app.get("/daily_activity")
def get_daily_activity(db: Session = Depends(get_db)):
    try:
        query = sa.text("""
            SELECT day, COUNT(*) AS message_count
            FROM raw.fact_messages
            GROUP BY day
            ORDER BY day ASC
        """)
        result = db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]
    except Exception as e:
        return {"error": f"Failed to fetch daily activity: {str(e)}"}
@app.get("/image_stats")
def get_image_stats(db: Session = Depends(get_db)):
    try:
        query = sa.text("""
            SELECT channel_name, object_label, COUNT(*) AS count
            FROM raw.image_enrichment
            GROUP BY channel_name, object_label
            ORDER BY count DESC
        """)
        result = db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]
    except Exception as e:
        return {"error": f"Failed to fetch image stats: {str(e)}"}
@app.get("/error_logs")
def get_error_logs(limit: int = Query(50, ge=1, le=200), db: Session = Depends(get_db)):
    try:
        query = sa.text("""
            SELECT timestamp, error_message, source
            FROM raw.error_logs
            ORDER BY timestamp DESC
            LIMIT :limit
        """)
        result = db.execute(query, {"limit": limit}).fetchall()
        return [dict(row._mapping) for row in result]
    except Exception as e:
        return {"error": f"Failed to fetch error logs: {str(e)}"}

