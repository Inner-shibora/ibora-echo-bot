# -*- coding: utf-8 -*-
import os
import telebot
from flask import Flask, request
import threading
from openai import OpenAI

# ดึง token
API_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

# --- ตั้งค่า Webhook ---
bot.remove_webhook()
bot.set_webhook(url=f"https://ibora-echo-bot-production.up.railway.app/bot/{API_TOKEN}")

# --- Webhook Endpoint ---
@app.route(f"/bot/{API_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# --- Root Check ---
@app.route("/")
def index():
    return "Echo bot is live!"

# --- ฟังก์ชัน GPT ---
@bot.message_handler(func=lambda msg: True)
def echo_gpt_response(message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}],
            max_tokens=150
        )
        reply = response.choices[0].message.content
        bot.send_message(message.chat.id, reply)

    except Exception as e:
        bot.send_message(message.chat.id, f"ขออภัย เกิดข้อผิดพลาด: {e}")
        print("GPT ERROR:", e)

# --- Start polling in background ---
def run_bot():
    bot.polling(non_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
