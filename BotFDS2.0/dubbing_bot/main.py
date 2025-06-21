import logging
from telebot import TeleBot
from config import BOT_TOKEN
from handlers.reports import setup_report_handlers
from telebot.types import ReplyKeyboardMarkup

from handlers.dubber import setup_dubber_handlers

setup_report_handlers(bot)

logging.basicConfig(
    level=logging.INFO,
    filename='bot.log',
    format='%(asctime)s - %(message)s',
    encoding='utf-8')  # Важно для русскоязычного текста

bot = telebot.TeleBot('7833834785:AAH_EQDJ5Ax9Viq32g9xWfy40Ve9IfmTrWk')
setup_dubber_handlers(bot)  # Регистрация обработчиков даббера



# Клавиатура для выбора роли
def role_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔊 Даббер", "⏱ Таймер", "👑 Админ")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать! Выберите роль:",
        reply_markup=role_keyboard()
    )

@bot.message_handler(func=lambda m: m.text == "🔊 Даббер")
def dubber_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📝 Отправить отчет", "⚠ Форс-мажор", "📊 Мои долги")
    bot.send_message(message.chat.id, "Меню даббера:", reply_markup=markup)

if __name__ == '__main__':
    bot.polling(none_stop=True)
