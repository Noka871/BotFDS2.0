# Фильтр по ролям пользователя
from aiogram import F
from aiogram.types import Message
from aiogram.filters import BaseFilter
from services.database.repositories import UserRepository

class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message, session) -> bool:
        repo = UserRepository(session)
        user = await repo.get_user(message.from_user.id)
        return user and user.role == 'admin'