from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from states.common import RegistrationStates
from services.database.repositories import UserRepository

router = Router()


@router.message(F.text.in_(["Даббер", "Таймер"]))
async def process_role_selection(message: Message, state: FSMContext, session):
    role = message.text.lower()
    repo = UserRepository(session)

    if await repo.get_user(message.from_user.id):
        await message.answer("Вы уже зарегистрированы!")
        return

    await repo.create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        role=role
    )

    await message.answer(
        f"Вы успешно зарегистрированы как {role}!\n"
        "Теперь вам доступно соответствующее меню.",
        reply_markup=menu_keyboard(role)
    )
    await state.clear()