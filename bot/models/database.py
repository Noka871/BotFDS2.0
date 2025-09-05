import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from config import DATABASE_URL, DB_ECHO

# Создание асинхронного движка БД
engine = create_async_engine(
    DATABASE_URL,
    echo=DB_ECHO,  # Показывать SQL запросы в консоли
    future=True
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)  # Telegram user ID
    username = Column(String(100), nullable=True)
    full_name = Column(String(200), nullable=False)
    role = Column(String(20), default="dubber")  # dubber, timer, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


class Title(Base):
    """Модель тайтла (проекта)"""
    __tablename__ = "titles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, unique=True)
    total_episodes = Column(Integer, default=0)
    current_episode = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"))  # ID создателя (таймера)
    created_at = Column(DateTime, default=func.now())
    marks_ready_at = Column(DateTime, nullable=True)  # Когда вышли метки

    def __repr__(self):
        return f"<Title {self.name} (Ep: {self.current_episode}/{self.total_episodes})>"


class UserTitle(Base):
    """Связь пользователя с тайтлом (многие ко многим)"""
    __tablename__ = "user_titles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title_id = Column(Integer, ForeignKey("titles.id"), nullable=False)
    assigned_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<UserTitle user_id={self.user_id}, title_id={self.title_id}>"


class Report(Base):
    """Модель отчета о сдаче серии"""
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title_id = Column(Integer, ForeignKey("titles.id"), nullable=False)
    episode = Column(Integer, nullable=False)
    status = Column(String(20))  # submitted, delayed, pending
    comment = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=func.now())
    deadline = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Report user_id={self.user_id} title_id={self.title_id} ep={self.episode} status={self.status}>"


class Penalty(Base):
    """Модель штрафа"""
    __tablename__ = "penalties"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title_id = Column(Integer, ForeignKey("titles.id"), nullable=False)
    episode = Column(Integer, nullable=False)
    amount = Column(Integer, default=0)  # Сумма штрафа
    reason = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))  # Кто выставил штраф
    created_at = Column(DateTime, default=func.now())
    is_paid = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Penalty user_id={self.user_id} amount={self.amount}>"


class Notification(Base):
    """Модель уведомления"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Если null - рассылка всем
    title_id = Column(Integer, ForeignKey("titles.id"), nullable=True)
    message = Column(Text, nullable=False)
    type = Column(String(20))  # marks_ready, force_majeure, broadcast, reminder
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Notification from={self.from_user_id} type={self.type}>"


async def init_db():
    """Инициализация базы данных - создание таблиц"""
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  # Раскомментировать для сброса БД
        await conn.run_sync(Base.metadata.create_all)
    print("✅ База данных инициализирована")


async def get_db():
    """Dependency для получения сессии БД"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()