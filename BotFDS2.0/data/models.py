from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    role = Column(String(20))  # 'dubber', 'timer', 'admin'


class Title(Base):
    __tablename__ = 'titles'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    total_episodes = Column(Integer)


class UserTitle(Base):
    __tablename__ = 'user_titles'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    title_id = Column(Integer, ForeignKey('titles.id'), primary_key=True)
    role = Column(String(20))  # 'dubber' или 'timer'


class Episode(Base):
    __tablename__ = 'episodes'
    id = Column(Integer, primary_key=True)
    title_id = Column(Integer, ForeignKey('titles.id'))
    number = Column(Integer)
    dubber_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String(20))  # 'pending', 'done', 'delayed'
    deadline = Column(DateTime)
    penalty = Column(Float, default=0)
    comment = Column(String(500))