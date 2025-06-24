from aiogram import Bot
from database.crud import get_pending_reports

async def send_reminders(bot: Bot):
    overdue = await get_pending_reports()
    for report in overdue:
        await bot.send_message(
            chat_id=report.user_id,
            text=f"Напоминание: сдайте серию {report.episode}"
        )