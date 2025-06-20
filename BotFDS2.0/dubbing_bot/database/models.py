# database/models.py
from sqlalchemy import Column, Integer, String, DateTime
from database.db import Base

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String)
    episode = Column(Integer)
    status = Column(String)  # "done" или "delayed"
    created_at = Column(DateTime)