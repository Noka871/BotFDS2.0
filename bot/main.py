import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from config import BOT_TOKEN
from database import Database
from handlers.common import start_handler, menu_handler
from handlers.dubber import dubber_menu_handler, select_title_handler
from handlers.timer import timer_menu_handler, create_title_handler
from utils.notifications import NotificationManager

# Настройка логгирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class DubbingBot:
    def __init__(self, token: str):
        self.updater = Updater(token=token, use_context=True)
        self.db = Database()
        self.dispatcher = self.updater.dispatcher

        # Регистрация обработчиков
        self._register_handlers()

    def _register_handlers(self):
        # Общие обработчики
        self.dispatcher.add_handler(CommandHandler('start', start_handler))
        self.dispatcher.add_handler(CommandHandler('menu', menu_handler))

        # Обработчики для дабберов
        self.dispatcher.add_handler(CallbackQueryHandler(dubber_menu_handler, pattern='^dubber_'))
        self.dispatcher.add_handler(CallbackQueryHandler(select_title_handler, pattern='^select_title_'))

        # Обработчики для таймеров
        self.dispatcher.add_handler(CallbackQueryHandler(timer_menu_handler, pattern='^timer_'))
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, create_title_handler))

        # Обработка ошибок
        self.dispatcher.add_error_handler(self.error_handler)

    def error_handler(self, update, context):
        logger.error(f'Update {update} caused error {context.error}')
        if update and update.message:
            update.message.reply_text('Произошла ошибка. Пожалуйста, попробуйте позже.')

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

    class DubbingBot:
     def __init__(self, token: str):
        self.updater = Updater(token=token, use_context=True)
        self.db = Database()
        self.notifier = NotificationManager(token)  # Добавляем менеджер уведомлений
        self.notifier.start_daily_notifications()  # Запускаем фоновые уведомления

if __name__ == '__main__':
    bot = DubbingBot(BOT_TOKEN)
    bot.run()