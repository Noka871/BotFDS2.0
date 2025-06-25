# Главный файл для запуска бота
import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN
from handlers import register_handlers

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)