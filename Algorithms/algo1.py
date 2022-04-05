import sys
import datetime
from getpass import getpass
import alpaca_trade_api as tradeapi

# Login Method
def login(attempts=3):
    try:
        # Ask for API Login Info
        print('Please enter account information.')
        BASE_URL = input('Base URL: ')
        ALPACA_API_KEY = input('API Key: ')
        ALPACA_SECRET_KEY = getpass('Secret Key: ')
    except KeyboardInterrupt:
        # Abort Login
        print('\n', 'Canceled by user. Exiting now.', sep='')
        sys.exit(0)
    except ValueError:
        # Retry Login with same attempts
        print('\n', 'Information is incorrect. Try again.', sep='')
        login(attempts)
    except HTTPError:
        # Retry Login with 1 less attempt
        print('\n', 'Information is incorrect. Try again.', sep='')
        attempts -= 1
        if attempts < 1:
            print('No more attempts. Exiting now.')
        else:
            print('{} attempt remaining.'.format(attempts))
            login(attempts)
    return BASE_URL, ALPACA_API_KEY, ALPACA_SECRET_KEY

# Assign API Login Info
sys.tracebacklimit = 0
BASE_URL, ALPACA_API_KEY, ALPACA_SECRET_KEY = login()
sys.tracebacklimit = None

# Instantiate REST API Connection
alpaca = tradeapi.REST(key_id=BASE_URL, secret_key=ALPACA_SECRET_KEY,
                    base_url=BASE_URL, api_version='v2')

# Print account details
alpaca.get_account()
