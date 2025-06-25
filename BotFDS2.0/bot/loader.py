# Инициализация бота и диспетчера
from aiogram import Bot, Dispatcher
from bot.config import config

bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()