# Добавьте ежедневные напоминания
async def send_dubber_reminders(bot: Bot):
    overdue = await db.get_overdue_reports()
    for report in overdue:
        await bot.send_message(
            report.user_id,
            f"⚠️ Просрочено: {report.title}, серия {report.episode}"
        )

        from services.broadcaster import broadcast_message

        async def send_reminders():
            await broadcast_message(bot, "Напоминание: сдать отчёты!")

            from services.broadcaster import broadcast

            async def send_reminders(bot: Bot):
                reports = await get_overdue_reports()
                for report in reports:
                    await broadcast(bot, f"Просрочен отчет: {report.title}")