# Конфигурация
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.BOT_TOKEN = os.getenv('BOT_TOKEN')
        self.ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS', '').split(',')))
        self.DB_URL = os.getenv('DB_URL', 'sqlite+aiosqlite:///db.sqlite3')