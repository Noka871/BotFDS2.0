from aiogram.dispatcher.middlewares import BaseMiddleware

class ACLMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        if message.from_user.id not in config.ADMIN_IDS:
            await message.answer("Доступ запрещён")
            raise CancelHandler()