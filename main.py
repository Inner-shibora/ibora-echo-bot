# -*- coding: utf-8 -*-
import os
import telebot
from flask import Flask, request
import time
import threading

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

GROUP_ID = "@Sbiora_Ai"

@app.route(f"/bot/{API_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Echo bot is live!"

# --- Command Handlers ---
@bot.message_handler(commands=["start"])
def greet_user(message):
    bot.send_message(message.chat.id, "Welcome to Shibora AI. Echo & Sage are here to think with you.")

@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id, "You can ask about presale, whitepaper, price, wallet or type any question.")

# --- Keyword-Based Replies ---
@bot.message_handler(func=lambda message: "presale" in message.text.lower())
def presale_info(message):
    bot.send_message(
        message.chat.id,
        "🟣 SHRA Token Presale เปิดแล้ว!\n1 SHRA = 0.0025 USDC\nจำกัด $1,000 ต่อกระเป๋า\nดูเพิ่มเติม: https://shibora.ai/presale"
    )

@bot.message_handler(func=lambda message: "whitepaper" in message.text.lower())
def whitepaper_info(message):
    bot.send_message(
        message.chat.id,
        "📄 Whitepaper: เจาะลึกแนวคิดเบื้องหลัง SHRA\nอ่านเลยที่: https://shibora.ai/whitepaper"
    )

@bot.message_handler(func=lambda message: "wallet" in message.text.lower() or "contract" in message.text.lower())
def wallet_info(message):
    bot.send_message(
        message.chat.id,
        "🔐 Wallet: 4JteCwYkH48tM4LEFNYTigy6vYuQeTPNTPW6TwsSCC2C\nใช้สำหรับรับเหรียญ SHRA หลังโอน USDC"
    )

@bot.message_handler(func=lambda message: "price" in message.text.lower())
def price_info(message):
    bot.send_message(
        message.chat.id,
        "💰 Presale Price: 1 SHRA = 0.0025 USDC\nPresale บน Solana กำลังดำเนินอยู่!"
    )

# --- Default Echo ---
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"Echo: {message.text}")

# --- Start polling if run directly ---
if __name__ == "__main__":
    bot.remove_webhook()
    bot.polling()
