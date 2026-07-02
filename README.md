# medical-telegram-warehouse
#  Medical Telegram Warehouse

Medical Telegram Warehouse is a data pipeline project that scrapes Telegram channels, stores raw data in PostgreSQL, transforms it with dbt, enriches images with YOLOv8, and exposes analytical APIs via FastAPI orchestrated by Dagster.

---

##  Project Structure

├── .vscode/
├── .github/
├── .env
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
├── data/
├── medical_warehouse/   # dbt project
├── src/                 # scraper + loaders
├── api/                 # FastAPI app
├── notebooks/
├── tests/
└── scripts/

---

## ⚙️ Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd medical-telegram-warehouse
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=+2519xxxxxxx
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=medical_warehouse

pip install -r requirements.txt

docker-compose up

## Task 2 — Load Raw Data into PostgreSQL

###  Goal
Take the JSON files scraped in Task 1 and insert them into PostgreSQL, creating the **raw layer** of the data warehouse.

---

###  Prerequisites
- Postgres running in Docker (`docker-compose up -d db`)
- Schema and table created:
  ```sql
  CREATE SCHEMA IF NOT EXISTS raw;

  CREATE TABLE IF NOT EXISTS raw.telegram_messages (
      message_id BIGINT PRIMARY KEY,
      channel_name TEXT,
      date TIMESTAMP,
      text TEXT,
      views INT,
      forwards INT,
      has_media BOOLEAN
  );

then run 
python src/loader.py
 to verifay postger db
 ``` docker exec -it medical-telegram-warehouse-db-1 psql -U postgres -d medical_warehouse
SELECT COUNT(*) FROM raw.telegram_messages;
## Task 3 — dbt Staging Models

### Goal
Transform raw Telegram messages into a clean staging layer for analysis.

---

### Prerequisites
- dbt installed (`pip install dbt-postgres`)
- `profiles.yml` configured with correct Postgres credentials
- Raw data loaded into `raw.telegram_messages`

---

### File Locations
- **Staging model** → `medical_warehouse/models/staging/stg_telegram_messages.sql`
- **Schema tests** → `medical_warehouse/models/staging/schema.yml`

---

### How to Run
```bash
dbt run --select stg_telegram_messages
dbt test --select stg_telegram_messages

##  Task 4 — dbt Marts

###  Goal
Build fact and dimension tables from the staging layer to support analytics and API queries.

---

###  Prerequisites
- Task 3 completed (staging models exist and tested).
- dbt connected to Postgres with working `profiles.yml`.
- Raw and staging schemas available in the database.

---

###  File Locations
- **Fact model** → `medical_warehouse/models/marts/fact_messages.sql`
- **Dimension model** → `medical_warehouse/models/marts/dim_channels.sql`
- **Schema tests** → `medical_warehouse/models/marts/schema.yml`

---

### How to Run
```bash
dbt run --select fact_messages
dbt run --select dim_channels
dbt test --select fact_messages dim_channels
##  Task 5 — FastAPI Integration

###  Goal
Expose dbt marts (`fact_messages`, `dim_channels`) as REST API endpoints for analytics and dashboards.

---

### 🛠️ Prerequisites
- Task 4 completed (marts created and tested).
- PostgreSQL running with dbt models built.
- Python virtual environment with FastAPI + SQLAlchemy installed.

---

###  File Locations
- **API entrypoint** → `api/main.py`
- **Database connection** → `api/database.py`
- **Package marker** → `api/__init__.py`

---

###  How to Run
```bash
uvicorn api.main:app --reload --port 8001



