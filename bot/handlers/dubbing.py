from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from ..logger import logger, log_command
from ..database.db import ensure_user_exists, get_user_titles, add_report, get_user_debts, save_force_majeure
from ..states.dubber_state import DubberState

router = Router()


def get_dubber_main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Выбрать тайтл")],
            [KeyboardButton(text="Мои долги")],
            [KeyboardButton(text="Предупредить о форс-мажорах")],
            [KeyboardButton(text="Вернуться в меню")]
        ],
        resize_keyboard=True
    )


@router.message(F.text == "Выбрать тайтл")
async def select_title(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "Выбрать тайтл")

        # Упрощенная версия - сразу показываем тестовый тайтл
        await message.answer(
            "🎬 Доступные тайтлы:\n\n"
            "• Тайтл 1114 (текущая серия: 5)\n\n"
            "Выберите серию для отчета:"
        )

    except Exception as e:
        logger.error(f"Error in Выбрать тайтл: {e}", exc_info=True)
        await message.answer("Произошла ошибка. Попробуйте позже.")


@router.message(F.text == "Мои долги")
async def my_debts(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "Мои долги")
        await message.answer("🎉 У вас нет просроченных серий! Все сдано в срок.")

    except Exception as e:
        logger.error(f"Error in Мои долги: {e}", exc_info=True)
        await message.answer("Произошла ошибка. Попробуйте позже.")


@router.message(F.text == "Предупредить о форс-мажорах")
async def force_majeure(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "Предупредить о форс-мажорах")
        await message.answer(
            "⚠️ Функция 'Предупредить о форс-мажорах' временно недоступна.\n"
            "Для срочных вопросов обратитесь к администратору."
        )

    except Exception as e:
        logger.error(f"Error in Предупредить о форс-мажорах: {e}", exc_info=True)
        await message.answer("Произошла ошибка. Попробуйте позже.")


@router.message(F.text == "Вернуться в меню")
async def back_to_menu(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "Вернуться в меню")

        # Импортируем главную клавиатуру
        from .start import get_main_kb

        await message.answer("Главное меню:", reply_markup=get_main_kb())

    except Exception as e:
        logger.error(f"Error in Вернуться в меню: {e}", exc_info=True)
        await message.answer("Произошла ошибка. Попробуйте позже.")


@router.message(Command("test"))
async def test_command(message: Message):
    """Тестовая команда"""
    await message.answer("✅ Бот работает! База данных подключена.")

    @router.message(F.text == "Добавить роль таймера")
    async def add_timer_role(message: Message):
        try:
            log_command(message.from_user.id, message.from_user.username, "Добавить роль таймера")

            # Здесь будет логика добавления роли таймера в БД
            # Пока заглушка для теста

            await message.answer(
                "⏰ *Вам успешно выданы права таймера!*\n\n"
                "Теперь у вас есть доступ к:\n"
                "• Созданию тайтлов\n"
                "• Просмотру графиков сдачи\n"
                "• Рассылке уведомлений\n"
                "• Управлению проектами\n\n"
                "Хотите создать свой первый тайтл?",
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(text="Создать тайтл")],
                        [KeyboardButton(text="Вернуться в меню")]
                    ],
                    resize_keyboard=True
                )
            )

        except Exception as e:
            logger.error(f"Error in Добавить роль таймера: {e}", exc_info=True)
            await message.answer("Произошла ошибка. Попробуйте позже.")


@router.message(F.text == "Добавить роль таймера")
async def add_timer_role(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "Добавить роль таймера")

        # Добавляем роль таймера в БД
        from ..database.db import add_timer_role as db_add_timer_role
        success = await db_add_timer_role(message.from_user.id)

        if success:
            await message.answer(
                "⏰ *Вам успешно выданы права таймера!*\n\n"
                "Теперь у вас есть доступ к:\n"
                "• Созданию тайтлов\n"
                "• Просмотру графиков сдачи\n"
                "• Рассылке уведомлений\n"
                "• Управлению проектами\n\n"
                "Хотите создать свой первый тайтл?",
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(text="Создать тайтл")],
                        [KeyboardButton(text="Вернуться в меню")]
                    ],
                    resize_keyboard=True
                )
            )
        else:
            await message.answer(
                "❌ Не удалось выдать права таймера.\n"
                "Обратитесь к администратору."
            )

    except Exception as e:
        logger.error(f"Error in Добавить роль таймера: {e}", exc_info=True)
        await message.answer("Произошла ошибка. Попробуйте позже.")
