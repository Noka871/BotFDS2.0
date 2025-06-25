# Точка входа
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import Config

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def on_startup(dp: Dispatcher):
    from bot.handlers import register_handlers
    from bot.middlewares import setup_middlewares

    setup_middlewares(dp)
    register_handlers(dp)

    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("menu", "Главное меню")
    ])


def main():
    try:
        bot = Bot(token=Config.BOT_TOKEN)
        storage = RedisStorage.from_url(Config.REDIS_URL) if Config.REDIS_URL else MemoryStorage()
        dp = Dispatcher(bot, storage=storage)

        executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")
    finally:
        if 'dp' in locals():
            dp.storage.close()


if __name__ == '__main__':
    main()