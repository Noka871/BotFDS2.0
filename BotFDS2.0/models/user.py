# Модель пользователя
from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    is_dubbing = Column(Boolean, default=False)
    is_timer = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User {self.username}>"