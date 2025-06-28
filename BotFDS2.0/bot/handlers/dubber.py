from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.main_menu import get_dubber_keyboard

# Обработчик кнопки "Даббер"
async def dubber_menu(message: types.Message):
    await message.answer(
        "🎤 Меню даббера:",
        reply_markup=get_dubber_keyboard()
    )

# Обработчик "Выбрать тайтл"
async def select_title(message: types.Message):
    # Здесь будет запрос к БД для получения списка тайтлов
    await message.answer("Выберите тайтл из списка...")

# Регистрация обработчиков даббера
def register_dubber_handlers(dp: Dispatcher):
    dp.register_message_handler(dubber_menu, text="Даббер")
    dp.register_message_handler(select_title, text="Выбрать тайтл")