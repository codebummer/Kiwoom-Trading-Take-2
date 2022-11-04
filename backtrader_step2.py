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
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=21)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f'BUY: Price {order.executed.price:,.0f}KRW, '
                    f'Bought {order.executed.size:,.0f} shares, '
                    f'Fees {order.executed.comm:,.0f}KRW, '
                    f'Current Value {cerebro.broker.getvalue():,.0f}KRW'
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(
                    f'SELL: Price {order.executed.price:,.0f}KRW, '
                    f'Sold {order.executed.size:,.0f} shares, '
                    f'fees {order.executed.comm:,.0f}KRW, '
                    f'Current Value {cerebro.broker.getvalue():,.0f}KRW'
                )
            self.bar_executed = len(self)
        elif order.status in [order.Canceled]:
            self.log('ORDER CANCELLED')
        elif order.status in [order.Margin]:
            self.log('ORDER MARGIN')
        elif order.status in [order.Rejected]:
            self.log('ORDER REJECTED')
        self.order = None

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
        else:
            if self.rsi > 70:
                self.order = self.sell()
    
    def log(self, text, dt=None):
        dt = self.datas[0].datetime.date(0)
        print(f'[{dt.isoformat()}] {text}')

start = datetime(2019, 1, 1)
end = datetime(2022, 11, 4)

cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)
# data = bt.feeds.YahooFinanceData(dataname='005930.KS', fromdate=start, todate=end)
data = bt.feeds.PandasData(dataname=yfinance.download('005930.KS', start, end))
cerebro.adddata(data)
cerebro.broker.setcash(30_000_000)
cerebro.broker.setcommission(commission=0.0014)
cerebro.addsizer(bt.sizers.PercentSizer, percents=90)

print(f'Initial Portfolio Value: {cerebro.broker.getvalue():,.0f}KRW')
cerebro.run()

print(f'Final Portfolio Value : {cerebro.broker.getvalue():,0.f}KRW')
cerebro.plot()
