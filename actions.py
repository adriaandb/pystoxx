from time import time, ctime
from datetime import date
from datetime import timedelta

import talib as ta
import pandas as pd
import pandas_datareader as web
import yfinance as yf
# from yahoofinancials import YahooFinancials
from forex_python.converter import CurrencyRates

import stockpool as sp


#GLOBAL VARIABLES
cr = CurrencyRates()

#CREATING DATE+TIME VARIABLES
today = date.today()
time = ctime(time())
print("Today's date:", today)
print('current time: '+ str(time))
if today.isoweekday() == 1:
    yesterday = today - timedelta(days = 3)
else:
    yesterday = today - timedelta(days = 1)
yesterday_db= today -timedelta(days = 2)

price_buy = 0.0
price_sell = 0.0


#CLASSES
class Conversion:
    def __init__(self, cash):
        self.cash_in = cash

    def dollar_to_euro(self, cash):
        rate = cr.get_rate('USD', 'EUR')
        return cash * rate

    def euro_to_dollar(self, cash):
        rate = cr.get_rate('EUR', 'USD')
        return cash * rate







#ANALYZE + DECIDE TO BUY/SELL and return leftover cash
def analyze(stock, stock_amt, cash, cash_percentage , buy_permission):
    stockId = stock.symbol
    # CREATING DATAFRAME
    data = web.DataReader(stockId, data_source="stooq", start=yesterday)
    print(stockId+'  ('+str(stock_amt)+'x in wallet)')
    print(data)
    advice = str(stock.get_analysis().summary["RECOMMENDATION"])
    print ('advice : ' + str(advice))
    global price_buy
    global price_sell
    price_buy = data.iloc[0]['Open']
    price_sell = data.iloc[0]['Open']
    print(f'cash amount before transaction: {cash}')

    if 'BUY' in advice:
        cash_available = cash * (cash_percentage/100)
        if  cash_available > price_buy and buy_permission == 1:
            buy(stock)
            cash_new = cash - price_buy
            stock_amt+=1
            f = open("transaction_log.txt", "a")
            f.write(f'\ntransaction at {time}: bought {price_buy} worth of {stock.symbol} shares. leftover cash: {cash_new}')
            f.close()
            print(f'cash amount after transaction: {cash_new}')
            return cash_new, stock_amt
        if buy_permission == 0:
            print('BUY WITHHELD\n\n')
            return cash, stock_amt
        else:
            return cash, stock_amt

    elif 'SELL' in advice and stock_amt>0:
        cash_new = cash + price_sell
        sell(stock)
        stock_amt+=-1
        f = open("transaction_log.txt", "a")
        f.write(f'\ntransaction at {time}: sold {price_sell} worth of {stock.symbol} shares. leftover cash: {cash_new}')
        f.close()
        print(f'cash amount after transaction: {cash_new}')
        return cash_new, stock_amt
    if stock_amt == 0:
        return  cash, stock_amt
        print('\n')

def buy(stock):
    print("BUY TRIGGERED")


def sell(stock):
    print("SELL TRIGGERED")


def get_stock_value(stock):
    stockId = stock.symbol
    # CREATING DATAFRAME
    data = web.DataReader(stockId, data_source="stooq", start=yesterday)
    value = data.iloc[0]['Open']
    # print('stock value '+stockId+': '+str(value)+' USD')
    return value


def get_stock_dataframe(stock):
    # yf.pdr_override()
    stockId = stock.symbol
    # my_data = yf.download(stockId, start='2024-01-15', end='2024-01-22', progress=False)
    # data = yf.download('TSLA', start='2021-12-17', end='2022-12-18', progress=False)
    data = web.DataReader(stockId, data_source="stooq", start=yesterday)

    # data = web.DataReader('TSLA', data_source="stooq", start=yesterday)

    return data

