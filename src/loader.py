import os, json, psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="localhost",   
    port=5432
)

cur = conn.cursor()

def load_json(file_path, channel_name):
    with open(file_path, "r", encoding="utf-8") as f:
        messages = json.load(f)
        for msg in messages:
            cur.execute("""
                INSERT INTO raw.telegram_messages
                (message_id, channel_name, date, text, views, forwards, has_media)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (message_id) DO NOTHING;
            """, (
                msg["message_id"],
                channel_name,
                msg["date"],
                msg["text"],
                msg["views"],
                msg["forwards"],
                msg["has_media"]
            ))
    conn.commit()

def main():
    base_dir = "data/raw/telegram_messages"
    for day in os.listdir(base_dir):
        day_dir = os.path.join(base_dir, day)
        for file in os.listdir(day_dir):
            if file.endswith(".json"):
                channel = file.replace(".json", "")
                load_json(os.path.join(day_dir, file), channel)

if __name__ == "__main__":
    main()
    cur.close()
    conn.close()
