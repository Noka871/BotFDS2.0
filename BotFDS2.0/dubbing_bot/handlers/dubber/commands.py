# handlers/dubber/commands.py
from aiogram import types, Dispatcher
from keyboards.reply import dubber_menu

async def dubber_start(message: types.Message):
    await message.answer("Меню даббера:", reply_markup=dubber_menu())

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(dubber_start, text="🔊 Даббер", state="*")