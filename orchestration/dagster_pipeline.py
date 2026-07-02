from dagster import job, op
import subprocess
import os
from dagster import schedule
from orchestration.dagster_pipeline import telegram_pipeline
from dagster import op, RetryPolicy
import logging
@op(retry_policy=RetryPolicy(max_retries=3, delay=30))
def run_dbt(): # type: ignore
    logging.info("Running dbt build...")
    import subprocess
    subprocess.run(["dbt", "build", "--project-dir", "medical_warehouse"], check=True)
    logging.info("dbt build complete")
    return "dbt_build_complete"

@schedule(cron_schedule="0 0 * * *", job=telegram_pipeline, execution_timezone="Africa/Addis_Ababa")
def daily_pipeline_schedule(_context):
    # Run the pipeline every midnight
    return {}


# --- Ops (tasks) ---

@op
def scrape_telegram():
    # Run your Telethon scraper
    subprocess.run(["python", "src/scraper/telegram_scraper.py"], check=True)
    return "data/raw/messages.json"

@op
def load_to_postgres(scraped_file: str):
    # Load scraped JSON into Postgres
    subprocess.run(["python", "src/loader/load_to_postgres.py", scraped_file], check=True)
    return "raw.fact_messages"

@op
def run_dbt():
    # Build dbt models/tests
    subprocess.run(["dbt", "build", "--project-dir", "medical_warehouse"], check=True)
    return "dbt_build_complete"

@op
def run_yolo():
    # Run YOLO enrichment
    subprocess.run(["python", "src/enrichment/yolo_enrich.py"], check=True)
    return "raw.image_enrichment"

# --- Job (pipeline) ---

@job
def telegram_pipeline():
    scraped_file = scrape_telegram()
    load_to_postgres(scraped_file)
    run_dbt()
    run_yolo()
