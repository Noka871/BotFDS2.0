from sqlalchemy import select
from database.db import async_session
from database.models import Report

async def create_report(user_id: int, title: str, episode: int, status: str):
    async with async_session() as session:
        report = Report(
            user_id=user_id,
            title=title,
            episode=episode,
            status=status
        )
        session.add(report)
        await session.commit()