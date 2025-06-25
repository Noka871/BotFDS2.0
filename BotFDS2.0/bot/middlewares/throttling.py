# Антифлуд
from aiogram import BaseMiddleware

class ThrottlingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        # Логика антифлуда
        return await handler(event, data)