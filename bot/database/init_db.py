import aiosqlite
import os
from pathlib import Path
from ..logger import logger


async def init_database():
    """Инициализация базы данных"""
    try:
        # Создаем папку для БД если ее нет
        db_dir = Path("database")
        db_dir.mkdir(exist_ok=True)

        db_path = db_dir / "bot.db"

        async with aiosqlite.connect(db_path) as db:
            # Включаем foreign keys
            await db.execute("PRAGMA foreign_keys = ON")

            # Таблица пользователей
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    full_name TEXT,
                    role TEXT DEFAULT 'dubber',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Таблица тайтлов
            await db.execute('''
                CREATE TABLE IF NOT EXISTS titles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    total_episodes INTEGER,
                    current_episode INTEGER DEFAULT 1,
                    created_by INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')

            # Таблица связи пользователей и тайтлов
            await db.execute('''
                CREATE TABLE IF NOT EXISTS user_titles (
                    user_id INTEGER,
                    title_id INTEGER,
                    is_active BOOLEAN DEFAULT TRUE,
                    PRIMARY KEY (user_id, title_id),
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (title_id) REFERENCES titles (id)
                )
            ''')

            # Таблица отчетов
            await db.execute('''
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    title_id INTEGER,
                    episode INTEGER,
                    status TEXT,
                    comment TEXT,
                    report_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    deadline DATETIME,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (title_id) REFERENCES titles (id)
                )
            ''')

            # Таблица форс-мажоров
            await db.execute('''
                CREATE TABLE IF NOT EXISTS force_majeure (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    message TEXT,
                    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_resolved BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            await db.commit()

        logger.info("Database initialized successfully")
        return db_path

    except Exception as e:
        logger.error(f"Error initializing database: {e}", exc_info=True)
        raise