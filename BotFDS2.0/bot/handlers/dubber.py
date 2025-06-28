# Для дабберов
from aiogram import types, Dispatcher
from bot.keyboards.main_menu import get_main_menu

async def select_title(message: types.Message):
    """Обработка выбора тайтла"""
    await message.answer("🔄 Список доступных тайтлов...")

async def show_debts(message: types.Message):
    """Показ несданных серий"""
    await message.answer("📝 Ваши текущие долги...")

def register_dubber_handlers(dp: Dispatcher):
    """Регистрация обработчиков дабберов"""
    dp.register_message_handler(select_title, text='Выбрать тайтл')
    dp.register_message_handler(show_debts, text='Мои долги')