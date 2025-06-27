from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.bot.config import config

engine = create_async_engine(config.DB_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_user_titles(user_id: int):
    async with async_session() as session:
        # Ваша логика запроса к БД
        pass

    async def test_connection():
        try:
            async with engine.connect() as conn:
                print("✅ Подключение к БД успешно!")
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")

    # Для теста:
    if __name__ == "__main__":
        import asyncio
        asyncio.run(test_connection())
