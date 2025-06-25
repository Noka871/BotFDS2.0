from aiogram import types
from aiogram.dispatcher import FSMContext
from services.database import Database
from services.notifications import Notifier

db = Database()
notifier = Notifier()


async def handle_dubber_menu(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        "📺 Выбрать тайтл",
        "⏱ Добавить роль таймера",
        "⚠️ Форс-мажор",
        "📋 Мои долги",
        "🔙 Назад"
    )
    await message.answer("Меню даббера:", reply_markup=markup)


async def select_title(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    titles = await db.get_user_titles(user_id)

    if not titles:
        await message.answer("У вас нет назначенных тайтлов.")
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    for title in titles[:5]:
        markup.add(types.InlineKeyboardButton(
            text=f"{title['name']} (серия {title['current_episode']})",
            callback_data=f"title_{title['id']}"
        ))

    if len(titles) > 5:
        markup.add(types.InlineKeyboardButton("➡️ Далее", callback_data="next_page_1"))

    await message.answer("Выберите тайтл:", reply_markup=markup)
    await state.set_state(Form.dubber_report)