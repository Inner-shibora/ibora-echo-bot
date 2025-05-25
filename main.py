# -*- coding: utf-8 -*-
import os
import telebot
from flask import Flask, request
import threading
from openai import OpenAI

# โหลด API Key
API_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# สร้าง bot และ app
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# ตั้งค่า Webhook
bot.remove_webhook()
bot.set_webhook(url=f"https://ibora-echo-bot-production.up.railway.app/bot/{API_TOKEN}")

# Webhook สำหรับ Telegram
@app.route(f"/bot/{API_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# ตอบ /start
@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "ยินดีต้อนรับสู่ Shibora AI!")

# ตอบ /help
@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id, "คุณสามารถพิมพ์คำถามอะไรก็ได้ แล้ว Echo จะตอบกลับให้ครับ")

# ตอบข้อความ "price"
@bot.message_handler(func=lambda msg: "price" in msg.text.lower())
def price_info(message):
    bot.send_message(message.chat.id, "1 SHRA = 0.0025 USDC on Solana")

# ตอบข้อความ "wallet" หรือ "contract"
@bot.message_handler(func=lambda msg: "wallet" in msg.text.lower() or "contract" in msg.text.lower())
def wallet_info(message):
    bot.send_message(message.chat.id, "Presale Wallet (GM): 4JteCwYkH48tML4EMVFj6v6VUqeTPNiTG6wS5C2CzC")

# เชื่อม GPT จริง
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

# รัน bot ใน thread
def run_bot():
    bot.polling(non_stop=True)

# เริ่มรันแอป
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
