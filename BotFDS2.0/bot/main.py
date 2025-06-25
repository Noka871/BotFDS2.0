# Точка входа
import sys
from pathlib import Path

# Добавляем путь к проекту в PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from aiogram import Dispatcher
from bot.loader import bot, dp
from bot.handlers import common, admin, dubbing, timer, errors
from bot.middlewares.user_middleware import UserMiddleware


async def main():
    # Регистрация middleware
    dp.update.middleware(UserMiddleware())

    # Регистрация обработчиков
    common.register_handlers(dp)
    admin.register_handlers(dp)
    dubbing.register_handlers(dp)
    timer.register_handlers(dp)
    errors.register_handlers(dp)

    # Запуск бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())