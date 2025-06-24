from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.states import ReportStates

@dp.message_handler(text="Сдать отчёт")
async def start_report(message: types.Message):
    await ReportStates.select_title.set()
    await message.answer("Выберите тайтл:")