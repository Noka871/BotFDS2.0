from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_titles_keyboard(titles):
    markup = InlineKeyboardMarkup(row_width=2)
    for title in titles:
        markup.insert(InlineKeyboardButton(
            title.name,
            callback_data=f"title_{title.id}"
        ))
    markup.add(InlineKeyboardButton("Назад", callback_data="role_dubber"))
    return markup