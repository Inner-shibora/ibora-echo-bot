import os
import telebot
from flask import Flask, request
import threading
import openai

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# ตั้งค่า OpenAI
openai.api_key = OPENAI_API_KEY

# --- Webhook ---
bot.remove_webhook()
bot.set_webhook(url=f"https://ibora-echo-bot-production.up.railway.app/bot/{API_TOKEN}")

@app.route(f"/bot/{API_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Echo bot is live!"

# --- Message Handler ---
@bot.message_handler(commands=["start"])
def greet_user(message):
    bot.send_message(message.chat.id, "Welcome to Shibora AI!")

@bot.message_handler(func=lambda msg: True)
def echo_gpt_response(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}],
            max_tokens=150
        )
        reply = response.choices[0].message.content
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, f"ขออภัย เกิดข้อผิดพลาด: {e}")
        print("GPT ERROR:", e)

# --- Thread สำหรับ Telegram Polling (ถ้าไม่ใช้ Webhook) ---
def run_bot():
    bot.polling(non_stop=True)

# --- Main ---
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
