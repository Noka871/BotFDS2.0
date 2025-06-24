import asyncio
from aiogram import executor
from core.bot import dp
from handlers import register_all_handlers
from services.scheduler import start_scheduler

async def on_startup(_):
    register_all_handlers(dp)
    start_scheduler()

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)