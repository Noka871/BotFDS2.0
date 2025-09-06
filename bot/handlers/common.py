"""
Общие обработчики команд (/start, /help, /menu)
"""
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards import get_main_menu_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    await state.clear()

    welcome_text = (
        "🎬 <b>Добро пожаловать в систему отчетности дубляжа!</b>\n\n"
        "Здесь вы можете:\n"
        "• 📝 Отмечать сданные серии\n"
        "• ⏰ Получать уведомления о дедлайнах\n"
        "• 📊 Следить за своими задачами\n"
        "• 🚀 Узнавать о выходе новых меток\n\n"
        "Используйте кнопки меню для навигации:"
    )

    await message.answer(welcome_text, reply_markup=get_main_menu_keyboard())


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    """Обработчик команды /menu"""
    await message.answer("📋 <b>Главное меню</b>", reply_markup=get_main_menu_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = (
        "🤖 <b>Помощь по боту</b>\n\n"
        "• /start - Запустить бота\n"
        "• /menu - Главное меню\n"
        "• /help - Эта справка\n\n"
        "🎭 <b>Для дабберов:</b>\n"
        "• Выбрать тайтл - отметить сдачу серии\n"
        "• Мои долги - посмотреть текущие задачи\n"
        "• Форс-мажор - сообщить о проблеме\n\n"
        "⏰ <b>Для таймеров:</b>\n"
        "• Создать тайтл - добавить новый проект\n"
        "• Редактировать тайтл - изменить параметры\n"
        "• Рассылка - отправить уведомление\n\n"
        "👨‍💼 <b>Для админов:</b>\n"
        "• Выгрузить отчет - получить статистики\n"
        "• Глобальная рассылка - уведомить всех\n"
    )

    await message.answer(help_text)


@router.message(F.text == "🔙 Вернуться в меню")
async def back_to_menu(message: Message):
    """Возврат в главное меню"""
    await cmd_menu(message)