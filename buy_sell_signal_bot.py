import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import asyncio
from telegram import Bot
from datetime import datetime, timedelta

# Global variable to track whether the message for no signals has been sent
sent_no_signal_message = False

# Function to send message to Telegram (with await for asynchronous execution)
async def send_telegram_message(message):
    bot_token = '7842360723:AAFnGrPHknlSuWLwGpQQhMH8Zl8AnSd9Ae8'
    chat_id = '5664156848'  # Your Telegram chat ID
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

# Define stock tickers
stocks = ["TSLA", "PLTR"]

# Function to calculate RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to calculate Moving Averages
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

# Get today's date and last date
today = datetime.today().strftime('%Y-%m-%d')
start_date = "2020-01-01"  # Keep this as the start date
end_date = today  # Use today's date as the end date

# Main function to execute the trading logic
async def main():
    global sent_no_signal_message  # Declare to modify the global variable

    # Send an immediate execution message
    await send_telegram_message("Trading bot execution started!")

    for stock in stocks:
        # Fetch historical stock data with daily interval
        data = yf.download(stock, start=start_date, end=end_date, interval="1d")

        # Calculate RSI, MA, and MACD
        data["RSI"] = calculate_rsi(data)
        data = calculate_ma(data)
        data = calculate_macd(data)

        # Generate buy/sell signals
        data["Buy_Signal"] = (data["RSI"] < 30) & (data["MA_50"] > data["MA_200"]) & (data["MACD"] > data["Signal_Line"])
        data["Sell_Signal"] = (data["RSI"] > 70) & (data["MA_50"] < data["MA_200"]) & (data["MACD"] < data["Signal_Line"])

        # Send Telegram alerts for buy/sell signals
        if data["Buy_Signal"].any():
            await send_telegram_message(f"Buy Signal detected at {data.index[data['Buy_Signal'].idxmax()]} for {stock}")
            sent_no_signal_message = False  # Reset the no signal message flag when a signal is sent
        elif data["Sell_Signal"].any():
            await send_telegram_message(f"Sell Signal detected at {data.index[data['Sell_Signal'].idxmax()]} for {stock}")
            sent_no_signal_message = False  # Reset the no signal message flag when a signal is sent
        elif not sent_no_signal_message:
            # Send the message only once if no signals are generated today
            await send_telegram_message(f"{stock}: No buy/sell signals today. Process completed!")
            sent_no_signal_message = True  # Set the flag to true to avoid repeated messages

        # Plot stock price, MA, RSI, and MACD with signals
        plt.figure(figsize=(10, 6))

        # Plot Closing Price and Moving Averages
        plt.subplot(2, 1, 1)
        plt.plot(data.index, data["Close"], label="Close Price", color="blue")
        plt.plot(data.index, data["MA_50"], label="50-Day MA", color="orange")
        plt.plot(data.index, data["MA_200"], label="200-Day MA", color="red")
        plt.scatter(data.index[data["Buy_Signal"]], data["Close"][data["Buy_Signal"]], label="Buy Signal", marker="^", color="green", alpha=1)
        plt.scatter(data.index[data["Sell_Signal"]], data["Close"][data["Sell_Signal"]], label="Sell Signal", marker="v", color="red", alpha=1)
        plt.title(f"{stock} Price & RSI + MA + MACD-based Signals")
        plt.legend()

        # Plot RSI Indicator
        plt.subplot(2, 1, 2)
        plt.plot(data.index, data["RSI"], label="RSI", color="red")
        plt.axhline(70, linestyle="--", color="gray")  # Overbought threshold
        plt.axhline(30, linestyle="--", color="gray")  # Oversold threshold
        plt.legend()

        # Save the chart
        plt.savefig(f"{stock}_RSI_MA_MACD_Signals.png")
        print(f"{stock} RSI + MA + MACD-based trading signals generated! Chart saved.")

    print("✅ Trading signals and alerts sent!")

# Run the main function
asyncio.run(main())
