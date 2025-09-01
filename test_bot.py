import asyncio
import logging
from aiogram import Bot
from aiogram.utils import exceptions
from aiogram.types import Update

# Настройка логов
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def test_bot():
    """Тестирование базовой функциональности бота"""
    try:
        # 1. Инициализация бота (ЗАМЕНИТЕ НА РЕАЛЬНЫЙ ТОКЕН)
        bot = Bot(token="7833834785:AAH_EQDJ5Ax9Viq32g9xWfy40Ve9IfmTrWk")

        # 2. Получение информации о боте (проверка токена)
        me = await bot.get_me()
        logger.info(f"Бот @{me.username} готов к работе")

        # 3. Получение chat_id (отправьте боту любое сообщение)
        updates = await bot.get_updates(offset=-1, timeout=10)
        if not updates:
            logger.error("Не найдены обновления. Отправьте боту сообщение!")
            return

        update = updates[0]  # Берем последнее обновление
        if not update.message:
            logger.error("Нет сообщений для определения chat_id")
            return

        chat_id = update.message.chat.id
        logger.info(f"Ваш chat_id: {chat_id}")

        # 4. Отправка тестового сообщения
        await bot.send_message(
            chat_id,
            "✅ Бот работает корректно!\n"
            f"Ваш ID: {chat_id}\n"
            f"Версия aiogram: 2.25.1"
        )
        logger.info("Тестовое сообщение отправлено")

    except exceptions.Unauthorized:
        logger.error("Неверный токен! Проверьте токен в @BotFather")
    except exceptions.TelegramAPIError as e:
        logger.error(f"Ошибка Telegram API: {e}")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
    finally:
        # 5. Корректное закрытие (для aiogram 2.x)
        if 'bot' in locals():
            await bot.close()


if __name__ == "__main__":
    # Особый вызов для Windows
    try:
        asyncio.run(test_bot())
    except RuntimeError as e:
        if "Event loop is closed" not in str(e):
            logger.error(f"Ошибка event loop: {e}")