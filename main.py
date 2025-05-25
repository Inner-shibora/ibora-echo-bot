import os
import telebot
from flask import Flask, request
import time
import threading

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

GROUP_ID = '@Sbiora_Ai'

@app.route(f"/bot{API_TOKEN}", methods=["POST"])
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
    bot.send_message(message.chat.id,
        "ð SHRA Token Presale is now LIVE!\n"
        "à¸£à¸²à¸à¸²: 1 SHRA = 0.0025 USDC\n"
        "à¸à¸³à¸à¸±à¸ $1,000 à¸à¹à¸­à¸à¸£à¸°à¹à¸à¹à¸²\n"
        "à¸£à¸±à¸à¹à¸à¹à¸à¸à¸à¸±à¸à¸à¸µ: https://shibora.ai/presale"
    )

@bot.message_handler(func=lambda message: "whitepaper" in message.text.lower())
def whitepaper_info(message):
    bot.send_message(message.chat.id,
        "ð à¸­à¹à¸²à¸ Whitepaper à¸à¸­à¸à¹à¸£à¸²:\n"
        "à¹à¸à¸§à¸à¸´à¸ AI à¸à¸£à¸±à¸à¸à¸², Tokenomics, à¸à¸§à¸²à¸¡à¹à¸à¸£à¹à¸à¹à¸ª\n"
        "https://shibora.ai/whitepaper"
    )

@bot.message_handler(func=lambda message: "à¸£à¸²à¸à¸²" in message.text.lower())
def price_info(message):
    bot.send_message(message.chat.id,
        "ð° 1 SHRA = 0.0025 USDC\n"
        "à¸à¸·à¹à¸­à¸à¹à¸§à¸¢ USDC à¸à¸ Solana\n"
        "Presale: https://shibora.ai/presale"
    )

@bot.message_handler(func=lambda message: "wallet" in message.text.lower() or "contract" in message.text.lower())
def wallet_info(message):
    bot.send_message(message.chat.id,
        "GM Wallet à¸ªà¸³à¸«à¸£à¸±à¸à¸à¸£à¸µà¹à¸à¸¥à¸¥à¹:\n"
        "4JteCwYkH48tM4LEFNYTigy6vYuQeTPNTPW6TwsSCC2C\n"
        "à¸à¸£à¸§à¸à¸ªà¸­à¸à¸à¸ Solscan à¹à¸à¹à¸à¸¸à¸à¸à¸¸à¸£à¸à¸£à¸£à¸¡"
    )

# --- Default Echo ---
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Echo: {message.text}")

# --- Echo x Sage Conversation ---
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
        time.sleep(600)  # Every 10 minutes

threading.Thread(target=ai_dialogue_loop, daemon=True).start()

app = app
