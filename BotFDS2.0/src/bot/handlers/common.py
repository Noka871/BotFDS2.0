# Общие команды (/start, /menu)
from aiogram import Router, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from src.bot.keyboards.reply import main_menu_kb

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать! Выберите роль:",
        reply_markup=main_menu_kb()
    )

def register_handlers(dp: Dispatcher):
    dp.include_router(router)
