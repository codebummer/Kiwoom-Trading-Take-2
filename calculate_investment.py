import pandas as pd
from datetime import datetime

class InvestEval():
    def __init__(self, past_orders=pd.DataFrame([])):
        '''
        In case there are past trasanction records and you want to use and continue trading with them,
        pass on the past information in the form of an object when instantiating the object. 
        Required information is as follows:
        
        past_orders = an object pointer for the dataframe that holds the entire past records
          
        past_buyID = a unique counter or ID numbers recorded to identify buy orders held in the above past_orders dataframe.
 
        past_sellID = the same as above
        '''               
        self.orders = past_orders
        
        #The following if blocks determine whether there are any past records passed on and process accordingly.
        
        #When there are no past records passed on
        if self.orders.empty:
            #self.invested amount: totoal amount of investment so far
            #self.current_cash: total cash amount not invested yet
            #self.commission: total amount of fees and taxes for making transactions and profits thereof
            self.invested_amount, self.current_cash = 0, 0
            self.commission = 0.0014
            
            #Decided to use separate counter or identifier variables for buy orders and sell orders
            self.buyID = self.sellID = 0
        
        #When there are past records,  
        else:
            #But, when there are only 'BUY' orders made
            if 'OrderID' in self.orders.columns: #if 'OrderID' in self.order: also works    
                self.invested_amount = self.orders['InvestAmount'].values(-1)
                self.current_cash = self.orders['CurrentCash'].values(-1)
                self.commission = 0.0014
                
                # buy_rows = self.orders[self.orders['OrderType']=='BUY']
                # last_buy = buy_rows['OrderID'].values(-1)
                # self.buyID = last_buy
                # Those above three lines are equivalent to the below one line
                self.buyID = self.orders[self.orders['OrderType']=='BUY']['OrderID'].values(-1)   
                
                #When there are also 'SELL' orders made as well
                if 'SELL' in self.orders.values:
                    self.sellID = self.orders[self.orders['OrderType']=='SELL']['OrderID'].values(-1)

                
                #When there are no 'SELL' orders made. This block works with the above only 'BUY' block.
                elif 'SELL' not in self.orders.values:
                    pass
                
                    # The following part of code is not recommended to use. 
                    # However those are kept just to remind how my thought process flew
                    
                    # last_order_row = self.orders.loc[len(self.orders['OrderID'])-1]
                    # if last_order_row['OrderType'] == 'BUY':
                    #     self.buyID = last_buy
                    # self.buyID = self.orders['OrderID'].values(-1)                   
                    # self.sellID = self.orders['OrderID'].values(-1)  
                    

            #When there are no past records of orders made, but only investment having been set.
            if 'InvestAmount' in self.orders.columns: 
                # Do not use 'elif' here, because 'elif' here will make this 'elif or if' block part of the above 'if' block.
                # That makes pass' exit the entire 'if~elif' block including this one, when the immediately above 'elif' evaluates to True. 
                # To avoid exiting the entire block including this one by the above 'pass',
                # this 'if' block should be a separate block from the above big block of 'if'.
                self.invested_amount = self.orders['InvestAmount'].values(-1)
                self.current_cash = self.orders['CurrentCash'].values(-1)                   
                self.buyID, self.sellID = 0, 0
                
                self.commission = 0.0014
             

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
        rows = self._find_paired_order(order_ID)
        if len(rows) == 0:
            print('No order is made yet. Profits cannot be calculated.')
            return
        elif len(rows) == 1:
            print('A sell order is not made for the matching buy order yet. Profits cannot be calculated.')
            return
        
        buyrow, sellrow = rows[0], rows[1]
        profit_loss = self.orders.loc[sellrow, 'Price'] * self.orders.loc[sellrow, 'Shares'] / self.orders.loc[buyrow, 'Price'] * self.orders.loc[buyrow, 'Shares'] - 1
        self.orders.loc[[buyrow, sellrow], 'PL'] = [profit_loss]

    def _find_paired_order(self, order_ID):
        return self.orders[self.orders['OrderID'] == order_ID].index
        # rowID = self.orders['OrderID'].str.findall(order_ID) : This was the second choice of the above implementation  

invested = InvestEval()




#The following snippet of code is to understand and practice pandas dataframes by playing with them
#It has nothing to do with the main code itself. 
a = {'InvestAmount': [1000, 2000, 3000], 'CurrentCash': [100, 100, 300]}
test = pd.DataFrame(a)
for key, value in test.items():
    print(key, value)


'InvestAmount' in test
'InvestAmount' in test.columns
test[test['CurrentCash']==100]['CurrentCash'].values

invested.get_orders()
test_invest = InvestEval(test)
 
if True:
    print('a')
    if True:
        print('b')
        if False:
            print('c')
        elif True:
            pass
    if True:
        print('d')
print('e')
