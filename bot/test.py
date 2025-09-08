print("✅ Python работает!")
print("Тестируем импорты...")

try:
    from bot.main import main
    print("✅ Модуль bot.main найден")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")

input("Нажмите Enter для выхода...")