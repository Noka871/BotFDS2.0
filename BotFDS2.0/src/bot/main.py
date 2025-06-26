# Точка входа
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Инициализация бота и диспетчера
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


# ========== КОМАНДА /start ==========
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add(KeyboardButton("🔊 Даббер"))
    menu.add(KeyboardButton("⏱ Таймер"))

    await message.answer(
        "🔮 <b>WitchKSH Bot</b>\n"
        "Выберите вашу роль:",
        reply_markup=menu,
        parse_mode="HTML"
    )


# ========== КОМАНДА /help ==========
@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    help_text = (
        "ℹ️ <b>Справка по боту</b>\n\n"
        "<b>Для дабберов:</b>\n"
        "- Отмечайте сданные серии\n"
        "- Получайте уведомления\n\n"
        "<b>Для таймеров:</b>\n"
        "- Управляйте тайтлами\n"
        "- Назначайте штрафы"
    )
    await message.answer(help_text, parse_mode="HTML")


# ========== КОМАНДА /menu ==========
@dp.message_handler(commands=['menu'])
async def cmd_menu(message: types.Message):
    # Здесь должна быть проверка роли пользователя
    menu = ReplyKeyboardMarkup(resize_keyboard=True)

    # Временное меню для примера
    menu.add(KeyboardButton("Мои задачи"))
    menu.add(KeyboardButton("Отчеты"))

    await message.answer("📋 Главное меню:", reply_markup=menu)


# ========== ОБРАБОТКА КНОПОК ==========
@dp.message_handler(text="🔊 Даббер")
async def set_dubber(message: types.Message):
    # Здесь должна быть логика назначения роли
    await message.answer("Вы выбрали роль 🔊 Даббера")


@dp.message_handler(text="⏱ Таймер")
async def set_timer(message: types.Message):
    # Здесь должна быть логика назначения роли
    await message.answer("Вы выбрали роль ⏱ Таймера")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)