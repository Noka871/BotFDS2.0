from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

from ..logger import logger, log_command
from ..keyboards.dubber_kb import get_main_kb, get_dubber_main_kb, get_timer_main_kb, get_admin_main_kb

router = Router()


def get_main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Даббер")],
            [KeyboardButton(text="Таймер")],
            [KeyboardButton(text="Админ")]
        ],
        resize_keyboard=True
    )


@router.message(Command("start"))
async def cmd_start(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "/start")

        await message.answer(
            "Добро пожаловать! Выберите вашу роль:",
            reply_markup=get_main_kb()
        )
        logger.info(f"User {message.from_user.id} started bot")

    except Exception as e:
        logger.error(f"Error in /start command: {e}", exc_info=True)
        await message.answer("Произошла ошибка. Попробуйте позже.")


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "/menu")

        await message.answer(
            "Главное меню:",
            reply_markup=get_main_kb()
        )
        logger.info(f"User {message.from_user.id} opened menu")

    except Exception as e:
        logger.error(f"Error in /menu command: {e}", exc_info=True)
        await message.answer("Произошла ошибка. Попробуйте позже.")


@router.message(Command("help"))
async def cmd_help(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "/help")

        help_text = """
🤖 *Помощь по боту*:

*/start* - Начать работу с ботом
*/menu* - Показать главное меню  
*/help* - Показать эту справку
*/stats* - Показать статистику

*Роли*:
• *Даббер* - Актер дубляжа, сдает аудиодорожки
• *Таймер* - Специалист по сведению звука
• *Админ* - Управление системой и отчеты

Для навигации используйте кнопки меню.
        """

        await message.answer(help_text, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error in /help command: {e}", exc_info=True)
        await message.answer("Произошла ошибка. Попробуйте позже.")


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "/stats")

        # Простая статистика (заглушка)
        stats_text = """
📊 *Статистика системы*:

• Пользователей: 0
• Активных тайтлов: 0
• Сданных серий: 0
• Просроченных: 0

*Ваша статистика*:
• Ваших тайтлов: 0
• Сданных серий: 0
• Просроченных: 0 ✅
        """

        await message.answer(stats_text, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error in /stats command: {e}", exc_info=True)
        await message.answer("Произошла ошибка. Попробуйте позже.")


@router.message(F.text == "Даббер")
async def dubbing_menu(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "Даббер")

        # Импортируем клавиатуру даббера здесь, чтобы избежать circular imports
        from ..keyboards.dubber_kb import get_dubber_main_kb

        await message.answer(
            "Добро пожаловать в систему отчетности дубляжа!\n\n"
            f"Привет, {message.from_user.full_name}!\n"
            "Ваша роль: dubber\n\n"
            "Используйте кнопки меню для навигации:",
            reply_markup=get_dubber_main_kb()
        )
        logger.info(f"User {message.from_user.id} entered dubber menu")

    except Exception as e:
        logger.error(f"Error in Даббер menu: {e}", exc_info=True)
        await message.answer("Произошла ошибка. Попробуйте позже.")


@router.message(F.text == "Таймер")
async def timer_menu(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "Таймер")

        # Импортируем клавиатуру таймера здесь, чтобы избежать circular imports
        from ..keyboards.timer_kb import get_timer_main_kb

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

@router.message(F.text == "Админ")
async def admin_menu(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "Админ")

        # Импортируем клавиатуру админа здесь, чтобы избежать circular imports
        from ..keyboards.admin_kb import get_admin_main_kb

        await message.answer(
            "👑 *Панель администратора*\n\n"
            "Доступные действия:",
            reply_markup=get_admin_main_kb(),
            parse_mode="Markdown"
        )
        logger.info(f"User {message.from_user.id} entered admin menu")

    except Exception as e:
        logger.error(f"Error in Админ menu: {e}", exc_info=True)
        await message.answer("Произошла ошибка. Попробуйте позже.")