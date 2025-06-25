# Работа с БД
from typing import List, Dict
import asyncpg


class Database:
    def __init__(self):
        self.pool: asyncpg.Pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=DB_DSN)

    async def get_user_titles(self, user_id: int) -> List[Dict]:
        async with self.pool.acquire() as conn:
            return await conn.fetch(
                "SELECT * FROM titles WHERE user_id = $1",
                user_id
            )