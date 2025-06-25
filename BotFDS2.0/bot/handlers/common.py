# Общие команды (/start, /menu)
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from bot.keyboards.reply import main_menu_kb

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработка команды /start - приветствие и выбор роли"""
    await message.answer(
        "Добро пожаловать в бот управления дубляжом!\n"
        "Пожалуйста, выберите вашу роль:",
        reply_markup=main_menu_kb()
    )

@router.message(Command("menu"))
@router.message(F.text == "Вернуться в меню")
async def show_menu(message: Message):
    """Показ главного меню"""
    await message.answer(
        "Главное меню:",
        reply_markup=main_menu_kb()
    )