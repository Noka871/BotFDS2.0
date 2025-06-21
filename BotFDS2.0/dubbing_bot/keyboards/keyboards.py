from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def get_dubber_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("📝 Отправить отчёт"),
        KeyboardButton("⚠ Форс-мажор"),
        KeyboardButton("📊 Мои долги")
    )
    return markup