from aiogram.dispatcher.middlewares import BaseMiddleware
from config.constants import Roles

class ACLMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        # Проверка прав доступа
        user_role = await get_user_role(message.from_user.id)  # Функция из CRUD
        data["role"] = user_role