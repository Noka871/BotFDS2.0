# Конфигурация
import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')  # Токен бота из переменных окружения
ADMIN_IDS = [6383312717]            # ID администраторов