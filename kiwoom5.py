import backtrader as bt
import os.path
import sys
import datetime

cerebro = bt.Cerebro()

# Datas are in a subfolder of the samples. Need to find where the script is
# because it could have been called from anywhere
modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
datapath = os.path.join(modpath, '../../datas/orcl-1995-2014.txt')

# Create a Data Feed
data = bt.feeds.YahooFinanceCSVData(
    dataname=datapath,
    # Do not pass values before this date
    fromdate=datetime.datetime(2000, 1, 1),
    # Do not pass values after this date
    todate=datetime.datetime(2021, 12, 31),
    reverse=False)

# datapath = 'D:/myProjects/bt_data.txt'
# data = bt.feeds.YahooFinanceCSVData(
#     dataname = datapath,
#     fromdate = datetime.datetime(2000, 1, 1),
#     todate = datetime.datetime(2000, 12, 31),
#     reverse = False
# )

# cerebro.adddata(data)
cerebro.broker.setcash(10000000)
print('Starting Portfolio Value: {:,.2f}'.format(cerebro.broker.getvalue()))
cerebro.run()
print('Final Portfolio Value: {:,.2f}'.format(cerebro.broker.getvalue()))
