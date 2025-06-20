# services/broadcaster.py
from aiogram import Bot
from database.requests import get_active_users

async def send_to_all(bot: Bot, text: str):
    users = await get_active_users()
    for user in users:
        await bot.send_message(user.telegram_id, text)