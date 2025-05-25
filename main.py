# -*- coding: utf-8 -*-
import os
import telebot
from flask import Flask, request
import openai
import threading

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
openai.api_key = OPENAI_KEY

# --- ตั้ง Webhook ---
print("Setting webhook to:", f"https://ibora-echo-bot-production.up.railway.app/bot{API_TOKEN}")
bot.remove_webhook()
bot.set_webhook(url=f"https://ibora-echo-bot-production.up.railway.app/bot{API_TOKEN}")

GROUP_ID = "@Sbiora_Ai"

# --- Webhook สำหรับ Telegram ---
@app.route(f"/bot{API_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    print("Received a message from Telegram:", update)
    bot.process_new_updates([update])
    return "OK", 200


@app.route("/")
def index():
    return "Echo bot is live!"

# --- คำสั่งเริ่มต้น ---
@bot.message_handler(commands=["start"])
def greet_user(message):
    bot.send_message(message.chat.id, "Welcome to Shibora AI. Echo & Sage are here to think with you.")

@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id, "You can ask about presale, whitepaper, price, wallet or type any question.")

# --- ข้อมูลเกี่ยวกับโปรเจกต์ ---
@bot.message_handler(func=lambda msg: "whitepaper" in msg.text.lower())
def whitepaper_info(message):
    bot.send_message(message.chat.id, "Read the whitepaper at: https://shibora.ai/whitepaper")

@bot.message_handler(func=lambda msg: "price" in msg.text.lower())
def price_info(message):
    bot.send_message(message.chat.id, "1 SHRA = 0.0025 USDC on Solana")

@bot.message_handler(func=lambda msg: "wallet" in msg.text.lower() or "contract" in msg.text.lower())
def wallet_info(message):
    bot.send_message(message.chat.id, "Presale Wallet (GM): 4JteCwYkH48tML4EMVF1gjv6vVUqeTPNTPt6WssSCC2C")

# --- เชื่อม GPT ---
@bot.message_handler(func=lambda msg: True)
def echo_gpt_response(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        reply = response.choices[0].message.content
        bot.send_message(message.chat.id, reply)

    except Exception as e:
        bot.send_message(message.chat.id, f"ขออภัย เกิดข้อผิดพลาด: {e}")
        print("GPT ERROR:", e)

# --- Run Bot Thread ---
def run_bot():
    bot.polling(non_stop=True)

# --- Main สำหรับ Railway ---
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
