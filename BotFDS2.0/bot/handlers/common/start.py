from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards.builders import role_keyboard

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Добро пожаловать в систему отчетов!\n"
        "Пожалуйста, выберите вашу роль:",
        reply_markup=role_keyboard()
    )