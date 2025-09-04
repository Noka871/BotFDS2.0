import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from telegram.constants import ParseMode

# ==================== НАСТРОЙКА ====================
# Загружаем переменные окружения
env_path = r'D:\BotFDS2.0\.env'
load_dotenv(env_path)

# Получаем токен бота
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Проверка токена
if not BOT_TOKEN:
    print("❌ ОШИБКА: Токен не найден!")
    exit(1)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# ==================== ЭМОЦИ И СТИЛЬ ====================
class Styles:
    """Класс для хранения стилей и эмодзи"""
    # Эмодзи
    SEARCH = "🔍"
    HELP = "❓"
    SETTINGS = "⚙️"
    STATS = "📊"
    BACK = "⬅️"
    RELOAD = "🔄"
    HOME = "🏠"
    DATABASE = "💾"
    INTERNET = "🌐"
    CROWN = "👑"
    WIZARD = "🧙"

    # Цветовые стили (для HTML разметки)
    class Colors:
        PRIMARY = "#2E86AB"
        SUCCESS = "#27AE60"
        WARNING = "#F39C12"
        DANGER = "#E74C3C"
        INFO = "#3498DB"

    # Текстовые стили
    @staticmethod
    def bold(text):
        return f"<b>{text}</b>"

    @staticmethod
    def italic(text):
        return f"<i>{text}</i>"

    @staticmethod
    def code(text):
        return f"<code>{text}</code>"

    @staticmethod
    def link(url, text):
        return f'<a href="{url}">{text}</a>'


# ==================== КЛАВИАТУРЫ ====================
class Keyboards:
    """Класс для создания красивых клавиатур"""

    @staticmethod
    def main_menu(user_id, is_admin=False):
        """Главное меню с красивыми кнопками"""
        keyboard = [
            # Первый ряд - основные действия
            [
                InlineKeyboardButton(
                    f"{Styles.SEARCH} Поиск",
                    callback_data="search_start"
                )
            ],
            # Второй ряд - информация и настройки
            [
                InlineKeyboardButton(
                    f"{Styles.HELP} Помощь",
                    callback_data="help_info"
                ),
                InlineKeyboardButton(
                    f"{Styles.SETTINGS} Настройки",
                    callback_data="settings"
                )
            ],
            # Третий ряд - статистика
            [
                InlineKeyboardButton(
                    f"{Styles.STATS} Статистика",
                    callback_data="stats"
                )
            ]
        ]

        # Добавляем админ-панель если пользователь админ
        if is_admin:
            keyboard.append([
                InlineKeyboardButton(
                    f"{Styles.CROWN} Админ-панель",
                    callback_data="admin_panel"
                )
            ])

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def search_menu():
        """Меню поиска"""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    f"{Styles.DATABASE} База данных",
                    callback_data="search_db"
                ),
                InlineKeyboardButton(
                    f"{Styles.INTERNET} Интернет",
                    callback_data="search_web"
                )
            ],
            [
                InlineKeyboardButton(
                    f"{Styles.BACK} Назад",
                    callback_data="back_main"
                )
            ]
        ])

    @staticmethod
    def back_button():
        """Кнопка назад"""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{Styles.BACK} Назад", callback_data="back_main")]
        ])

    @staticmethod
    def stats_menu():
        """Меню статистики"""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    f"{Styles.RELOAD} Обновить",
                    callback_data="stats_refresh"
                ),
                InlineKeyboardButton(
                    f"{Styles.BACK} Назад",
                    callback_data="back_main"
                )
            ]
        ])


# ==================== ТЕКСТОВЫЕ СООБЩЕНИЯ ====================
class Messages:
    """Класс для красивых текстовых сообщений"""

    @staticmethod
    def welcome(first_name):
        """Приветственное сообщение"""
        return f"""
🎉 {Styles.bold(f'Добро пожаловать, {first_name}!')}

{Styles.italic('Я умный бот для поиска и анализа информации')}

✨ {Styles.bold('Что я умею:')}
• {Styles.SEARCH} Искать информацию в различных источниках
• {Styles.STATS} Собирать и показывать статистику
• {Styles.SETTINGS} Настраиваться под ваши preferences

Выберите действие из меню ниже:
        """

    @staticmethod
    def help():
        """Сообщение помощи"""
        return f"""
{Styles.HELP} {Styles.bold('Помощь по боту')}

{Styles.bold('Основные команды:')}
/{Styles.code('start')} - показать главное меню
/{Styles.code('help')} - эта справка

{Styles.bold('Кнопки меню:')}
• {Styles.SEARCH} {Styles.bold('Поиск')} - начать поиск информации
• {Styles.SETTINGS} {Styles.bold('Настройки')} - настройки бота
• {Styles.STATS} {Styles.bold('Статистика')} - ваша статистика

{Styles.italic('Для навигации используйте кнопки меню')}
        """

    @staticmethod
    def search():
        """Сообщение поиска"""
        return f"""
{Styles.SEARCH} {Styles.bold('Режим поиска')}

Выберите где искать информацию:

• {Styles.DATABASE} {Styles.bold('База данных')} - поиск в локальной базе
• {Styles.INTERNET} {Styles.bold('Интернет')} - поиск в интернете

{Styles.italic('Выберите источник для поиска:')}
        """

    @staticmethod
    def settings():
        """Сообщение настроек"""
        return f"""
{Styles.SETTINGS} {Styles.bold('Настройки')}

Здесь вы можете настроить бота под себя:

{Styles.bold('Доступные настройки:')}
• Уведомления
• Язык интерфейса
• Часовой пояс
• Формат даты

{Styles.italic('Настройки будут доступны в будущих обновлениях')}
        """

    @staticmethod
    def stats():
        """Сообщение статистики"""
        return f"""
{Styles.STATS} {Styles.bold('Ваша статистика')}

{Styles.bold('Активность:')}
• Поисковых запросов: {Styles.code('15')}
• Найдено результатов: {Styles.code('127')}
• Активных дней: {Styles.code('3')}

{Styles.bold('Эффективность:')}
• Среднее время ответа: {Styles.code('1.2с')}
• Точность поиска: {Styles.code('89%')}

{Styles.italic('Статистика обновляется автоматически')}
        """


# ==================== ОБРАБОТЧИКИ ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start с красивым оформлением"""
    try:
        user = update.effective_user
        is_admin = user.id in [123456789]  # Замените на ваши ID админов

        # Отправляем красивое сообщение
        await update.message.reply_text(
            Messages.welcome(user.first_name),
            reply_markup=Keyboards.main_menu(user.id, is_admin),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )

        logger.info(f"👤 Пользователь {user.first_name} запустил бота")

    except Exception as e:
        logger.error(f"Ошибка в start: {e}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    await update.message.reply_text(
        Messages.help(),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Главный обработчик callback запросов"""
    try:
        query = update.callback_query
        await query.answer()

        user = query.from_user
        callback_data = query.data

        logger.info(f"🔘 Нажата кнопка: {callback_data} пользователем {user.first_name}")

        # Обработка всех типов кнопок
        if callback_data == "search_start":
            await handle_search(query)

        elif callback_data == "help_info":
            await handle_help(query)

        elif callback_data == "settings":
            await handle_settings(query)

        elif callback_data == "stats":
            await handle_stats(query)

        elif callback_data == "search_db":
            await handle_search_db(query)

        elif callback_data == "search_web":
            await handle_search_web(query)

        elif callback_data == "stats_refresh":
            await handle_stats_refresh(query)

        elif callback_data == "back_main":
            await handle_back_main(query)

        elif callback_data == "admin_panel":
            await handle_admin_panel(query)

        else:
            await query.edit_message_text(
                "❌ Неизвестная команда",
                parse_mode=ParseMode.HTML
            )

    except Exception as e:
        logger.error(f"Ошибка в обработчике кнопок: {e}")


# ==================== ОБРАБОТЧИКИ КНОПОК ====================

async def handle_search(query):
    """Обработчик кнопки поиска"""
    await query.edit_message_text(
        Messages.search(),
        reply_markup=Keyboards.search_menu(),
        parse_mode=ParseMode.HTML
    )


async def handle_help(query):
    """Обработчик кнопки помощи"""
    await query.edit_message_text(
        Messages.help(),
        reply_markup=Keyboards.back_button(),
        parse_mode=ParseMode.HTML
    )


async def handle_settings(query):
    """Обработчик кнопки настроек"""
    await query.edit_message_text(
        Messages.settings(),
        reply_markup=Keyboards.back_button(),
        parse_mode=ParseMode.HTML
    )


async def handle_stats(query):
    """Обработчик кнопки статистики"""
    await query.edit_message_text(
        Messages.stats(),
        reply_markup=Keyboards.stats_menu(),
        parse_mode=ParseMode.HTML
    )


async def handle_search_db(query):
    """Обработчик поиска в базе данных"""
    await query.edit_message_text(
        f"""
{Styles.DATABASE} {Styles.bold('Поиск в базе данных')}

{Styles.italic('Ищем информацию в локальной базе данных...')}

{Styles.bold('Статус:')} {Styles.code('Поиск выполняется')}
{Styles.bold('Ожидайте результатов:')} ⏳
        """,
        reply_markup=Keyboards.back_button(),
        parse_mode=ParseMode.HTML
    )


async def handle_search_web(query):
    """Обработчик поиска в интернете"""
    await query.edit_message_text(
        f"""
{Styles.INTERNET} {Styles.bold('Поиск в интернете')}

{Styles.italic('Ищем информацию в открытых источниках...')}

{Styles.bold('Статус:')} {Styles.code('Сканирование сети')}
{Styles.bold('Источники:')} {Styles.code('Google, Yandex, Bing')}
        """,
        reply_markup=Keyboards.back_button(),
        parse_mode=ParseMode.HTML
    )


async def handle_stats_refresh(query):
    """Обработчик обновления статистики"""
    await query.edit_message_text(
        f"""
{Styles.STATS} {Styles.bold('Статистика обновлена!')} {Styles.RELOAD}

{Styles.bold('Обновленные данные:')}
• Поисковых запросов: {Styles.code('18')} ↗️
• Найдено результатов: {Styles.code('145')} ↗️
• Активных дней: {Styles.code('4')} ↗️

{Styles.italic('Данные успешно обновлены')}
        """,
        reply_markup=Keyboards.stats_menu(),
        parse_mode=ParseMode.HTML
    )


async def handle_back_main(query):
    """Обработчик кнопки назад"""
    user = query.from_user
    is_admin = user.id in [123456789]  # Замените на ваши ID админов

    await query.edit_message_text(
        Messages.welcome(user.first_name),
        reply_markup=Keyboards.main_menu(user.id, is_admin),
        parse_mode=ParseMode.HTML
    )


async def handle_admin_panel(query):
    """Обработчик админ-панели"""
    await query.edit_message_text(
        f"""
{Styles.CROWN} {Styles.bold('Админ-панель')}

{Styles.bold('Доступные действия:')}
• Просмотр статистики бота
• Управление пользователями
• Системные настройки
• Логи и мониторинг

{Styles.italic('Доступ только для администраторов')}
        """,
        reply_markup=Keyboards.back_button(),
        parse_mode=ParseMode.HTML
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    text = update.message.text

    if not text.startswith('/'):
        await update.message.reply_text(
            f"""
{Styles.WIZARD} {Styles.bold('Я не понимаю текстовые сообщения!')}

Используйте {Styles.code('кнопки меню')} или команды:
• {Styles.code('/start')} - главное меню
• {Styles.code('/help')} - справка

{Styles.italic('Для навигации используйте интерактивные кнопки')}
            """,
            parse_mode=ParseMode.HTML
        )


# ==================== ЗАПУСК БОТА ====================

def main() -> None:
    """Основная функция запуска бота"""
    try:
        # Создаем приложение
        application = Application.builder().token(BOT_TOKEN).build()

        # Регистрируем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CallbackQueryHandler(handle_callback_query))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Красивое сообщение о запуске
        print("✨" * 50)
        print("🎮 BOT FDS 2.0 - ЗАПУСК")
        print("✨" * 50)
        print("📊 Режим: ПРОДУКШЕН")
        print("🎨 Стиль: ПРЕМИУМ")
        print("🚀 Статус: ЗАПУЩЕН")
        print("✨" * 50)

        logger.info("🤖 Бот запущен с премиум оформлением!")

        # Запускаем бота
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=['message', 'callback_query']
        )

    except Exception as e:
        logger.critical(f"❌ Критическая ошибка: {e}")


if __name__ == '__main__':
    main()