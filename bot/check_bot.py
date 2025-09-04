import requests
from dotenv import load_dotenv
import os

# Загружаем токен
load_dotenv(r'D:\BotFDS2.0\.env')
BOT_TOKEN = os.getenv('BOT_TOKEN')

print("🔍 ДИАГНОСТИКА БОТА")
print("=" * 40)

# 1. Проверяем токен
print("1. Проверка токена...")
url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
response = requests.get(url)
if response.status_code == 200:
    print("   ✅ Токен рабочий")
    bot_info = response.json()
    print(f"   Имя бота: {bot_info['result']['first_name']}")
    print(f"   Username: @{bot_info['result']['username']}")
else:
    print("   ❌ Токен невалидный!")
    print(f"   Ошибка: {response.json()}")

# 2. Проверяем webhook info
print("\n2. Проверка webhook...")
url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
response = requests.get(url)
webhook_info = response.json()
print(f"   Webhook URL: {webhook_info['result']['url']}")
print(f"   Has pending updates: {webhook_info['result']['has_pending_updates']}")

# 3. Очищаем старые updates
print("\n3. Очистка старых updates...")
url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset=-1"
response = requests.get(url)
print("   ✅ Старые updates очищены")

print("\n" + "=" * 40)
print("🎯 Диагностика завершена!")
print("Запустите бота: python bot_fixed.py")