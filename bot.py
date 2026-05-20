import os
import re
import logging
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Get token from environment variable
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Character and word counting function
def analyze_text(text: str):
    # Remove whitespace for character count
    text_stripped = text.strip()
    
    # Count characters (excluding spaces? Include spaces - more common)
    char_count_with_spaces = len(text_stripped)
    char_count_no_spaces = len(text_stripped.replace(" ", ""))
    
    # Count words
    words = text_stripped.split()
    word_count = len(words)
    
    # Count sentences (simple: . ! ?)
    sentence_endings = re.findall(r'[.!?]+', text_stripped)
    sentence_count = len(sentence_endings) if sentence_endings else (1 if text_stripped else 0)
    
    # Estimate reading time (average 200 words per minute)
    if word_count > 0:
        reading_minutes = word_count / 200
        if reading_minutes < 1:
            reading_time = "Less than 1 min"
        elif reading_minutes < 2:
            reading_time = "1 min"
        else:
            reading_time = f"{int(reading_minutes)} mins"
    else:
        reading_time = "Less than 1 min"
    
    # Count top keywords (simple frequency, excluding common stop words)
    stop_words = {'the', 'and', 'to', 'of', 'a', 'in', 'for', 'on', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'but', 'or', 'so', 'if', 'then', 'else', 'when', 'where', 'which', 'while', 'who', 'whom', 'this', 'that', 'these', 'those', 'from', 'at', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'under', 'over', 'your', 'our', 'their', 'my', 'his', 'her', 'its', 'our', 'their', 'i', 'you', 'he', 'she', 'it', 'we', 'they'}
    
    word_freq = {}
    for word in words:
        clean_word = word.lower().strip('.,!?;:()[]{}"\'')
        if clean_word and clean_word not in stop_words and len(clean_word) > 2:
            word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
    
    # Get top 3 keywords
    top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:3]
    keywords_text = ", ".join([f"{kw} ({count}x)" for kw, count in top_keywords]) if top_keywords else "None"
    
    return {
        'words': word_count,
        'characters_with_spaces': char_count_with_spaces,
        'characters_no_spaces': char_count_no_spaces,
        'sentences': sentence_count,
        'reading_time': reading_time,
        'top_keywords': keywords_text
    }

# /start command handler
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "Welcome to TextMetrics Bot\n\n"
        "Send me any text and I will analyze:\n"
        "• Word count\n"
        "• Character count\n"
        "• Sentence count\n"
        "• Reading time\n"
        "• Top keywords\n\n"
        "Just type or paste your text below to begin."
    )
    await update.message.reply_text(welcome_message)

# /help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = (
        "How to use TextMetrics Bot\n\n"
        "1. Send any text message\n"
        "2. Wait for analysis results\n"
        "3. Send more text anytime\n\n"
        "Commands:\n"
        "/start - Restart the bot\n"
        "/help - Show this message"
    )
    await update.message.reply_text(help_message)

# Handle regular text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Ignore commands that slip through
    if user_text.startswith('/'):
        return
    
    # Analyze the text
    stats = analyze_text(user_text)
    
    # Format response (clean, no emojis to be extra safe with policy)
    response = (
        f"Text Analysis Results\n\n"
        f"Words: {stats['words']}\n"
        f"Characters: {stats['characters_with_spaces']}\n"
        f"Sentences: {stats['sentences']}\n"
        f"Reading Time: {stats['reading_time']}\n"
        f"Top Keywords: {stats['top_keywords']}\n\n"
        f"Send more text for another analysis."
    )
    
    await update.message.reply_text(response)

# Handle errors
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")

# Set bot commands menu
async def set_commands(application: Application):
    commands = [
        BotCommand("start", "Restart the bot"),
        BotCommand("help", "Show help information"),
    ]
    await application.bot.set_my_commands(commands)

def main():
    print("Starting TextMetrics Bot...")
    
    # Create application
    app = Application.builder().token(TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)
    
    # Set commands menu (callback after bot is ready)
    app.post_init = set_commands
    
    # Start polling
    print("Bot is running...")
    app.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main()
