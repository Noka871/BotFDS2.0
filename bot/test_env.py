# test_env.py
import os
from dotenv import load_dotenv

env_path = r'D:\BotFDS2.0\.env'
print(f"Проверяем путь: {env_path}")

if os.path.exists(env_path):
    print("✅ Файл .env существует")
    load_dotenv(env_path)
    token = os.getenv('BOT_TELEGRAMMA')
    if token:
        print("✅ Токен найден")
        print(f"Длина токена: {len(token)} символов")
        print(f"Начинается с: {token[:10]}...")
    else:
        print("❌ Токен НЕ найден")
        print("Проверьте написание: BOT_TELEGRAMMA")
else:
    print("❌ Файл .env НЕ существует")
    print("Создайте файл или проверьте путь")