# Регистрация всех обработчиков
from .common import register_common_handlers
from .admin import register_admin_handlers
from .dubber import register_dubber_handlers
from .timer import register_timer_handlers

def register_handlers(dp):
    register_common_handlers(dp)
    register_admin_handlers(dp)
    register_dubber_handlers(dp)
    register_timer_handlers(dp)