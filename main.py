import os
import telebot
from flask import Flask, request

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@app.route(f"/bot{API_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Echo bot is live!"

# ฟังก์ชัน presale มาก่อน
@bot.message_handler(commands=['presale'])
def announce_presale(message):
    bot.send_message(
        message.chat.id,
        "🚀 SHRA Token Presale is LIVE now!\nVisit https://shibora.ai/presale to join before it's gone!"
    )

@bot.message_handler(func=lambda message: 'presale' in message.text.lower())
def keyword_presale(message):
    bot.send_message(
        message.chat.id,
        "🔥 Looks like you're interested in the SHRA presale!\nCheck it out here: https://shibora.ai/presale"
    )

# ฟังก์ชัน echo มาทีหลังสุด
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"🟢 Echo: {message.text}")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://ibora-echo-bot-production.up.railway.app/bot{API_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
