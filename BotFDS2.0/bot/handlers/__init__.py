# Регистрация всех обработчиков
from aiogram import Router
from .common import common_router
from .admin import admin_router
from .dubber import dubber_router
from .timer import timer_router

router = Router()
router.include_router(common_router)
router.include_router(admin_router)
router.include_router(dubber_router)
router.include_router(timer_router)