from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline import get_titles_keyboard
from utils.states import DubberStates

@dp.callback_query_handler(text="role_dubber")
async def dubber_menu(callback: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Выбрать тайтл", callback_data="select_title"))
    markup.add(types.InlineKeyboardButton("Мои долги", callback_data="my_debts"))
    await callback.message.edit_text("Меню даббера:", reply_markup=markup)

@dp.callback_query_handler(text="select_title")
async def select_title(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    titles = await get_user_titles(user_id)  # Ваша функция для получения тайтлов пользователя
    await callback.message.edit_text(
        "Выберите тайтл:",
        reply_markup=get_titles_keyboard(titles)
    )
    await DubberStates.select_episode.set()