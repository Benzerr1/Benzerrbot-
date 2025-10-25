import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- CONFIGURATION ---
BOT_TOKEN = "8422123429:AAHhgmzCBEPFezLBICovDLW4TpDVo0wwith"  # Replace with your actual Telegram bot token
API_KEY = "9f29e5b7bamsh94c856f9545626cp1b01b6jsna90412146954"      # Replace with your actual API-Football key
API_HOST = "api-football-v1.p.rapidapi.com"

# --- LOGGER ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Benzerr Football Predictor!\n\n"
        "Use /predict TeamA vs TeamB\n"
        "Example: /predict Arsenal vs Chelsea\n\n"
        "I'll fetch live data, odds, predictions, scores and league info ⚽"
    )

# --- PREDICT COMMAND ---
async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3 or "vs" not in context.args:
        await update.message.reply_text("Please use format:\n/predict TeamA vs TeamB")
        return

    # Parse input
    text = " ".join(context.args)
    try:
        team_a, team_b = text.lower().split(" vs ")
    except ValueError:
        await update.message.reply_text("Please use correct format: /predict TeamA vs TeamB")
        return

    await update.message.reply_text(f"🔎 Searching for {team_a.title()} vs {team_b.title()}...")

    url = f"https://{API_HOST}/v3/fixtures"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    params = {"season": "2025", "status": "NS"}  # Upcoming matches only

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        matches = data.get("response", [])
        found_match = None

        for match in matches:
            home = match["teams"]["home"]["name"].lower()
            away = match["teams"]["away"]["name"].lower()
            if team_a in home and team_b in away or team_b in home and team_a in away:
                found_match = match
                break

        if not found_match:
            await update.message.reply_text("⚽ Game not available. Please try another matchup.")
            return

        # Extract details
        league = found_match["league"]["name"]
        country = found_match["league"]["country"]
        date = found_match["fixture"]["date"].split("T")[0]
        home_team = found_match["teams"]["home"]["name"]
        away_team = found_match["teams"]["away"]["name"]

        # Try to get prediction
        pred_url = f"https://{API_HOST}/v3/predictions"
        pred_params = {"fixture": found_match["fixture"]["id"]}
        pred_res = requests.get(pred_url, headers=headers, params=pred_params).json()

        if pred_res.get("response"):
            pred_data = pred_res["response"][0]["predictions"]
            winner = pred_data.get("winner", {}).get("name", "Unknown")
            percent = pred_data.get("percent", {}).get("home", "N/A")
            await update.message.reply_text(
                f"🏆 League: {league} ({country})\n"
                f"⚽ Match: {home_team} vs {away_team}\n"
                f"📅 Date: {date}\n"
                f"🔮 Prediction: {winner} likely to win ({percent}% confidence)"
            )
        else:
            await update.message.reply_text(
                f"🏆 League: {league} ({country})\n"
                f"⚽ Match: {home_team} vs {away_team}\n"
                f"📅 Date: {date}\n"
                f"❌ Prediction not available yet."
            )

    except Exception as e:
        logger.error(f"Error fetching prediction: {e}")
        await update.message.reply_text("⚠️ Error retrieving match data. Please try again later.")

# --- MAIN FUNCTION ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("predict", predict))
    logger.info("✅ Benzerr Football Predictor running...")
    app.run_polling()

if __name__ == "__main__":
    main()
