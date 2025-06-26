# Инлайн кнопки
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def titles_kb(titles: list[str]) -> InlineKeyboardMarkup:
    """Клавиатура с выбором тайтлов"""
    buttons = [
        [InlineKeyboardButton(text=title, callback_data=f"title_{title}")]
        for title in titles
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def episodes_kb(episodes: list[int]) -> InlineKeyboardMarkup:
    """Клавиатура с выбором серий"""
    buttons = [
        [InlineKeyboardButton(text=f"Серия {ep}", callback_data=f"ep_{ep}")]
        for ep in episodes
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Экспорт функций
__all__ = ['titles_kb', 'episodes_kb']

if __name__ == "__main__":
    print("Пример тайтлов:", titles_kb(["Тайтл 1", "Тайтл 2"]))
    print("Пример серий:", episodes_kb([1, 2, 3]))