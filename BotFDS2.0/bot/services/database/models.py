from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    full_name = Column(String(200))
    role = Column(String(20), nullable=False)  # 'dubber', 'timer', 'admin'
    created_at = Column(DateTime, default=datetime.utcnow)

    titles = relationship('UserTitle', back_populates='user')


class Title(Base):
    __tablename__ = 'titles'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    episodes_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship('UserTitle', back_populates='title')
    episodes = relationship('Episode', back_populates='title')


class UserTitle(Base):
    __tablename__ = 'user_titles'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    title_id = Column(Integer, ForeignKey('titles.id'), primary_key=True)

    user = relationship('User', back_populates='titles')
    title = relationship('Title', back_populates='users')