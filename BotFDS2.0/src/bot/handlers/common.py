# Общие команды (/start, /menu)
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards import dubber_menu_kb, timer_menu_kb, admin_menu_kb
from database import get_user_role


async def setup_common_handlers(dp):
    @dp.message_handler(commands=['menu'])
    async def show_menu(message: types.Message):
        user_role = await get_user_role(message.from_user.id)

        if user_role == 'dubber':
            kb = dubber_menu_kb()
        elif user_role == 'timer':
            kb = timer_menu_kb()
        elif user_role == 'admin':
            kb = admin_menu_kb()
        else:
            kb = types.ReplyKeyboardRemove()

        await message.answer("Главное меню:", reply_markup=kb)
