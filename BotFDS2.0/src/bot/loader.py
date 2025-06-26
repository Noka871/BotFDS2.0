# Инициализация бота и диспетчера
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from src.bot.config import config

session = AiohttpSession()

# Проверка токена перед созданием бота
if not config.BOT_TOKEN or len(config.BOT_TOKEN) < 30:
    raise ValueError("Неверный формат токена!")

bot = Bot(
    token=config.BOT_TOKEN,
    session=session,  # Добавьте этот параметр
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher()

print("Бот инициализирован | Токен:", config.BOT_TOKEN[:10] + "...")