import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN

# Импорты обработчиков для aiogram 2.x
from handlers.common import register_common_handlers
from handlers.dubber import register_dubber_handlers
from handlers.timer import register_timer_handlers
from handlers.admin import register_admin_handlers

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Основная функция запуска бота для aiogram 2.x"""
    try:
        # Инициализация бота для aiogram 2.x
        bot = Bot(token=BOT_TOKEN)
        storage = MemoryStorage()
        dp = Dispatcher(bot, storage=storage)

        # Регистрация обработчиков
        register_common_handlers(dp)
        register_dubber_handlers(dp)
        register_timer_handlers(dp)
        register_admin_handlers(dp)

        logger.info("✅ Бот инициализирован (aiogram 2.x)")
        logger.info("✅ Обработчики зарегистрированы")

        # Запускаем бота
        logger.info("🤖 Бот запущен")
        await dp.start_polling()

    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(main())