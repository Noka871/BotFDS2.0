from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_title_selection_keyboard(titles, page=0, page_size=5):
    """Клавиатура для выбора тайтла с пагинацией"""
    builder = InlineKeyboardBuilder()

    # Добавляем тайтлы для текущей страницы
    start_idx = page * page_size
    end_idx = start_idx + page_size

    # Если titles - список строк (названий)
    if titles and isinstance(titles[0], str):
        paginated_titles = titles[start_idx:end_idx]
        for title in paginated_titles:
            builder.add(InlineKeyboardButton(
                text=f"🎬 {title}",
                callback_data=f"select_title:{title}"
            ))
    else:
        # Если titles - список объектов
        paginated_titles = titles[start_idx:end_idx]
        for title in paginated_titles:
            builder.add(InlineKeyboardButton(
                text=f"🎬 {title}",
                callback_data=f"select_title:{title}"
            ))

    # Добавляем кнопки навигации
    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=f"title_page:{page - 1}"
        ))
    if end_idx < len(titles):
        navigation_buttons.append(InlineKeyboardButton(
            text="Вперед ➡️",
            callback_data=f"title_page:{page + 1}"
        ))

    if navigation_buttons:
        builder.row(*navigation_buttons)

    builder.row(InlineKeyboardButton(
        text="🔙 Отмена",
        callback_data="cancel_title_selection"
    ))

    return builder.as_markup()


def get_episode_status_keyboard():
    """Клавиатура для выбора статуса серии"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="✅ Серию сдал", callback_data="episode:submitted"),
        InlineKeyboardButton(text="⏰ Серию задержу", callback_data="episode:delayed"),
        InlineKeyboardButton(text="🔙 Отмена", callback_data="cancel_episode")
    )
    builder.adjust(2)
    return builder.as_markup()


def get_confirmation_keyboard():
    """Клавиатура подтверждения"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="✅ Да", callback_data="confirm:yes"),
        InlineKeyboardButton(text="❌ Нет", callback_data="confirm:no")
    )
    return builder.as_markup()


def get_back_menu():
    """Клавиатура с кнопкой Назад"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))
    return builder.as_markup()