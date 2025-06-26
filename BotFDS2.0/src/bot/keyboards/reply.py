# Ответные кнопки
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_kb() -> ReplyKeyboardMarkup:
    """Возвращает главное меню бота"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Даббер")],
            [KeyboardButton(text="Таймер")],
            [KeyboardButton(text="Админ")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

# Тестовая проверка
if __name__ == "__main__":
    print(main_menu_kb())