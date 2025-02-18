import backtrader as bt
import yfinance as yf
import matplotlib
matplotlib.use('TkAgg')  # Use a GUI backend that supports windowed plots
import matplotlib.pyplot as plt

# Define the trading strategy (applied per instrument)
class MyStrategy(bt.Strategy):
    def __init__(self):
        # Calculate technical indicators based on the data feed
        self.rsi = bt.indicators.RelativeStrengthIndex(self.data.close, period=14)
        self.ma50 = bt.indicators.SimpleMovingAverage(self.data.close, period=50)
        self.ma200 = bt.indicators.SimpleMovingAverage(self.data.close, period=200)
        self.macd = bt.indicators.MACD(self.data.close)
        self.signal = self.macd.signal

    def next(self):
        # Buy signal: RSI < 50 and (MA50 > MA200 or MACD > Signal)
        if (self.rsi[0] < 50) and ((self.ma50[0] > self.ma200[0]) or (self.macd[0] > self.signal[0])):
            if not self.getposition().size:
                cash = self.broker.get_cash()
                size = int(cash // self.data.close[0])
                if size > 0:
                    self.buy(size=size)
                    print(f"Buy signal at {self.data.datetime.date(0)} for {self.data._name}: size {size} at price {self.data.close[0]}")
        # Sell signal: RSI > 70 and (MA50 < MA200 or MACD < Signal)
        elif (self.rsi[0] > 70) and ((self.ma50[0] < self.ma200[0]) or (self.macd[0] < self.signal[0])):
            if self.getposition().size:
                size = self.getposition().size
                self.sell(size=size)
                print(f"Sell signal at {self.data.datetime.date(0)} for {self.data._name}: size {size} at price {self.data.close[0]}")

    def notify_order(self, order):
        # Print order execution details when an order is completed
        if order.status in [order.Completed]:
            if order.isbuy():
                print(f"Buy order executed at {order.executed.price} for {order.data._name}, size {order.executed.size}")
            elif order.issell():
                print(f"Sell order executed at {order.executed.price} for {order.data._name}, size {order.executed.size}")

def download_data(symbol, start, end):
    """
    Download and preprocess stock data using yfinance.
    """
    data = yf.download(symbol, start=start, end=end)
    # Flatten MultiIndex columns if necessary
    data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
    return data[['Open', 'High', 'Low', 'Close', 'Volume']]

def run_backtest(symbol, name, initial_cash=10000):
    """
    Run a backtest for a given symbol with the specified initial cash.
    Returns the figure handle, final portfolio value, and calculated return percentage.
    """
    # Download data for the symbol (from 2020 to 2025)
    data = download_data(symbol, start='2020-01-01', end='2025-01-01')
    bt_data = bt.feeds.PandasData(dataname=data)
    
    # Create a separate Cerebro instance for this instrument
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy)
    cerebro.adddata(bt_data, name=name)
    cerebro.broker.set_cash(initial_cash)
    cerebro.broker.setcommission(commission=0.001)
    
    print(f'\nStarting Portfolio Value for {name}: {cerebro.broker.getvalue():.2f}')
    cerebro.run()
    final_value = cerebro.broker.getvalue()
    print(f'Ending Portfolio Value for {name}: {final_value:.2f}')
    ret = ((final_value - initial_cash) / initial_cash) * 100
    print(f"Return for {name}: {ret:.2f}%")
    
    # Get non-blocking plot
    figs = cerebro.plot(style='candlestick', block=False)
    # cerebro.plot() returns a nested list: [[fig1, ...]]
    # We'll assume the first figure is what we need.
    return figs[0][0], final_value, ret

def main():
    # Run backtests for Tesla and Palantir separately
    fig_tesla, final_tesla, ret_tesla = run_backtest('TSLA', 'Tesla', initial_cash=10000)
    fig_palantir, final_palantir, ret_palantir = run_backtest('PLTR', 'Palantir', initial_cash=10000)
    
    # Create a new figure with 2 subplots to combine both plots
    combined_fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Extract and copy plot data from Tesla's figure
    try:
        tesla_ax = fig_tesla.axes[0]
        for line in tesla_ax.get_lines():
            ax1.plot(line.get_xdata(), line.get_ydata(), label=line.get_label())
        ax1.set_title(f"Tesla Backtest (Return: {ret_tesla:.2f}%)")
        ax1.legend()
    except Exception as e:
        print("Error processing Tesla plot:", e)
    
    # Extract and copy plot data from Palantir's figure
    try:
        palantir_ax = fig_palantir.axes[0]
        for line in palantir_ax.get_lines():
            ax2.plot(line.get_xdata(), line.get_ydata(), label=line.get_label())
        ax2.set_title(f"Palantir Backtest (Return: {ret_palantir:.2f}%)")
        ax2.legend()
    except Exception as e:
        print("Error processing Palantir plot:", e)
    
    plt.tight_layout()
    plt.show(block=True)

if __name__ == '__main__':
    main()
