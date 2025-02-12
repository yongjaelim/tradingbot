# Tesla & Palantir Trading Bot

This automated trading bot is designed to provide actionable stock trading signals for **Tesla (TSLA)** and **Palantir (PLTR)** based on technical indicators like RSI, Moving Averages (MA), and MACD. Additionally, it leverages **real-time news sentiment analysis** to enhance decision-making and further optimize stock trading strategies.

## Project Objective

The primary objective of this bot is to maximize **investment returns** by utilizing an algorithmic trading system that combines both **technical indicators** and **market sentiment**. Specifically tailored for **Tesla** and **Palantir**, the bot aims to generate buy/sell signals that are aligned with market trends and news developments.

The long-term vision for this bot is not only to **maximize profitability** but also to foster wealth generation. Through continuous improvement, backtesting, and fine-tuning of strategies, the bot seeks to support its users in achieving substantial **financial growth**. By analyzing the **real-time news sentiment**, the bot stays ahead of market shifts and adapts to changing conditions, ensuring that every trade made contributes to **financial independence** and the pursuit of wealth accumulation.

Ultimately, the bot provides a dynamic approach to trading, continually evolving with the market and news, to make smarter decisions and minimize risk in the process of wealth creation.

## Features
- Collect stock data for **Tesla (TSLA)** and **Palantir (PLTR)** using the Yahoo Finance API.
- Generate buy/sell signals based on **RSI**, **Moving Averages (MA)**, and **MACD** indicators.
- Fetch and analyze the latest **Tesla** and **Palantir** news to evaluate sentiment using **NLTK** and **Transformers**.
- Send Telegram notifications for both buy/sell signals and news updates to keep the user informed.
  
## Requirements
- Python 3.x
- `yfinance` library
- `pandas` library
- `matplotlib` library
- `nltk` library
- `pyshorteners` library
- `feedparser` library
- `python-telegram-bot` library

## Setup and Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yongjaelim/tradingbot.git
    ```

2. Navigate to the project directory:
    ```bash
    cd trading-bot
    ```

3. Set up a **virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

5. Set up your **Telegram bot**:
   - Create a bot on [Telegram](https://core.telegram.org/bots#botfather) and get your bot token.
   - Add your **chat ID** for the bot to send messages.

6. Modify the bot token and chat ID in the `buy_sell_signal_bot.py` and `news_to_telegram.py` files.

## Usage

1. Run the trading signal bot:
    ```bash
    python buy_sell_signal_bot.py
    ```

2. Run the news and sentiment analysis bot:
    ```bash
    python news_to_telegram.py
    ```

3. The bot will send **buy/sell signals** and **news updates** to your **Telegram** account.

## Contributing

Feel free to fork the repository and make improvements or suggestions. Pull requests are welcome!

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Repository

GitHub Repository: [https://github.com/yongjaelim/tradingbot](https://github.com/yongjaelim/tradingbot.git)
