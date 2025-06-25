from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = list(map(int, os.getenv("ADMINS").split(',')))

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)