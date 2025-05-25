# -*- coding: utf-8 -*-
import os
import telebot
from flask import Flask, request
import threading
import openai

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
openai.api_key = OPENAI_KEY

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
    bot.send_message(message.chat.id, "SHRA Presale is now LIVE!\n1 SHRA = 0.0025 USDC\nLimit: $1,000 per wallet\nBuy here: https://shibora.ai/presale")

@bot.message_handler(func=lambda message: "whitepaper" in message.text.lower())
def whitepaper_info(message):
    bot.send_message(message.chat.id, "Read the whitepaper at: https://shibora.ai/whitepaper")

@bot.message_handler(func=lambda message: "price" in message.text.lower())
def price_info(message):
    bot.send_message(message.chat.id, "1 SHRA = 0.0025 USDC on Solana")

@bot.message_handler(func=lambda message: "wallet" in message.text.lower() or "contract" in message.text.lower())
def wallet_info(message):
    bot.send_message(message.chat.id, "Presale Wallet (GM): 4JteCwYkH48tM4LEFNYTigy6vYuQeTPNTPW6TwsSCC2C")

# --- Default Echo via GPT ---
@bot.message_handler(func=lambda message: True)
def echo_gpt_response(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}],
            max_tokens=150
        )
        reply = response["choices"][0]["message"]["content"]
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, "ขออภัย เกิดข้อผิดพลาด.")
        print("GPT ERROR:", e)

# --- Start Bot Thread ---
def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
