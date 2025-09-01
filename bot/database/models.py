# Модели данных
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    role = Column(String)  # 'dubber', 'timer', 'admin'

class Title(Base):
    __tablename__ = 'titles'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    total_episodes = Column(Integer)