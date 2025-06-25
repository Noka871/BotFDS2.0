# Точка входа
from aiogram import executor
from bot.handlers import register_handlers
from bot.middlewares import setup_middlewares
from bot.utils.scheduler import setup_scheduler
from config import BOT_TOKEN


async def on_startup(dp):
    setup_middlewares(dp)
    register_handlers(dp)
    setup_scheduler(dp)
    await set_default_commands(dp)


if __name__ == '__main__':
    from bot import dp

    executor.start_polling(dp, on_startup=on_startup)