import feedparser
import asyncio
from telegram import Bot
import pyshorteners

# Function to send message to Telegram
async def send_telegram_message(message):
    bot_token = '7842360723:AAFnGrPHknlSuWLwGpQQhMH8Zl8AnSd9Ae8'  # Your bot token
    chat_id = '5664156848'  # Your chat ID
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

# Function to shorten the URL using pyshorteners
def shorten_url(url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)  # You can also use other services like Bitly if preferred

# Fetch Google News RSS feed for Tesla
def fetch_tesla_news():
    url = "https://news.google.com/rss/search?q=Tesla"
    feed = feedparser.parse(url)

    tesla_news_list = []
    for entry in feed.entries[:5]:  # Limit to top 5 news
        news_title = entry.title
        news_link = entry.link
        # Shorten the news link
        shortened_link = shorten_url(news_link)
        tesla_news_list.append(f"{news_title}\n{shortened_link}")

    return "\n\n".join(tesla_news_list)

# Fetch Google News RSS feed for Palantir
def fetch_palantir_news():
    url = "https://news.google.com/rss/search?q=Palantir"
    feed = feedparser.parse(url)

    palantir_news_list = []
    for entry in feed.entries[:5]:  # Limit to top 5 news
        news_title = entry.title
        news_link = entry.link
        # Shorten the news link
        shortened_link = shorten_url(news_link)
        palantir_news_list.append(f"{news_title}\n{shortened_link}")

    return "\n\n".join(palantir_news_list)

# Main function to fetch news and send to Telegram
async def main():
    print("Starting news fetch...")  # Debugging line
    tesla_news = fetch_tesla_news()
    palantir_news = fetch_palantir_news()

    if tesla_news:
        await send_telegram_message(f"Latest Tesla News:\n\n{tesla_news}")
    else:
        await send_telegram_message("No recent Tesla news found.")

    if palantir_news:
        await send_telegram_message(f"Latest Palantir News:\n\n{palantir_news}")
    else:
        await send_telegram_message("No recent Palantir news found.")

    print("News sent!")  # Debugging line

# This will ensure that the main() function is only run if this script is executed directly
if __name__ == "__main__":
    asyncio.run(main())  # Running the main function with asyncio
