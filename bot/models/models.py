from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timedelta
import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    full_name = Column(String(100))
    role = Column(String(20), default="dubber")  # dubber, timer, admin
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи
    titles = relationship("UserTitle", back_populates="user")
    reports = relationship("Report", back_populates="user")
    penalties = relationship("Penalty", back_populates="user")
    notifications = relationship("Notification", back_populates="user")


class Title(Base):
    __tablename__ = "titles"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    total_episodes = Column(Integer, default=0)
    current_episode = Column(Integer, default=1)
    timer_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    marks_ready_at = Column(DateTime)

    # Связи
    users = relationship("UserTitle", back_populates="title")
    reports = relationship("Report", back_populates="title")
    penalties = relationship("Penalty", back_populates="title")
    notifications = relationship("Notification", back_populates="title")


class UserTitle(Base):
    __tablename__ = "user_titles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title_id = Column(Integer, ForeignKey("titles.id"))

    # Связи
    user = relationship("User", back_populates="titles")
    title = relationship("Title", back_populates="users")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title_id = Column(Integer, ForeignKey("titles.id"))
    episode = Column(Integer, nullable=False)
    status = Column(String(20))  # submitted, delayed
    comment = Column(Text)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    deadline = Column(DateTime)

    # Связи
    user = relationship("User", back_populates="reports")
    title = relationship("Title", back_populates="reports")


class Penalty(Base):
    __tablename__ = "penalties"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title_id = Column(Integer, ForeignKey("titles.id"))
    episode = Column(Integer)
    amount = Column(Integer, default=0)
    reason = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи
    user = relationship("User", back_populates="penalties")
    title = relationship("Title", back_populates="penalties")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    from_user_id = Column(Integer, ForeignKey("users.id"))
    title_id = Column(Integer, ForeignKey("titles.id"), nullable=True)
    message = Column(Text)
    type = Column(String(20))  # marks_ready, force_majeure, broadcast
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи
    user = relationship("User", back_populates="notifications")
    title = relationship("Title", back_populates="notifications")