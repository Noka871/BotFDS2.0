from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from ..logger import logger, log_command
from ..states.timer_state import TimerState

router = Router()


def get_timer_main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Создать тайтл"), KeyboardButton(text="Отредактировать тайтл")],
            [KeyboardButton(text="Просмотреть график сдавших"), KeyboardButton(text="Создать рассылку")],
            [KeyboardButton(text="Просмотреть предупреждения"), KeyboardButton(text="Предупредить о форс-мажорах")],
            [KeyboardButton(text="Вернуться в меню")]
        ],
        resize_keyboard=True
    )


@router.message(F.text == "Таймер")
async def timer_menu(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "Таймер")

        await message.answer(
            "⏰ *Панель таймера*\n\n"
            "Выберите действие:",
            reply_markup=get_timer_main_kb(),
            parse_mode="Markdown"
        )
        logger.info(f"User {message.from_user.id} entered timer menu")

    except Exception as e:
        logger.error(f"Error in Таймер menu: {e}", exc_info=True)
        await message.answer("Произошла ошибка. Попробуйте позже.")


@router.message(F.text == "Создать тайтл")
async def create_title(message: Message, state: FSMContext):
    try:
        log_command(message.from_user.id, message.from_user.username, "Создать тайтл")

        await message.answer(
            "🎬 *Создание нового тайтла*\n\n"
            "Введите название тайтла:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="❌ Отмена")]],
                resize_keyboard=True
            ),
            parse_mode="Markdown"
        )
        await state.set_state(TimerState.creating_title)

    except Exception as e:
        logger.error(f"Error in Создать тайтл: {e}", exc_info=True)


@router.message(F.text == "Просмотреть график сдавших")
async def view_schedule(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "Просмотреть график сдавших")

        # Заглушка для теста
        schedule_text = """
📊 *График сдавших*:

*Тайтл 1114* (серия 5):
• User1 - ✅ Сдано
• User2 - ⏰ Задержка (1 день)
• User3 - ❌ Не сдано

*Тайтл 5678* (серия 3):
• User4 - ✅ Сдано
• User5 - ✅ Сдано
        """

        await message.answer(schedule_text, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error in Просмотреть график сдавших: {e}", exc_info=True)


@router.message(F.text == "Создать рассылку")
async def create_broadcast(message: Message, state: FSMContext):
    try:
        log_command(message.from_user.id, message.from_user.username, "Создать рассылку")

        await message.answer(
            "📢 *Создание рассылки*\n\n"
            "Введите сообщение для рассылки:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="❌ Отмена")]],
                resize_keyboard=True
            ),
            parse_mode="Markdown"
        )
        await state.set_state(TimerState.creating_broadcast)

    except Exception as e:
        logger.error(f"Error in Создать рассылку: {e}", exc_info=True)


@router.message(F.text == "Вернуться в меню")
async def back_to_menu(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "Вернуться в меню")

        from .start import get_main_kb
        await message.answer("Главное меню:", reply_markup=get_main_kb())

    except Exception as e:
        logger.error(f"Error in Вернуться в меню: {e}", exc_info=True)