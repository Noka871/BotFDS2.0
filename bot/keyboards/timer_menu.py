from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_timer_main_keyboard():
    """Главное меню таймера"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🎬 Создать тайтл", callback_data="timer:create_title"),
        InlineKeyboardButton(text="✏️ Редактировать тайтл", callback_data="timer:edit_title"),
        InlineKeyboardButton(text="📊 График сдавших", callback_data="timer:stats"),
        InlineKeyboardButton(text="📢 Создать рассылку", callback_data="timer:broadcast"),
        InlineKeyboardButton(text="🔔 Предупреждения", callback_data="timer:warnings"),
        InlineKeyboardButton(text="⚠️ Форс-мажор", callback_data="timer:force_majeure")
    )
    builder.adjust(2)
    return builder.as_markup()

def get_title_edit_keyboard(title_id: int):
    """Клавиатура редактирования тайтла"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="✏️ Название", callback_data=f"edit_title:name:{title_id}"),
        InlineKeyboardButton(text="📺 Серии", callback_data=f"edit_title:episodes:{title_id}"),
        InlineKeyboardButton(text="🎭 Дабберы", callback_data=f"edit_title:dubbers:{title_id}"),
        InlineKeyboardButton(text="🚀 Вышли метки", callback_data=f"edit_title:marks:{title_id}"),
        InlineKeyboardButton(text="❌ Удалить", callback_data=f"edit_title:delete:{title_id}"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="edit_title:cancel")
    )
    builder.adjust(2)
    return builder.as_markup()

def get_confirmation_keyboard(action: str, item_id: int):
    """Клавиатура подтверждения действия"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="✅ Да", callback_data=f"confirm:{action}:{item_id}"),
        InlineKeyboardButton(text="❌ Нет", callback_data=f"cancel:{action}:{item_id}")
    )
    return builder.as_markup()

def get_broadcast_type_keyboard():
    """Клавиатура выбора типа рассылки"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📢 Всем дабберам", callback_data="broadcast:all"),
        InlineKeyboardButton(text="🎬 По тайтлу", callback_data="broadcast:title"),
        InlineKeyboardButton(text="👤 Конкретному дабберу", callback_data="broadcast:user")
    )
    builder.adjust(1)
    return builder.as_markup()