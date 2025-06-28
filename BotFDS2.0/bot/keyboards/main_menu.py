from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура выбора роли
def get_role_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("Даббер"),
        KeyboardButton("Таймер"),
        KeyboardButton("Админ")
    )
    return markup

# Клавиатура даббера
def get_dubber_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("Выбрать тайтл"),
        KeyboardButton("Мои долги"),
        KeyboardButton("Вернуться в меню")
    )
    return markup

# Клавиатура таймера
def get_timer_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("Создать тайтл"),
        KeyboardButton("Просмотреть график"),
        KeyboardButton("Вернуться в меню")
    )
    return markup