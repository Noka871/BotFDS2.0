# Точка входа
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import Config


async def main():
    try:
        config = Config()
        bot = Bot(token=config.BOT_TOKEN)
        dp = Dispatcher(storage=MemoryStorage())

        # Инициализация остальных компонентов
        from bot.handlers import router
        dp.include_router(router)

        print("Бот запущен!")
        await dp.start_polling(bot)

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())