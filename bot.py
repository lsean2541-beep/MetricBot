import telebot
import re
from collections import Counter
from telebot import types

# INSERT YOUR REAL TOKEN BELOW
API_TOKEN = '8791708356:AAF5B2TGxkxZK7Os3zGUzX6KsVP9UY442jM'
bot = telebot.TeleBot(API_TOKEN)

def analyze_text(text):
    # Basic counts
    char_count = len(text)
    words = re.findall(r'\w+', text.lower())
    word_count = len(words)
    sentences = len(re.findall(r'[.!?]+', text))
    
    # Reading time (avg 200 words per minute)
    read_time = round(word_count / 200, 1)
    if read_time < 1:
        read_time = "Less than 1 min"
    else:
        read_time = f"{read_time} min"

    # Most frequent words (ignoring very short words)
    long_words = [w for w in words if len(w) > 3]
    common = Counter(long_words).most_common(3)
    top_words = ", ".join([f"{word} ({count}x)" for word, count in common]) if common else "None"

    return {
        "chars": char_count,
        "words": word_count,
        "sentences": sentences,
        "time": read_time,
        "top": top_words
    }

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, "📊 *Send me any text (article, post, or caption), and I will analyze it for you!*", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_analysis(message):
    stats = analyze_text(message.text)
    
    response = (
        "📝 *Text Analysis Results:*\n\n"
        f"🔢 *Words:* {stats['words']}\n"
        f"🔤 *Characters:* {stats['chars']}\n"
        f"📍 *Sentences:* {stats['sentences']}\n"
        f"⏱️ *Est. Reading Time:* {stats['time']}\n"
        f"🔝 *Top Keywords:* {stats['top']}\n\n"
        "Keep writing! Send more text anytime."
    )
    
    bot.send_message(message.chat.id, response, parse_mode="Markdown")

bot.polling()
