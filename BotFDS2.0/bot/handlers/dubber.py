# Логика дабберов
from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.keyboards import dubber_keyboards
from bot.services.database import Database

router = Router()

@router.message(Text("Выбрать тайтл"))
async def select_title(message: types.Message, state: FSMContext):
    titles = await Database().get_user_titles(message.from_user.id)
    await message.answer(
        "Выберите тайтл:",
        reply_markup=dubber_keyboards.titles_kb(titles)
    )