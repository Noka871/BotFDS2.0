from aiogram.types import Message
import asyncio

async def typing_animation(message: Message, duration: float = 1.0):
    """Анимация печати"""
    await message.bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(duration)

async def success_animation(message: Message, text: str):
    """Анимация успешного действия"""
    await typing_animation(message, 0.5)
    await message.answer(f"✅ {text}")

async def error_animation(message: Message, text: str):
    """Анимация ошибки"""
    await typing_animation(message, 0.5)
    await message.answer(f"❌ {text}")

async def loading_animation(message: Message, text: str = "Загрузка..."):
    """Анимация загрузки"""
    msg = await message.answer(f"⏳ {text}")
    await typing_animation(message, 1.0)
    return msg