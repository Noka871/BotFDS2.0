# handlers/dubber.py
from email import message

from telebot import TeleBot
from telebot.types import Message
from keyboards import get_dubber_menu  # Импорт клавиатуры
print(f"Кнопка нажата: {message.text}")  # Проверьте вывод в PythonAnywhere → Web → Error log

def setup_dubber_handlers(bot: TeleBot):
    # Обработчик кнопки "📝 Отправить отчет"
    @bot.message_handler(func=lambda message: message.text == "📝 Отправить отчет")
    def handle_report(message: Message):
        bot.reply_to(message, "Выберите тайтл:")  # Ответ при нажатии

    # Обработчик кнопки "⚠ Форс-мажор"
    @bot.message_handler(func=lambda message: message.text == "⚠ Форс-мажор")
    def handle_emergency(message: Message):
        bot.reply_to(message, "Опишите проблему:")