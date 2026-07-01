# medical-telegram-warehouse
# 📦 Medical Telegram Warehouse

Medical Telegram Warehouse is a data pipeline project that scrapes Telegram channels, stores raw data in PostgreSQL, transforms it with dbt, enriches images with YOLOv8, and exposes analytical APIs via FastAPI orchestrated by Dagster.

---

## 📂 Project Structure

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

