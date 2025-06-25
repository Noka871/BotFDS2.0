# Конфигурация
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DB_URL = os.getenv("DB_URL")
    REDIS_URL = os.getenv("REDIS_URL")
    ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS").split(",")))