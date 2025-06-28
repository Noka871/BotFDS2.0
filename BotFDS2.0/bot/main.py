# Точка входа
import asyncio
import logging
from aiogram import Bot, Dispatcher, executor
from bot.config import BOT_TOKEN, ADMIN_IDS
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.handlers import register_common_handlers, register_admin_handlers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

async def on_startup(dp: Dispatcher):
    bot = dp.bot
    try:
        me = await bot.get_me()
        logging.info(f"Бот @{me.username} запущен")
        await bot.send_message(ADMIN_IDS[0], "🟢 Бот перезапущен!")
    except Exception as e:
        logging.error(f"Ошибка уведомления: {e}")

def main():
    if hasattr(asyncio, 'WindowsProactorEventLoopPolicy'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    # Регистрация обработчиков
    register_common_handlers(dp)
    register_admin_handlers(dp)

    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup
    )

if __name__ == "__main__":
    main()