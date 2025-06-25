# Обработчики для дабберов
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database import Session
from models import Title, Report
from keyboards import get_dubbing_menu


class DubbingStates(StatesGroup):
    choosing_title = State()
    choosing_episode = State()
    report_status = State()
    force_majeure = State()


async def dubbing_menu(message: types.Message):
    await message.answer("Меню даббера:", reply_markup=get_dubbing_menu())


async def choose_title(message: types.Message):
    session = Session()
    # Получаем список тайтлов для этого даббера
    titles = session.query(Title).filter(Title.dubbers.any(username=message.from_user.username)).all()
    Session.remove()

    if not titles:
        await message.answer("У вас нет назначенных тайтлов.")
        return

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for title in titles:
        keyboard.add(KeyboardButton(title.name))
    keyboard.add(KeyboardButton("Назад"))

    await message.answer("Выберите тайтл:", reply_markup=keyboard)
    await DubbingStates.choosing_title.set()

# ... другие обработчики для дабберов