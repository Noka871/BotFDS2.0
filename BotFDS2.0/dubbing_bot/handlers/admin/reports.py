# Добавьте экспорт отчётов
from utils.spreadsheet import generate_report

@dp.message_handler(text='📊 Выгрузить отчет')
async def export_reports(message: types.Message):
    data = await db.get_all_reports()
    report_path = generate_report(data)
    await message.answer_document(open(report_path, 'rb'))

    async def get_overdue_reports():
        return await session.execute(
            select(Report)
            .where(Report.status == "delayed")
            .where(Report.created_at < datetime.now() - timedelta(days=2))
        )