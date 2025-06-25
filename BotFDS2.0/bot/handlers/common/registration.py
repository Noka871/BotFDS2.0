from aiogram import Router, F
from aiogram.types import Message
from services.database.repositories import UserRepository

router = Router()

@router.message(F.text.in_(["Даббер", "Таймер"]))
async def register_user(message: Message, session: AsyncSession):
    repo = UserRepository(session)
    user = await repo.create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        role=message.text.lower()
    )
    await message.answer(f"Вы зарегистрированы как {user.role}!")