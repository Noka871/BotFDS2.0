# Работа с базой данных
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base

DATABASE_URL = "sqlite:///dubbing.db"

engine = create_engine(DATABASE_URL)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

Base.metadata.create_all(engine)