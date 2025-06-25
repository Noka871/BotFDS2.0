# Middleware для работы с пользователями
from aiogram import BaseMiddleware
from typing import Callable, Awaitable
from aiogram.types import TelegramObject

class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict
    ) -> Any:
        # Здесь можно добавить логику работы с пользователем
        return await handler(event, data)

    