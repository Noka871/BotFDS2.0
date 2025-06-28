# Основные обработчики
from aiogram import types, Dispatcher
from bot.keyboards.main_menu import get_main_menu
from bot.config import ADMIN_IDS


async def cmd_start(message: types.Message):
    """Обработка команды /start"""
    role = "admin" if message.from_user.id in ADMIN_IDS else "user"
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!",
        reply_markup=get_main_menu(role)
    )


async def cmd_help(message: types.Message):
    """Обработка кнопки Помощь"""
    help_text = """
    📚 Справка по боту:

    • /start - Главное меню
    • Для дабберов:
      - Выбрать тайтл - выбор проекта
      - Мои долги - просмотр несданных серий
    • Для таймеров:
      - Создать тайтл - добавить новый проект
      - Просмотреть график - статистика сдачи
    """
    await message.answer(help_text)


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(cmd_help, text="Помощь")