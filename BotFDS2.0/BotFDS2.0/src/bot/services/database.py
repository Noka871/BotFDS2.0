# Работа с БД
async def setup_db():
    # Создаем таблицу пользователей
    await db.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        role TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    # Другие таблицы по ТЗ