import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

from .logger import setup_logger, logger
from .database.init_db import init_database
from .database.db import close_db_connection
from .error_handler import register_error_handlers
from .utils.notifications import start_notification_scheduler

# Настраиваем логирование
setup_logger()

load_dotenv()


async def main():
    try:
        logger.info("Starting bot...")

        # Инициализация БД
        await init_database()

        bot = Bot(token=os.getenv('BOT_TOKEN'))
        dp = Dispatcher(storage=MemoryStorage())

        # Запускаем систему уведомлений
        await start_notification_scheduler(bot)

        # Регистрируем обработчики ошибок
        register_error_handlers(dp)

        # Импортируем роутеры после инициализации
        from .handlers import start, dubbing, timer, admin

        # Регистрация роутеров
        dp.include_router(start.router)
        dp.include_router(dubbing.router)
        dp.include_router(timer.router)
        dp.include_router(admin.router)

        logger.info("Bot started successfully")
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Failed to start bot: {e}", exc_info=True)
        raise
    finally:
        # Всегда закрываем соединение с БД
        await close_db_connection()
        logger.info("Database connection closed")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)