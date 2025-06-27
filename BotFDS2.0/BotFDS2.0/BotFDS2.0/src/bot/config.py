# Конфигурация бота
import os
from dotenv import load_dotenv
from pathlib import Path

# Загружаем .env из корня проекта
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(env_path)

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
    DB_PATH = os.getenv('DB_PATH', 'database.db')

config = Config()

