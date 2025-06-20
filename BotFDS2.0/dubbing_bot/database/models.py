from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    role = Column(String)  # 'dubber', 'timer', 'admin'
    created_at = Column(DateTime, default=datetime.utcnow)


class Title(Base):
    __tablename__ = "titles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    episodes_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    dubbers = relationship("UserTitle", back_populates="title")


class UserTitle(Base):
    __tablename__ = "user_titles"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    title_id = Column(Integer, ForeignKey("titles.id"), primary_key=True)

    user = relationship("User")
    title = relationship("Title")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title_id = Column(Integer, ForeignKey("titles.id"))
    episode = Column(Integer)
    status = Column(String)  # 'submitted', 'delayed'
    comment = Column(String, nullable=True)
    penalty = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    deadline = Column(DateTime)

    user = relationship("User")
    title = relationship("Title")