"""
Обработчики для функционала таймера
"""
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, Filters
from database import Database
from utils.keyboards import get_timer_menu_keyboard, get_titles_keyboard
from utils.notifications import NotificationManager

# Состояния для ConversationHandler
TITLE_NAME, TITLE_EPISODES, TITLE_DUBBERS, PENALTY_AMOUNT, PENALTY_REASON = range(5)

def timer_menu_handler(update: Update, context: CallbackContext):
    """Обработчик меню таймера"""
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(
        text="⏱ Меню таймера:",
        reply_markup=get_timer_menu_keyboard()
    )

def create_title_start(update: Update, context: CallbackContext):
    """Начало создания нового тайтла"""
    query = update.callback_query
    query.answer()
    
    query.edit_message_text("Введите название тайтла:")
    return TITLE_NAME

def create_title_name(update: Update, context: CallbackContext):
    """Обработка названия тайтла"""
    context.user_data['new_title'] = {'name': update.message.text}
    update.message.reply_text("Введите количество серий в тайтле:")
    return TITLE_EPISODES

def create_title_episodes(update: Update, context: CallbackContext):
    """Обработка количества серий"""
    try:
        episodes = int(update.message.text)
        if episodes <= 0:
            raise ValueError
        
        context.user_data['new_title']['episodes'] = episodes
        update.message.reply_text(
            "Введите username дабберов через пробел (например, @user1 @user2):"
        )
        return TITLE_DUBBERS
    except ValueError:
        update.message.reply_text("Некорректное число. Введите целое положительное число:")
        return TITLE_EPISODES

def create_title_dubbers(update: Update, context: CallbackContext):
    """Обработка списка дабберов и сохранение тайтла"""
    db = Database()
    user_id = update.effective_user.id
    dubbers = update.message.text.split()
    
    # Создаем тайтл
    title_id = db.add_title(
        name=context.user_data['new_title']['name'],
        total_episodes=context.user_data['new_title']['episodes'],
        created_by=user_id
    )
    
    # Добавляем дабберов к тайтлу
    for username in dubbers:
        # Здесь должна быть логика получения user_id по username
        # Для упрощения предполагаем, что username без @
        pass
    
    update.message.reply_text(
        f"Тайтл '{context.user_data['new_title']['name']}' успешно создан!",
        reply_markup=get_timer_menu_keyboard()
    )
    return ConversationHandler.END

def send_marks_start(update: Update, context: CallbackContext):
    """Начало процесса отправки меток"""
    query = update.callback_query
    query.answer()
    
    db = Database()
    titles = db.get_timer_titles(update.effective_user.id)
    
    if not titles:
        query.edit_message_text("У вас нет созданных тайтлов.")
        return ConversationHandler.END
    
    query.edit_message_text(
        text="Выберите тайтл для отправки меток:",
        reply_markup=get_titles_keyboard(titles, 'timer_send_marks')
    )
    return SELECT_TITLE

def send_marks(update: Update, context: CallbackContext):
    """Отправка уведомлений о готовности меток"""
    query = update.callback_query
    query.answer()
    
    title_id = int(query.data.split('_')[-1])
    
    notifier = NotificationManager(context.bot.token)
    notifier.notify_new_marks(title_id)
    
    query.edit_message_text(
        "Уведомления о готовности меток отправлены дабберам!",
        reply_markup=get_timer_menu_keyboard()
    )
    return ConversationHandler.END

def assign_penalty_start(update: Update, context: CallbackContext):
    """Начало процесса назначения штрафа"""
    query = update.callback_query
    query.answer()
    
    db = Database()
    titles = db.get_timer_titles(update.effective_user.id)
    
    if not titles:
        query.edit_message_text("У вас нет созданных тайтлов.")
        return ConversationHandler.END
    
    query.edit_message_text(
        text="Выберите тайтл для назначения штрафа:",
        reply_markup=get_titles_keyboard(titles, 'timer_penalty_title')
    )
    return SELECT_TITLE

# Другие обработчики для таймера...

# Создание ConversationHandler для таймера
timer_conv_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(create_title_start, pattern='^timer_create_title$'),
        CallbackQueryHandler(send_marks_start, pattern='^timer_send_marks$'),
        CallbackQueryHandler(assign_penalty_start, pattern='^timer_assign_penalty$')
    ],
    states={
        TITLE_NAME: [
            MessageHandler(Filters.text & ~Filters.command, create_title_name)
        ],
        TITLE_EPISODES: [
            MessageHandler(Filters.text & ~Filters.command, create_title_episodes)
        ],
        TITLE_DUBBERS: [
            MessageHandler(Filters.text & ~Filters.command, create_title_dubbers)
        ],
        SELECT_TITLE: [
            CallbackQueryHandler(send_marks, pattern='^timer_send_marks_'),
            CallbackQueryHandler(select_penalty_episode, pattern='^timer_penalty_title_')
        ],
        # Другие состояния...
    },
    fallbacks=[
        CommandHandler('cancel', cancel_timer_actions),
        MessageHandler(Filters.command, cancel_timer_actions)
    ]
)