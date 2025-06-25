# Работа с БД
import asyncpg
from config import Config

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(Config.DB_URL)

    async def get_user_titles(self, user_id: int):
        async with self.pool.acquire() as conn:
            return await conn.fetch(
                "SELECT title FROM user_titles WHERE user_id = $1",
                user_id
            )