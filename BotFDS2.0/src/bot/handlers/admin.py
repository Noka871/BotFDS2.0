# Админские функции
from aiogram import Router, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

# Создаем роутер
admin_router = Router()

# Регистрируем обработчики
@admin_router.message(Command("admin"))
async def admin_panel(message: Message):
    await message.answer("Добро пожаловать в админ-панель!")

# Функция для регистрации обработчиков
def register_handlers(dp: Dispatcher):
    dp.include_router(admin_router)

    print("Админ-модуль загружен")

    @admin_router.message(Command("ban"))
    async def ban_user(message: Message):
        # Логика бана пользователя
        pass

    from src.bot.config import config

    @admin_router.message(Command("admin"))
    async def admin_panel(message: Message):
        if message.from_user.id not in config.ADMIN_IDS:
            return await message.answer("Доступ запрещен!")
        # Показать админ-панель