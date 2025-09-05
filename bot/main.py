import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from handlers.common import router as common_router
from handlers.dubber import router as dubber_router
from handlers.timer import router as timer_router
from handlers.admin import router as admin_router
from models.database import init_db

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def set_bot_commands(bot: Bot):
    """Установка команд бота"""
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/menu", description="Главное меню"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/stats", description="Моя статистика"),
    ]
    await bot.set_my_commands(commands)


async def main():
    """Основная функция запуска бота"""
    try:
        # Инициализация базы данных
        await init_db()
        logger.info("✅ База данных инициализирована")

        # Инициализация бота и диспетчера
        bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)

        # Регистрация роутеров
        dp.include_router(common_router)
        dp.include_router(dubber_router)
        dp.include_router(timer_router)
        dp.include_router(admin_router)

        # Установка команд бота
        await set_bot_commands(bot)

        logger.info("🤖 Бот запущен и готов к работе!")
        logger.info("📊 База данных: SQLite")
        logger.info("👤 Режим: Development")

        # Запуск опроса
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())