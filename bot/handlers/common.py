"""
Общие обработчики команд (/start, /help, /menu)
"""
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import logging

from keyboards import get_main_menu_keyboard
from models.database import AsyncSessionLocal
from utils.helpers import get_or_create_user

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    logger.info(f"Обработка /start от пользователя {message.from_user.id}")
    await state.clear()

    try:
        async with AsyncSessionLocal() as session:
            user = await get_or_create_user(
                session,
                message.from_user.id,
                message.from_user.username,
                message.from_user.full_name
            )

            welcome_text = (
                "🎬 <b>Добро пожаловать в систему отчетности дубляжа!</b>\n\n"
                f"👋 Привет, {message.from_user.full_name}!\n"
                f"🎭 Ваша роль: {user.role}\n\n"
                "Используйте кнопки меню для навигации:"
            )

            await message.answer(welcome_text, reply_markup=get_main_menu_keyboard(user.role))
            logger.info(f"Отправлено приветствие пользователю {message.from_user.id}")

    except Exception as e:
        logger.error(f"Ошибка в /start: {e}")
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    """Обработчик команды /menu"""
    logger.info(f"Обработка /menu от пользователя {message.from_user.id}")

    try:
        async with AsyncSessionLocal() as session:
            user = await get_or_create_user(
                session,
                message.from_user.id,
                message.from_user.username,
                message.from_user.full_name
            )

            logger.info(f"Роль пользователя {message.from_user.id}: {user.role}")
            await message.answer("📋 <b>Главное меню</b>", reply_markup=get_main_menu_keyboard(user.role))
            logger.info(f"Отправлено меню пользователю {message.from_user.id}")

    except Exception as e:
        logger.error(f"Ошибка в /menu: {e}")
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    logger.info(f"Обработка /help от пользователя {message.from_user.id}")

    try:
        help_text = (
            "🤖 <b>Помощь по боту</b>\n\n"
            "• /start - Запустить бота\n"
            "• /menu - Главное меню\n"
            "• /help - Эта справка\n\n"
            "Нажмите /menu чтобы увидеть доступные функции!"
        )

        await message.answer(help_text)
        logger.info(f"Отправлена справка пользователю {message.from_user.id}")

    except Exception as e:
        logger.error(f"Ошибка в /help: {e}")
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")

"""Обработчики для кнопок меню"""

@router.message(F.text == "🔙 Вернуться в меню")
async def back_to_menu(message: Message):
    """Возврат в главное меню"""
    logger.info(f"Возврат в меню от пользователя {message.from_user.id}")
    await cmd_menu(message)

# Обработчики для кнопок меню
@router.message(F.text == "🎭 Выбрать тайтл")
async def select_title_handler(message: Message):
    """Обработчик кнопки Выбрать тайтл"""
    logger.info(f"Нажата кнопка 'Выбрать тайтл' от {message.from_user.id}")
    await message.answer("🎭 Функция выбора тайтла будет доступна soon!")

@router.message(F.text == "⚙️ Добавить роль таймера")
async def add_timer_role_handler(message: Message):
    """Обработчик кнопки Добавить роль таймера"""
    logger.info(f"Нажата кнопка 'Добавить роль таймера' от {message.from_user.id}")
    await message.answer("⚙️ Функция добавления роли таймера будет доступна soon!")

@router.message(F.text == "⚠️ Предупредить о форс-мажорах")
async def force_majeure_handler(message: Message):
    """Обработчик кнопки Форс-мажор"""
    logger.info(f"Нажата кнопка 'Форс-мажор' от {message.from_user.id}")
    await message.answer("⚠️ Функция форс-мажора будет доступна soon!")

@router.message(F.text == "📋 Мои долги")
async def my_debts_handler(message: Message):
    """Обработчик кнопки Мои долги"""
    logger.info(f"Нажата кнопка 'Мои долги' от {message.from_user.id}")
    await message.answer("📋 Функция просмотра долгов будет доступна soon!")

@router.message(F.text == "🎬 Создать тайтл")
async def create_title_handler(message: Message):
    """Обработчик кнопки Создать тайтл"""
    logger.info(f"Нажата кнопка 'Создать тайтл' от {message.from_user.id}")
    await message.answer("🎬 Функция создания тайтла будет доступна soon!")

@router.message(F.text == "✏️ Отредактировать тайтл")
async def edit_title_handler(message: Message):
    """Обработчик кнопки Редактировать тайтл"""
    logger.info(f"Нажата кнопка 'Редактировать тайтл' от {message.from_user.id}")
    await message.answer("✏️ Функция редактирования тайтла будет доступна soon!")

@router.message(F.text == "📊 Просмотреть график сдавших")
async def view_stats_handler(message: Message):
    """Обработчик кнопки График сдавших"""
    logger.info(f"Нажата кнопка 'График сдавших' от {message.from_user.id}")
    await message.answer("📊 Функция графика сдавших будет доступна soon!")

@router.message(F.text == "📢 Создать рассылку")
async def create_broadcast_handler(message: Message):
    """Обработчик кнопки Создать рассылку"""
    logger.info(f"Нажата кнопка 'Создать рассылку' от {message.from_user.id}")
    await message.answer("📢 Функция рассылки будет доступна soon!")

@router.message(F.text == "🔔 Просмотреть предупреждения")
async def view_warnings_handler(message: Message):
    """Обработчик кнопки Просмотреть предупреждения"""
    logger.info(f"Нажата кнопка 'Просмотреть предупреждения' от {message.from_user.id}")
    await message.answer("🔔 Функция просмотра предупреждений будет доступна soon!")

@router.message(F.text == "📤 Выгрузить отчет")
async def export_report_handler(message: Message):
    """Обработчик кнопки Выгрузить отчет"""
    logger.info(f"Нажата кнопка 'Выгрузить отчет' от {message.from_user.id}")
    await message.answer("📤 Функция выгрузки отчета будет доступна soon!")

# Дебаг обработчик для всех сообщений
@router.message()
async def debug_all_messages(message: Message):
    """Обработчик для отладки всех сообщений"""
    logger.info(f"Получено сообщение: '{message.text}' от {message.from_user.id}")
    await message.answer(f"🔍 Получено: '{message.text}'\nЭта функция还在开发中!")