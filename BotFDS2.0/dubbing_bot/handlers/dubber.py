from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.keyboards import get_dubber_menu

class DubberStates(StatesGroup):
    menu = State()
    select_title = State()
    select_episode = State()
    report_status = State()

async def dubber_menu(message: types.Message, state: FSMContext):
    await DubberStates.menu.set()
    await message.answer("Меню даббера:", reply_markup=get_dubber_menu())

def register_handlers_dubber(dp: Dispatcher):
    dp.register_message_handler(dubber_menu, text="🔊 Даббер", state="*")