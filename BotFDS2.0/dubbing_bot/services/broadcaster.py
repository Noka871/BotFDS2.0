# services/broadcaster.py
import logging

from aiogram import Bot
from database.requests import get_active_users
async def broadcast(bot: Bot, text: str):
    users = await get_active_users()
    for user in users:
        await bot.send_message(user.telegram_id, text)

from aiogram import Bot

async def broadcast_message(bot: Bot, text: str):
    """Массовая рассылка сообщения всем пользователям"""
    users = await get_active_users()
    for user in users:
        try:
            await bot.send_message(user.telegram_id, text)
            except Exception as e:
            logging.error(f"Ошибка отправки {user.telegram_id}: {e}")

        except Exception as e:
            print(f"Ошибка отправки пользователю {user.telegram_id}: {e}")

