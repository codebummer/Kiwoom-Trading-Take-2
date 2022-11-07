
class InvestEval():
    def __init__(self):
        self.orders = pd.DataFrame([])
        self.buyID, self.sellID = [], []            
    
    def setcash(self, amount):
        self.invested_amount = amount
    
    def setcomm(self, comm):
        self.commission = comm
        
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
    
    def make_order(self, order, price, shares):
        self._log_orders(order, price, shares, datetime.today())
        if order == 'SELL':
            self.calc_profit(self.orders['OrderID'])
    
    def _find_order(self, order_ID):
        buyrow, sellrow = self.orders[self.orders['OrderID'] == order_ID].index
        return self.orders.loc[buyrow, '']
    
    
    
        # rowID = self.orders['OrderID'].str.findall(order_ID)
        for row in rowID:
            if self.orders.loc[row, 'OrderType'] == 'BUY':
                buyprice = self.orders.loc[row, 'Price']
                buyshares = self.orders.loc[row, 'Shares']
                buyamount = buyprice * buyshares
            elif self.orders.loc[row, 'OrderType'] == 'SELL':
                sellprice = self.orders.loc[row, 'Price']
                sellshares = self.orders.loc[row, 'Shares']
                sellamount = sellprice * sellshares       


            
    def calc_profit(self, order_ID):
        if len(self.orders) == 0:
            print('Only the first order is made. Profits cannot be calculated yet.')
            return
        
        rowID = self.orders['OrderID'].str.findall(order_ID)
        for row in rowID:
            if self.orders.loc[row, 'OrderType'] == 'BUY':
                buyprice = self.orders.loc[row, 'Price']
                buyshares = self.orders.loc[row, 'Shares']
                buyamount = buyprice * buyshares
            elif self.orders.loc[row, 'OrderType'] == 'SELL':
                sellprice = self.orders.loc[row, 'Price']
                sellshares = self.orders.loc[row, 'Shares']
                sellamount = sellprice * sellshares
        
        profit_loss = sellamount / buyamount - 1
        self.orders.loc[[row[0], row[1]], 'PL'] = profit_loss

invested = InvestEval()
