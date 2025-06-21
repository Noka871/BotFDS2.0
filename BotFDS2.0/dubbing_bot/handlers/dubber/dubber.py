# handlers/dubber.py
from telebot import TeleBot
from telebot.types import Message


def setup_dubber_handlers(bot: TeleBot):
    @bot.message_handler(func=lambda message: message.text == "📝 Отправить отчет")
    def handle_report(message: Message):
        bot.reply_to(message, "🔍 Выберите тайтл:")  # Ответ с цитированием

    @bot.message_handler(func=lambda message: message.text == "⚠ Форс-мажор")
    def handle_emergency(message: Message):
        bot.send_message(message.chat.id, "✍️ Опишите проблему:")  # Новое сообщение

    @bot.message_handler(func=lambda message: message.text == "📊 Мои долги")
    def handle_debts(message: Message):
        bot.send_message(message.chat.id, "🔄 Загружаю список долгов...")