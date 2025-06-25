# Построители клавиатур
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keyboards.templates import MENU_BUTTONS

def role_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Даббер")
    builder.button(text="Таймер")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def menu_keyboard(role: str):
    builder = ReplyKeyboardBuilder()
    for button in MENU_BUTTONS[role]:
        builder.button(text=button)
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)