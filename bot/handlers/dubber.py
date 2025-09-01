"""
Обработчики для функционала даббера
"""
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, Filters
from database import Database
from utils.keyboards import get_dubber_menu_keyboard, get_titles_keyboard, get_episode_status_keyboard

# Состояния для ConversationHandler
SELECT_TITLE, SELECT_EPISODE, EPISODE_STATUS, FORCE_MAJEURE = range(4)

def dubber_menu_handler(update: Update, context: CallbackContext):
    """Обработчик меню даббера"""
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(
        text="📌 Меню даббера:",
        reply_markup=get_dubber_menu_keyboard()
    )

def select_title_start(update: Update, context: CallbackContext):
    """Начало выбора тайтла для отметки сдачи"""
    query = update.callback_query
    query.answer()
    
    db = Database()
    titles = db.get_dubber_titles(update.effective_user.id)
    
    if not titles:
        query.edit_message_text("У вас нет назначенных тайтлов.")
        return ConversationHandler.END
    
    query.edit_message_text(
        text="Выберите тайтл:",
        reply_markup=get_titles_keyboard(titles, 'dubber_title')
    )
    return SELECT_TITLE

def select_title(update: Update, context: CallbackContext):
    """Обработка выбора тайтла"""
    query = update.callback_query
    query.answer()
    
    title_id = int(query.data.split('_')[-1])
    context.user_data['current_title'] = title_id
    
    query.edit_message_text("Введите номер серии:")
    return SELECT_EPISODE

def select_episode(update: Update, context: CallbackContext):
    """Обработка номера серии"""
    try:
        episode_number = int(update.message.text)
        if episode_number <= 0:
            raise ValueError
        
        context.user_data['current_episode'] = episode_number
        update.message.reply_text(
            "Выберите статус:",
            reply_markup=get_episode_status_keyboard()
        )
        return EPISODE_STATUS
    except ValueError:
        update.message.reply_text("Некорректный номер серии. Введите целое положительное число:")
        return SELECT_EPISODE

def episode_status(update: Update, context: CallbackContext):
    """Обработка статуса серии"""
    query = update.callback_query
    query.answer()
    
    status = query.data.split('_')[-1]
    title_id = context.user_data['current_title']
    episode_number = context.user_data['current_episode']
    user_id = update.effective_user.id
    
    db = Database()
    
    if status == 'completed':
        db.set_episode_status(title_id, episode_number, user_id, 'completed')
        message = "✅ Серия отмечена как сданная!"
    elif status == 'delayed':
        db.set_episode_status(title_id, episode_number, user_id, 'delayed')
        message = "⚠️ Вы отметили задержку сдачи. Пожалуйста, укажите причину:"
        query.edit_message_text(message)
        return FORCE_MAJEURE
    else:  # cancel
        message = "Действие отменено."
    
    query.edit_message_text(
        text=message + "\n\nХотите отметить еще одну серию?",
        reply_markup=get_dubber_menu_keyboard()
    )
    return ConversationHandler.END

def force_majeure_reason(update: Update, context: CallbackContext):
    """Обработка причины задержки (форс-мажора)"""
    reason = update.message.text
    user_id = update.effective_user.id
    
    db = Database()
    db.add_force_majeure(user_id, reason)
    
    update.message.reply_text(
        "Ваше сообщение о форс-мажоре сохранено. Спасибо!",
        reply_markup=get_dubber_menu_keyboard()
    )
    return ConversationHandler.END

def cancel_dubber_actions(update: Update, context: CallbackContext):
    """Отмена действий даббера"""
    update.message.reply_text(
        "Действие отменено.",
        reply_markup=get_dubber_menu_keyboard()
    )
    return ConversationHandler.END

# Создание ConversationHandler для даббера
dubber_conv_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(select_title_start, pattern='^dubber_select_title$')
    ],
    states={
        SELECT_TITLE: [
            CallbackQueryHandler(select_title, pattern='^dubber_title_')
        ],
        SELECT_EPISODE: [
            MessageHandler(Filters.text & ~Filters.command, select_episode)
        ],
        EPISODE_STATUS: [
            CallbackQueryHandler(episode_status, pattern='^status_')
        ],
        FORCE_MAJEURE: [
            MessageHandler(Filters.text & ~Filters.command, force_majeure_reason)
        ]
    },
    fallbacks=[
        CommandHandler('cancel', cancel_dubber_actions),
        MessageHandler(Filters.command, cancel_dubber_actions)
    ]
)ы