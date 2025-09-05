from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.database import User, Title, UserTitle, Report


async def get_or_create_user(session: AsyncSession, user_id: int, username: str, full_name: str) -> User:
    """Получить или создать пользователя"""
    result = await session.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        user = User(user_id=user_id, username=username, full_name=full_name)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    elif user.username != username or user.full_name != full_name:
        # Обновляем данные, если изменились
        user.username = username
        user.full_name = full_name
        await session.commit()
        await session.refresh(user)

    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    """Получить пользователя по ID"""
    result = await session.execute(select(User).where(User.user_id == user_id))
    return result.scalar_one_or_none()


async def get_user_titles(session: AsyncSession, user_id: int) -> list[Title]:
    """Получить тайтлы пользователя"""
    result = await session.execute(
        select(Title)
        .join(UserTitle, UserTitle.title_id == Title.id)
        .join(User, User.id == UserTitle.user_id)
        .where(User.user_id == user_id)
        .where(Title.is_active == True)
    )
    return result.scalars().all()


async def is_user_admin(session: AsyncSession, user_id: int) -> bool:
    """Проверить, является ли пользователь админом"""
    user = await get_user_by_id(session, user_id)
    return user and user.role == "admin"


async def is_user_timer(session: AsyncSession, user_id: int) -> bool:
    """Проверить, является ли пользователь таймером"""
    user = await get_user_by_id(session, user_id)
    return user and user.role in ["timer", "admin"]


async def get_title_by_name(session: AsyncSession, name: str) -> Title:
    """Получить тайтл по имени"""
    result = await session.execute(select(Title).where(Title.name == name))
    return result.scalar_one_or_none()


async def create_user_title_association(session: AsyncSession, user_id: int, title_id: int):
    """Создать связь пользователя с тайтлом"""
    # Проверяем, нет ли уже такой связи
    result = await session.execute(
        select(UserTitle)
        .where(UserTitle.user_id == user_id)
        .where(UserTitle.title_id == title_id)
    )
    existing = result.scalar_one_or_none()

    if not existing:
        user_title = UserTitle(user_id=user_id, title_id=title_id)
        session.add(user_title)
        await session.commit()


async def get_user_reports(session: AsyncSession, user_id: int, title_id: int = None) -> list[Report]:
    """Получить отчеты пользователя"""
    query = select(Report).where(Report.user_id == user_id)

    if title_id:
        query = query.where(Report.title_id == title_id)

    result = await session.execute(query)
    return result.scalars().all()