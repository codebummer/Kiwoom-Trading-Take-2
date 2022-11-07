import pandas as pd
from datetime import datetime

class InvestEval():
    def __init__(self):
        self.orders = pd.DataFrame([])
        self.buyID, self.sellID = [], [] 
        self.invested_amount, self.current_cash = 0, 0        
    
    def setcash(self, cash):
        self.invested_amount += cash
        self.current_cash += cash
        self.orders['CurrentCash'] = self.current_cash
        #Do other columns than CurrentCash have to be filled when extra cash is added without an order
        #to make the dataframe work without an error?

    def _log_current_cash(self, order, price, shares):
        if order == 'BUY':
            self.current_cash -= price * shares
            self.orders['CurrentCash'] = self.current_cash
        elif order == 'SELL':
            self.current_cash += price * shares
            self.orders['CurrentCash'] = self.current_cash

        # if order == 'CASHIN':
        #     self.orders['CurrentCash'] = cash
        # elif order == 'BUY':
        #     self.current_cash -= self.orders['Price'].values(-1) * self.orders['Shares'].values(-1)
        #     self.orders['CurrentCash'] = self.current_cash
        # elif order == 'SELL':
        #     self.current_cash += self.orders['Price'].values(-1) * self.orders['Shares'].values(-1)
        #     self.orders['CurrentCash'] = self.current_cash
        '''
        When a new value is added to a dataframe, it can be indexed like 
        orders['Price'] = 1000
        However, when a currently existing value, especially the most recent one, is indexed, it should be located like 
        order['Price'].values(-1)
        because the first form gives the entire column when you need one value from that column.
        When you use the second form, it will give you a Numpy array 
        which can be individually indexed with parentheses().
        '''
    
    def setcomm(self, comm):
        self.commission = comm

    def make_order(self, order, price, shares):
        if order == 'BUY' and self.current_cash < price*shares*1.05: #1.05 is multiplied for paying fees and taxes
            print('Cash in insufficient to make the order')
            return

        self._log_orders(order, price, shares, datetime.today())
        self._log_current_cash(order, price, shares)

        if order == 'SELL':
            self._calc_profit(self.orders['OrderID'])
    

    def _log_orders(self, order, price, shares, time):
        self.orders['Time'] = time
        self._order_tracker(order)
        if order == 'BUY':
            self.orders['OrderType'] = 'BUY'
        if order == 'SELL':
            self.orders['OrderType'] = 'SELL'
        self.orders['Price'] = price
        self.orders['Shares'] = shares
              
        
    def _order_tracker(self, order):
        if order == 'BUY':
            self.buyID += 1
            self.orders['OrderID'] = self.buyID

        if order == 'SELL':            
            self.sellID += 1
            self.orders['OrderID'] = self.sellID
             
    def _calc_profit(self, order_ID):
        if len(self.orders) == 0:
            print('Only the first order is made. Profits cannot be calculated yet.')
            return
        
        buyrow, sellrow = self._find_paired_order(order_ID)
        profit_loss = self.orders.loc[sellrow, 'Price'] * self.orders.loc[sellrow, 'Shares'] / self.orders.loc[buyrow, 'Price'] * self.orders.loc[buyrow, 'Shares'] - 1
        self.orders.loc[[buyrow, sellrow], 'PL'] = profit_loss

    def _find_paired_order(self, order_ID):
        return self.orders[self.orders['OrderID'] == order_ID].index
        # rowID = self.orders['OrderID'].str.findall(order_ID) : This was the second choice of the above implementation  

invested = InvestEval()
