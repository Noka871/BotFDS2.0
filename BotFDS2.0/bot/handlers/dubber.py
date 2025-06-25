# Логика дабберов
from aiogram import Router, types
from aiogram.filters import Command
from bot.states import DubberStates
from bot.services.database import Database

router = Router()

@router.message(Command("report"))
async def start_report(message: types.Message, state: FSMContext):
    titles = await Database().get_user_titles(message.from_user.id)
    await message.answer("Выберите тайтл:", reply_markup=build_titles_kb(titles))
    await state.set_state(DubberStates.selecting_title)