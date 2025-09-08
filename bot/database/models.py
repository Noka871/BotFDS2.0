# database/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    role = Column(String)  # 'dubber', 'timer', 'admin'


class Title(Base):
    __tablename__ = 'titles'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    episodes_count = Column(Integer)
    current_episode = Column(Integer)


class DubberTitle(Base):
    __tablename__ = 'dubber_titles'
    id = Column(Integer, primary_key=True)
    dubber_id = Column(Integer)
    title_id = Column(Integer)