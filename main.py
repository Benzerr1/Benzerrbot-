import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import threading
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer

# 🔹 Replace with your actual bot token
BOT_TOKEN = "8422123429:AAHhgmzCBEPFezLBICovDLW4TpDVo0wke74"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Telegram bot handler ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Your bot is alive and running on Render!")

# --- Fake web server to keep Render alive ---
def run_fake_server():
    port = int(os.environ.get("PORT", 10000))  # Default port 10000
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    print(f"🌐 Fake web server running on port {port} to keep Render alive.")
    server.serve_forever()

# --- Start web server in a thread ---
threading.Thread(target=run_fake_server, daemon=True).start()

# --- Run Telegram bot on main thread ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("✅ Bot is running on Render (Free plan)...")
    app.run_polling()

if __name__ == "__main__":
    main()
    while True:
        time.sleep(60)
