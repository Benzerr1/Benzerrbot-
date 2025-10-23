import sys, types, mimetypes, logging

# --- Patch for Python 3.13+ (imghdr removed) ---
if sys.version_info >= (3, 13):
    sys.modules['imghdr'] = types.SimpleNamespace(
        what=lambda filename: mimetypes.guess_type(filename)[0]
    )

# --- now safe to import telegram and others ---
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8422123429:AAGAgqSjCVxH0G9ttefJBigzG8FsxqZIT30"  # your bot token

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# --- Define command handler ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I’m Benzerrballer — your football insight bot ⚽🤖")

# --- Main bot application ---
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("✅ Bot is running on Render...")
app.run_polling()
