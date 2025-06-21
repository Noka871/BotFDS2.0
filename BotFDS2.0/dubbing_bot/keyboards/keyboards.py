# keyboards.py
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def get_dubber_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("📝 Отправить отчет"),  # Текст должен совпадать с обработчиком
        KeyboardButton("⚠ Форс-мажор")
    )
    return markup