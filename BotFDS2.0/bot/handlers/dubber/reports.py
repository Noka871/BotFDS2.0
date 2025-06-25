from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from states.dubber import ReportStates
from services.database.repositories import TitleRepository

router = Router()


@router.message(F.text == "Отчет о сдаче")
async def start_report(message: Message, state: FSMContext, session):
    repo = TitleRepository(session)
    titles = await repo.get_user_titles(message.from_user.id)

    if not titles:
        await message.answer("У вас нет назначенных тайтлов")
        return

    await state.set_state(ReportStates.select_title)
    await message.answer(
        "Выберите тайтл:",
        reply_markup=titles_keyboard(titles)
    )