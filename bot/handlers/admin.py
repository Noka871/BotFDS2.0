"""
Обработчики для функционала администратора
"""
from aiogram import F, Router
from aiogram.types import Message

router = Router()

@router.message(F.text == "📤 Выгрузить отчет")
async def export_report(message: Message):
    """Выгрузка отчета"""
    await message.answer("📤 Функция выгрузки отчета будет доступна soon!")