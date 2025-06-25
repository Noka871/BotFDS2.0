# Планировщик задач
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.notifications import send_reminders

scheduler = AsyncIOScheduler()

def setup_scheduler(bot):
    scheduler.add_job(
        send_reminders,
        'cron',
        hour=10,
        minute=0,
        args=[bot]
    )
    scheduler.start()