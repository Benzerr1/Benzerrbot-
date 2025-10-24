import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === Replace these with your keys ===
TELEGRAM_BOT_TOKEN = "8422123429:AAHhgmzCBEPFezLBICovDLW4TpDVo0wke74"
API_FOOTBALL_KEY = "9f29e5b7bamsh94c856f9545626cp1b01b6jsna90412146954"

# === Set up logging ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# === Football prediction logic ===
def get_match_predictions():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"next": "5"}  # Next 5 matches
    headers = {
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        "x-rapidapi-key": API_FOOTBALL_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        matches = data.get("response", [])
        if not matches:
            return "No upcoming matches found."

        predictions = []
        for match in matches:
            teams = match["teams"]
            home = teams["home"]["name"]
            away = teams["away"]["name"]

            # Simple prediction logic (you can make this smarter later)
            if "city" in home.lower() or "united" in home.lower():
                prediction = f"{home} might win vs {away}"
            else:
                prediction = f"{away} might surprise {home}"

            predictions.append(prediction)

        return "\n".join(predictions)

    except Exception as e:
        logging.error(f"Error fetching matches: {e}")
        return "⚠️ Could not fetch match data. Try again later."

# === Telegram Bot Commands ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ Welcome to Benzerr Football Predictor! Type /predict to get upcoming match tips.")

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Fetching predictions, please wait...")
    predictions = get_match_predictions()
    await update.message.reply_text(predictions)

# === Main Bot Runner ===
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("predict", predict))

    logging.info("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
