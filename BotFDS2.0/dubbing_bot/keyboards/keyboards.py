from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_role_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🔊 Даббер"))
    keyboard.add(KeyboardButton("⏱ Таймер"))
    keyboard.add(KeyboardButton("👑 Админ"))
    return keyboard

def get_dubber_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("📝 Отправить отчет"))
    keyboard.add(KeyboardButton("⚠ Форс-мажор"))
    keyboard.add(KeyboardButton("📊 Мои долги"))
    keyboard.add(KeyboardButton("🔙 Назад"))
    return keyboard