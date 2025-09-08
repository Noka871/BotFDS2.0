import aiosqlite
from pathlib import Path
from datetime import datetime, timedelta
from ..logger import logger

# Глобальное соединение с БД
_db_connection = None

async def get_db_connection():
    """Получить или создать соединение с БД"""
    global _db_connection
    if _db_connection is None:
        db_path = Path("database") / "bot.db"
        _db_connection = await aiosqlite.connect(db_path)
        # Включаем foreign keys
        await _db_connection.execute("PRAGMA foreign_keys = ON")
    return _db_connection

async def close_db_connection():
    """Закрыть соединение с БД"""
    global _db_connection
    if _db_connection:
        await _db_connection.close()
        _db_connection = None

async def ensure_user_exists(user_id: int, username: str, full_name: str):
    """Убедиться, что пользователь существует в БД"""
    try:
        db = await get_db_connection()
        await db.execute(
            "INSERT OR IGNORE INTO users (id, username, full_name) VALUES (?, ?, ?)",
            (user_id, username, full_name)
        )
        await db.commit()
    except Exception as e:
        logger.error(f"Error ensuring user exists: {e}")

async def get_user_titles(user_id: int):
    """Получить тайтлы пользователя - УПРОЩЕННАЯ ВЕРСИЯ"""
    try:
        # Временная заглушка для теста
        return [{'id': 1, 'name': 'Тайтл 1114', 'current_episode': 5}]
    except Exception as e:
        logger.error(f"Error getting user titles: {e}")
        return []

async def add_report(user_id: int, title_id: int, episode: int, status: str, comment: str = None):
    """Добавить отчет о сдаче серии - ЗАГЛУШКА"""
    try:
        logger.info(f"Report: user={user_id}, title={title_id}, episode={episode}, status={status}")
        if comment:
            logger.info(f"Comment: {comment}")
        return True
    except Exception as e:
        logger.error(f"Error adding report: {e}")
        return False

async def get_user_debts(user_id: int):
    """Получить долги пользователя - УПРОЩЕННАЯ ВЕРСИЯ"""
    try:
        # Временная заглушка для теста
        return []
    except Exception as e:
        logger.error(f"Error getting user debts: {e}")
        return []

async def save_force_majeure(user_id: int, message: str):
    """Сохранить предупреждение о форс-мажоре - УПРОЩЕННАЯ ВЕРСИЯ"""
    try:
        logger.info(f"Force majeure from user {user_id}: {message}")
        return True
    except Exception as e:
        logger.error(f"Error saving force majeure: {e}")
        return False

async def add_timer_role(user_id: int):
    """Добавить пользователю роль таймера"""
    try:
        db = await get_db_connection()
        await db.execute(
            "UPDATE users SET role = 'timer' WHERE id = ?",
            (user_id,)
        )
        await db.commit()
        logger.info(f"User {user_id} granted timer role")
        return True
    except Exception as e:
        logger.error(f"Error adding timer role: {e}")
        return False