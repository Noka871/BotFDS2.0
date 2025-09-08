from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_dubber_main_kb():
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

def get_titles_kb(titles):
    buttons = []
    for title in titles:
        buttons.append([InlineKeyboardButton(
            text=title['name'],
            callback_data=f"title_{title['id']}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_episode_status_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Серию сдал")],
            [KeyboardButton(text="Серию задержу")],
            [KeyboardButton(text="Отмена")]
        ],
        resize_keyboard=True
    )
