from aiogram.utils.keyboard import ReplyKeyboardBuilder

def dubber_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Отчет о сдаче")
    builder.button(text="Мои долги")
    builder.button(text="Форс-мажор")
    builder.button(text="Назад")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)