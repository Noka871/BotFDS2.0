import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from handlers import common, dubber, timer, admin
from utils.states import register_handlers_common
from services.scheduler import setup_scheduler


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token="ваш_токен_бота")
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    # Регистрация хэндлеров
    register_handlers_common(dp)
    admin.register_handlers_admin(dp)
    dubber.register_handlers_dubber(dp)
    timer.register_handlers_timer(dp)

    # Настройка планировщика
    setup_scheduler(bot)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())