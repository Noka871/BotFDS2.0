# Работа с БД
import sqlite3
import os
from bot.config import ADMIN_IDS  # Добавляем импорт

DB_PATH = os.path.join(os.path.dirname(__file__), 'bot.db')


def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users
                   (
                       user_id
                       INTEGER
                       PRIMARY
                       KEY,
                       username
                       TEXT,
                       role
                       TEXT
                       DEFAULT
                       'dubber'
                   )
                   ''')

    # Добавляем администраторов
    for admin_id in ADMIN_IDS:
        cursor.execute(
            'INSERT OR IGNORE INTO users VALUES (?, ?, ?)',
            (admin_id, 'admin', 'admin')
        )

    conn.commit()
    conn.close()


def get_user_role(user_id):
    """Получение роли пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM users WHERE user_id = ?', (user_id,))
    role = cursor.fetchone()
    conn.close()
    return role[0] if role else 'dubber'