# Точка входа
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import Config
from bot.handlers import register_handlers
from bot.middlewares import register_middlewares
from bot.utils.scheduler import setup_scheduler



async def main():
    from services.database.core import create_db
    await create_db()  # Создаём БД
    config = Config()
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    register_middlewares(dp, config)
    register_handlers(dp)
    setup_scheduler(bot)  # Планировщик для напоминаний

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())