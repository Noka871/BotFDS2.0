from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.keyboards import get_role_keyboard

async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "👋 Добро пожаловать в бот для управления отчетностью!\n"
        "Выберите вашу роль:",
        reply_markup=get_role_keyboard()
    )

def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")