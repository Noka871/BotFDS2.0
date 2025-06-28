import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Токен из .env
ADMIN_IDS = [123456789]             # ID админов (можно несколько)

# Путь к базе данных
DB_PATH = "database.db"