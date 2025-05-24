import os
import telebot
from flask import Flask, request

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

# ตอบกลับเมื่อมีข้อความใหม่
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, f"คุณพิมพ์ว่า: {message.text}")

# route สำหรับ webhook
@app.route(f"/bot{API_TOKEN}", methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

# root test
@app.route("/")
def root():
    return "Echo Bot is live!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    bot.remove_webhook()
    bot.set_webhook(url=f"https://ibora-echo-bot-production.up.railway.app/bot{API_TOKEN}")
    app.run(host="0.0.0.0", port=port)
