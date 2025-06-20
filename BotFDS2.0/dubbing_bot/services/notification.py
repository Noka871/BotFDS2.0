from aiogram import Bot
from config.settings import settings
from datetime import datetime, timedelta
from database.repository import Repository

async def send_reminder(bot: Bot, chat_id: int, title_id: int, episode: int):
    title = await Repository.get_title(title_id)
    await bot.send_message(
        chat_id,
        f"⏰ Напоминание! Серия {episode} тайтла '{title.name}' не сдана!"
    )

async def check_deadlines(bot: Bot):
    expired_reports = await Repository.get_expired_reports()
    for report in expired_reports:
        await send_reminder(bot, report.user.telegram_id, report.title_id, report.episode)
        await Repository.apply_penalty(report.id, penalty=100)  # Пример штрафа