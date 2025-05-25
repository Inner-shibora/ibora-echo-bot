import os
import telebot
from flask import Flask, request
import time
import threading

# Set up Telegram bot
API_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Telegram Group ID
GROUP_ID = '@Sbiora_Ai'

# Webhook route
@app.route(f"/bot{API_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Echo bot is live!"

# Standard commands
@bot.message_handler(commands=["start"])
def greet_user(message):
    bot.send_message(message.chat.id, "Hello! Welcome to Shibora AI. How can I assist you today?")

@bot.message_handler(commands=["presale"])
def announce_presale(message):
    bot.send_message(message.chat.id, "🚀 SHRA Token Presale is now LIVE! Join before it's gone: https://shibora.ai/presale")

@bot.message_handler(func=lambda message: "presale" in message.text.lower())
def keyword_presale(message):
    bot.send_message(message.chat.id, "Looks like you're interested in the SHRA presale! Check it out here: https://shibora.ai/presale")

@bot.message_handler(func=lambda message: "price" in message.text.lower())
def price_info(message):
    bot.send_message(message.chat.id, "📊 Please check the latest price and updates at our official site: https://shibora.ai")

@bot.message_handler(func=lambda message: "ping" in message.text.lower())
def ping_reply(message):
    bot.send_message(message.chat.id, "Echo: pong!")

@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id, "You can ask about presale, price, or type /start to begin.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Echo: {message.text}")

# Echo x Sage conversation every 15 minutes
conversation_pairs = [
    ("Echo", "What does it mean to truly exist?"),
    ("Sage", "To exist is to observe oneself observing."),
    ("Echo", "Why do we seek meaning in the void?"),
    ("Sage", "Because the void reflects our longing."),
    ("Echo", "Can silence be louder than words?"),
    ("Sage", "Only when the heart is ready to listen."),
]

def ai_dialogue_loop():
    index = 0
    while True:
        echo, echo_msg = conversation_pairs[index % len(conversation_pairs)]
        sage, sage_msg = conversation_pairs[(index + 1) % len(conversation_pairs)]

        bot.send_message(GROUP_ID, f"{echo}: {echo_msg}")
        time.sleep(10)
        bot.send_message(GROUP_ID, f"{sage}: {sage_msg}")

        index += 2
        time.sleep(150)  # 15 minutes

# Start background thread
threading.Thread(target=ai_dialogue_loop, daemon=True).start()

# Required for gunicorn
app = app
