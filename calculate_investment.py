import pandas as pd
from datetime import datetime

class InvestEval():
    def __init__(self, past_orders=pd.DataFrame([])):
        '''
        In case there are past trasanction records and you want to continue with them for the investment you begin,
        pass on past information when instantiating the object. Required information is as follows:
        
        past_orders = an object pointer for the dataframe that holds the entire past records
          
        past_buyID = a unique counter or ID numbers recorded to identify buy orders held in the above past_orders dataframe.
 
        past_sellID = the same as above
        '''
        self.orders = past_orders
        if self.orders.empty:
            self.buyID, self.sellID, self.invested_amount, self.current_cash = 0, 0, 0, 0
            self.commission = 0.0014
        else:
            if 'OrderID' in self.orders.columns: #if 'OrderID' in self.order: also works    
                self.commission = 0.0014                    
                self.buyID = self.orders['OrderID'].values(-1)
                self.sellID = self.orders['OrderID'].values(-1)       
                self.invested_amount = self.orders['InvestAmount'].values(-1)
                self.current_cash = self.orders['CurrentCash'].values(-1)

            elif 'InvestAmount' in self.orders.columns:
                self.buyID, self.sellID = 0, 0
                self.commission = 0.0014
                self.invested_amount = self.orders['InvestAmount'].values(-1)
                self.current_cash = self.orders['CurrentCash'].values(-1)                

    def get_orders(self):
        return self.orders       
    
    def setcash(self, cash):
        self.invested_amount += cash
        self.current_cash += cash
        self.orders['InvestAmount'] = [self.invested_amount]
        self.orders['CurrentCash'] = [self.current_cash]

    def _log_current_cash(self, order, price, shares):
        if order == 'BUY':
            self.current_cash -= price * shares
            self.orders['CurrentCash'] = [self.current_cash]
        elif order == 'SELL':
            self.current_cash += price * shares
            self.orders['CurrentCash'] = [self.current_cash]

        self.orders['InvestAmount'] = [self.invested_amount]

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
    
    def setcomm(self, comm=0.0014):
        self.commission = comm

    def make_order(self, order, price, shares):
        if order == 'BUY' and self.current_cash < price*shares*1.05: #1.05 is multiplied for paying fees and taxes
            print('Cash in insufficient to make the order')
            return #you can use the return statement without any parameter to exit a function

        self._log_orders(order, price, shares, datetime.today())
        self._log_current_cash(order, price, shares)

        if order == 'SELL':
            self._calc_profit(self.orders['OrderID'].values(-1))


    def _log_orders(self, order, price, shares, time):       
        self._order_tracker(order)
        if order == 'BUY':
            self.orders['OrderType'] = ['BUY']
        if order == 'SELL':
            self.orders['OrderType'] = ['SELL']
        self.orders['Time', 'Price', 'Shares'] = [time, price, shares]     
     
    def _order_tracker(self, order):
        if order == 'BUY':
            self.buyID += 1
            self.orders['OrderID'] = [self.buyID]

        if order == 'SELL':            
            self.sellID += 1
            self.orders['OrderID'] = [self.sellID]
             
    def _calc_profit(self, order_ID):
        if len(self.orders) == 0:
            print('Only the first order is made. Profits cannot be calculated yet.')
            return
        
        buyrow, sellrow = self._find_paired_order(order_ID)
        profit_loss = self.orders.loc[sellrow, 'Price'] * self.orders.loc[sellrow, 'Shares'] / self.orders.loc[buyrow, 'Price'] * self.orders.loc[buyrow, 'Shares'] - 1
        self.orders.loc[[buyrow, sellrow], 'PL'] = [profit_loss]

    def _find_paired_order(self, order_ID):
        return self.orders[self.orders['OrderID'] == order_ID].index
        # rowID = self.orders['OrderID'].str.findall(order_ID) : This was the second choice of the above implementation  

invested = InvestEval()


a = {'InvestAmount': 1000, 'CurrentCash': 1000}
test = pd.DataFrame([])
for key, value in a.items():
    print(key, value)
    test[key] = [value]

'InvestAmount' in test
'InvestAmount' in test.columns

invested.get_orders()
test_invest = InvestEval(test)
