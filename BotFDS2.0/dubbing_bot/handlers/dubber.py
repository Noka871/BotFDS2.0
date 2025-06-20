from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from keyboards.builders import build_titles_keyboard
from services.notification import send_reminder
from utils.states import ReportStates
from database.repository import Repository


async def dubber_start(message: types.Message, repo: Repository):
    titles = await repo.get_user_titles(message.from_user.id)
    if not titles:
        await message.answer("У вас нет назначенных тайтлов.")
        return

    keyboard = build_titles_keyboard(titles)
    await message.answer("Выберите тайтл:", reply_markup=keyboard)
    await ReportStates.select_title.set()


async def process_title_selection(
        message: types.Message,
        state: FSMContext,
        repo: Repository
):
    title = await repo.get_title_by_name(message.text)
    if not title:
        await message.answer("Тайтл не найден")
        return

    await state.update_data(title_id=title.id)
    await message.answer(f"Введите номер серии (1-{title.episodes_count}):")
    await ReportStates.select_episode.set()


async def process_episode_selection(
        message: types.Message,
        state: FSMContext,
        repo: Repository
):
    try:
        episode = int(message.text)
        data = await state.get_data()
        title = await repo.get_title(data['title_id'])

        if not 1 <= episode <= title.episodes_count:
            raise ValueError

        await state.update_data(episode=episode)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Сдал в срок", "Задержка")
        await message.answer("Статус сдачи:", reply_markup=keyboard)
        await ReportStates.report_status.set()

    except ValueError:
        await message.answer("Некорректный номер серии")


async def process_report_status(
        message: types.Message,
        state: FSMContext,
        repo: Repository,
        user: User
):
    if message.text not in ["Сдал в срок", "Задержка"]:
        await message.answer("Выберите вариант из клавиатуры")
        return

    data = await state.get_data()
    status = "submitted" if message.text == "Сдал в срок" else "delayed"

    report = Report(
        user_id=user.id,
        title_id=data['title_id'],
        episode=data['episode'],
        status=status,
        deadline=datetime.utcnow() + timedelta(days=2) if status == "submitted" else None
    )

    await repo.create_report(report)

    if status == "delayed":
        await send_reminder(user.telegram_id, data['title_id'], data['episode'])

    await message.answer("Отчет сохранен!", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()