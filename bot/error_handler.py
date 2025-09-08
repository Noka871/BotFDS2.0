import logging
from aiogram import Dispatcher
from aiogram.types import ErrorEvent

from .logger import logger

async def error_handler(event: ErrorEvent):
    """Глобальный обработчик ошибок"""
    logger.error(
        f"Exception occurred: {event.exception}",
        exc_info=event.exception
    )

def register_error_handlers(dp: Dispatcher):
    """Регистрация обработчиков ошибок"""
    dp.errors.register(error_handler)