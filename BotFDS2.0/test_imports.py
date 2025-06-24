try:
    import aiogram
    import sqlalchemy
    from dotenv import load_dotenv
    print("✅ Все зависимости установлены корректно!")
except ImportError as e:
    print(f"❌ Ошибка: {e}")