"""
Конфигурационный файл бота для системы управления дубляжом.

Этот файл содержит все настройки и конфигурации бота, которые
загружаются из переменных окружения или имеют значения по умолчанию.

Для работы бота необходимо создать файл .env в корневой директории
и заполнить его согласно примеру в .env.example
"""

import os
from typing import List
from dotenv import load_dotenv  # Для загрузки переменных из .env файла

# Загружаем переменные окружения из файла .env
# Если файл .env не существует, используются системные переменные окружения
load_dotenv()

# =============================================================================
# НАСТРОЙКИ БОТА
# =============================================================================

# Токен бота, полученный от @BotFather в Telegram
# Обязательная переменная! Без нее бот не запустится.
# Пример: BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

# Список ID администраторов бота (через запятую)
# Администраторы имеют полный доступ ко всем функциям бота
# Пример: ADMIN_IDS=123456789,987654321,555555555
ADMIN_IDS: List[int] = (
    list(map(int, os.getenv("ADMIN_IDS", "").split(',')))
    if os.getenv("ADMIN_IDS")
    else []
)

# URL для подключения к базе данных
# По умолчанию используется SQLite с асинхронным драйвером
# Поддерживаемые СУБД:
# - SQLite: sqlite+aiosqlite:///./bot.db
# - PostgreSQL: postgresql+asyncpg://user:password@localhost/dbname
# - MySQL: mysql+aiomysql://user:password@localhost/dbname
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bot.db")

# Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# DEBUG - максимальная детализация, подходит для разработки
# INFO - обычный уровень для production
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

# =============================================================================
# НАСТРОЙКИ БАЗЫ ДАННЫХ
# =============================================================================

# Эхо-запросы (вывод SQL запросов в консоль)
# True - показывать все SQL запросы (удобно для разработки)
# False - не показывать (рекомендуется для production)
DB_ECHO: bool = os.getenv("DB_ECHO", "False").lower() == "true"

# Размер пула соединений с базой данных
# Минимальное количество соединений в пуле
DB_POOL_MIN_SIZE: int = int(os.getenv("DB_POOL_MIN_SIZE", "5"))

# Максимальное количество соединений в пуле
DB_POOL_MAX_SIZE: int = int(os.getenv("DB_POOL_MAX_SIZE", "20"))

# Время жизни соединения в пуле (в секундах)
DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "3600"))

# =============================================================================
# НАСТРОЙКИ УВЕДОМЛЕНИЙ
# =============================================================================

# Время отправки ежедневных напоминаний (в формате ЧЧ:ММ)
# По умолчанию: 10:00 утра
REMINDER_TIME: str = os.getenv("REMINDER_TIME", "10:00")

# Количество дней для дедлайна сдачи серий после получения меток
# По умолчанию: 2 дня (как указано в ТЗ)
DEADLINE_DAYS: int = int(os.getenv("DEADLINE_DAYS", "2"))


# =============================================================================
# ПРОВЕРКИ КОНФИГУРАЦИИ
# =============================================================================

def validate_config() -> None:
    """
    Проверяет корректность конфигурации.
    Вызывает исключение, если обязательные параметры не заполнены.
    """
    if not BOT_TOKEN:
        raise ValueError(
            "❌ ОШИБКА КОНФИГУРАЦИИ: BOT_TOKEN не указан!\n"
            "Добавьте BOT_TOKEN в файл .env или переменные окружения.\n"
            "Получить токен можно у @BotFather в Telegram."
        )

    if not BOT_TOKEN.startswith('') or ':' not in BOT_TOKEN:
        raise ValueError(
            "❌ ОШИБКА КОНФИГУРАЦИИ: Неверный формат BOT_TOKEN!\n"
            "Токен должен быть в формате: 1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )

    if not DATABASE_URL:
        raise ValueError(
            "❌ ОШИБКА КОНФИГУРАЦИИ: DATABASE_URL не указан!"
        )

    # Проверяем уровень логирования
    valid_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if LOG_LEVEL not in valid_log_levels:
        raise ValueError(
            f"❌ ОШИБКА КОНФИГУРАЦИИ: Неверный LOG_LEVEL '{LOG_LEVEL}'!\n"
            f"Допустимые значения: {', '.join(valid_log_levels)}"
        )


# Автоматически проверяем конфигурацию при импорте модуля
try:
    validate_config()
except ValueError as e:
    print(f"\n{'=' * 60}")
    print("КРИТИЧЕСКАЯ ОШИБКА КОНФИГУРАЦИИ")
    print('=' * 60)
    print(e)
    print(f"{'=' * 60}\n")
    raise


# =============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =============================================================================

def get_config_summary() -> str:
    """
    Возвращает строку с краткой сводкой конфигурации.
    Useful for debugging and logging.
    """
    return (
        f"🤖 Конфигурация бота:\n"
        f"• BOT_TOKEN: {'установлен' if BOT_TOKEN else 'отсутствует'}\n"
        f"• ADMIN_IDS: {len(ADMIN_IDS)} администраторов\n"
        f"• DATABASE_URL: {DATABASE_URL.split('://')[0]}://...\n"
        f"• LOG_LEVEL: {LOG_LEVEL}\n"
        f"• REMINDER_TIME: {REMINDER_TIME}\n"
        f"• DEADLINE_DAYS: {DEADLINE_DAYS} дней"
    )


# Выводим информацию о конфигурации при запуске
if __name__ == "__main__":
    print(f"\n{'=' * 60}")
    print("КОНФИГУРАЦИЯ СИСТЕМЫ УПРАВЛЕНИЯ ДУБЛЯЖОМ")
    print('=' * 60)
    print(get_config_summary())
    print(f"{'=' * 60}\n")