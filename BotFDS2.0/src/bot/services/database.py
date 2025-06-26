# Работа с БД
import aiosqlite
import logging
from pathlib import Path
from .config import config

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Path(__file__).parent.parent.parent / config.DB_PATH


    async def __aenter__(self):
        self.conn = await aiosqlite.connect(self.db_path)
        self.conn.row_factory = aiosqlite.Row
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()

    async def execute(self, query, params=(), fetchone=False, fetchall=False, commit=False):
        async with self as db:
            cursor = await db.conn.execute(query, params)
            if commit:
                await db.conn.commit()
            if fetchone:
                return await cursor.fetchone()
            if fetchall:
                return await cursor.fetchall()
            return cursor

    async def init_db(self):
        queries = [
            """CREATE TABLE IF NOT EXISTS users
               (
                   user_id
                   INTEGER
                   PRIMARY
                   KEY,
                   username
                   TEXT,
                   role
                   TEXT,
                   created_at
                   TIMESTAMP
                   DEFAULT
                   CURRENT_TIMESTAMP
               )""",
            """CREATE TABLE IF NOT EXISTS titles
               (
                   id
                   INTEGER
                   PRIMARY
                   KEY
                   AUTOINCREMENT,
                   name
                   TEXT
                   UNIQUE,
                   episodes
                   INTEGER,
                   created_by
                   INTEGER
               )""",
            """CREATE TABLE IF NOT EXISTS reports
               (
                   id
                   INTEGER
                   PRIMARY
                   KEY
                   AUTOINCREMENT,
                   user_id
                   INTEGER,
                   title
                   TEXT,
                   episode
                   INTEGER,
                   status
                   TEXT,
                   comment
                   TEXT,
                   created_at
                   TIMESTAMP
                   DEFAULT
                   CURRENT_TIMESTAMP
               )"""
        ]
        async with self as db:
            for query in queries:
                await db.conn.execute(query)
            await db.conn.commit()

    async def set_user_role(self, user_id, role, username=None):
        await self.execute(
            """INSERT OR REPLACE INTO users (user_id, username, role)
               VALUES (?, ?, ?)""",
            (user_id, username, role),
            commit=True
        )

    async def get_user_titles(self, user_id):
        result = await self.execute(
            "SELECT name FROM titles WHERE created_by = ?",
            (user_id,),
            fetchall=True
        )
        return [row['name'] for row in result] if result else []