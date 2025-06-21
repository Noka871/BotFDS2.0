from telebot import TeleBot
from telebot.types import Message


def setup_dubber_handlers(bot: TeleBot):
    @bot.message_handler(func=lambda m: m.text == "📝 Отправить отчет")
    def handle_report(message: Message):
        bot.send_message(message.chat.id, "Выберите тайтл:")  # Исправлено

    @bot.message_handler(func=lambda m: m.text == "⚠ Форс-мажор")  # Тире добавлено
    def handle_emergency(message: Message):
        bot.send_message(message.chat.id, "Опишите проблему:")

    # Добавьте этот обработчик
    @bot.message_handler(func=lambda m: m.text == "📊 Мои долги")
    def handle_debts(message: Message):
        bot.send_message(message.chat.id, "Ваши долги: ...")