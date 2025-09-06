from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """Модель пользователя системы"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)  # username может быть None
    role = Column(String, default='dubber')  # Роль: dubber, timer, admin
    created_at = Column(DateTime, default=datetime.now)

    # Связи с другими таблицами
    created_titles = relationship("Title", back_populates="creator")
    dubber_titles = relationship("DubberTitle", back_populates="dubber")
    reports = relationship("Report", back_populates="dubber")
    force_majeures = relationship("ForceMajeure", back_populates="user")
    penalties = relationship("Penalty", foreign_keys="Penalty.dubber_id", back_populates="dubber")
    created_penalties = relationship("Penalty", foreign_keys="Penalty.created_by", back_populates="creator")


class Title(Base):
    """Модель тайтла (аниме/сериала)"""
    __tablename__ = 'titles'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Название тайтла
    total_episodes = Column(Integer, default=0)  # Общее количество серий
    current_episode = Column(Integer, default=0)  # Текущая серия
    created_by = Column(Integer, ForeignKey('users.id'))  # ID создателя
    created_at = Column(DateTime, default=datetime.now)

    # Связи
    creator = relationship("User", back_populates="created_titles")
    dubber_titles = relationship("DubberTitle", back_populates="title")
    reports = relationship("Report", back_populates="title")
    penalties = relationship("Penalty", back_populates="title")


class DubberTitle(Base):
    """Связующая таблица между дабберами и тайтлами"""
    __tablename__ = 'dubber_titles'

    id = Column(Integer, primary_key=True)
    dubber_id = Column(Integer, ForeignKey('users.id'))  # ID даббера
    title_id = Column(Integer, ForeignKey('titles.id'))  # ID тайтла
    assigned_at = Column(DateTime, default=datetime.now)  # Время назначения

    # Связи
    dubber = relationship("User", back_populates="dubber_titles")
    title = relationship("Title", back_populates="dubber_titles")


class Report(Base):
    """Модель отчета о сдаче серии"""
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True)
    dubber_id = Column(Integer, ForeignKey('users.id'))  # ID даббера
    title_id = Column(Integer, ForeignKey('titles.id'))  # ID тайтла
    episode = Column(Integer)  # Номер серии
    status = Column(String, default='pending')  # Статус: pending, submitted, delayed
    comment = Column(Text, nullable=True)  # Комментарий при задержке
    submitted_at = Column(DateTime, nullable=True)  # Время сдачи
    deadline = Column(DateTime, nullable=True)  # Дедлайн сдачи
    created_at = Column(DateTime, default=datetime.now)  # Время создания отчета

    # Связи
    dubber = relationship("User", back_populates="reports")
    title = relationship("Title", back_populates="reports")


class ForceMajeure(Base):
    """Модель уведомления о форс-мажоре"""
    __tablename__ = 'force_majeure'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # ID пользователя
    message = Column(Text, nullable=False)  # Сообщение о форс-мажоре
    created_at = Column(DateTime, default=datetime.now)  # Время создания

    # Связи
    user = relationship("User", back_populates="force_majeures")


class Penalty(Base):
    """Модель штрафа за просрочку сдачи"""
    __tablename__ = 'penalties'

    id = Column(Integer, primary_key=True)
    dubber_id = Column(Integer, ForeignKey('users.id'))  # ID даббера
    title_id = Column(Integer, ForeignKey('titles.id'))  # ID тайтла
    episode = Column(Integer)  # Номер серии
    amount = Column(Float, default=0)  # Сумма штрафа
    reason = Column(Text, nullable=True)  # Причина штрафа
    created_by = Column(Integer, ForeignKey('users.id'))  # ID создателя штрафа
    created_at = Column(DateTime, default=datetime.now)  # Время создания штрафа

    # Связи
    dubber = relationship("User", foreign_keys=[dubber_id], back_populates="penalties")
    title = relationship("Title", back_populates="penalties")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_penalties")