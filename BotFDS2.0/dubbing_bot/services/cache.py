# services/cache.py
from redis import asyncio as redis

async def get_cached_report(user_id: int):
    cache = redis.Redis()
    return await cache.get(f"report:{user_id}")