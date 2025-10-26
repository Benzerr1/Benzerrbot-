import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your actual tokens
BOT_TOKEN = "8422123429:AAHaDrgJt5pxGDyZkrqrmQfPJlUuyiAVH6g"
API_KEY = "9f29e5b7bamsh94c856f9545626cp1b01b6jsna90412146954"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ Welcome to *Benzerr Football Predictor!* \n\n"
        "Use /predict followed by a match like this:\n"
        "`/predict Arsenal vs Chelsea`\n\n"
        "I'll show you stats and prediction probability!",
        parse_mode="Markdown"
    )

# Predict command
async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗Please provide a match, e.g. `/predict Arsenal vs Chelsea`")
        return

    query = " ".join(context.args)
    url = "https://api-football-v1.p.rapidapi.com/v3/predictions"
    headers = {
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        "x-rapidapi-key": API_KEY
    }
    params = {"q": query}

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if not data or "response" not in data or not data["response"]:
            await update.message.reply_text("⚠️ Game not available or no prediction data found.")
            return

        match = data["response"][0]
        teams = match["teams"]
        league = match["league"]

        msg = (
            f"🏆 *{league['name']}* ({league['country']})\n"
            f"⚔️ {teams['home']['name']} vs {teams['away']['name']}\n"
        )

        if "predictions" in match and match["predictions"]:
            pred = match["predictions"]
            msg += (
                f"\n📊 *Prediction:* {pred.get('winner', {}).get('name', 'N/A')}\n"
                f"💪 Confidence: {pred.get('percent', 'N/A')}%"
            )
        else:
            msg += "\n⚠️ No prediction data available."

        await update.message.reply_text(msg, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error fetching prediction: {e}")
        await update.message.reply_text("⚠️ Error retrieving prediction data. Try again later.")

# Main function
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("predict", predict))
    logger.info("✅ Benzerr Football Predictor is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
