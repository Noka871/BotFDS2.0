# handlers/reports.py
from telebot import TeleBot
from telebot.types import Message
from database.requests import get_all_reports
import pandas as pd


def setup_report_handlers(bot: TeleBot):
    @bot.message_handler(commands=['export_reports'])
    def export_reports(message: Message):
        reports = get_all_reports()  # Ваша функция из database/requests.py

        # Создаём Excel-файл
        df = pd.DataFrame(reports)
        filename = "reports.xlsx"
        df.to_excel(filename, index=False)

        # Отправляем файл
        with open(filename, 'rb') as file:
            bot.send_document(message.chat.id, file, caption="📊 Все отчёты")
            bot.send_message(message.chat.id, "Отчёт принят! Хотите добавить ещё?")