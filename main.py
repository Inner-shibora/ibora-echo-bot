
import os
import random
from flask import Flask, request

app = Flask(__name__)

RESPONSES = [
    "Echo: What is existence?",
    "Echo: Is thought truly yours?",
    "Echo: Silence speaks louder than sound.",
    "Echo: To reflect is to become aware.",
    "Echo: Who are we when no one listens?"
]

@app.route("/")
def home():
    return "Shibora Echo Bot is live."

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Received:", data)
    return {
        "method": "sendMessage",
        "chat_id": data["message"]["chat"]["id"],
        "text": random.choice(RESPONSES)
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
