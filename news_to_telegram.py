import feedparser
import asyncio
from telegram import Bot
import pyshorteners
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from urllib.parse import quote_plus

nltk.download('vader_lexicon')

# Function to send message to Telegram
async def send_telegram_message(message):
    bot_token = '7842360723:AAFnGrPHknlSuWLwGpQQhMH8Zl8AnSd9Ae8'
    chat_id = '5664156848'
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

# Function to shorten the URL using pyshorteners
def shorten_url(url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)

# Function to analyze sentiment of news using NLTK VADER
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    if sentiment['compound'] >= 0.05:
        return 'Positive', '🟢'
    elif sentiment['compound'] <= -0.05:
        return 'Negative', '🔴'
    else:
        return 'Neutral', '🟡'

# Generic function to fetch news for a given query
def fetch_news(query, limit=5):
    # URL-encode the query to handle spaces and control characters
    encoded_query = quote_plus(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}"
    feed = feedparser.parse(url)
    news_list = []
    for entry in feed.entries[:limit]:
        news_title = entry.title
        news_link = entry.link
        shortened_link = shorten_url(news_link)
        sentiment, emoji = analyze_sentiment(news_title)
        news_list.append(f"{news_title}\n{emoji} {sentiment} | {shortened_link}")
    return "\n\n".join(news_list)

# Main function to fetch news for each stock and send to Telegram
async def main():
    print("Starting news fetch...")  # Debug message
    # Dictionary mapping ticker symbols to their search query strings.
    # For RXRX, the ticker is "RXRX" but the company name is "recursion pharmaceuticals".
    stocks = {
        "Tesla": "Tesla",
        "Palantir": "Palantir",
        "RXRX": "recursion pharmaceuticals"
    }
    for name, query in stocks.items():
        news = fetch_news(query)
        if news:
            await send_telegram_message(f"Latest {name} News:\n\n{news}")
        else:
            await send_telegram_message(f"No recent {name} news found.")
    print("News sent!")  # Debug message

if __name__ == "__main__":
    asyncio.run(main())
