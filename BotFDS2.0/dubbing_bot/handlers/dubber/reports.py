from telebot.types import ReplyKeyboardMarkup
from database.requests import create_report

def register_dubber_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == "📝 Отправить отчет")
    def select_title(message):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        # Здесь нужно добавить тайтлы из БД
        markup.add("Тайтл 1", "Тайтл 2", "Назад")
        bot.send_message(message.chat.id, "Выберите тайтл:", reply_markup=markup)

    @bot.message_handler(func=lambda m: m.text in ["Тайтл 1", "Тайтл 2"])
    def select_episode(message):
        bot.send_message(message.chat.id, "Введите номер серии:")
        bot.register_next_step_handler(message, process_episode)

    def process_episode(message):
        try:
            episode = int(message.text)
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("✅ Сдал", "⚠ Задержка")
            bot.send_message(message.chat.id, "Статус:", reply_markup=markup)
            bot.register_next_step_handler(
                message,
                lambda m: process_report(m, episode)
        except ValueError:
            bot.send_message(message.chat.id, "Введите число!")