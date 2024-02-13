import actions
import stockpool
import talib as ta
import pandas_datareader as web
from datetime import date
from datetime import timedelta

import stockpool as sp
import wallet
from wallet import Wallet

from forex_python.converter import CurrencyRates
from time import time, ctime


#CREATING DATE+TIME VARIABLES
# today = date.today()
# time = ctime(time())
#
# if today.isoweekday() == 1:
#     yesterday = today - timedelta(days = 3)
# else:
#     yesterday = today - timedelta(days = 1)
# print(yesterday)
# data = web.DataReader('AAPL', data_source="stooq", start=yesterday)
# print(data)


#
# data = actions.get_stock_dataframe(sp.tesla)
# print('dataframe:\n'+data)

# tesla_openprice = sp.tesla.get_analysis().indicators["open"]
# print("tesla open price: "+ str(tesla_openprice) + ' USD')


email_body = 'dit is een test'
actions.send_mail(email_body)


# import os
# import pandas_datareader as pdr
# pdr.get_data_stooq()
# df = pdr.get_data_tiingo('GOOG', api_key=os.getenv('0b1aa0a7c64f506c0607f87e78fd7f377427e2cb'))
# df = pdr.get_data_tiingo('GOOG', '0b1aa0a7c64f506c0607f87e78fd7f377427e2cb')
# df.head()