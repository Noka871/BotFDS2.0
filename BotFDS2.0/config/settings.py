import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS").split(",")]
    DB_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///database.db")

config = Settings()