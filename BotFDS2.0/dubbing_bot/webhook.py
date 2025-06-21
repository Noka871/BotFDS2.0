from flask import Flask, request
import telebot
from config import BOT_TOKEN

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)

# Пример обработчика
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для дабберов.")

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://ВАШ_NGROK_URL/webhook')
    app.run(host='0.0.0.0', port=5000)

    @app.route('/webhook', methods=['POST'])
    def webhook():
        try:
            update = request.get_json()
            logging.info(f"Received update: {update}")
            bot.process_new_updates([telebot.types.Update.de_json(update)])
            return 'ok', 200
        except Exception as e:
            logging.error(f"Webhook error: {e}")
            return 'error', 500