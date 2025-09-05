"""
Обработчики для функционала таймера
"""
from aiogram import F, Router
from aiogram.types import Message

router = Router()

@router.message(F.text == "🎬 Создать тайтл")
async def create_title(message: Message):
    """Создание тайтла"""
    await message.answer("🎬 Функция создания тайтла будет доступна soon!")

@router.message(F.text == "✏️ Отредактировать тайтл")
async def edit_title(message: Message):
    """Редактирование тайтла"""
    await message.answer("✏️ Функция редактирования тайтла будет доступна soon!")