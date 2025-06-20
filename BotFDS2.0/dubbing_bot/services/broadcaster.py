from aiogram import Bot
from database.requests import get_active_users

async def broadcast_message(bot: Bot, text: str):
    """Массовая рассылка сообщения всем пользователям"""
    users = await get_active_users()
    for user in users:
        try:
            await bot.send_message(chat_id=user.telegram_id, text=text)
        except Exception as e:
            print(f"Ошибка отправки пользователю {user.telegram_id}: {e}")