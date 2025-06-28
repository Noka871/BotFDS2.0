from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN
import handlers.common  # Импортируем обработчики

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()  # Хранилище состояний (FSM)
dp = Dispatcher(bot, storage=storage)

# Регистрируем обработчики
handlers.common.register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)