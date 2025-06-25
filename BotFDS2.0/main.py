from aiogram import executor
from config.config import dp
import handlers

async def on_startup(_):
    from data.db import init_db
    await init_db()
    print("Бот запущен")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)