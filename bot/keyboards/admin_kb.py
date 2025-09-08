from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_admin_main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Выгрузить отчет"), KeyboardButton(text="Статистика системы")],
            [KeyboardButton(text="Управление пользователями"), KeyboardButton(text="Отправить уведомление")],
            [KeyboardButton(text="Даббер"), KeyboardButton(text="Таймер")],
            [KeyboardButton(text="Вернуться в меню")]
        ],
        resize_keyboard=True
    )