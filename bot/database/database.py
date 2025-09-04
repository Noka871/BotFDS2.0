"""
Модуль для работы с базой данных SQLite
Реализует все необходимые запросы для работы системы
"""
import sqlite3
import os
from typing import List, Tuple, Optional

# Константы для работы с базой данных
DB_NAME = "users.db"
TABLE_NAME = "users"

class Database:
    def __init__(self, db_name: str = DB_NAME):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Создает таблицу пользователей, если она не существует"""
        query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            phone_number TEXT,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def user_exists(self, user_id: int) -> bool:
        """Проверяет, существует ли пользователь в базе данных"""
        query = f"SELECT 1 FROM {TABLE_NAME} WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone() is not None

    def add_user(self, user_id: int, username: str, first_name: str, last_name: str, phone_number: str = None):
        """Добавляет нового пользователя в базу данных"""
        if not self.user_exists(user_id):
            query = f"""
            INSERT INTO {TABLE_NAME} (user_id, username, first_name, last_name, phone_number)
            VALUES (?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (user_id, username, first_name, last_name, phone_number))
            self.connection.commit()
            return True
        return False

    def get_user(self, user_id: int) -> Optional[Tuple]:
        """Возвращает данные пользователя по ID"""
        query = f"SELECT * FROM {TABLE_NAME} WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()

    def get_all_users(self) -> List[Tuple]:
        """Возвращает всех пользователей"""
        query = f"SELECT * FROM {TABLE_NAME}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_phone_number(self, user_id: int, phone_number: str):
        """Обновляет номер телефона пользователя"""
        query = f"UPDATE {TABLE_NAME} SET phone_number = ? WHERE user_id = ?"
        self.cursor.execute(query, (phone_number, user_id))
        self.connection.commit()

    def delete_user(self, user_id: int):
        """Удаляет пользователя из базы данных"""
        query = f"DELETE FROM {TABLE_NAME} WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        self.connection.commit()

    def get_users_count(self) -> int:
        """Возвращает количество пользователей"""
        query = f"SELECT COUNT(*) FROM {TABLE_NAME}"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def close(self):
        """Закрывает соединение с базой данных"""
        self.connection.close()

    def __enter__(self):
        """Для использования с контекстным менеджером"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Для использования с контекстным менеджером"""
        self.close()