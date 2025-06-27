"""
Общие обработчики команд (/start, /help, /menu)
"""
from telegram import Update
from telegram.ext import CallbackContext
from database import Database
from utils.keyboards import get_main_menu_keyboard

def start_handler(update: Update, context: CallbackContext):
    """Обработчик команды /start"""
    user = update.effective_user
    db = Database()
    
    # Регистрация пользователя в системе
    db.add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        role='dubber'  # По умолчанию роль даббера
    )
    
    # Отправка приветственного сообщения
    update.message.reply_text(
        f"Привет, {user.first_name}!\n"
        "Я бот для учета сдачи аудиодорожек.\n"
        "Пожалуйста, выбери свою роль:",
        reply_markup=get_main_menu_keyboard()
    )

def menu_handler(update: Update, context: CallbackContext):
    """Обработчик команды /menu"""
    user = update.effective_user
    update.message.reply_text(
        "Главное меню:",
        reply_markup=get_main_menu_keyboard()
    )

def help_handler(update: Update, context: CallbackContext):
    """Обработчик команды /help"""
    help_text = (
        "📌 Доступные команды:\n"
        "/start - Начало работы с ботом\n"
        "/menu - Главное меню\n"
        "/help - Справка\n\n"
        "Если у вас возникли проблемы, обратитесь к администратору."
    )
    update.message.reply_text(help_text)