from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_admin_main_keyboard():
    """Главное меню админа"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📤 Выгрузить отчет", callback_data="admin:export"),
        InlineKeyboardButton(text="📊 Статистика", callback_data="admin:stats"),
        InlineKeyboardButton(text="👥 Управление пользователями", callback_data="admin:users"),
        InlineKeyboardButton(text="⚙️ Настройки", callback_data="admin:settings"),
        InlineKeyboardButton(text="📢 Глобальная рассылка", callback_data="admin:global_broadcast")
    )
    builder.adjust(2)
    return builder.as_markup()

def get_report_type_keyboard():
    """Клавиатура выбора типа отчета"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📊 По тайтлам", callback_data="report:titles"),
        InlineKeyboardButton(text="👥 По дабберам", callback_data="report:dubbers"),
        InlineKeyboardButton(text="⏰ По срокам", callback_data="report:deadlines"),
        InlineKeyboardButton(text="💰 Штрафы", callback_data="report:penalties"),
        InlineKeyboardButton(text="📈 Полный отчет", callback_data="report:full")
    )
    builder.adjust(2)
    return builder.as_markup()

def get_user_management_keyboard():
    """Клавиатура управления пользователями"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="👑 Назначить админа", callback_data="admin:promote"),
        InlineKeyboardButton(text="⏰ Назначить таймера", callback_data="admin:make_timer"),
        InlineKeyboardButton(text="🎭 Назначить даббера", callback_data="admin:make_dubber"),
        InlineKeyboardButton(text="👀 Просмотреть пользователей", callback_data="admin:view_users")
    )
    builder.adjust(2)
    return builder.as_markup()