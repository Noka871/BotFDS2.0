from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_timer_main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Создать тайтл"), KeyboardButton(text="Отредактировать тайтл")],
            [KeyboardButton(text="Просмотреть график сдавших"), KeyboardButton(text="Создать рассылку")],
            [KeyboardButton(text="Просмотреть предупреждения"), KeyboardButton(text="Предупредить о форс-мажорах")],
            [KeyboardButton(text="Вернуться в меню")]
        ],
        resize_keyboard=True
    )