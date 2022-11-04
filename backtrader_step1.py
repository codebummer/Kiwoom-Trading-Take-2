import pandas as pd
from datetime import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import yfinance


'''
To run this code without errors,
matplotlib should be the version 3.2.2,
and since "backtrader.feed.YahooFinanceData" does not work,
"backtrader.feed.PandasData" should be used with "yfinance" as an argument.
'''


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
        else:
            if self.rsi > 70:
                self.order = self.sell()

start = datetime(1990, 1, 1)
end = datetime(2022, 11, 4)

cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)
# data = bt.feeds.YahooFinanceData(dataname='005930.KS', fromdate=start, todate=end)
data = bt.feeds.PandasData(dataname=yfinance.download('005930.KS', start, end))
cerebro.adddata(data)
cerebro.broker.setcash(10_000_000)
cerebro.addsizer(bt.sizers.SizerFix, stake=30)

print(f'Initial Portfolio Value: {cerebro.broker.getvalue():,.0f}KRW')
cerebro.run()

print(f'Final Portfolio Value : {cerebro.broker.getvalue():,0.f}KRW')
cerebro.plot()
