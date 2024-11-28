import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from api_requests1 import GroqChatAgent
from weather_forecast import get_weather_forecast

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7930053151:AAFGKd3erV9QcghtScB9fY4R4nlkH22r8fQ"  # Replace with your actual token

# Initialize the GroqChatAgent
API_KEY = "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"  # Replace with your actual API key
SYSTEM_PROMPT = "You're an AI bot here to help farmers. Provide helpful, respectful, and polite answers."
MEMORY_LENGTH = 5
CSV_FILE = "Crop_Recommendation.csv"

agent = GroqChatAgent(API_KEY, SYSTEM_PROMPT, MEMORY_LENGTH, CSV_FILE)

# Define command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hello! I'm here to help you with farming information. Ask me anything!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "You can ask me farming-related questions or ask for weather updates, e.g., 'weather in Bengaluru'."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower()

    # Check if the user asked for a website to buy and sell goods
    if "website" in user_message or "buy and sell goods" in user_message:
        await update.message.reply_text("You can visit this website to buy and sell goods: http://127.0.0.1:5000")
        return

    # Check if the user asked for weather in a specific location
    if "weather" in user_message:
        location = "Bengaluru"  # Default location
        if "in " in user_message:
            location = user_message.split("in ")[-1].strip()
        weather_report = get_weather_forecast(location)
        await update.message.reply_text(weather_report)
        return

    # General query handling
    response = agent.get_response(user_message)
    await update.message.reply_text(response)

def main() -> None:
    # Create the application and pass it your bot's token
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
