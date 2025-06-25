# Работа с БД
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from bot.config import config

# Настройка подключения к БД
engine = create_async_engine(config.DB_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_user_titles(user_id: int):
    """Получение тайтлов пользователя"""
    async with async_session() as session:
        # Запрос к БД для получения тайтлов пользователя
        pass