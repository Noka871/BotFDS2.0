# Клавиатуры
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu(role: str = "user"):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    if role == "admin":
        markup.add(KeyboardButton("Выгрузить отчет"))
        markup.add(KeyboardButton("Рассылка"))

    markup.add(KeyboardButton("Помощь"))
    return markup

def get_admin_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Выгрузить отчет", "Рассылка")
    markup.row("Помощь", "Назад")
    return markup