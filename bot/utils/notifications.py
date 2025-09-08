import asyncio
from datetime import datetime, timedelta
from aiogram import Bot
from ..database.db import get_db_connection
from ..logger import logger


async def check_deadlines(bot: Bot):
    """Проверка дедлайнов и отправка уведомлений"""
    try:
        logger.info("Checking deadlines...")

        # Здесь будет логика проверки просроченных заданий
        # и отправки уведомлений пользователям

        # Заглушка для теста
        logger.info("Deadline check completed")

    except Exception as e:
        logger.error(f"Error in deadline check: {e}")


async def start_notification_scheduler(bot: Bot):
    """Запуск планировщика уведомлений"""

    async def scheduler():
        while True:
            try:
                # Проверяем дедлайны каждый день в 10:00
                now = datetime.now()
                target_time = now.replace(hour=10, minute=0, second=0, microsecond=0)

                if now > target_time:
                    target_time += timedelta(days=1)

                wait_seconds = (target_time - now).total_seconds()
                await asyncio.sleep(wait_seconds)

                await check_deadlines(bot)

                # Ждем до следующего дня
                await asyncio.sleep(86400 - wait_seconds)

            except Exception as e:
                logger.error(f"Error in notification scheduler: {e}")
                await asyncio.sleep(3600)  # Ждем час при ошибке

    # Запускаем планировщик в фоне
    asyncio.create_task(scheduler())
    logger.info("Notification scheduler started")