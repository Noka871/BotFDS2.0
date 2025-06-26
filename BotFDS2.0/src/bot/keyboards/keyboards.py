from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def dubber_menu_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Выбрать тайтл"))
    kb.add(KeyboardButton("Мои долги"))
    kb.add(KeyboardButton("Предупредить о форс-мажорах"))
    return kb

def timer_menu_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Создать тайтл"))
    kb.add(KeyboardButton("Просмотреть график сдавших"))
    # ... остальные кнопки
    return kb

def admin_menu_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Выгрузить отчет"))
    # ... можно добавить кнопки и из других меню
    return kb