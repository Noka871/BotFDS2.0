# Уведомления
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from sqlalchemy.future import select

from models.database import AsyncSessionLocal
from models.models import Title, User, Report


async def send_daily_reminders(bot):
    """Ежедневные напоминания о несданных сериях"""
    async with AsyncSessionLocal() as session:
        # Находим просроченные сдачи
        result = await session.execute(
            select(Report)
            .where(Report.deadline < datetime.utcnow())
            .where(Report.status.is_(None))
        )
        overdue_reports = result.scalars().all()

        for report in overdue_reports:
            try:
                await bot.send_message(
                    report.user.user_id,
                    f"⏰ <b>Напоминание о просрочке</b>\n\n"
                    f"🎬 Тайтл: {report.title.name}\n"
                    f"📺 Серия: {report.episode}\n"
                    f"❌ Просрочено: {report.deadline.strftime('%d.%m.%Y %H:%M')}\n\n"
                    f"Пожалуйста, сдайте серию как можно скорее!"
                )
            except Exception as e:
                print(f"Не удалось отправить напоминание пользователю {report.user.username}: {e}")


async def schedule_daily_reminders(bot):
    """Планирование ежедневных напоминаний"""
    scheduler = AsyncIOScheduler()

    # Напоминания каждый день в 10:00
    scheduler.add_job(
        send_daily_reminders,
        CronTrigger(hour=10, minute=0),
        args=[bot]
    )

    scheduler.start()