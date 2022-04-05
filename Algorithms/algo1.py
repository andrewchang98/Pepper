import sys
import datetime
from getpass import getpass
import alpaca_trade_api as tradeapi

def login(attempts=3):
    try:
        # Ask for API Info
        print('Please enter account information.')
        BASE_URL = input('Base URL: ')
        ALPACA_API_KEY = input('API Key: ')
        ALPACA_SECRET_KEY = getpass('Secret Key: ')
    except KeyboardInterrupt:
        # Abort login
        print()
        print('Canceled by user. Exiting now.')
        sys.exit(0)
    except HTTPError:
        # Retry (Default 3 attempts)
        print()
        print('Information is incorrect. Try again.')
        attempts -= 1
        if attempts < 1:
            print('No more attempts. Exiting now.')
        else:
            print('{} attempt remaining.'.format(attempts))
            login(attempts)

# Instantiate REST API Connection
alpaca = tradeapi.REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY,
                    base_url=BASE_URL, api_version='v2')

alpaca.get_account()
