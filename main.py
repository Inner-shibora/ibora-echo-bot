import os
import requests
from flask import Flask, request

app = Flask(__name__)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.route("/")
def index():
    return "Bot is alive!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    payload = {
        "chat_id": chat_id,
        "text": f"คุณพิมพ์ว่า: {text}"
    }
    requests.post(TELEGRAM_API_URL, json=payload)

    return "OK"

if __name__ == "__main__":
    app.run(debug=True)
