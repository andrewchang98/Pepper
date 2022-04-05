import sys
import datetime
from getpass import getpass
import alpaca_trade_api as tradeapi

# UNCOMMENT TO REMOVE TRACEBACKS
#sys.tracebacklimit = 0

# LOGIN METHOD
def login(attempts=3):
    global alpaca
    print('Please enter account information.')
    try:
        # ASK FOR API ACCOUNT INFO
        BASE_URL = input('Base URL: ')
        ALPACA_API_KEY = input('API Key: ')
        ALPACA_SECRET_KEY = getpass('Secret Key: ')
        # INSTANTIATE REST API CONNECTION
        alpaca = tradeapi.REST(key_id=BASE_URL, secret_key=ALPACA_SECRET_KEY,
                            base_url=BASE_URL, api_version='v2')
    except KeyboardInterrupt:
        # ABORT LOGIN
        print('\n', 'Canceled by user. Exiting now.', sep='')
        sys.exit(0)
    except ValueError:
        # RETRY LOGIN WITH SAME ATTEMPTS
        print('\n', 'Info must be in correct form. Try again.', '\n', sep='')
        login(attempts)
    except HTTPError:
        # RETRY LOGIN WITH 1 LESS ATTEMPT
        attempts -= 1
        if attempts < 1:
            print('No attempts remaining. Exiting now.')
        else:
            print('\n', 'Incorrect account key(s). Try again.', sep='')
            print('{} attempt remaining.'.format(attempts), '\n', sep='')
            login(attempts)
    return BASE_URL, ALPACA_API_KEY, ALPACA_SECRET_KEY

# ASSIGN API LOGIN INFO
BASE_URL, ALPACA_API_KEY, ALPACA_SECRET_KEY = login()

# PRINT ACCOUNT DETAILS
print(alpaca.get_account())
