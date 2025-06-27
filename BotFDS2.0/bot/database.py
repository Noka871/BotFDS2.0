"""
Модуль для работы с базой данных SQLite
Реализует все необходимые запросы для работы системы
"""
import sqlite3
from typing import List, Dict, Optional, Union
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_name: str = DB_NAME):
        """Инициализация подключения к базе данных"""
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row  # Для доступа к полям по имени
        self.create_tables()

    def create_tables(self):
        """Создание всех таблиц, если они не существуют"""
        cursor = self.conn.cursor()
        
        # Пользователи системы
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            role TEXT CHECK(role IN ('dubber', 'timer', 'admin')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Таблица проектов (тайтлов)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS titles (
            title_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            total_episodes INTEGER NOT NULL,
            created_by INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users(user_id)
        )
        """)
        
        # Связь дабберов с тайтлами (многие ко многим)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dubber_titles (
            dubber_id INTEGER NOT NULL,
            title_id INTEGER NOT NULL,
            PRIMARY KEY (dubber_id, title_id),
            FOREIGN KEY (dubber_id) REFERENCES users(user_id),
            FOREIGN KEY (title_id) REFERENCES titles(title_id)
        )
        """)
        
        # Статусы серий
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS episodes (
            episode_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title_id INTEGER NOT NULL,
            episode_number INTEGER NOT NULL,
            dubber_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'completed', 'delayed')),
            submitted_at TIMESTAMP,
            deadline TIMESTAMP,
            penalty INTEGER DEFAULT 0,
            comment TEXT,
            FOREIGN KEY (title_id) REFERENCES titles(title_id),
            FOREIGN KEY (dubber_id) REFERENCES users(user_id),
            UNIQUE(title_id, episode_number, dubber_id)
        )
        """)
        
        # Форс-мажорные сообщения
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS force_majeure (
            fm_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        """)
        
        # Лог штрафов
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS penalty_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dubber_id INTEGER NOT NULL,
            timer_id INTEGER NOT NULL,
            title_id INTEGER NOT NULL,
            episode_number INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            reason TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (dubber_id) REFERENCES users(user_id),
            FOREIGN KEY (timer_id) REFERENCES users(user_id),
            FOREIGN KEY (title_id) REFERENCES titles(title_id)
        )
        """)
        
        self.conn.commit()

    # ========== Методы для работы с пользователями ==========
    def add_user(self, user_id: int, username: str, first_name: str, last_name: str, role: str = 'dubber'):
        """Добавление/обновление пользователя"""
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT OR REPLACE INTO users 
            (user_id, username, first_name, last_name, role) 
            VALUES (?, ?, ?, ?, ?)""",
            (user_id, username, first_name, last_name, role)
        )
        self.conn.commit()

    def get_user(self, user_id: int) -> Optional[Dict]:
        """Получение информации о пользователе"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return dict(cursor.fetchone()) if cursor.fetchone() else None

    def update_user_role(self, user_id: int, role: str):
        """Изменение роли пользователя"""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE users SET role = ? WHERE user_id = ?",
            (role, user_id)
        )
        self.conn.commit()

    # ========== Методы для работы с тайтлами ==========
    def add_title(self, name: str, total_episodes: int, created_by: int) -> int:
        """Добавление нового тайтла"""
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO titles (name, total_episodes, created_by) 
            VALUES (?, ?, ?)""",
            (name, total_episodes, created_by)
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_title(self, title_id: int) -> Optional[Dict]:
        """Получение информации о тайтле"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM titles WHERE title_id = ?", (title_id,))
        result = cursor.fetchone()
        return dict(result) if result else None

    def add_dubber_to_title(self, dubber_id: int, title_id: int):
        """Добавление даббера к тайтлу"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO dubber_titles (dubber_id, title_id) VALUES (?, ?)",
            (dubber_id, title_id)
        )
        self.conn.commit()

    def get_dubber_titles(self, dubber_id: int) -> List[Dict]:
        """Получение списка тайтлов даббера"""
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT t.title_id, t.name 
            FROM titles t
            JOIN dubber_titles dt ON t.title_id = dt.title_id
            WHERE dt.dubber_id = ?""",
            (dubber_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

    # ========== Методы для работы с сериями ==========
    def set_episode_status(self, title_id: int, episode_number: int, 
                         dubber_id: int, status: str, comment: str = None):
        """Установка статуса серии"""
        cursor = self.conn.cursor()
        
        if status == 'completed':
            submitted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            submitted_at = None
        
        cursor.execute(
            """INSERT OR REPLACE INTO episodes 
            (title_id, episode_number, dubber_id, status, submitted_at, comment) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (title_id, episode_number, dubber_id, status, submitted_at, comment)
        )
        self.conn.commit()

    def set_episode_deadline(self, title_id: int, dubber_id: int, deadline: datetime):
        """Установка дедлайна для всех серий тайтла"""
        cursor = self.conn.cursor()
        cursor.execute(
            """UPDATE episodes 
            SET deadline = ?
            WHERE title_id = ? AND dubber_id = ? AND status = 'pending'""",
            (deadline.strftime('%Y-%m-%d %H:%M:%S'), title_id, dubber_id)
        )
        self.conn.commit()

    def get_pending_episodes(self) -> List[Dict]:
        """Получение списка несданных серий"""
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT e.*, u.username, t.name as title_name
            FROM episodes e
            JOIN users u ON e.dubber_id = u.user_id
            JOIN titles t ON e.title_id = t.title_id
            WHERE e.status = 'pending' AND e.deadline IS NOT NULL"""
        )
        return [dict(row) for row in cursor.fetchall()]

    # ========== Методы для работы с штрафами ==========
    def add_penalty(self, dubber_id: int, timer_id: int, title_id: int, 
                   episode_number: int, amount: int, reason: str):
        """Добавление штрафа"""
        cursor = self.conn.cursor()
        
        # Добавляем запись в лог штрафов
        cursor.execute(
            """INSERT INTO penalty_logs 
            (dubber_id, timer_id, title_id, episode_number, amount, reason)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (dubber_id, timer_id, title_id, episode_number, amount, reason)
        )
        
        # Обновляем информацию о серии
        cursor.execute(
            """UPDATE episodes 
            SET penalty = ?, comment = ?
            WHERE title_id = ? AND episode_number = ? AND dubber_id = ?""",
            (amount, reason, title_id, episode_number, dubber_id)
        )
        
        self.conn.commit()

    def get_penalties(self, dubber_id: int = None, title_id: int = None) -> List[Dict]:
        """Получение информации о штрафах"""
        cursor = self.conn.cursor()
        query = """SELECT pl.*, u.username as dubber_name, t.name as title_name
                 FROM penalty_logs pl
                 JOIN users u ON pl.dubber_id = u.user_id
                 JOIN titles t ON pl.title_id = t.title_id"""
        params = []
        
        conditions = []
        if dubber_id:
            conditions.append("pl.dubber_id = ?")
            params.append(dubber_id)
        if title_id:
            conditions.append("pl.title_id = ?")
            params.append(title_id)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    # ========== Методы для форс-мажоров ==========
    def add_force_majeure(self, user_id: int, message: str):
        """Добавление сообщения о форс-мажоре"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO force_majeure (user_id, message) VALUES (?, ?)",
            (user_id, message)
        )
        self.conn.commit()

    def get_force_majeures(self, limit: int = 50) -> List[Dict]:
        """Получение последних форс-мажоров"""
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT fm.*, u.username 
            FROM force_majeure fm
            JOIN users u ON fm.user_id = u.user_id
            ORDER BY fm.created_at DESC
            LIMIT ?""",
            (limit,)
        )
        return [dict(row) for row in cursor.fetchall()]

    def close(self):
        """Закрытие соединения с базой данных"""
        self.conn.close()