# Регистрация всех обработчиков
from aiogram import Dispatcher

def register_handlers(dp: Dispatcher):
    from . import common  # Импорт других обработчиков
    common.register_handlers(dp)