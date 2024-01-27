import stockpool
import talib as ta
import datetime as dt
from datetime import date
# from time import sleep, ctime
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web
from tradingview_ta import TA_Handler, Exchange, Interval

import stockpool as sp
from wallet import Wallet
from actions import analyze

#schrijf een programma dat op bepaalde tijden de stockwaarden ophaalt en simuleer aankoop en verkoop van stock in een gesimuleerde portefeuille
#gebruik de MACD: verkopen boven 0.7 / kopen als onder 0.3(?) OF de suggestie van TAhandler
#bekijk ETF's
#portefeuille (=class) starten met beginbudget, kosten van transactie niet vergeten, max aantal transacties per periode in te stellen
#verschillende portefeuilles die verschillende strategieen weergeven, en te vergelijken
#verschillende portefeuilles die verschillende samenstelling weergeven, en te vergelijken
#portefeuilles desbetreffende stock info laten opslaan in pandas dataframe
#maak log van aan/verkopen
#installeer programma op rpi en laat nonstop draaien, access via vnc/ssh/webbrowser
#aparte thread met functie die wallets vergelijkt
#rapporting function die mail stuurt wanneer je moet (ver)kopen
#hookers and champagne

#https://tvdb.brianthe.dev/
# telenet : 81.83.208.32 - 240123

initial_cash_amount = 5000


cash_percentage = 20 #available for trading

analyze_frequency = 5 #amount of seconds
buy_permission = 1   #0 or 1

global cycle
cycle = ' '

# current_time = ctime(time())



def main():

    #today = date.today()
    #print("Today's date:", today)

    wallet_tech=Wallet("wallet tech", initial_cash_amount, sp.stockpool_tech)

    print(wallet_tech)


#trigger analyze and buy/sell
    #analyse en kopen te ontkoppelen, stuur signal variabele mee
    while wallet_tech.amt_cash > initial_cash_amount*(1-cash_percentage/100):
        time.sleep(analyze_frequency)
        print('\n------------------------------------------')
        for stock in wallet_tech.stocks.values():
            # print(current_time)
            cash_new, stock_amt = analyze(stock['handler'], stock['amount'], wallet_tech.amt_cash , cash_percentage , buy_permission )
            wallet_tech.amt_cash = cash_new
            stock['amount'] = stock_amt
            print('--------------\n')

    wallet_tech.stocks_value = wallet_tech.calculate_stocks_worth()

    print(f'amount of cash at start: {wallet_tech.amt_start} USD')
    print(f'amount of cash in total: {wallet_tech.amt_cash} USD')
    print(f'amount of stock in total: {wallet_tech.stocks_value} USD')
    print(f'amount of wallet in total: {wallet_tech.amt_current} USD')

    # print (wallet_tech.stocks)



if __name__ == "__main__":
    main()