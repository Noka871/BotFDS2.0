import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    REDIS_URL = os.getenv("REDIS_URL", None)
    ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))
    TIMEZONE = "Europe/Moscow"

# Для удобства импорта
BOT_TOKEN = Config.BOT_TOKEN
REDIS_URL = Config.REDIS_URL