import os
import logging
import requests
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# ==================== НАСТРОЙКА ====================
# Загружаем переменные окружения из файла .env
env_path = r'D:\BotFDS2.0\.env'  # Полный путь к файлу
load_dotenv(env_path)

# Получаем токен бота
BOT_TOKEN = os.getenv('BOT_TOKEN')

# ★★★ КРИТИЧЕСКИ ВАЖНАЯ ПРОВЕРКА ★★★
if not BOT_TOKEN:
    print("❌ ОШИБКА: Токен не найден!")
    print("Проверьте что в файле .env есть строка:")
    print("BOT_TOKEN=ваш_токен_здесь")
    exit(1)

# Настраиваем подробное логирование для отладки
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # ★ Меняем на DEBUG для подробных логов ★
)
logger = logging.getLogger(__name__)


# ==================== ФУНКЦИИ БОТА ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /start
    Создает главное меню с inline-кнопками
    """
    try:
        # Создаем клавиатуру с кнопками
        keyboard = [
            [InlineKeyboardButton("🔍 Начать поиск", callback_data="search_start")],
            [InlineKeyboardButton("ℹ️ Помощь", callback_data="help_info"),
             InlineKeyboardButton("⚙️ Настройки", callback_data="settings")],
            [InlineKeyboardButton("📊 Статистика", callback_data="stats")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляем сообщение с клавиатурой
        await update.message.reply_text(
            f"👋 Привет, {update.effective_user.first_name}!\n\n"
            "Я бот для поиска информации. Выберите действие:",
            reply_markup=reply_markup
        )

        logger.info(f"Отправлено меню пользователю {update.effective_user.id}")

    except Exception as e:
        logger.error(f"Ошибка в start: {e}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = (
        "🤖 **Справка по боту**\n\n"
        "• /start - показать главное меню\n"
        "• /help - эта справка\n\n"
        "**Кнопки:**\n"
        "• 🔍 Поиск - начать поиск информации\n"
        "• ⚙️ Настройки - настройки бота\n"
        "• 📊 Статистика - ваша статистика"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    ★★★ ГЛАВНЫЙ ОБРАБОТЧИК НАЖАТИЙ НА КНОПКИ ★★★
    Эта функция обрабатывает ВСЕ callback запросы от inline-кнопок
    """
    try:
        # Получаем запрос
        query = update.callback_query
        user_id = query.from_user.id
        callback_data = query.data

        logger.debug(f"Получен callback от {user_id}: {callback_data}")

        # ★★★ ОБЯЗАТЕЛЬНО: подтверждаем получение запроса ★★★
        await query.answer()
        logger.debug("Callback подтвержден")

        # Обрабатываем разные типы кнопок
        if callback_data == "search_start":
            await handle_search(query)

        elif callback_data == "help_info":
            await handle_help(query)

        elif callback_data == "settings":
            await handle_settings(query)

        elif callback_data == "stats":
            await handle_stats(query)

        else:
            await query.edit_message_text("❌ Неизвестная команда")

    except Exception as e:
        logger.error(f"Ошибка в обработчике кнопок: {e}")
        # Пытаемся ответить даже при ошибке
        try:
            await query.answer("⚠️ Произошла ошибка")
        except:
            pass


async def handle_search(query) -> None:
    """Обработка кнопки поиска"""
    try:
        # Создаем новую клавиатуру для поиска
        keyboard = [
            [InlineKeyboardButton("📁 База данных", callback_data="search_db")],
            [InlineKeyboardButton("🌐 Интернет", callback_data="search_web")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
        ]

        await query.edit_message_text(
            "🔍 **Режим поиска**\n\n"
            "Выберите где искать:",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        logger.info(f"Пользователь {query.from_user.id} начал поиск")

    except Exception as e:
        logger.error(f"Ошибка в handle_search: {e}")


async def handle_help(query) -> None:
    """Обработка кнопки помощи"""
    help_text = (
        "❓ **Помощь**\n\n"
        "• Нажмите 'Начать поиск' для поиска информации\n"
        "• Используйте кнопки для навигации\n"
        "• /help - показать эту справку"
    )

    await query.edit_message_text(
        help_text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
        ])
    )


async def handle_settings(query) -> None:
    """Обработка кнопки настроек"""
    await query.edit_message_text(
        "⚙️ **Настройки**\n\n"
        "Здесь будут настройки вашего аккаунта",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
        ])
    )


async def handle_stats(query) -> None:
    """Обработка кнопки статистики"""
    stats_text = (
        "📊 **Ваша статистика**\n\n"
        "• Поисков: 12\n"
        "• Найдено: 45 результатов\n"
        "• Активность: 3 дня\n\n"
        "_Статистика обновляется автоматически_"
    )

    await query.edit_message_text(
        stats_text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Обновить", callback_data="stats_refresh"),
             InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
        ])
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    text = update.message.text
    user_id = update.effective_user.id

    logger.debug(f"Текстовое сообщение от {user_id}: {text}")

    # Если это не команда, предлагаем использовать меню
    if not text.startswith('/'):
        await update.message.reply_text(
            "🤖 Используйте кнопки меню или команды!\n"
            "Напишите /start для показа меню."
        )


# ==================== ЗАПУСК БОТА ====================

def cleanup_old_updates():
    """
    Очищаем старые updates чтобы избежать проблем
    """
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset=-1"
        response = requests.get(url)
        logger.info("Старые updates очищены")
    except Exception as e:
        logger.warning(f"Не удалось очистить updates: {e}")


def main() -> None:
    """Основная функция запуска бота"""
    try:
        logger.info("🚀 Запуск бота...")

        # Создаем приложение
        application = Application.builder().token(BOT_TOKEN).build()

        # ★★★ РЕГИСТРИРУЕМ ОБРАБОТЧИКИ ★★★

        # 1. Обработчики команд
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))

        # 2. ★★★ САМОЕ ВАЖНОЕ: Обработчик callback запросов ★★★
        application.add_handler(CallbackQueryHandler(handle_callback_query))

        # 3. Обработчик текстовых сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Очищаем старые updates перед запуском
        cleanup_old_updates()

        logger.info("✅ Обработчики зарегистрированы")
        logger.info("📋 Зарегистрированные обработчики:")
        for i, handler in enumerate(application.handlers[0]):
            logger.info(f"  {i + 1}. {handler.callback.__name__}")

        # ★★★ ЗАПУСКАЕМ БОТА С ПРАВИЛЬНЫМИ ПАРАМЕТРАМИ ★★★
        logger.info("🔄 Запускаем polling...")

        application.run_polling(
            poll_interval=1.0,  # Интервал опроса
            timeout=10,  # Таймаут запроса
            drop_pending_updates=True,  # ★ Очищаем старые updates ★
            allowed_updates=['message', 'callback_query']  # ★ Разрешаем callback ★
        )

    except Exception as e:
        logger.critical(f"❌ Критическая ошибка при запуске: {e}")
        raise


if __name__ == '__main__':
    # Выводим информацию о запуске
    print("=" * 50)
    print("🤖 BOT FDS 2.0 - ЗАПУСК")
    print("=" * 50)
    print(f"Токен: {BOT_TOKEN[:15]}...")
    print("Режим: DEBUG (подробное логирование)")
    print("=" * 50)

    main()