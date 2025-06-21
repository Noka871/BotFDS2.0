import logging
logging.basicConfig(
    level=logging.INFO,
    filename='bot.log',
    format='%(asctime)s - %(message)s',
    encoding='utf-8'
)
from telebot import TeleBot
from config import BOT_TOKEN
from handlers.dubber import setup_dubber_handlers

bot = TeleBot(BOT_TOKEN())
setup_dubber_handlers(bot)

if __name__ == '__main__':
    print("Бот запускается...")  # Для отладки
    bot.polling(none_stop=True, interval=2)  # Интервал опроса 2 сек

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
