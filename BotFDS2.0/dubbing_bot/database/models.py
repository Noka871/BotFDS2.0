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

    # database/models.py
    class User(Base):
        # ...
        reports = relationship("Report", back_populates="user")

    class Report(Base):
        # ...
        user_id = Column(Integer, ForeignKey('users.id'))
        user = relationship("User", back_populates="reports")

        class Title(Base):
            __tablename__ = 'titles'
            id = Column(Integer, primary_key=True)
            dubbers = relationship("User", secondary="user_titles")

        user_titles = Table(
            'user_titles', Base.metadata,
            Column('user_id', ForeignKey('users.id')),
            Column('title_id', ForeignKey('titles.id'))
        )