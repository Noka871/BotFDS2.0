# Построители клавиатур
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def build_dynamic_kb(items: list, width: int = 2):
    builder = ReplyKeyboardBuilder()
    for item in items:
        builder.button(text=item['name'])
    builder.adjust(width)
    return builder.as_markup()