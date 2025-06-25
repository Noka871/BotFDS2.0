# Точка входа
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config
from bot.handlers import setup_handlers
from bot.middlewares import setup_middlewares


async def main():
    config = Config.load()

    # Инициализация бота и диспетчера
    bot = Bot(token=config.bot.token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Настройка middleware
    setup_middlewares(dp, config)

    # Настройка обработчиков
    setup_handlers(dp)

    # Запуск бота
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())