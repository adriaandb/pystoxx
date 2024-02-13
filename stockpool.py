import talib as ta
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web
from tradingview_ta import TA_Handler, Exchange, Interval




tesla = TA_Handler(
    symbol = 'TSLA',
    screener = 'america',
    exchange = 'NASDAQ',
    interval = Interval.INTERVAL_1_DAY
)

apple = TA_Handler(
    symbol = 'AAPL',
    screener = 'america',
    exchange = 'NASDAQ',
    interval = Interval.INTERVAL_1_DAY
)

amazon = TA_Handler(
    symbol = 'AMZN',
    screener = 'america',
    exchange = 'NASDAQ',
    interval = Interval.INTERVAL_1_DAY
)

microsoft = TA_Handler(
    symbol = 'MSFT',
    screener = 'america',
    exchange = 'NASDAQ',
    interval = Interval.INTERVAL_1_DAY
)


stockpool_tech = {
    'TSLA':{'amount' : 0, 'handler' : tesla, 'data' : 'dataframe'},
    'AMZN':{'amount' : 0, 'handler' : amazon, 'data' : 'dataframe'},
    'MSFT':{'amount' : 0, 'handler' : microsoft, 'data': 'dataframe'},
    'AAPL':{'amount' : 0, 'handler' : apple, 'data' : 'dataframe'}
                 }