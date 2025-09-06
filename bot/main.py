import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# ==================== ИМПОРТЫ КОНФИГУРАЦИИ ====================
from config import BOT_TOKEN  # Импорт токена бота из config.py

# ==================== ИМПОРТЫ ОБРАБОТЧИКОВ ====================
# Основные обработчики (команды /start, /menu и т.д.)
from handlers.common import register_common_handlers

# Обработчики функционала даббера (ВЫ ДОБАВЛЯЕТЕ ЭТОТ ИМПОРТ!)
from handlers.dubber import register_dubber_handlers

# Обработчики функционала таймера
from handlers.timer import register_timer_handlers

# Обработчики функционала администратора
from handlers.admin import register_admin_handlers

# ==================== ИМПОРТЫ БАЗЫ ДАННЫХ ====================
from database.database import init_db  # Функция инициализации БД
from database.models import Base  # Модели SQLAlchemy

# ==================== НАСТРОЙКА ЛОГГИРОВАНИЯ ====================
# Настройка формата логов для удобного отслеживания работы бота
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)  # Создаем логгер для этого модуля


async def main():
    """
    Основная функция запуска бота.
    Инициализирует все компоненты и запускает polling.
    """

    # ==================== ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ ====================
    logger.info("🔄 Инициализация базы данных...")
    try:
        # Создаем все таблицы, если они еще не существуют
        init_db()
        logger.info("✅ База данных успешно инициализирована")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации базы данных: {e}")
        return  # Завершаем работу при ошибке БД

    # ==================== ИНИЦИАЛИЗАЦИЯ БОТА И ДИСПЕТЧЕРА ====================
    logger.info("🔄 Инициализация бота...")
    try:
        # Создаем экземпляр бота с токеном из config.py
        bot = Bot(token=BOT_TOKEN)

        # Используем MemoryStorage для хранения состояний FSM
        storage = MemoryStorage()

        # Создаем диспетчер для обработки updates
        dp = Dispatcher(bot, storage=storage)

        logger.info("✅ Бот и диспетчер успешно инициализированы")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации бота: {e}")
        return

    # ==================== РЕГИСТРАЦИЯ ОБРАБОТЧИКОВ ====================
    logger.info("🔄 Регистрация обработчиков...")

    try:
        # 1. Регистрируем общие обработчики (команды /start, /help, /menu)
        register_common_handlers(dp)
        logger.info("✅ Общие обработчики зарегистрированы")

        # 2. Регистрируем обработчики даббера (ВЫ ДОБАВЛЯЕТЕ ЭТУ СТРОЧКУ!)
        register_dubber_handlers(dp)
        logger.info("✅ Обработчики даббера зарегистрированы")

        # 3. Регистрируем обработчики таймера
        register_timer_handlers(dp)
        logger.info("✅ Обработчики таймера зарегистрированы")

        # 4. Регистрируем обработчики администратора
        register_admin_handlers(dp)
        logger.info("✅ Обработчики администратора зарегистрированы")

    except Exception as e:
        logger.error(f"❌ Ошибка регистрации обработчиков: {e}")
        return

    # ==================== ЗАПУСК БОТА ====================
    logger.info("🚀 Запуск бота...")
    logger.info(f"📊 Режим: Development")
    logger.info(f"👤 Бот: @{bot._me.username if bot._me else 'Unknown'}")

    try:
        # Запускаем long-polling для получения updates
        await dp.start_polling()

    except KeyboardInterrupt:
        # Корректное завершение по Ctrl+C
        logger.info("⏹️ Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка в работе бота: {e}")
    finally:
        # Всегда закрываем сессию бота при завершении
        await bot.close()
        logger.info("👋 Бот завершил работу")


# ==================== ТОЧКА ВХОДА ====================
if __name__ == '__main__':
    """
    Точка входа в приложение.
    Запускает асинхронную функцию main().
    """
    try:
        # Запускаем асинхронный event loop
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 До свидания!")
    except Exception as e:
        print(f"❌ Непредвиденная ошибка: {e}")