importfrom telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8422123429:AAHhgmzCBEPFezLBICovDLW4TpDVo0wke74"  # paste your real token here

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I’m Benzerrballer — your football insight bot ⚽🤖")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("✅ Bot is running on Render...")
app.run_polling()  # this keeps the bot online and listening

print("✅ Bot is running on Render...")
app.run_polling()
