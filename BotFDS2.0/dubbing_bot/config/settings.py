import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))
    DB_URL = os.getenv("DB_URL", "sqlite+aiosqlite:///db.sqlite3")

settings = Settings()