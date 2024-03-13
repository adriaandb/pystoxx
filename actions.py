from time import time, ctime
from datetime import date
from datetime import timedelta

# import talib as ta
# import pandas as pd
# import pandas_datareader as web
# import yfinance as yf
# from yahoofinancials import YahooFinancials
from forex_python.converter import CurrencyRates
from email.message import EmailMessage
import ssl
import smtplib

import envs   # email variable


#(GLOBAL) VARIABLES
cr = CurrencyRates()
price_buy = 0.0
price_sell = 0.0
cash_permitted_buy = 0.0


global summary
summary = ''
global time_now


#CREATING DATE+TIME VARIABLES
today = date.today()
time_now = ctime(time())
print("Today's date:", today)
print('current time: '+ str(time_now))
if today.isoweekday() == 1:
    yesterday = today - timedelta(days = 3)
else:
    yesterday = today - timedelta(days = 1)
yesterday_db= today -timedelta(days = 2)







#EMAIL VARIABLES
email_sender = 'adriaan.debelder@gmail.com'
email_password = envs.EMAIL_PASS
email_receiver = 'adriaan.debelder@gmail.com'
subject = 'Pystoxx: percentage reached '
body = 'hier komt de info'

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
# em.set_content(body)

context = ssl.create_default_context()

def send_mail(body):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        em.set_content(body)
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())



#CLASSES
class Conversion:
    def __init__(self, cash):
        self.cash_in = cash

    def dollar_to_euro(self, cash):
        #rate = cr.get_rate('USD', 'EUR')
        rate = 0.93
        return cash * rate

    def euro_to_dollar(self, cash):
        #rate = cr.get_rate('EUR', 'USD')
        rate = 1.08
        return cash * rate



#ANALYZE + DECIDE TO BUY/SELL and return leftover cash
def analyze(stock, stock_amt, cash, cash_permitted_netto , buy_permission):
    stockId = stock.symbol
    time_now = ctime(time())
    # CREATING DATAFRAME
    #data = web.DataReader(stockId, data_source="stooq", start=yesterday)
    print(stockId+'  ('+str(stock_amt)+'x in wallet)')
    #print(data)
    advice = str(stock.get_analysis().summary["RECOMMENDATION"])
    print ('advice : ' + str(advice))
    value = get_stock_value(stock)
    print(stockId + " open price: " + str(value) + ' USD')
    global price_buy
    global price_sell
    global cash_available
    global buy_amt
    global sell_amt
    # price_buy = data.iloc[0]['Open']
    # price_sell = data.iloc[0]['Open']
    price_buy = value
    buy_amt = 1
    price_sell = value
    sell_amt = 1
    print(f'cash amount before transaction: {round(cash,2)}')
    if buy_permission == -1 and stock_amt > 0:
        cash_new = cash + price_sell
        sell(stock, sell_amt)
        stock_amt += -sell_amt
        log(f'\n transaction at {time_now}: sold {price_sell} \t worth of {stock.symbol} shares. \tleftover cash: {round(cash_new , 2 )}')
        print(f'cash amount after transaction: {round(cash_new , 2 )}')
        return cash_new, stock_amt

    if 'BUY' in advice:
        cash_permitted_buy = cash_permitted_netto - price_buy
        if  cash_permitted_buy > price_buy and buy_permission == 1:
            buy(stock, buy_amt)
            cash_new = cash - (price_buy * buy_amt)
            stock_amt += buy_amt
            log(f'\n  transaction at {time_now}: bought \t {price_buy} \t worth of \t {stock.symbol} shares. \tleftover cash: {round(cash_new , 2 )}')
            print(f'cash amount after transaction: {round(cash_new , 2 )}')
            return cash_new, stock_amt
        if buy_permission == 0:
            print('BUY WITHHELD\n\n')
            return cash, stock_amt
        else:
            return cash, stock_amt

    elif 'SELL' in advice and stock_amt>0 :
        cash_new = cash + (price_sell * sell_amt)
        sell(stock, sell_amt)
        stock_amt += -sell_amt
        log(f'\n  transaction at {time_now}: sold \t {price_sell} \t worth of \t {stock.symbol} shares. \tleftover cash: {round(cash_new , 2 )}')
        print(f'cash amount after transaction: {round(cash_new , 2 )}')
        return cash_new, stock_amt

    if stock_amt == 0:
        log(f'\n  transaction at {time_now}: None. \tleftover cash: {round(cash, 2)}')
        return  cash, stock_amt
        print('\n')


def buy(stock, amount):
    print(f'BUY TRIGGERED {amount} times')


def sell(stock, amount):
    print(f'SELL TRIGGERED {amount} times')


def get_stock_value(stock):
    stockId = stock.symbol
    # CREATING DATAFRAME
    #data = web.DataReader(stockId, data_source="stooq", start=yesterday)
    value = stock.get_analysis().indicators["open"]
    #value = data.iloc[0]['Open']
    # print('stock value '+stockId+': '+str(value)+' USD')
    return value

def get_summary(wallet):
    summary = f'TRADE PERCENTAGE REACHED of \'{wallet.name}\'\n'
    summary += f'amount of cash at start: {wallet.amt_start} USD\n'
    summary += f'percentage of cash made available for stock: {wallet.trade_percentage}%\n'
    summary += f'amount of cash in total: {round(wallet.amt_cash, 2 )} USD\n'
    summary += f'amount of stock in total: {round(wallet.stocks_value, 2 )} USD\n'
    for stock in wallet.stocks.values():
        stockname = stock['handler'].symbol
        stock_amount = stock['amount']
        total_value = round(stock_amount * stock['handler'].get_analysis().indicators["open"],2)
        summary_stock = f'stock: {stockname }, amount: {stock_amount} , total value: {total_value}\n'
        summary += summary_stock
    summary +=  f'amount of wallet in total: {round(wallet.amt_current , 2 )} USD'
    log(summary)
    return summary

#VEROUDERD
def get_stock_dataframe(stock):
    # yf.pdr_override()
    stockId = stock.symbol
    # my_data = yf.download(stockId, start='2024-01-15', end='2024-01-22', progress=False)
    # data = yf.download('TSLA', start='2021-12-17', end='2022-12-18', progress=False)
    data = web.DataReader(stockId, data_source="stooq", start=yesterday)

    # data = web.DataReader('TSLA', data_source="stooq", start=yesterday)

    return data

def log(message):
    f = open("transaction_log.txt", "a")
    f.write(message)
    f.close()