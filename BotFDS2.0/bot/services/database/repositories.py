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

    from sqlalchemy import select
    from sqlalchemy.ext.asyncio import AsyncSession
    from .models import User, Title, Episode

    class UserRepository:
        def __init__(self, session: AsyncSession):
            self.session = session

        async def create_user(self, telegram_id: int, username: str, role: str):
            user = User(telegram_id=telegram_id, username=username, role=role)
            self.session.add(user)
            await self.session.commit()
            return user

    class TitleRepository:
        def __init__(self, session: AsyncSession):
            self.session = session

        async def create_title(self, name: str, episodes_count: int):
            title = Title(name=name, episodes_count=episodes_count)
            self.session.add(title)
            await self.session.commit()
            return title