"""
!!!NOT FUNCTIONAL!!!
RANDOM CODE IS BEING STORED HERE BEFORE DELETION

"""

"""
Alpaca Crypto Trading Algorithm

"""

"""
Alpaca Stock Trading Algorithm

"""

['DCFC', 'DXCM', 'LDOS', 'LAC', 'SEDG', 'LIN', 'ENPH', 'GLD']

from utilities import boot
from utilities.slowprinter import Printer

slow = Printer()

# LOGIN AND ASSIGN ALPACA AND STREAM OBJECTS
try:
    bot = boot.Connection()
except RecursionError as error:
    slow.printer(str(error))


import time
import pickle
import login
from datetime import datetime
from alpaca_trade_api.rest import TimeFrame
from alpaca_trade_api.stream import Stream

class Bot:
    def __init__(self, name, symbol, initial_buying_power, account, stream):
        self.name = name
        self.symbol = symbol
        self.totalvalue = initial_buying_power
        self.account, self.stream = login.login()

    def stringdate(dt):
        if type(dt) == str:
            return dt
        return dt.strftime('%Y-%m-%d')

    def run(self, tf, start_date, end_datetime=None):
        try:
            while end_datetime is None or end_datetime > datetime.now():
                self.account.get_bars(self.symbol, tf,
                                      stringdate(start_date),
                                      stringdate(datetime.now()), adjustment='raw')
        except KeyboardInterrupt:
            print("!!!CANCELLED BY USER!!!")


"""
GET CLOCK DATA
account.get_clock().timestamp.is_open

account.get_clock().timestamp.year
account.get_clock().timestamp.month
account.get_clock().timestamp.week
account.get_clock().timestamp.day
account.get_clock().timestamp.minute
account.get_clock().timestamp.second
account.get_clock().timestamp.microsecond
account.get_clock().timestamp.nanosecond

account.get_clock().next_open.year
...

account.get_clock().next_close.year
...
"""
