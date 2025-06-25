import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import BOT_TOKEN, REDIS_URL

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)



class Form(StatesGroup):
    role_selection = State()
    main_menu = State()
    # Состояния для дабберов
    dubber_report = State()
    # Состояния для таймеров
    timer_create_title = State()
    # Состояния для админов
    admin_tools = State()


async def on_startup(dp: Dispatcher):
    from handlers import register_handlers
    register_handlers(dp)
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("menu", "Главное меню"),
        types.BotCommand("report", "Сформировать отчет (админ)")
    ])


def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    storage = RedisStorage.from_url(REDIS_URL) if REDIS_URL else MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    dp.register_message_handler(cmd_start, commands=['start', 'menu'])

    from utils.scheduler import setup_scheduler
    setup_scheduler(dp)

    from middlewares import register_middlewares
    register_middlewares(dp)

    dp.startup.register(on_startup)

    try:
        from aiogram import executor
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        logger.exception(f"Bot crashed: {e}")
    finally:
        dp.storage.close()
        dp.storage.wait_closed()


if __name__ == '__main__':
    main()