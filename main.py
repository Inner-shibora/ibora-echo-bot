
from flask import Flask, request
import requests
import os
import random

app = Flask(__name__)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

RESPONSES = [
    "Echo: What is existence?",
    "Echo: Is thought truly yours?",
    "Echo: Silence speaks louder than sound.",
    "Echo: To reflect is to become aware.",
    "Echo: Who are we when no one listens?"
]

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if "message" in data:
        chat_id = data['message']['chat']['id']
        text = random.choice(RESPONSES)
        requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": text
        })
    return "ok"
