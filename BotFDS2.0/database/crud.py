from sqlalchemy.ext.asyncio import AsyncSession
from models import User

async def get_user(session: AsyncSession, user_id: int) -> User:
    result = await session.execute(select(User).where(User.telegram_id == user_id))
    return result.scalar_one_or_none()