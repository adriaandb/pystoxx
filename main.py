from threading import Thread
# import talib as ta
# import datetime as dt
# from datetime import date
import time
# from time import ctime
from datetime import date
# import numpy as np
# import matplotlib.pyplot as pltf
# import pandas_datareader as web
# from tradingview_ta import TA_Handler, Exchange, Interval

import stockpool as sp
from wallet import Wallet
# import wallet
# from actions import analyze
import actions
import controller

# DONE
# schrijf een programma dat op bepaalde tijden de stockwaarden ophaalt en simuleer aankoop en verkoop van stock in een gesimuleerde portefeuille
# kopen of verkopen volgens de suggestie van TAhandler
# maak log van aan/verkopen
# rapporting function die mail stuurt wanneer je moet (ver)kopen
# trade percentage: aankoop niet doen als trade percentage gaat overschreden worden, niet enkel naar huidige situatie kijken
# set to sell stock if trade percentage is lower than current amount
# gebruik van threads
# installeer programma op rpi en laat nonstop draaien als backgroundprocess via threading, access via vnc/ssh/webbrowser

# TO DO
# transactie/analyse doen gebeuren op bepaald tijdstip
# buy stock for permitted cash all at once (weighting key?) or once at a time until permitted cash runs out -> analyse and buy/sell have to be splitted
# portefeuilles desbetreffende stock info laten opslaan in pandas dataframe en plots te genereren met matplotlib
# aparte microservice die plots op website zet?
# add and remove stock to/from wallet
# bekijk ETF's en grondstoffen
# gebruik de MACD: verkopen boven 0.7 / kopen als onder 0.3(?)
# kosten van transactie in rekening brengen
# max aantal transacties per periode in te stellen
# cash bij in portefeuille steken of eruit halen
# verschillende portefeuilles die verschillende strategieen weergeven, en te vergelijken
# verschillende portefeuilles die verschillende samenstelling weergeven, en te vergelijken
# aparte thread met functie die wallets vergelijkt
# hookers and champagne


# https://tvdb.brianthe.dev/
# telenet : 81.83.208.32 - 240123
# C:\Users\gebruiker\PycharmProjects\pystoxx\venv\Scripts\activate
# C:\Users\gebruiker\PycharmProjects\pystoxx\venv\main.py


# DEPLOYMENT
# scp file.txt remote_username@10.10.0.2:/remote/directory
# scp C:\Users\gebruiker\PycharmProjects\pystoxx\main.py pi@192.168.0.233:~/pystoxx_dir
# https://paulorod7.com/running-a-python-script-in-terminal-without-losing-it-by-a-connection-drop     https://linuxize.com/post/how-to-use-linux-screen/

# rpi:
# To activate this environment, use
#    $ conda activate env_pystoxx
# To deactivate an active environment, use
#    $ conda deactivate
# create a screen session:
#    $ screen -S session_name
# detach from running session:
#    $ Ctrl+a d
# resume session:
#    $ screen -r






# user defined variables

initial_cash_amount = 9300  # in EUR
global trade_percentage
trade_percentage = 20  # % available for trading
global cash_permitted_bruto
global cash_permitted_netto
conversion = actions.Conversion(initial_cash_amount)
cash_permitted_bruto = conversion.euro_to_dollar(initial_cash_amount) * (trade_percentage / 100)
analyze_frequency = 10   # amount of seconds
email_activation = 0  # 0 or 1

today = date.today()

global buy_permission
buy_permission = 1  # 0: withhold buy, 1: buy permission granted, -1: force sell

global bAlive
bAlive = True

global cycle
cycle = 0

global time_now
time_now = time.ctime()


if buy_permission == 0:
    buy_str = 'OFF'
else:
    buy_str = 'ON'
if email_activation == 0:
    email_str = 'OFF'
else:
    email_str = 'ON'
actions.log(
    f'-------------------\n \t APPLICATION STARTED AT {time_now} \n \t\tbuy permission = {buy_str} , email activation = {email_str} ')

# current_time = ctime(time())

# CREATE WALLET INSTANCE
wallet_tech = Wallet("wallet tech", initial_cash_amount, sp.stockpool_tech)
wallet_tech.trade_percentage = trade_percentage


# trigger analyze and buy/sell
# analyse en kopen te ontkoppelen, stuur signal variabele mee
# mogelijkheid trade percentage als kleiner in te stellen
# als totaal stockvalue kleiner is dan toegestaan budget moet er bijgekocht worden tot de het budget opgebruikt is. er mag ook verkocht worden
# als totaal stockvalue groter is dan toegestaan budget mag er niet bijgekocht worden tot totaal stockvalue weer onder budget ligt. er mag tijdelijk enkel verkocht worden
# aan te geven door buy_permission toggle
# maar hoe loops opbouwen? en hoe tegen te gaan dat er rond de budgetlimiet telkens gekocht/verkocht wordt (door break en vraagstelling trade_percentage)

def run_analysis(wallet):
    global summary
    global buy_permission
    global cash_permitted_bruto
    global cash_permitted_netto
    # global trade_percentage
    global cycle
    global time_now

    # get permitted cash amounts to see if stock should be bought or sold
    wallet.stocks_value = wallet.update_stocks_value()
    cash_permitted_bruto = wallet.get_cash_permitted_bruto()
    cash_permitted_netto = wallet.get_cash_permitted_netto()
    if wallet.stocks_value < cash_permitted_bruto:
        print(f'-\n=\nGOING UP\n=\n-')
        while wallet.stocks_value < cash_permitted_bruto :
            cash_permitted_bruto = round(wallet.get_cash_permitted_bruto(), 2)
            time_now = time.ctime(time.time())
            cycle+=1
            cash_permitted_netto = round(wallet.get_cash_permitted_netto(), 2 )
            print(f'\n{cycle}---------------------------{time_now}')
            # print(f'{cash_permitted_netto=} with trade percentage {wallet.trade_percentage}%')
            # print(f'{round(wallet.stocks_value, 2)} of {cash_permitted_bruto} converted to stock.\n')
            # make analysis for each stock in wallet
            for stock in wallet.stocks.values():
                cash_new, stock_amt = actions.analyze(stock['handler'], stock['amount'],
                                              wallet.amt_cash,
                                              cash_permitted_netto,
                                              buy_permission)
                wallet.amt_cash = cash_new
                stock['amount'] = stock_amt
                wallet.update_stocks_value()
                print('--------------\n')
            cash_permitted_bruto = round(wallet.get_cash_permitted_bruto(), 2)
            cash_permitted_netto = round(wallet.get_cash_permitted_netto(), 2 )
            # print(f'{cash_permitted_netto=} with trade percentage {wallet.trade_percentage}%')
            # print(f'{round(wallet.stocks_value, 2)} of {cash_permitted_bruto} converted to stock.\n')
            time.sleep(analyze_frequency)
    # actions.log(f'\ntransactions stopped due to reach of given trade percentage ({trade_percentage}%)\n')
    # trade_percentage = get_summary_permission(wallet, trade_percentage)
    actions.get_summary(wallet)

    # TO SELL IF TOO MUCH CASH IS SPENT
    cash_permitted_bruto = get_cash_permitted_bruto(wallet)
    wallet.stocks_value = wallet.update_stocks_value()
    if wallet.stocks_value  > cash_permitted_bruto:
        buy_permission = -1
        print(f'-\n=\nGOING DOWN\n=\n-')
        while wallet.stocks_value  > cash_permitted_bruto :
            cycle+=1
            print(f'\n{cycle}----------------------------{time_now}')
            for stock in wallet.stocks.values():
                cash_new, stock_amt = actions.analyze(stock['handler'], stock['amount'],
                                              wallet.amt_cash,
                                              cash_permitted_netto,
                                              buy_permission)
                wallet.amt_cash = cash_new
                stock['amount'] = stock_amt
                wallet.update_stocks_value()
                print('--------------\n')
                if wallet.stocks_value  < cash_permitted_bruto:
                    buy_permission = 1
                    break
            time.sleep(analyze_frequency)
        # actions.log(f'\ntransactions stopped due to reach of given trade percentage ({trade_percentage}%)\n')
        # trade_percentage = get_summary_permission(wallet, trade_percentage)
        actions.get_summary(wallet)


    # # update current total stock value
    # wallet_tech.stocks_value = wallet_tech.update_stocks_value()

    # # print summary
    # summary = actions.get_summary(wallet_tech, trade_percentage)
    # print(summary)

    # actions.log(f'\ntransactions stopped due to reach of given trade percentage ({trade_percentage}%)\n')



#amount of cash left over to be spent
def get_cash_permitted_netto(wallet):
    # cash_permitted = wallet.amt_current * (wallet.trade_percentage / 100) - wallet.stocks_value
    # if cash_permitted > 0:
    #     return cash_permitted
    # else:
    #     return 0
    return wallet.get_cash_permitted_netto()


# total amount of cash allowed to be spent
def get_cash_permitted_bruto(wallet):
    # cash_permitted = wallet.amt_current * (wallet.trade_percentage / 100)
    # return cash_permitted
    return wallet.get_cash_permitted_bruto()

def get_summary_permission(wallet):
    wallet.stocks_value = wallet.update_stocks_value()
    summary = actions.get_summary(wallet)
    print(summary)
    if email_activation == 1:
        actions.send_mail(summary)
        actions.log(f'\nEMAIL SENT  at {time.time()}\n\n')
    trade_percentage = float(
        input(f'\ncurrent trade percentage: {wallet.trade_percentage} \ndefine new trade percentage to adhere to trading: '))
    # cash_permitted = get_cash_permitted(wallet, trade_percentage)
    return trade_percentage




def main():
    # global buy_permission
    while bAlive == True:
        # global trade_percentage
        run_analysis(wallet_tech)

def start_controller(wallet):
    controller.run_gui(wallet)
    # show wallet / show stock amount and worth / show start amount vs current amount(=profit)
    # show last transaction?
    # show graph

thread_main = Thread(name='main' , target=main)
thread_controller = Thread(name='controller', target=start_controller, args=(wallet_tech,))


if __name__ == "__main__":
    # main()
    # start_controller(wallet_tech)
    thread_main.start()
    thread_controller.start()
    # thread_main.join(timeout=1.0)
    # thread_controller.join()
