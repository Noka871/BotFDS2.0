from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.database import Database
from services.notifications import Notifier

db = Database()
notifier = Notifier()


def setup_scheduler(dp):
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    @scheduler.scheduled_job("cron", hour=10, minute=0)
    async def send_daily_reminders():
        overdue = await db.get_overdue_reports()
        for report in overdue:
            await notifier.send_reminder(
                user_id=report['user_id'],
                title=report['title'],
                episode=report['episode'],
                days_overdue=report['days_overdue']
            )

    scheduler.start()