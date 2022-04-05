import sys
import requests
import datetime
from getpass import getpass
import alpaca_trade_api as tradeapi


# USER LOGIN METHOD
def account(BASE_URL='https://paper-api.alpaca.markets', attempts=3):
    print('Please enter account keys.')
    try:
        # ASK FOR API ACCOUNT KEYS
        ALPACA_API_KEY = input('API Key: ')
        ALPACA_SECRET_KEY = getpass('Secret Key: ')
        # INSTANTIATE REST API CONNECTION
        alpaca = tradeapi.REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY,
                            base_url=BASE_URL, api_version='v2')
        return alpaca
    except KeyboardInterrupt:
        # ABORT LOGIN
        print('\n', 'Canceled by user. Exiting now.', sep='')
        sys.exit(0)
    except ValueError:
        # RETRY LOGIN WITH SAME ATTEMPTS
        print('\n', 'Keys must be in correct form. Try again.', '\n', sep='')
        return account(BASE_URL='https://paper-api.alpaca.markets',
                        attempts=attempts)
    except requests.exceptions.HTTPError:
        # RETRY LOGIN WITH 1 LESS ATTEMPT
        attempts -= 1
        if attempts < 1:
            print('No attempts remaining. Exiting now.')
        else:
            print('\n', 'Incorrect key(s). Try again.', sep='')
            print('{} attempt remaining.'.format(attempts), '\n', sep='')
            return account(BASE_URL='https://paper-api.alpaca.markets',
                            attempts=attempts)
