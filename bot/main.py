import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    CallbackQueryHandler, ContextTypes, ConversationHandler
)
from database import Database

# ==================== НАСТРОЙКА ЛОГИРОВАНИЯ ====================
# Настройка формата и уровня логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO  # DEBUG для подробных логов, INFO для обычных
)
logger = logging.getLogger(__name__)

# ==================== ЗАГРУЗКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ ====================
load_dotenv()  # Загружаем переменные из файла .env

BOT_TOKEN = os.getenv('BOT_TOKEN')  # Токен бота из .env
ADMIN_ID = os.getenv('ADMIN_ID')  # ID администратора из .env


# ==================== ОСНОВНОЙ КЛАСС БОТА ====================
class DubbingBot:
    def __init__(self, token: str):
        """
        Инициализация бота
        :param token: Токен бота от @BotFather
        """
        # Создаем приложение с токеном
        self.application = Application.builder().token(token).build()
        # Инициализируем базу данных
        self.db = Database()
        # Настраиваем обработчики команд
        self.setup_handlers()

    def setup_handlers(self):
        """
        Настройка всех обработчиков команд
        ВАЖНО: Порядок обработчиков имеет значение!
        """
        logger.info("Настройка обработчиков...")

        # 1. Обработчики ТЕКСТОВЫХ КОМАНД (начинаются с /)
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("menu", self.menu_command))
        self.application.add_handler(CommandHandler("test", self.test_command))  # Тестовая команда

        # 2. Обработчики CALLBACK_QUERY (нажатия на inline-кнопки)
        # ВАЖНО: Сначала общий обработчик, потом специфичные!

        # УНИВЕРСАЛЬНЫЙ обработчик - ловит ВСЕ callback_data
        self.application.add_handler(CallbackQueryHandler(self.universal_callback))

        # Специфичные обработчики для разных типов кнопок
        self.application.add_handler(CallbackQueryHandler(self.role_callback, pattern="^role_"))
        self.application.add_handler(CallbackQueryHandler(self.menu_callback, pattern="^menu_"))
        self.application.add_handler(CallbackQueryHandler(self.test_callback, pattern="^test_"))

        # 3. Обработчик ОБЫЧНЫХ ТЕКСТОВЫХ СООБЩЕНИЙ (не команд)
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        logger.info("Обработчики настроены успешно")

    # ==================== ОБРАБОТЧИКИ КОМАНД ====================

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Обработчик команды /start
        Показывает выбор роли пользователя
        """
        user = update.effective_user
        logger.info(f"Пользователь {user.id} запустил бота")

        # Добавляем/обновляем пользователя в базе данных
        self.db.add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name or ""  # Если нет фамилии - пустая строка
        )

        # СОЗДАЕМ ИНЛАЙН-КЛАВИАТУРУ с кнопками выбора роли
        # InlineKeyboardButton создает интерактивные кнопки
        keyboard = [
            # Первый ряд кнопок
            [InlineKeyboardButton("🎤 Даббер", callback_data="role_dubber")],
            # Второй ряд кнопок
            [InlineKeyboardButton("🎧 Таймер", callback_data="role_timer")],
            # Третий ряд кнопок
            [InlineKeyboardButton("👑 Админ", callback_data="role_admin")]
        ]

        # Преобразуем клавиатуру в разметку для Telegram
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляем сообщение с inline-кнопками
        # reply_markup - обязательно для отображения кнопок
        await update.message.reply_text(
            f"Привет, {user.first_name}! Выбери свою роль:",
            reply_markup=reply_markup
        )

    async def test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Тестовая команда /test для проверки работы кнопок
        """
        # Простые тестовые кнопки
        keyboard = [
            [InlineKeyboardButton("Тестовая кнопка 1", callback_data="test_1")],
            [InlineKeyboardButton("Тестовая кнопка 2", callback_data="test_2")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "🔧 Тестовые кнопки. Нажмите любую для проверки:",
            reply_markup=reply_markup
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help - показывает справку"""
        help_text = """
        🤖 Бот для управления процессом дубляжа

        Основные команды:
        /start - Начать работу с ботом
        /menu - Главное меню  
        /help - Помощь
        /test - Тест кнопок

        Возможности:
        • Отметка о сдаче аудиодорожек
        • Уведомления о новых сериях
        • Предупреждения о форс-мажорах
        • Просмотр долгов и статистики
        """
        await update.message.reply_text(help_text)

    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /menu - показывает главное меню"""
        user = update.effective_user
        user_data = self.db.get_user(user.id)

        if not user_data:
            await update.message.reply_text("Сначала выполните /start для регистрации")
            return

        role = user_data[5]  # 5-й элемент в tuple - роль пользователя

        # Создаем клавиатуру меню в зависимости от роли
        keyboard = [
            [InlineKeyboardButton("📺 Выбрать тайтл", callback_data="menu_select_title")],
            [InlineKeyboardButton("⚠️ Предупредить о форс-мажоре", callback_data="menu_warning")],
            [InlineKeyboardButton("💳 Мои долги", callback_data="menu_debts")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"🎮 Главное меню ({self.get_role_name(role)})\nВыберите действие:",
            reply_markup=reply_markup
        )

    # ==================== ОБРАБОТЧИКИ CALLBACK (НАЖАТИЯ НА КНОПКИ) ====================

    async def universal_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        УНИВЕРСАЛЬНЫЙ обработчик для ВСЕХ callback_data
        Этот обработчик ловит все нажатия на кнопки
        """
        query = update.callback_query
        await query.answer()  # Важно: подтверждаем получение callback (убирает "часики")

        user = query.from_user
        callback_data = query.data

        # Логируем полученный callback_data
        logger.info(f"🔍 UNIVERSAL: Пользователь {user.id} нажал кнопку: '{callback_data}'")

        # Редактируем сообщение чтобы показать что кнопка сработала
        await query.edit_message_text(
            f"✅ Кнопка нажата!\n"
            f"Callback_data: '{callback_data}'\n\n"
            f"Обработчик: universal_callback"
        )

    async def role_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Обработчик для кнопок выбора роли (pattern='^role_')
        Вызывается из universal_callback
        """
        query = update.callback_query
        await query.answer()

        user = query.from_user
        role = query.data.replace("role_", "")  # Извлекаем роль из callback_data

        logger.info(f"ROLE: Пользователь {user.id} выбрал роль: {role}")

        # Обновляем роль пользователя в базе данных
        self.db.update_user_role(user.id, role)

        # Получаем человеко-читаемое название роли
        role_name = self.get_role_name(role)

        # Редактируем сообщение
        await query.edit_message_text(
            text=f"✅ Роль '{role_name}' успешно установлена!\n\n"
                 f"Теперь используйте команду /menu для доступа к функциям."
        )

    async def menu_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Обработчик для кнопок меню (pattern='^menu_')
        Вызывается из universal_callback
        """
        query = update.callback_query
        await query.answer()

        user = query.from_user
        action = query.data.replace("menu_", "")  # Извлекаем действие

        logger.info(f"MENU: Пользователь {user.id} выбрал действие: {action}")
        await query.edit_message_text(f"📋 Выбрано меню: {action}")

    async def test_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Обработчик для тестовых кнопок (pattern='^test_')
        Вызывается из universal_callback
        """
        query = update.callback_query
        await query.answer()

        test_number = query.data.replace("test_", "")
        user = query.from_user

        logger.info(f"TEST: Пользователь {user.id} нажал тестовую кнопку: {test_number}")
        await query.edit_message_text(f"✅ Тестовая кнопка {test_number} работает!")

    # ==================== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ====================

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик обычных текстовых сообщений (не команд)"""
        await update.message.reply_text("📝 Сообщение получено! Эта функция в разработке.")

    def get_role_name(self, role: str) -> str:
        """Возвращает читаемое название роли"""
        role_names = {
            "dubber": "Даббер",
            "timer": "Таймер",
            "admin": "Администратор"
        }
        return role_names.get(role, "Неизвестно")

    def run(self):
        """Запуск бота"""
        logger.info("Бот запускается...")
        self.application.run_polling()  # Запускаем бота в режиме polling


# ==================== ГЛАВНАЯ ФУНКЦИЯ ====================
def main():
    """Главная функция запуска бота"""
    try:
        # Проверяем что токен загружен
        if not BOT_TOKEN:
            logger.error("❌ BOT_TOKEN не найден! Проверьте файл .env")
            return

        logger.info("✅ Бот запускается с правильным токеном")

        # Создаем и запускаем бота
        bot = DubbingBot(BOT_TOKEN)
        bot.run()

    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")


# Точка входа в программу
if __name__ == "__main__":
    main()