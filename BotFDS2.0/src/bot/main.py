# Точка входа
# Точка входа
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties  # Добавьте этот импорт
from dotenv import load_dotenv
from os import getenv
import logging
import asyncio

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка .env
load_dotenv()

dp = Dispatcher()


@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    try:
        await message.answer(
            "🔮 <b>WitchKSH Bot</b>\n\n"
            "✨ <u>Доступные команды</u>:\n"
            "/start - Перезапуск\n"
            "/help - Помощь\n"
            "/menu - Основное меню",
            parse_mode=ParseMode.HTML
        )
        logger.info(f"Отправлено меню для {message.from_user.id}")
    except Exception as e:
        logger.error(f"Ошибка: {e}")


async def main():
    try:
        token = getenv("BOT_TOKEN")
        if not token:
            raise ValueError("Токен не найден в .env!")

        # Исправленная строка с новым способом передачи parse_mode
        bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"Ошибка запуска: {e}")


if __name__ == "__main__":
    asyncio.run(main())