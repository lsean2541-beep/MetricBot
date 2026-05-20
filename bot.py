import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Your private channel invite link
CHANNEL_LINK = "https://t.me/+MSNeKqoJlwFmOGU8"

async def start(update, context):
    """Send a single button to join the channel immediately."""
    # Single, clear button with your requested text
    keyboard = [
        [InlineKeyboardButton("🚀 Unlock Access", url=CHANNEL_LINK)]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Your exact welcome and redirecting message
    await update.message.reply_text(
        f"🔓 **Access unlocked.**\n\n"
        f"**Private channel is now available.**\n\n"
        f"👇 **Enter below before access closes.**",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def main():
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    main()
