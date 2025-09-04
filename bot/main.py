import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from database.database import Database

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения ДО их использования
load_dotenv()

# Теперь определяем переменные ПОСЛЕ загрузки .env
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Проверка, что токен загружен
if not BOT_TOKEN:
    logger.error("BOT_TOKEN не найден! Проверьте файл .env")
    exit(1)


class DubbingBot:
    def __init__(self, token: str):
        self.application = Application.builder().token(token).build()
        self.db = Database()
        self.setup_handlers()

    def setup_handlers(self):
        """Настройка обработчиков команд"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        # Добавьте другие обработчики здесь

    async def start_command(self, update, context):
        """Обработчик команды /start"""
        user = update.effective_user
        await update.message.reply_text(f"Привет, {user.first_name}! Я бот для дубляжа.")

        # Добавляем пользователя в базу данных
        self.db.add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )

    async def help_command(self, update, context):
        """Обработчик команды /help"""
        await update.message.reply_text("Это помощь по боту!")

    def run(self):
        """Запуск бота"""
        logger.info("Бот запускается...")
        self.application.run_polling()


# Главная функция
def main():
    try:
        # Создаем и запускаем бота
        bot = DubbingBot(BOT_TOKEN)
        bot.run()
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")


if __name__ == "__main__":
    main()