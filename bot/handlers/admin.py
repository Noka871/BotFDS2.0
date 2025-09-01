"""
Обработчики для функционала администратора
"""
from telegram import Update
from telegram.ext import CallbackContext
from database import Database
from utils.keyboards import get_admin_menu_keyboard

def admin_menu_handler(update: Update, context: CallbackContext):
    """Обработчик меню администратора"""
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(
        text="🛠 Админ-панель:",
        reply_markup=get_admin_menu_keyboard()
    )

def export_report(update: Update, context: CallbackContext):
    """Выгрузка отчета"""
    query = update.callback_query
    query.answer()
    
    db = Database()
    
    # Получаем данные для отчета
    pending_episodes = db.get_pending_episodes()
    penalties = db.get_penalties()
    force_majeures = db.get_force_majeures()
    
    # Формируем отчет
    report = "📊 Отчет по системе:\n\n"
    
    report += "⏳ Несданные серии:\n"
    for ep in pending_episodes:
        report += f"- {ep['title_name']} #{ep['episode_number']} (@{ep['username']})\n"
    
    report += "\n🚨 Штрафы:\n"
    for p in penalties:
        report += f"- {p['title_name']} #{p['episode_number']}: {p['amount']} руб. (@{p['dubber_name']})\n"
    
    report += "\n⚠️ Форс-мажоры:\n"
    for fm in force_majeures:
        report += f"- @{fm['username']}: {fm['message']}\n"
    
    query.edit_message_text(
        text=report,
        reply_markup=get_admin_menu_keyboard()
    )

def manage_users(update: Update, context: CallbackContext):
    """Управление пользователями (заглушка)"""
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(
        text="Функционал управления пользователями в разработке.",
        reply_markup=get_admin_menu_keyboard()
    )