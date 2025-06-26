# Работа с БД
async def get_user_role(user_id: int) -> str:
    """Получаем роль пользователя из БД"""
    user = await db.execute("SELECT role FROM users WHERE user_id = ?", (user_id,), fetchone=True)
    return user['role'] if user else None