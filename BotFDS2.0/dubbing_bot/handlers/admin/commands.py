# handlers/admin/commands.py
@dp.message_handler(commands="test_notify")
async def test_notify(message: types.Message):
    await broadcast(bot, "Тест системы уведомлений")
    await message.answer("✅ Рассылка запущена")