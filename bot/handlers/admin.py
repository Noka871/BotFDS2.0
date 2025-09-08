from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

from ..logger import logger, log_command

router = Router()


def get_admin_main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Выгрузить отчет"), KeyboardButton(text="Статистика системы")],
            [KeyboardButton(text="Управление пользователями"), KeyboardButton(text="Отправить уведомление")],
            [KeyboardButton(text="Даббер"), KeyboardButton(text="Таймер")],
            [KeyboardButton(text="Вернуться в меню")]
        ],
        resize_keyboard=True
    )


@router.message(F.text == "Админ")
async def admin_menu(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "Админ")

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


@router.message(F.text == "Выгрузить отчет")
async def export_report(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "Выгрузить отчет")

        # Заглушка для теста
        report_text = """
📈 *Отчет системы*:

*Общая статистика:*
• Пользователей: 15
• Тайтлов: 8
• Всего серий: 245
• Сдано вовремя: 89%
• Просрочено: 11%

*Топ дабберов:*
1. User1 - 98% вовремя
2. User2 - 95% вовремя  
3. User3 - 92% вовремя

Отчет готов к выгрузке в CSV.
        """

        await message.answer(report_text, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error in Выгрузить отчет: {e}", exc_info=True)


@router.message(F.text == "Статистика системы")
async def system_stats(message: Message):
    try:
        log_command(message.from_user.id, message.from_user.username, "Статистика системы")

        stats_text = """
📊 *Статистика системы*:

*Активность за неделю:*
• Новых отчетов: 47
• Предупреждений: 3
• Создано тайтлов: 2

*Производительность:*
• Среднее время сдачи: 1.2 дня
• Процент просрочек: 8.5%
• Активных пользователей: 12/15
        """

        await message.answer(stats_text, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error in Статистика системы: {e}", exc_info=True)