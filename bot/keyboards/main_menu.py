# Клавиатуры
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_menu_keyboard(role: str = "dubber"):
    """Главное меню в зависимости от роли пользователя"""
    builder = ReplyKeyboardBuilder()

    if role == "dubber":
        builder.add(
            KeyboardButton(text="🎭 Выбрать тайтл"),
            KeyboardButton(text="⚙️ Добавить роль таймера"),
            KeyboardButton(text="⚠️ Предупредить о форс-мажорах"),
            KeyboardButton(text="📋 Мои долги")
        )
    elif role == "timer":
        builder.add(
            KeyboardButton(text="🎬 Создать тайтл"),
            KeyboardButton(text="✏️ Отредактировать тайтл"),
            KeyboardButton(text="📊 Просмотреть график сдавших"),
            KeyboardButton(text="📢 Создать рассылку"),
            KeyboardButton(text="🔔 Просмотреть предупреждения"),
            KeyboardButton(text="⚠️ Предупредить о форс-мажорах")
        )
    elif role == "admin":
        builder.add(
            KeyboardButton(text="🎭 Выбрать тайтл"),
            KeyboardButton(text="🎬 Создать тайтл"),
            KeyboardButton(text="✏️ Отредактировать тайтл"),
            KeyboardButton(text="📊 Просмотреть график сдавших"),
            KeyboardButton(text="📢 Создать рассылку"),
            KeyboardButton(text="🔔 Просмотреть предупреждения"),
            KeyboardButton(text="⚠️ Предупредить о форс-мажорах"),
            KeyboardButton(text="📋 Мои долги"),
            KeyboardButton(text="📤 Выгрузить отчет")
        )

    builder.add(KeyboardButton(text="🔙 Вернуться в меню"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)