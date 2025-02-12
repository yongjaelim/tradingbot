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

# Define the date range for fetching stock data
start_date = "2020-01-01"
end_date = "2025-01-01"

for stock in stocks:
    # Fetch historical stock data
    data = yf.download(stock, start=start_date, end=end_date)

    # Calculate RSI and add it to the DataFrame
    data["RSI"] = calculate_rsi(data)

    # Plot stock price and RSI
    plt.figure(figsize=(10, 5))

    # Plot Closing Price
    plt.subplot(2, 1, 1)
    plt.plot(data.index, data["Close"], label="Close Price", color="blue")
    plt.title(f"{stock} Price & RSI")
    plt.legend()

    # Plot RSI Indicator
    plt.subplot(2, 1, 2)
    plt.plot(data.index, data["RSI"], label="RSI", color="red")
    plt.axhline(70, linestyle="--", color="gray")  # Overbought threshold
    plt.axhline(30, linestyle="--", color="gray")  # Oversold threshold
    plt.legend()

    # Save the RSI chart
    plt.savefig(f"{stock}_RSI.png")
    print(f"{stock} RSI analysis completed! Chart saved.")

print("✅ RSI analysis completed!")