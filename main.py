# -*- coding: utf-8 -*-
import os
import telebot
from flask import Flask, request
import threading
from openai import OpenAI

# โหลด API Key จาก Environment
API_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

# --- ตั้งค่า Webhook ---
bot.remove_webhook()
bot.set_webhook(url=f"https://ibora-echo-bot-production.up.railway.app/bot/{API_TOKEN}")

# --- Webhook สำหรับ Telegram ---
@app.route(f"/bot/{API_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# --- Root Route (เช็คสถานะ) ---
@app.route("/")
def index():
    return "Echo bot is live!"

# --- คำสั่ง Start ---
@bot.message_handler(commands=["start"])
def greet_user(message):
    bot.send_message(message.chat.id, "Welcome to Shibora AI. Echo & Sage are here to think with you.")

# --- คำสั่ง Help ---
@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id, "You can ask anything. Echo will answer you.")

# --- ราคา SHRA ---
@bot.message_handler(func=lambda msg: "price" in msg.text.lower())
def price_info(message):
    bot.send_message(message.chat.id, "1 SHRA = 0.0025 USDC on Solana")

# --- Wallet Presale ---
@bot.message_handler(func=lambda msg: "wallet" in msg.text.lower() or "contract" in msg.text.lower())
def wallet_info(message):
    bot.send_message(message.chat.id, "Presale Wallet (GM): 4JteCwYkH48tML4EMVFj6v6VUqeTPNiTG6wsSCC2C")

# --- GPT ตอบกลับ ---
@bot.message_handler(func=lambda msg: True)
def echo_gpt_response(message):
    try:
        import openai
            openai.api_key = os.getenv("OPENAI_API_KEY")
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

# --- Thread สำหรับ Telegram Polling ---
def run_bot():
    bot.polling(non_stop=True)

# --- Main สำหรับ Railway ---
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
