import yfinance as yf
import pandas as pd

# Set stock tickers to analyze
stocks = ["TSLA", "PLTR"]

# Set time period
start_date = "2022-01-01"
end_date = "2024-01-01"

# Fetch each stock data
for stock in stocks:
    data = yf.download(stock, start=start_date, end=end_date)
    data.to_csv(f"{stock}_data.csv")  # save as csv file
    print(f"{stock} Data saved!")

print("Downloaded all stocks data!")