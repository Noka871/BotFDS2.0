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

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')


class DubbingBot:
    def __init__(self, token: str):
        # Создаем приложение с токеном
        self.application = Application.builder().token(token).build()
        # Инициализируем базу данных
        self.db = Database()
        # Настраиваем обработчики
        self.setup_handlers()

    def setup_handlers(self):
        """Настройка всех обработчиков команд"""
        # Обработчики текстовых команд
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("menu", self.menu_command))

        # Обработчики нажатий на inline-кнопки
        # pattern="^role_" - ловит все callback_data начинающиеся с "role_"
        self.application.add_handler(CallbackQueryHandler(self.role_callback, pattern="^role_"))
        # pattern="^menu_" - ловит все callback_data начинающиеся с "menu_"
        self.application.add_handler(CallbackQueryHandler(self.menu_callback, pattern="^menu_"))

        # Обработчик обычных текстовых сообщений (не команд)
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start - показывает выбор роли"""
        user = update.effective_user
        logger.info(f"User {user.id} started the bot")

        # Добавляем/обновляем пользователя в базе данных
        self.db.add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name or ""  # Если нет фамилии - пустая строка
        )

        # СОЗДАЕМ ИНЛАЙН-КЛАВИАТУРУ с кнопками выбора роли
        keyboard = [
            # Первый ряд кнопок
            [
                InlineKeyboardButton("🎤 Даббер", callback_data="role_dubber"),
                InlineKeyboardButton("🎧 Таймер", callback_data="role_timer")
            ],
            # Второй ряд кнопок
            [
                InlineKeyboardButton("👑 Админ", callback_data="role_admin")
            ]
        ]

        # Преобразуем клавиатуру в разметку
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляем сообщение с inline-кнопками
        await update.message.reply_text(
            f"Привет, {user.first_name}! Выбери свою роль:",
            reply_markup=reply_markup  # Важно: передаем клавиатуру здесь
        )

    async def role_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатия на кнопку выбора роли"""
        query = update.callback_query
        # Подтверждаем получение callback (убирает "часики" на кнопке)
        await query.answer()

        user = query.from_user
        # Извлекаем роль из callback_data (убираем префикс "role_")
        role = query.data.replace("role_", "")

        logger.info(f"User {user.id} selected role: {role}")

        # Обновляем роль пользователя в базе данных
        self.db.update_user_role(user.id, role)

        # Получаем человеко-читаемое название роли
        role_name = self.get_role_name(role)

        # РЕДАКТИРУЕМ исходное сообщение с новым текстом
        await query.edit_message_text(
            text=f"✅ Роль '{role_name}' успешно установлена!\n\n"
                 f"Теперь используйте команду /menu для доступа к функциям."
        )

    async def menu_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на кнопки меню"""
        query = update.callback_query
        await query.answer()  # Подтверждаем получение

        user = query.from_user
        action = query.data.replace("menu_", "")  # Извлекаем действие

        logger.info(f"User {user.id} selected menu action: {action}")

        # Получаем данные пользователя из БД
        user_data = self.db.get_user(user.id)
        role = user_data[5] if user_data else "dubber"  # 5-й элемент - роль

        # Обрабатываем разные действия
        if action == "back":
            await self.show_main_menu_from_callback(update, role)
        elif action == "select_title":
            await self.show_titles_menu(update, user.id)
        elif action == "warning":
            await query.edit_message_text("⚠️ Опишите проблему в следующем сообщении...")
        elif action == "debts":
            await self.show_user_debts(update, user.id)
        elif action == "add_timer_role":
            await self.add_timer_role(update, user.id)
        else:
            await query.edit_message_text("🛠️ Эта функция в разработке")

    async def show_user_debts(self, update: Update, user_id: int):
        """Показывает долги пользователя"""
        query = update.callback_query
        debts = self.db.get_user_debts(user_id)

        if debts:
            debt_text = "💳 Ваши долги:\n\n"
            for debt in debts:
                debt_text += f"• {debt[0]} - серия {debt[1]} ({debt[2]})\n"
            await query.edit_message_text(debt_text)
        else:
            await query.edit_message_text("🎉 У вас нет долгов!")

    async def add_timer_role(self, update: Update, user_id: int):
        """Добавляет пользователю роль таймера"""
        query = update.callback_query
        self.db.update_user_role(user_id, "timer")
        await query.edit_message_text("✅ Вам выданы права таймера! Используйте /menu")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = """
        🤖 Бот для управления процессом дубляжа

        Основные команды:
        /start - Начать работу с ботом
        /menu - Главное меню
        /help - Помощь

        Возможности:
        • Отметка о сдаче аудиодорожек
        • Уведомления о новых сериях
        • Предупреждения о форс-мажорах
        • Просмотр долгов и статистики
        """
        await update.message.reply_text(help_text)

    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /menu"""
        user = update.effective_user
        user_data = self.db.get_user(user.id)

        if not user_data:
            await update.message.reply_text("Сначала выполните /start для регистрации")
            return

        role = user_data[5]  # 5-й элемент - роль
        await self.show_main_menu(update, role)

    async def show_main_menu(self, update: Update, role: str):
        """Показывает главное меню для разных ролей"""
        # Создаем клавиатуру в зависимости от роли
        if role == "dubber":
            keyboard = [
                [InlineKeyboardButton("📺 Выбрать тайтл", callback_data="menu_select_title")],
                [InlineKeyboardButton("⚠️ Предупредить о форс-мажоре", callback_data="menu_warning")],
                [InlineKeyboardButton("💳 Мои долги", callback_data="menu_debts")],
                [InlineKeyboardButton("🔄 Добавить роль таймера", callback_data="menu_add_timer_role")]
            ]
        elif role == "timer":
            keyboard = [
                [InlineKeyboardButton("➕ Создать тайтл", callback_data="menu_create_title")],
                [InlineKeyboardButton("✏️ Редактировать тайтл", callback_data="menu_edit_title")],
                [InlineKeyboardButton("📊 График сдач", callback_data="menu_schedule")],
                [InlineKeyboardButton("📨 Рассылка", callback_data="menu_broadcast")],
                [InlineKeyboardButton("⚠️ Предупреждения", callback_data="menu_warnings")]
            ]
        else:  # admin
            keyboard = [
                [InlineKeyboardButton("📺 Выбрать тайтл", callback_data="menu_select_title")],
                [InlineKeyboardButton("➕ Создать тайтл", callback_data="menu_create_title")],
                [InlineKeyboardButton("📊 Выгрузить отчет", callback_data="menu_export")],
                [InlineKeyboardButton("📨 Рассылка", callback_data="menu_broadcast")],
                [InlineKeyboardButton("⚠️ Предупреждения", callback_data="menu_warnings")]
            ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"🎮 Главное меню ({self.get_role_name(role)})\nВыберите действие:",
            reply_markup=reply_markup
        )

    async def show_main_menu_from_callback(self, update: Update, role: str):
        """Показывает главное меню из callback (редактирует сообщение)"""
        query = update.callback_query

        # Создаем клавиатуру (аналогично show_main_menu)
        if role == "dubber":
            keyboard = [
                [InlineKeyboardButton("📺 Выбрать тайтл", callback_data="menu_select_title")],
                [InlineKeyboardButton("⚠️ Предупредить о форс-мажоре", callback_data="menu_warning")],
                [InlineKeyboardButton("💳 Мои долги", callback_data="menu_debts")],
                [InlineKeyboardButton("🔄 Добавить роль таймера", callback_data="menu_add_timer_role")]
            ]
        elif role == "timer":
            keyboard = [
                [InlineKeyboardButton("➕ Создать тайтл", callback_data="menu_create_title")],
                [InlineKeyboardButton("✏️ Редактировать тайтл", callback_data="menu_edit_title")],
                [InlineKeyboardButton("📊 График сдач", callback_data="menu_schedule")],
                [InlineKeyboardButton("📨 Рассылка", callback_data="menu_broadcast")],
                [InlineKeyboardButton("⚠️ Предупреждения", callback_data="menu_warnings")]
            ]
        else:
            keyboard = [
                [InlineKeyboardButton("📺 Выбрать тайтл", callback_data="menu_select_title")],
                [InlineKeyboardButton("➕ Создать тайтл", callback_data="menu_create_title")],
                [InlineKeyboardButton("📊 Выгрузить отчет", callback_data="menu_export")],
                [InlineKeyboardButton("📨 Рассылка", callback_data="menu_broadcast")],
                [InlineKeyboardButton("⚠️ Предупреждения", callback_data="menu_warnings")]
            ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        # РЕДАКТИРУЕМ существующее сообщение
        await query.edit_message_text(
            text=f"🎮 Главное меню ({self.get_role_name(role)})\nВыберите действие:",
            reply_markup=reply_markup
        )

    async def show_titles_menu(self, update: Update, user_id: int):
        """Показывает меню выбора тайтлов"""
        query = update.callback_query
        titles = self.db.get_user_titles(user_id)

        if not titles:
            await query.edit_message_text("📭 У вас нет назначенных тайтлов.")
            return

        # Создаем кнопки для каждого тайтла
        keyboard = []
        for title in titles:
            keyboard.append([InlineKeyboardButton(f"📀 {title[1]}", callback_data=f"title_{title[0]}")])

        # Добавляем кнопку "Назад"
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="menu_back")])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "📺 Выберите тайтл:",
            reply_markup=reply_markup
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
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
        self.application.run_polling()


def main():
    """Главная функция"""
    try:
        if not BOT_TOKEN:
            logger.error("❌ BOT_TOKEN не найден! Проверьте файл .env")
            return

        logger.info("✅ Бот запускается с правильным токеном")
        bot = DubbingBot(BOT_TOKEN)
        bot.run()
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")


if __name__ == "__main__":
    main()