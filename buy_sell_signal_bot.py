import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import asyncio
from telegram import Bot
from datetime import datetime
import importlib
import os
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Dictionary to manage signal message state per stock
sent_no_signal_message = {}

# Hardcoded default Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = '7842360723:AAFnGrPHknlSuWLwGpQQhMH8Zl8AnSd9Ae8'
TELEGRAM_CHAT_ID = '5664156848'

# Asynchronous function to send Telegram messages
async def send_telegram_message(message):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.info(f"Telegram message sent: {message}")
    except Exception as e:
        logging.error(f"Failed to send Telegram message: {e}")

# Function to calculate RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to calculate moving averages
def calculate_ma(data):
    data["MA_50"] = data["Close"].rolling(window=50).mean()
    data["MA_200"] = data["Close"].rolling(window=200).mean()
    return data

# Function to calculate MACD and Signal Line
def calculate_macd(data):
    short_ema = data["Close"].ewm(span=12, adjust=False).mean()
    long_ema = data["Close"].ewm(span=26, adjust=False).mean()
    data["MACD"] = short_ema - long_ema
    data["Signal_Line"] = data["MACD"].ewm(span=9, adjust=False).mean()
    return data

# Asynchronous function to process each stock:
# Data download, indicator calculation, signal generation, Telegram notification, and chart saving.
async def process_stock(stock, start_date, end_date):
    global sent_no_signal_message

    try:
        data = yf.download(stock, start=start_date, end=end_date, interval="1d")
    except Exception as e:
        logging.error(f"{stock} data download failed: {e}")
        return

    if data.empty:
        logging.warning(f"No data available for {stock}.")
        return

    # Calculate indicators
    data["RSI"] = calculate_rsi(data)
    data = calculate_ma(data)
    data = calculate_macd(data)

    # Generate buy/sell signals over the entire dataset
    data["Buy_Signal"] = (data["RSI"] < 50) & ((data["MA_50"] > data["MA_200"]) | (data["MACD"] > data["Signal_Line"]))
    data["Sell_Signal"] = (data["RSI"] > 70) & ((data["MA_50"] < data["MA_200"]) | (data["MACD"] < data["Signal_Line"]))

    if stock not in sent_no_signal_message:
        sent_no_signal_message[stock] = False

    # Check only the latest (most recent) row for today's signal
    latest_date = data.index[-1]
    buy_signal = data["Buy_Signal"].iat[-1]
    sell_signal = data["Sell_Signal"].iat[-1]

    if buy_signal:
        await send_telegram_message(f"{stock} - Buy Signal detected on {latest_date}")
        sent_no_signal_message[stock] = False
    elif sell_signal:
        await send_telegram_message(f"{stock} - Sell Signal detected on {latest_date}")
        sent_no_signal_message[stock] = False
    elif not sent_no_signal_message[stock]:
        await send_telegram_message(f"{stock}: No buy/sell signals today.")
        sent_no_signal_message[stock] = True

    try:
        plt.figure(figsize=(10, 6))
        # Plot Close Price and Moving Averages
        plt.subplot(2, 1, 1)
        plt.plot(data.index, data["Close"], label="Close Price", color="blue")
        plt.plot(data.index, data["MA_50"], label="50-Day MA", color="orange")
        plt.plot(data.index, data["MA_200"], label="200-Day MA", color="red")
        plt.scatter(data.index[data["Buy_Signal"]], data["Close"][data["Buy_Signal"]],
                    label="Buy Signal", marker="^", color="green", alpha=1)
        plt.scatter(data.index[data["Sell_Signal"]], data["Close"][data["Sell_Signal"]],
                    label="Sell Signal", marker="v", color="red", alpha=1)
        plt.title(f"{stock} Price and Indicator Signals")
        plt.legend()

        # Plot RSI
        plt.subplot(2, 1, 2)
        plt.plot(data.index, data["RSI"], label="RSI", color="red")
        plt.axhline(70, linestyle="--", color="gray")
        plt.axhline(30, linestyle="--", color="gray")
        plt.legend()

        chart_filename = f"{stock}_RSI_MA_MACD_Signals.png"
        plt.savefig(chart_filename)
        plt.close()
        logging.info(f"{stock} chart saved as {chart_filename}.")
    except Exception as e:
        logging.error(f"Failed to create/save chart for {stock}: {e}")

# Main asynchronous function to process all stocks and run the news module.
async def main():
    await send_telegram_message("Trading bot execution started!")

    stocks = ["TSLA", "PLTR"]
    today = datetime.today().strftime('%Y-%m-%d')
    start_date = "2020-01-01"
    end_date = today

    tasks = [process_stock(stock, start_date, end_date) for stock in stocks]
    await asyncio.gather(*tasks)

    try:
        news_module = importlib.import_module('news_to_telegram')
        await news_module.main()
    except Exception as e:
        logging.error(f"Failed to execute news_to_telegram module: {e}")

    logging.info("Trading signals and alerts sent!")

if __name__ == "__main__":
    asyncio.run(main())
