from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text
from keyboards.dubber import dubber_menu_keyboard

router = Router()

@router.message(Text("Меню даббера"))
async def dubber_menu(message: Message):
    await message.answer(
        "Выберите действие:",
        reply_markup=dubber_menu_keyboard()
    )