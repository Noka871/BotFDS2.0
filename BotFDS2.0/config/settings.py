import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))

    @classmethod
    def validate(cls):
        if not cls.BOT_TOKEN:
            raise ValueError("Токен бота не указан в .env")