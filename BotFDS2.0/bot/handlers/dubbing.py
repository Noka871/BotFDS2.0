# Функционал для дабберов
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.keyboards.inline import titles_kb, episodes_kb
from bot.utils.states import DubbingStates
from bot.services.database import get_user_titles

router = Router()

@router.message(F.text == "Даббер")
async def dubbing_menu(message: Message):
    """Меню даббера"""
    await message.answer(
        "Выберите действие:",
        reply_markup=get_dubbing_menu_kb()
    )

@router.message(F.text == "Выбрать тайтл")
async def select_title(message: Message):
    """Выбор тайтла для отметки о сдаче"""
    titles = await get_user_titles(message.from_user.id)
    await message.answer(
        "Выберите тайтл:",
        reply_markup=titles_kb(titles)
    )

# Другие обработчики для дабберов...