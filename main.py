import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# =====================================================
#  🔧 Replace these with your actual keys
# =====================================================
BOT_TOKEN = "8422123429:AAHaDrgJt5pxGDyZkrqrmQfPJlUuyiAVH6g"
API_FOOTBALL_KEY = "9f29e5b7bamsh94c856f9545626cp1b01b6jsna90412146954"
# =====================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

API_URL = "https://v3.football.api-sports.io"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ Welcome to *Benzerr Football Predictor!*\n\n"
        "Use this format to get match predictions:\n"
        "`/predict team1 vs team2`\n\n"
        "Example: `/predict Barcelona vs Real Madrid`",
        parse_mode="Markdown",
    )

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please use `/predict team1 vs team2` format.")
        return

    query = " ".join(context.args)
    if "vs" not in query.lower():
        await update.message.reply_text("❌ Please include 'vs' between teams.")
        return

    team1, team2 = [t.strip() for t in query.split("vs", 1)]

    headers = {
        "x-apisports-key": API_FOOTBALL_KEY,
    }

    try:
        # Search both teams
        team1_resp = requests.get(f"{API_URL}/teams?search={team1}", headers=headers).json()
        team2_resp = requests.get(f"{API_URL}/teams?search={team2}", headers=headers).json()

        if not team1_resp["response"] or not team2_resp["response"]:
            await update.message.reply_text("❌ Game not available or teams not found.")
            return

        # Pick first matching results
        team1_info = team1_resp["response"][0]
        team2_info = team2_resp["response"][0]

        country1 = team1_info["team"]["country"]
        league_resp = requests.get(
            f"{API_URL}/leagues?team={team1_info['team']['id']}", headers=headers
        ).json()

        league_name = league_resp["response"][0]["league"]["name"] if league_resp["response"] else "Unknown League"
        league_country = league_resp["response"][0]["country"]["name"] if league_resp["response"] else "Unknown Country"

        # Example "fake" win chance (later replace with real prediction logic)
        import random
        t1_chance = random.randint(40, 60)
        t2_chance = 100 - t1_chance

        await update.message.reply_text(
            f"🏆 *{league_name}* ({league_country})\n\n"
            f"⚔️ {team1} vs {team2}\n\n"
            f"📊 Predicted Win Chances:\n"
            f"{team1}: {t1_chance}%\n"
            f"{team2}: {t2_chance}%\n\n"
            f"🔮 (Data from API-Football)",
            parse_mode="Markdown",
        )

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        await update.message.reply_text("⚠️ Error fetching prediction data.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("predict", predict))
    logger.info("✅ Benzerr Football Predictor is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
