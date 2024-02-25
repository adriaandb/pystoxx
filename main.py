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


# DONE
# schrijf een programma dat op bepaalde tijden de stockwaarden ophaalt en simuleer aankoop en verkoop van stock in een gesimuleerde portefeuille
# kopen of verkopen volgens de suggestie van TAhandler
# maak log van aan/verkopen
# rapporting function die mail stuurt wanneer je moet (ver)kopen
# cash percentage: aankoop niet doen als cash percentage gaat overschreden worden, niet enkel naar huidige situatie kijken
# set to sell stock if cash percentage is lower than current amount
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
global cash_percentage
cash_percentage = 20  # % available for trading
global cash_permitted_bruto
global cash_permitted_netto
conversion = actions.Conversion(initial_cash_amount)
cash_permitted_bruto = conversion.euro_to_dollar(initial_cash_amount) * (cash_percentage / 100)
analyze_frequency = 5  # amount of seconds
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


# trigger analyze and buy/sell
# analyse en kopen te ontkoppelen, stuur signal variabele mee
# mogelijkheid cash percentage als kleiner in te stellen
# als totaal stockvalue kleiner is dan toegestaan budget moet er bijgekocht worden tot de het budget opgebruikt is. er mag ook verkocht worden
# als totaal stockvalue groter is dan toegestaan budget mag er niet bijgekocht worden tot totaal stockvalue weer onder budget ligt. er mag tijdelijk enkel verkocht worden
# aan te geven door buy_permission toggle
# maar hoe loops opbouwen? en hoe tegen te gaan dat er rond de budgetlimiet telkens gekocht/verkocht wordt (door break en vraagstelling cash_percentage)
def run_analysis(wallet):
    global summary
    global buy_permission
    global cash_permitted_bruto
    global cash_permitted_netto
    global cash_percentage
    global cycle
    global time_now

    wallet.stocks_value = wallet.calculate_stocks_value()
    cash_permitted_bruto = get_cash_permitted_bruto(wallet, cash_percentage)
    cash_permitted_netto = get_cash_permitted_netto(wallet, cash_percentage)
    if wallet.stocks_value < cash_permitted_bruto:
        while wallet.stocks_value < cash_permitted_bruto :
            time_now = time.ctime(time.time())
            cycle+=1
            cash_permitted_netto = round(get_cash_permitted_netto(wallet, cash_percentage), 2 )
            print(f'\n{cycle}---------------------------{time_now}')
            print(f'{cash_permitted_netto=}\n')
            for stock in wallet.stocks.values():
                cash_new, stock_amt = actions.analyze(stock['handler'], stock['amount'],
                                              wallet.amt_cash,
                                              cash_permitted_netto,
                                              buy_permission)
                wallet.amt_cash = cash_new
                stock['amount'] = stock_amt
                wallet.calculate_stocks_value()

                print('--------------\n')
            time.sleep(analyze_frequency)
    # actions.log(f'\ntransactions stopped due to reach of given cash percentage ({cash_percentage}%)\n')
    # cash_percentage = get_summary_permission(wallet, cash_percentage)
    actions.get_summary(wallet, cash_percentage)

    # TO SELL IF TOO MUCH CASH IS SPENT
    cash_permitted_bruto = get_cash_permitted_bruto(wallet, cash_percentage)
    wallet.stocks_value = wallet.calculate_stocks_value()
    if wallet.stocks_value  > cash_permitted_bruto:
        buy_permission = -1
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
                wallet.calculate_stocks_value()
                print('--------------\n')
                if wallet.stocks_value  < cash_permitted_bruto:
                    buy_permission = 1
                    break
            time.sleep(analyze_frequency)
        # actions.log(f'\ntransactions stopped due to reach of given cash percentage ({cash_percentage}%)\n')
        # cash_percentage = get_summary_permission(wallet, cash_percentage)
        actions.get_summary(wallet, cash_percentage)


    # # update current total stock value
    # wallet_tech.stocks_value = wallet_tech.calculate_stocks_value()

    # # print summary
    # summary = actions.get_summary(wallet_tech, cash_percentage)
    # print(summary)

    # actions.log(f'\ntransactions stopped due to reach of given cash percentage ({cash_percentage}%)\n')




def get_cash_permitted_netto(wallet, cash_percentage):
    cash_permitted = wallet.amt_current * (cash_percentage / 100) - wallet.stocks_value
    return cash_permitted

def get_cash_permitted_bruto(wallet, cash_percentage):
    cash_permitted = wallet.amt_current * (cash_percentage / 100)
    return cash_permitted


def get_summary_permission(wallet, cash_percentage):
    wallet.stocks_value = wallet.calculate_stocks_value()
    summary = actions.get_summary(wallet, cash_percentage)
    print(summary)
    if email_activation == 1:
        actions.send_mail(summary)
        actions.log(f'\nEMAIL SENT  at {time.time()}\n\n')
    cash_percentage = float(
        input(f'\ncurrent cash percentage: {cash_percentage} \ndefine new cash percentage to adhere to trading: '))
    # cash_permitted = get_cash_permitted(wallet, cash_percentage)
    return cash_percentage




def main():
    # global buy_permission
    while bAlive == True:
        # global cash_percentage
        run_analysis(wallet_tech)


thread_main = Thread(target=main, daemon=False)
# thread_main.start()
# thread_main.join()

if __name__ == "__main__":
#     main()
    thread_main.start()