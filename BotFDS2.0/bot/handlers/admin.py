from functools import wraps
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.config import ADMIN_IDS


# Декоратор для проверки прав администратора
def admin_required(func):
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        if message.from_user.id not in ADMIN_IDS:
            await message.answer("🔒 Доступ только для администраторов")
            return
        return await func(message, *args, **kwargs)

    return wrapper


# Состояния для рассылки
class BroadcastState(StatesGroup):
    message = State()


# Обработчик выгрузки отчета
@admin_required
async def export_report(message: types.Message):
    """Выгрузка отчета в Excel"""
    try:
        await message.answer("📊 Начинаю генерацию отчета...")

        # Здесь будет реальная логика генерации отчета
        # Пока просто пример:
        import io
        from openpyxl import Workbook

        wb = Workbook()
        ws = wb.active
        ws.title = "Отчет"
        ws.append(["Дата", "Пользователь", "Статус"])
        ws.append(["2023-01-01", "User1", "Активен"])

        excel_file = io.BytesIO()
        wb.save(excel_file)
        excel_file.seek(0)

        await message.answer_document(
            types.InputFile(excel_file, filename="report.xlsx"),
            caption="✅ Отчет готов"
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка генерации отчета: {e}")


# Обработчик начала рассылки
@admin_required
async def start_broadcast(message: types.Message):
    """Начало процесса рассылки"""
    await BroadcastState.message.set()
    await message.answer("📢 Введите сообщение для рассылки:")


# Обработчик текста рассылки
@admin_required
async def process_broadcast(message: types.Message, state: FSMContext):
    """Обработка текста рассылки"""
    try:
        # Здесь будет реальная рассылка
        # Пока просто пример:
        await message.answer(f"🔔 Тест рассылки: {message.text}\n\n"
                             "В реальной версии это сообщение получат все пользователи")
    finally:
        await state.finish()


def register_admin_handlers(dp: Dispatcher):
    """Регистрация обработчиков административных команд"""
    dp.register_message_handler(export_report, text="Выгрузить отчет")
    dp.register_message_handler(start_broadcast, text="Рассылка")
    dp.register_message_handler(process_broadcast, state=BroadcastState.message)