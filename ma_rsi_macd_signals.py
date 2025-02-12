import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define stock tickers
stocks = ["TSLA", "PLTR"]

# Function to calculate RSI
def calculate_rsi(data, window=14):
    """
    Calculates the Relative Strength Index (RSI).
    :param data: DataFrame containing stock price data
    :param window: Look-back period for RSI calculation (default: 14)
    :return: RSI values
    """
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to calculate Moving Averages
def calculate_ma(data):
    """
    Calculates 50-day and 200-day moving averages.
    :param data: DataFrame containing stock price data
    :return: DataFrame with MA_50 and MA_200 columns
    """
    data["MA_50"] = data["Close"].rolling(window=50).mean()
    data["MA_200"] = data["Close"].rolling(window=200).mean()
    return data

# Function to calculate MACD and Signal Line
def calculate_macd(data):
    """
    Calculates MACD and Signal Line.
    :param data: DataFrame containing stock price data
    :return: DataFrame with MACD and Signal Line
    """
    short_ema = data["Close"].ewm(span=12, adjust=False).mean()
    long_ema = data["Close"].ewm(span=26, adjust=False).mean()
    data["MACD"] = short_ema - long_ema
    data["Signal_Line"] = data["MACD"].ewm(span=9, adjust=False).mean()
    return data

# Define the date range for fetching stock data
start_date = "2020-01-01"
end_date = "2025-01-01"

for stock in stocks:
    # Fetch historical stock data
    data = yf.download(stock, start=start_date, end=end_date)

    # Calculate RSI, MA, and MACD
    data["RSI"] = calculate_rsi(data)
    data = calculate_ma(data)
    data = calculate_macd(data)

    # Generate buy/sell signals
    # data["Buy_Signal"] = (data["RSI"] < 30) & (data["MA_50"] > data["MA_200"]) & (data["MACD"] > data["Signal_Line"])
    # data["Sell_Signal"] = (data["RSI"] > 70) & (data["MA_50"] < data["MA_200"]) & (data["MACD"] < data["Signal_Line"])
    # Buy Signal: Only RSI condition, MA condition or MACD condition, instead of all
    data["Buy_Signal"] = (data["RSI"] < 30) | (data["MA_50"] > data["MA_200"]) | (data["MACD"] > data["Signal_Line"])
    # Sell Signal: Similarly, use OR for each condition
    data["Sell_Signal"] = (data["RSI"] > 70) | (data["MA_50"] < data["MA_200"]) | (data["MACD"] < data["Signal_Line"])


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

print("✅ RSI + MA + MACD-based trading signals analysis completed!")
