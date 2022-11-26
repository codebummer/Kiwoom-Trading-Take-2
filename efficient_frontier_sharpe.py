import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from datetime import datetime
import os, json
# from Investar import Analyzer

os.chdir(r'D:\myprojects\TradingDB')
with open('stocklist.json', 'r') as file:
    ticker_stock = json.load(file)

# returns the portfolio's ticker-stock pair dictionary
def stock_to_ticker(stocks):
    held = {}
    stocks = [stock.strip(' \'') for stock in stocks.split(',')]
    for stock in stocks:
        held[ticker_stock['stockkeys'][stock]] = stock
    return held

# returns the held stocks' {stockname1: close prices, stockname2, close prices...} dictionaries
def fetch_prices(held_dict):
    add = {}
    start = datetime(2019, 1, 1)
    end = datetime(2022, 11, 4)
    for ticker, stock in held_dict.items():
         add[stock] = (web.DataReader(ticker, 'naver', start, end)['Close'])
    return pd.DataFrame(add).astype('float64')

def montecarlo(held_prices):
    BIZDAYS_A_YEAR = 252
    daily_ret = held_prices.pct_change()
    annual_ret = daily_ret.mean() * BIZDAYS_A_YEAR
    daily_cov = daily_ret.cov()
    annual_cov = daily_cov * BIZDAYS_A_YEAR
    add = {'Returns':[], 'Risks':[], 'Weights':[], 'Sharpe':[]}
    MONTECARLO_REPEAT = 60_000
    for _ in range(MONTECARLO_REPEAT):
        weights = np.random.random(len(held_prices.columns)) #len(held_prices.columns) = held_prices.shape[1]
        weights /= np.sum(weights)
        
        returns = np.dot(weights, annual_ret)
        risks = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights))) #X.T produces X transpose
        
        add['Returns'].append(returns)
        add['Risks'].append(risks)
        add['Weights'].append(weights)
        add['Sharpe'].append(returns/risks)
    return add

def calculate_efficient_weights(stocks, possibilities):
    portfolio = {'Returns': possibilities['Returns'], 'Risks':possibilities['Risks'], 'Sharpe':possibilities['Sharpe']}
    for idx, stock in enumerate(stocks):
        portfolio[stock] = [weight[idx] for weight in possibilities['Weights']]
    return pd.DataFrame(portfolio)

def sharpe(data):
    max_sharpe = data.loc[data['Sharpe']==data['Sharpe'].max()]
    #sharpe = data[data['Sharpe']==data['Sharpe'].max()] -> This is same as above
    min_risks = data.loc[data['Risks']==data['Risks'].min()]
    return max_sharpe, min_risks

def visualize(portfolio, max_sharpe, min_risks):    
    portfolio.plot.scatter(x='Risks', y='Returns', c='Sharpe', cmap='viridis', 
        edgecolors='k', figsize=(11,7), grid=True)
    plt.scatter(x=max_sharpe['Risks'], y=max_sharpe['Returns'], c='r', marker='*', s=300, label='Maximum Sharpe')
    plt.scatter(x=min_risks['Risks'], y=min_risks['Returns'], c='r', marker='X', s=200, label='Minimum Risks')
    plt.title('Efficient Frontier / Portfolio Optimization')
    plt.xlabel('Risks')
    plt.ylabel('Expected Returns')
    plt.legend() #with "scatter(..., label='....')", plt.legend() will actually show label as a legend in display
    plt.show()

def make_portfolio(stocks):
    #portfolio: the portfolio's ticker-stock pair dictionary
    held = stock_to_ticker(stocks) 
    #held_prices: the held stocks' dataframe converted from
    #{stockname1: close prices, stockname2, close prices...} 
    held_prices = fetch_prices(held)
    #possibilities = {'Returns': [..], 'Risks': [...], 'Weights': [...]}
    possibilities = montecarlo(held_prices)
    #input stock names and possibilities(returns/risks/weights). 
    #returns the efficient frontier weight dataframe
    portfolio = calculate_efficient_weights(held.values(), possibilities)
    max_sharpe, min_risks = sharpe(portfolio)
    print('\n\nMaximun Sharpe Portfolio: \n', max_sharpe, '\n\nMinimum Risks Portfolio: \n', min_risks)
    # portfolio = portfolio[['Returns', 'Risks']+[stock for stock in held.values()]] -> duplicate. Don't use
    visualize(portfolio, max_sharpe, min_risks)

#input stock names as a one long string quoted by '' or "" and seperate each names with ,
make_portfolio('삼성전자, 현대차, LG전자, SK텔레콤, POSCO홀딩스, 신한지주, 하나금융지주')

