from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.main_menu import get_role_keyboard, get_dubber_keyboard, get_timer_keyboard

# Команда /start
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Выбери свою роль:",
        reply_markup=get_role_keyboard()
    )

# Обработчик кнопки "Даббер"
async def dubber_handler(message: types.Message):
    await message.answer(
        "🎤 Вы в меню даббера:",
        reply_markup=get_dubber_keyboard()  # Показываем клавиатуру даббера
    )

# Обработчик кнопки "Таймер"
async def timer_handler(message: types.Message):
    await message.answer(
        "⏱️ Вы в меню таймера:",
        reply_markup=get_timer_keyboard()  # Показываем клавиатуру таймера
    )

# Обработчик кнопки "Админ"
async def admin_handler(message: types.Message):
    await message.answer("🔐 Вы в меню администратора.")

# Регистрация всех обработчиков
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(dubber_handler, text="Даббер")
    dp.register_message_handler(timer_handler, text="Таймер")
    dp.register_message_handler(admin_handler, text="Админ")