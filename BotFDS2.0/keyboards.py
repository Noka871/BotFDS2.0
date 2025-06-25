# Генерация клавиатур
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_role_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Даббер"))
    keyboard.add(KeyboardButton("Таймер"))
    keyboard.add(KeyboardButton("Админ"))
    return keyboard

def get_dubbing_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Выбрать тайтл"))
    keyboard.add(KeyboardButton("Добавить роль таймера"))
    keyboard.add(KeyboardButton("Предупредить о форс-мажорах"))
    keyboard.add(KeyboardButton("Мои долги"))
    keyboard.add(KeyboardButton("Вернуться в меню"))
    return keyboard

# ... другие клавиатуры