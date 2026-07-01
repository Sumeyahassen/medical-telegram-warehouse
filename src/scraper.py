import os, json, logging
from datetime import datetime
from telethon import TelegramClient
from dotenv import load_dotenv

# Load secrets
load_dotenv()
api_id = int(os.getenv("TELEGRAM_API_ID")) # type: ignore
api_hash = os.getenv("TELEGRAM_API_HASH")
phone = os.getenv("TELEGRAM_PHONE")

# Logging setup
logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

client = TelegramClient("session", api_id, api_hash)

async def scrape_channel(channel_name, limit=100):
    messages_data = []
    today = datetime.today().strftime("%Y-%m-%d")
    json_dir = f"data/raw/telegram_messages/{today}"
    img_dir = f"data/raw/images/{channel_name}"
    os.makedirs(json_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    async for msg in client.iter_messages(channel_name, limit=limit):
        record = {
            "message_id": msg.id,
            "date": str(msg.date),
            "text": msg.text,
            "views": msg.views,
            "forwards": msg.forwards,
            "has_media": bool(msg.photo)
        }
        messages_data.append(record)

        if msg.photo:
            img_path = f"{img_dir}/{msg.id}.jpg"
            await msg.download_media(img_path)

    # Save JSON
    with open(f"{json_dir}/{channel_name}.json", "w", encoding="utf-8") as f:
        json.dump(messages_data, f, ensure_ascii=False, indent=2)

    logging.info(f"Scraped {len(messages_data)} messages from {channel_name}")

async def main():
    await client.start(phone=phone) # type: ignore
    channels = ["CheMed", "LobeliaCosmetics", "TikvahPharma"]
    for ch in channels:
        await scrape_channel(ch)

with client:
    client.loop.run_until_complete(main())
