# Планировщик задач
from apscheduler.schedulers.asyncio import AsyncIOScheduler

def setup_scheduler(dp):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_overdue, 'cron', hour=10)
    scheduler.start()