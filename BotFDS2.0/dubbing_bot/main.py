# main.py
from handlers.admin import register_handlers_admin
from handlers.dubber import register_handlers_dubber
from middlewares.throttle import ThrottlingMiddleware
from services.broadcaster import broadcast_message
def main():
    dp.middleware.setup(ThrottlingMiddleware())
    register_handlers_admin(dp)
    register_handlers_dubber(dp)

    # Для теста можно добавить команду
    @dp.message_handler(commands="broadcast")
    async def cmd_broadcast(message: types.Message):
        await broadcast_message(bot, "Тестовое уведомление!")


