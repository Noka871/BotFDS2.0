"""
Модуль для работы с базой данных SQLite
Реализует все необходимые запросы для работы системы
"""
import sqlite3
import os
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime, timedelta

DB_NAME = "dubbing_bot.db"
TABLE_USERS = "users"
TABLE_TITLES = "titles"
TABLE_ASSIGNMENTS = "assignments"
TABLE_SUBMISSIONS = "submissions"
TABLE_WARNINGS = "warnings"
TABLE_PENALTIES = "penalties"


class Database:
    def __init__(self, db_name: str = DB_NAME):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        """Создает все необходимые таблицы"""
        # Таблица пользователей
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_USERS} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                role TEXT DEFAULT 'dubber',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Таблица тайтлов
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_TITLES} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                total_episodes INTEGER,
                current_episode INTEGER DEFAULT 1,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES {TABLE_USERS}(id)
            )
        """)

        # Таблица назначений
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_ASSIGNMENTS} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title_id INTEGER,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES {TABLE_USERS}(id),
                FOREIGN KEY (title_id) REFERENCES {TABLE_TITLES}(id),
                UNIQUE(user_id, title_id)
            )
        """)

        # Таблица сдач серий
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_SUBMISSIONS} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title_id INTEGER,
                episode INTEGER,
                status TEXT,
                comment TEXT,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                deadline TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES {TABLE_USERS}(id),
                FOREIGN KEY (title_id) REFERENCES {TABLE_TITLES}(id)
            )
        """)

        # Таблица предупреждений
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_WARNINGS} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title_id INTEGER,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES {TABLE_USERS}(id),
                FOREIGN KEY (title_id) REFERENCES {TABLE_TITLES}(id)
            )
        """)

        # Таблица штрафов
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_PENALTIES} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title_id INTEGER,
                amount REAL,
                reason TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES {TABLE_USERS}(id),
                FOREIGN KEY (title_id) REFERENCES {TABLE_TITLES}(id)
            )
        """)

        self.connection.commit()

    def add_user(self, user_id: int, username: str, first_name: str, last_name: str, role: str = "dubber"):
        """Добавляет или обновляет пользователя"""
        if not self.user_exists(user_id):
            query = f"""
            INSERT INTO {TABLE_USERS} (user_id, username, first_name, last_name, role)
            VALUES (?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (user_id, username, first_name, last_name, role))
        else:
            query = f"""
            UPDATE {TABLE_USERS} 
            SET username = ?, first_name = ?, last_name = ?
            WHERE user_id = ?
            """
            self.cursor.execute(query, (username, first_name, last_name, user_id))
        self.connection.commit()

    def get_user(self, user_id: int) -> Optional[Tuple]:
        """Возвращает данные пользователя"""
        query = f"SELECT * FROM {TABLE_USERS} WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()

    def update_user_role(self, user_id: int, role: str):
        """Обновляет роль пользователя"""
        query = f"UPDATE {TABLE_USERS} SET role = ? WHERE user_id = ?"
        self.cursor.execute(query, (role, user_id))
        self.connection.commit()

    def add_title(self, name: str, total_episodes: int, created_by: int):
        """Добавляет новый тайтл"""
        query = f"""
        INSERT INTO {TABLE_TITLES} (name, total_episodes, created_by)
        VALUES (?, ?, ?)
        """
        self.cursor.execute(query, (name, total_episodes, created_by))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_title(self, title_id: int) -> Optional[Tuple]:
        """Возвращает данные тайтла"""
        query = f"SELECT * FROM {TABLE_TITLES} WHERE id = ?"
        self.cursor.execute(query, (title_id,))
        return self.cursor.fetchone()

    def get_user_titles(self, user_id: int) -> List[Tuple]:
        """Возвращает тайтлы пользователя"""
        query = f"""
        SELECT t.* FROM {TABLE_TITLES} t
        JOIN {TABLE_ASSIGNMENTS} a ON t.id = a.title_id
        JOIN {TABLE_USERS} u ON a.user_id = u.id
        WHERE u.user_id = ?
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def assign_user_to_title(self, user_id: int, title_id: int):
        """Назначает пользователя на тайтл"""
        query = f"""
        INSERT INTO {TABLE_ASSIGNMENTS} (user_id, title_id)
        VALUES (?, ?)
        """
        try:
            self.cursor.execute(query, (user_id, title_id))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def add_submission(self, user_id: int, title_id: int, episode: int, status: str, comment: str = None):
        """Добавляет запись о сдаче серии"""
        deadline = datetime.now() + timedelta(days=2)

        query = f"""
        INSERT INTO {TABLE_SUBMISSIONS} (user_id, title_id, episode, status, comment, deadline)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (user_id, title_id, episode, status, comment, deadline))
        self.connection.commit()

    def get_user_debts(self, user_id: int) -> List[Tuple]:
        """Возвращает долги пользователя"""
        query = f"""
        SELECT t.name, s.episode, s.status, s.deadline 
        FROM {TABLE_SUBMISSIONS} s
        JOIN {TABLE_TITLES} t ON s.title_id = t.id
        WHERE s.user_id = ? AND s.status != 'submitted'
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def add_warning(self, user_id: int, title_id: int, message: str):
        """Добавляет предупреждение о форс-мажоре"""
        query = f"""
        INSERT INTO {TABLE_WARNINGS} (user_id, title_id, message)
        VALUES (?, ?, ?)
        """
        self.cursor.execute(query, (user_id, title_id, message))
        self.connection.commit()

    def user_exists(self, user_id: int) -> bool:
        """Проверяет существование пользователя"""
        query = f"SELECT 1 FROM {TABLE_USERS} WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone() is not None

    def close(self):
        """Закрывает соединение"""
        self.connection.close()