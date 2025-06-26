# Точка входа
import sys
from pathlib import Path
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .database import Database
from .config import config

sys.path.append(str(Path(__file__).parent.parent.parent))

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
storage = MemoryStorage()
db = Database()


# ============== СОСТОЯНИЯ FSM ==============
class DubberStates(StatesGroup):
    select_title = State()
    select_episode = State()
    report_status = State()
    report_comment = State()


class TimerStates(StatesGroup):
    create_title = State()
    assign_penalty = State()


# ============== КЛАВИАТУРЫ ==============
def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔊 Даббер"), KeyboardButton(text="⏱ Таймер")],
            [KeyboardButton(text="👑 Админ")] if config.ADMIN_ID else []
        ],
        resize_keyboard=True
    )


def get_dubber_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Отметить сдачу")],
            [KeyboardButton(text="📊 Мои долги"), KeyboardButton(text="🚨 Форс-мажор")],
            [KeyboardButton(text="🏠 Главное меню")]
        ],
        resize_keyboard=True
    )


# ============== ОБРАБОТЧИКИ КОМАНД ==============
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await db.set_user_role(message.from_user.id, "unassigned", message.from_user.username)
    await message.answer("Выберите роль:", reply_markup=get_main_menu())


@dp.message(F.text == "🔊 Даббер")
async def dubber_mode(message: types.Message):
    await db.set_user_role(message.from_user.id, "dubber")
    await message.answer("Режим даббера активирован!", reply_markup=get_dubber_menu())


# ============== ОТЧЕТНОСТЬ ДАББЕРОВ ==============
@dp.message(F.text == "📝 Отметить сдачу")
async def start_report(message: types.Message, state: FSMContext):
    titles = await db.get_user_titles(message.from_user.id)
    if not titles:
        return await message.answer("❌ Нет доступных тайтлов")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=title)] for title in titles],
        resize_keyboard=True
    )
    await message.answer("Выберите тайтл:", reply_markup=keyboard)
    await state.set_state(DubberStates.select_title)


@dp.message(DubberStates.select_title)
async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Введите номер серии:")
    await state.set_state(DubberStates.select_episode)


@dp.message(DubberStates.select_episode)
async def process_episode(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("❌ Введите число!")

    await state.update_data(episode=int(message.text))

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Сдал"), KeyboardButton(text="⏳ Задержка")]
        ],
        resize_keyboard=True
    )
    await message.answer("Статус сдачи:", reply_markup=keyboard)
    await state.set_state(DubberStates.report_status)


# ============== ЗАПУСК БОТА ==============
async def main():
    await db.init_db()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())