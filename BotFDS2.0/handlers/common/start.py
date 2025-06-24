from aiogram import types
from aiogram.dispatcher import FSMContext
from core.bot import dp
from utils.keyboards import main_menu_kb

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать! Выберите роль:",
        reply_markup=main_menu_kb()
    )