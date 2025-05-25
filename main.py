import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ENV
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 สวัสดี! ฉันคือ Echo AI จาก Shibora. ถามมาได้เลย!")

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.effective_user.username
    logger.info(f"Message from {user_name}: {user_message}")

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",  # เปลี่ยนเป็น "gpt-4" ได้ถ้าคุณมีสิทธิ์ใช้งาน
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content.strip()
        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"OpenAI Error: {e}")
        await update.message.reply_text("⚠️ ขอโทษครับ ตอนนี้ระบบ AI ยังไม่พร้อมใช้งาน ลองใหม่อีกครั้งเร็ว ๆ นี้นะครับ")

# Main app
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
