"""
Обработчики для функционала даббера
"""
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from keyboards import (
    get_title_selection_keyboard,
    get_episode_status_keyboard,
    get_confirmation_keyboard
)
from models.database import AsyncSessionLocal, Title, UserTitle, Report
from utils.helpers import get_user_titles, get_user_by_id
from utils.states import DubberStates

router = Router()


class ReportStates(StatesGroup):
    selecting_title = State()
    selecting_episode = State()
    reporting_status = State()
    adding_comment = State()


@router.message(F.text == "🎭 Выбрать тайтл")
async def select_title(message: Message, state: FSMContext):
    """Обработчик выбора тайтла"""
    async with AsyncSessionLocal() as session:
        user = await get_user_by_id(session, message.from_user.id)
        if not user:
            await message.answer("❌ Сначала зарегистрируйтесь с помощью /start")
            return

        user_titles = await get_user_titles(session, user.user_id)

        if not user_titles:
            await message.answer("🎭 У вас нет доступных тайтлов.")
            return

        # Преобразуем в список названий для клавиатуры
        title_names = [title.name for title in user_titles]
        keyboard = get_title_selection_keyboard(title_names)

        await message.answer("🎬 Выберите тайтл:", reply_markup=keyboard)
        await state.set_state(ReportStates.selecting_title)


@router.callback_query(F.data.startswith("select_title:"))
async def process_title_selection(callback: CallbackQuery, state: FSMContext):
    """Обработчик выбора конкретного тайтла"""
    title_name = callback.data.split(":")[1]

    async with AsyncSessionLocal() as session:
        # Находим тайтл в базе
        result = await session.execute(select(Title).where(Title.name == title_name))
        title = result.scalar_one_or_none()

        if title:
            await state.update_data(selected_title_id=title.id, selected_title_name=title.name)
            await callback.message.edit_text(
                f"🎬 Выбран тайтл: <b>{title.name}</b>\n"
                f"📺 Текущая серия: {title.current_episode}\n"
                f"📊 Всего серий: {title.total_episodes}\n\n"
                f"Введите номер серии для отчета:"
            )
            await state.set_state(ReportStates.selecting_episode)
        else:
            await callback.message.edit_text("❌ Тайтл не найден в базе данных.")

    await callback.answer()


@router.message(ReportStates.selecting_episode)
async def process_episode_selection(message: Message, state: FSMContext):
    """Обработчик выбора серии"""
    try:
        episode = int(message.text)
        data = await state.get_data()

        async with AsyncSessionLocal() as session:
            # Проверяем валидность номера серии
            result = await session.execute(select(Title).where(Title.id == data['selected_title_id']))
            title = result.scalar_one_or_none()

            if not title:
                await message.answer("❌ Тайтл не найден.")
                return

            if episode < 1 or episode > title.total_episodes:
                await message.answer(f"❌ Неверный номер серии. Допустимо от 1 до {title.total_episodes}.")
                return

            await state.update_data(selected_episode=episode)
            await message.answer(
                f"📺 Серия {episode} тайтла <b>{title.name}</b>\n"
                f"Выберите статус:",
                reply_markup=get_episode_status_keyboard()
            )
            await state.set_state(ReportStates.reporting_status)

    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректный номер серии.")


@router.callback_query(F.data.startswith("episode:"))
async def process_episode_status(callback: CallbackQuery, state: FSMContext):
    """Обработчик статуса серии"""
    status = callback.data.split(":")[1]
    data = await state.get_data()

    if status == "submitted":
        # Сохраняем отчет о сдаче
        async with AsyncSessionLocal() as session:
            user = await get_user_by_id(session, callback.from_user.id)

            report = Report(
                user_id=user.id,
                title_id=data['selected_title_id'],
                episode=data['selected_episode'],
                status="submitted",
                submitted_at=datetime.utcnow()
            )
            session.add(report)
            await session.commit()

        await callback.message.edit_text(
            "✅ <b>Спасибо за предоставленную информацию!</b>\n\n"
            "Серия отмечена как сданная.\n"
            "Хотите добавить еще серию?",
            reply_markup=get_confirmation_keyboard()
        )

    elif status == "delayed":
        await callback.message.edit_text(
            "⚠️ <b>Сообщение о задержке</b>\n\n"
            "Пожалуйста, укажите причину задержки:"
        )
        await state.set_state(ReportStates.adding_comment)


@router.message(ReportStates.adding_comment)
async def process_delay_comment(message: Message, state: FSMContext):
    """Обработчик комментария о задержке"""
    data = await state.get_data()

    async with AsyncSessionLocal() as session:
        user = await get_user_by_id(session, message.from_user.id)

        report = Report(
            user_id=user.id,
            title_id=data['selected_title_id'],
            episode=data['selected_episode'],
            status="delayed",
            comment=message.text,
            submitted_at=datetime.utcnow()
        )
        session.add(report)
        await session.commit()

    await message.answer(
        "✅ <b>Информация о задержке сохранена!</b>\n\n"
        "Ваша ситуация записана. Таймер будет уведомлен.\n"
        "Хотите добавить еще серию?",
        reply_markup=get_confirmation_keyboard()
    )


@router.callback_query(F.data.startswith("confirm:"))
async def process_add_more(callback: CallbackQuery, state: FSMContext):
    """Обработчик подтверждения добавления еще одной серии"""
    confirm = callback.data.split(":")[1]

    if confirm == "yes":
        await callback.message.edit_text("🎭 Выберите тайтл:")
        await select_title(callback.message, state)
    else:
        await callback.message.edit_text("✅ Отчеты сохранены. Возврат в меню.")
        await state.clear()

    await callback.answer()


@router.message(F.text == "📋 Мои долги")
async def show_debts(message: Message):
    """Показать долги даббера"""
    async with AsyncSessionLocal() as session:
        user = await get_user_by_id(session, message.from_user.id)
        if not user:
            await message.answer("❌ Сначала зарегистрируйтесь с помощью /start")
            return

        user_titles = await get_user_titles(session, user.user_id)

        if not user_titles:
            await message.answer("🎭 У вас нет активных тайтлов.")
            return

        debts_text = "📋 <b>Ваши текущие задачи:</b>\n\n"

        for title in user_titles:
            # Здесь будет логика определения несданных серий
            debts_text += f"🎬 <b>{title.name}</b>\n"
            debts_text += f"📺 Текущая серия: {title.current_episode}\n"
            debts_text += f"⏰ Статус: В процессе\n\n"

        debts_text += "💡 Это демо-данные. Реальные данные будут из базы данных."

        await message.answer(debts_text)