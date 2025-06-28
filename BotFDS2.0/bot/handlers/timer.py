# Для таймеров
from aiogram import types, Dispatcher

async def create_title(message: types.Message):
    """Создание нового тайтла"""
    await message.answer("📌 Введите название нового тайтла:")

async def view_schedule(message: types.Message):
    """Просмотр графика сдачи"""
    await message.answer("📊 График сдачи серий...")

def register_timer_handlers(dp: Dispatcher):
    """Регистрация обработчиков таймеров"""
    dp.register_message_handler(create_title, text='Создать тайтл')
    dp.register_message_handler(view_schedule, text='Просмотреть график')