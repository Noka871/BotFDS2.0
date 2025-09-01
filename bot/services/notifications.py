# Уведомления
from aiogram import Bot
from datetime import datetime, timedelta

async def send_daily_reminders(bot: Bot):
    # Получаем просроченные задачи
    overdue = await get_overdue_episodes()
    for task in overdue:
        await bot.send_message(
            task.user_id,
            f"⚠️ Просрочена сдача: {task.title_name} серия {task.episode}"