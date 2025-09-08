from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_kb():
    """Главное меню выбора роли"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Даббер")],
            [KeyboardButton(text="Таймер")],
            [KeyboardButton(text="Админ")]
        ],
        resize_keyboard=True
    )

def get_dubber_main_kb():
    """Меню даббера"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Выбрать тайтл")],
            [KeyboardButton(text="Добавить роль таймера")],
            [KeyboardButton(text="Предупредить о форс-мажорах")],
            [KeyboardButton(text="Мои долги")],
            [KeyboardButton(text="Вернуться в меню")]
        ],
        resize_keyboard=True
    )

def get_timer_main_kb():
    """Меню таймера"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Создать тайтл"), KeyboardButton(text="Отредактировать тайтл")],
            [KeyboardButton(text="Просмотреть график сдавших"), KeyboardButton(text="Создать рассылку")],
            [KeyboardButton(text="Просмотреть предупреждения"), KeyboardButton(text="Предупредить о форс-мажорах")],
            [KeyboardButton(text="Вернуться в меню")]
        ],
        resize_keyboard=True
    )

def get_admin_main_kb():
    """Меню администратора"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Выгрузить отчет"), KeyboardButton(text="Статистика системы")],
            [KeyboardButton(text="Управление пользователями"), KeyboardButton(text="Отправить уведомление")],
            [KeyboardButton(text="Даббер"), KeyboardButton(text="Таймер")],
            [KeyboardButton(text="Вернуться в меню")]
        ],
        resize_keyboard=True
    )