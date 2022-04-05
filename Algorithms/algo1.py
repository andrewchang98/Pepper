""" ENTER URL FOR PAPER/LIVE TRADING HERE: """
BASE_URL = 'https://paper-api.alpaca.markets'


import sys
import datetime
from getpass import getpass
import alpaca_trade_api as tradeapi

from ..utilities.login import login

alpaca = login.login(attempts=3)


# USER LOGIN METHOD
def login(attempts):
    print('Please enter account keys.')
    try:
        # ASK FOR API ACCOUNT KEYS
        ALPACA_API_KEY = input('API Key: ')
        ALPACA_SECRET_KEY = getpass('Secret Key: ')
        # INSTANTIATE REST API CONNECTION
        alpaca = tradeapi.REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY,
                            base_url=BASE_URL, api_version='v2')
    except KeyboardInterrupt:
        # ABORT LOGIN
        print('\n', 'Canceled by user. Exiting now.', sep='')
        sys.exit(0)
    except ValueError:
        # RETRY LOGIN WITH SAME ATTEMPTS
        print('\n', 'Keys must be in correct form. Try again.', '\n', sep='')
        login(attempts)
    except HTTPError:
        # RETRY LOGIN WITH 1 LESS ATTEMPT
        attempts -= 1
        if attempts < 1:
            print('No attempts remaining. Exiting now.')
        else:
            print('\n', 'Incorrect key(s). Try again.', sep='')
            print('{} attempt remaining.'.format(attempts), '\n', sep='')
            login(attempts)
    return alpaca


# PROMPT USER TO LOGIN TO ALPACA AND ASSIGN OBJECT
#alpaca = login(attempts=3)


# PRINT ACCOUNT DETAILS
print(alpaca.get_account())


bar_iter = alpaca.get_bars_iter("DCFC", tradeapi.rest.TimeFrame.Minute, "2022-04-04", "2022-04-04", adjustment='raw')
for bar in bar_iter:
    print(bar)
