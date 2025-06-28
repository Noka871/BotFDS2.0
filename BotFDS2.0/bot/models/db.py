import sqlite3
from config import DB_PATH

# Создание таблиц при первом запуске
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        role TEXT  # 'dubber', 'timer', 'admin'
    )
    """)

    # Таблица тайтлов
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS titles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        episodes INTEGER,
        dubbers TEXT  # Список ID дабберов через запятую
    )
    """)

    conn.commit()
    conn.close()

# Пример функции для добавления пользователя
def add_user(user_id: int, username: str, role: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO users VALUES (?, ?, ?)",
        (user_id, username, role)
    )
    conn.commit()
    conn.close()