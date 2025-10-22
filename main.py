import mimetypes
import sys
import types
import logging

# Patch for Python 3.13+ removal of imghdr
if sys.version_info >= (3, 13):
    sys.modules['imghdr'] = types.SimpleNamespace(
        what=lambda filename: mimetypes.guess_type(filename)[0]
    )from telegram import Update
from telegram.ext import ContextTypes
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # replace this with your actual bot token

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I’m Benzerrballer — your football insight bot ⚽🤖")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot is running...")
app.run_polling()
