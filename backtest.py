import backtrader as bt
import yfinance as yf
import matplotlib.pyplot as plt

# Define the trading strategy
class MyStrategy(bt.Strategy):
    def __init__(self):
        # Define technical indicators
        self.rsi = bt.indicators.RelativeStrengthIndex(period=14)
        self.ma50 = bt.indicators.SimpleMovingAverage(self.data.close, period=50)
        self.ma200 = bt.indicators.SimpleMovingAverage(self.data.close, period=200)
        self.macd = bt.indicators.MACD(self.data.close)
        self.signal = bt.indicators.MACD(self.data.close).signal

    def next(self):
        # Buy signal: RSI < 50, MA50 > MA200, MACD > Signal Line (Condition Relaxed)
        if self.rsi < 50 and self.ma50 > self.ma200 and self.macd > self.signal:  # Relaxed condition
            if not self.position:
                cash = self.broker.get_cash()  # Get available cash
                size = cash // self.data.close[0]  # Calculate the number of shares we can buy with available cash
                self.buy(size=size)
                self.buy_signal = True
                self.plot_buy_signal()  # Plot Buy Signal
                print(f"Buy signal at {self.data.datetime.date(0)} for {self.data._name} with size {size} at price {self.data.close[0]} (Amount: {size * self.data.close[0]:.2f})")

        # Sell signal: RSI > 60, MA50 < MA200, MACD < Signal Line (Condition Relaxed)
        elif self.rsi > 60 and self.ma50 < self.ma200 and self.macd < self.signal:
            if self.position:
                size = self.position.size  # Sell the entire position
                self.sell(size=size)
                self.sell_signal = True
                self.plot_sell_signal()  # Plot Sell Signal
                print(f"Sell signal at {self.data.datetime.date(0)} for {self.data._name} with size {size} at price {self.data.close[0]} (Amount: {size * self.data.close[0]:.2f})")

    def plot_buy_signal(self):
        plt.scatter(self.data.datetime.datetime(), self.data.close[0], marker="^", color="green", label="Buy Signal", alpha=1)

    def plot_sell_signal(self):
        plt.scatter(self.data.datetime.datetime(), self.data.close[0], marker="v", color="red", label="Sell Signal", alpha=1)

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                print(f"Buy order completed at {order.executed.price} for {self.data._name}, size {order.executed.size} (Amount: {order.executed.size * order.executed.price:.2f})")
            elif order.issell():
                print(f"Sell order completed at {order.executed.price} for {self.data._name}, size {order.executed.size} (Amount: {order.executed.size * order.executed.price:.2f})")

# Download stock data (Tesla and Palantir) with a sufficient date range (at least 200 days)
data_tesla = yf.download('TSLA', start='2018-01-01', end='2025-01-01')
data_palantir = yf.download('PLTR', start='2018-01-01', end='2025-01-01')

# Flatten the MultiIndex columns and use only relevant columns
data_tesla.columns = [col[0] if isinstance(col, tuple) else col for col in data_tesla.columns]
data_palantir.columns = [col[0] if isinstance(col, tuple) else col for col in data_palantir.columns]

# Use only the required columns
data_tesla = data_tesla[['Open', 'High', 'Low', 'Close', 'Volume']]
data_palantir = data_palantir[['Open', 'High', 'Low', 'Close', 'Volume']]

# Convert the data to Backtrader's PandasData format
bt_data_tesla = bt.feeds.PandasData(dataname=data_tesla)
bt_data_palantir = bt.feeds.PandasData(dataname=data_palantir)

# Create a Cerebro engine and add strategy
cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)

# Add data feeds to the engine
cerebro.adddata(bt_data_tesla, name='Tesla')  # Adding Tesla data
cerebro.adddata(bt_data_palantir, name='Palantir')  # Adding Palantir data

# Set initial cash
cerebro.broker.set_cash(10000)

# Set commission
cerebro.broker.setcommission(commission=0.001)

# Run the backtest
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Plot the result
cerebro.plot(style='candlestick')
