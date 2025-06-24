from aiogram.dispatcher import FSMContext

@dp.message_handler(commands=["report"])
async def start_report(message: types.Message, state: FSMContext):
    await ReportStates.select_title.set()
    await message.answer("Выберите тайтл:")