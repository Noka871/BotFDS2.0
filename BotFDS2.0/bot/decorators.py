# bot/decorators.py
# bot/decorators.py
def role_required(required_role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(message: types.Message, *args, **kwargs):
            user_role = get_user_role(message.from_user.id)  # Ваша функция получения роли
            if user_role != required_role:
                await message.answer(f"🔒 Требуется роль: {required_role}")
                return
            return await func(message, *args, **kwargs)
        return wrapper
    return decorator

# Использование:
@role_required("admin")
async def admin_command(message: types.Message):
    ...