import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Logging setup ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# --- Keys and headers ---
BOT_TOKEN = "8422123429:AAHhgmzCBEPFezLBICovDLW4TpDVo0wke74"
API_FOOTBALL_KEY = "9f29e5b7bamsh94c856f9545626cp1b01b6jsna90412146954"

HEADERS = {
    "x-rapidapi-key": API_FOOTBALL_KEY,
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

# --- API URLs ---
FIXTURES_URL = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
PREDICTIONS_URL = "https://api-football-v1.p.rapidapi.com/v3/predictions"

# --- /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to *Benzerr Football Predictor!*\n\n"
        "Use `/predict TeamA vs TeamB`\n"
        "Example: `/predict Arsenal vs Chelsea`\n\n"
        "I’ll fetch live data, odds, predictions, scores and league info ⚽",
        parse_mode="Markdown"
    )

# --- /predict ---
async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please use format: `/predict TeamA vs TeamB`", parse_mode="Markdown")
        return

    query = " ".join(context.args)
    teams = query.split("vs")

    if len(teams) != 2:
        await update.message.reply_text("⚠️ Please use correct format: `/predict TeamA vs TeamB`", parse_mode="Markdown")
        return

    home_team = teams[0].strip()
    away_team = teams[1].strip()

    await update.message.reply_text(f"🔍 Searching for *{home_team}* vs *{away_team}*...", parse_mode="Markdown")

    try:
        # Step 1: Find the fixture
        params = {"team": home_team, "season": 2025}
        fixture_response = requests.get(FIXTURES_URL, headers=HEADERS, params=params).json()

        fixture = None
        for f in fixture_response.get("response", []):
            if away_team.lower() in f["teams"]["away"]["name"].lower():
                fixture = f
                break

        if not fixture:
            await update.message.reply_text("⚽ Game not available. Please try another matchup.")
            return

        fixture_id = fixture["fixture"]["id"]
        match_date = fixture["fixture"]["date"]
        status = fixture["fixture"]["status"]["short"]
        league_name = fixture["league"]["name"]
        country_name = fixture["league"]["country"]
        home_score = fixture["goals"]["home"]
        away_score = fixture["goals"]["away"]

        # Step 2: Get prediction data
        prediction_data = requests.get(PREDICTIONS_URL, headers=HEADERS, params={"fixture": fixture_id}).json()

        if not prediction_data.get("response"):
            await update.message.reply_text("⚽ No prediction data found for this game.")
            return

        prediction = prediction_data["response"][0]["predictions"]
        winner = prediction["winner"]["name"] or "No clear favorite"
        advice = prediction["advice"]

        # Step 3: Live score info (if match ongoing)
        live_text = ""
        if status in ["1H", "2H", "HT", "LIVE"]:
            events = fixture.get("events", [])
            scorers = []
            for e in events:
                if e.get("type") == "Goal":
                    player = e["player"]["name"]
                    team = e["team"]["name"]
                    scorers.append(f"{player} ({team})")
            scorers_text = ", ".join(scorers) if scorers else "No goal data yet"
            live_text = f"\n🔥 *Live Score:* {home_score} - {away_score}\n⚽ *Scorers:* {scorers_text}"

        # Step 4: Format message
        message = (
            f"🏆 *League:* {league_name} ({country_name})\n"
            f"📅 *Date:* {match_date[:16].replace('T', ' ')}\n"
            f"⏱️ *Status:* {status}\n\n"
            f"🏠 {home_team} vs {away_team}\n"
            f"📊 *Prediction:* {winner}\n"
            f"💬 *Advice:* {advice}"
            f"{live_text}"
        )

        await update.message.reply_text(message, parse_mode="Markdown")

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("❌ Something went wrong while fetching data.")

# --- Main ---
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("predict", predict))

    print("✅ Benzerr Football Predictor running...")
    app.run_polling()
