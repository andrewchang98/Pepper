import sys
import requests
import datetime
from getpass import getpass
import alpaca_trade_api as tradeapi
from alpaca_trade_api.stream import Stream


# USER LOGIN METHOD
def account(BASE_URL='https://paper-api.alpaca.markets', attempts=3):
    print('Please enter account keys.')
    try:
        # ASK FOR API ACCOUNT KEYS
        ALPACA_API_KEY = input('API Key: ')
        ALPACA_SECRET_KEY = getpass('Secret Key: ')
        # INSTANTIATE REST API CONNECTION AND STREAM
        try:
            alpaca = tradeapi.REST(key_id=ALPACA_API_KEY,
                                   secret_key=ALPACA_SECRET_KEY,
                                   base_url=BASE_URL,
                                   api_version='v2')
            stream = Stream(key_id=ALPACA_API_KEY,
                            secret_key=ALPACA_SECRET_KEY,
                            base_url='https://paper-api.alpaca.markets',
                            data_feed='sip')
            print('\n', 'Success!', sep='')
            # PRINT ACCOUNT DETAILS
            print('\n', alpaca.get_account(), '\n', sep='')
            # RETURN API AND STREAM OBJECTS
            return alpaca, stream

        # !!!THIS EXCEPTION IS BROKEN!!!
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if e == 403:
                print('403')
            # RETRY LOGIN WITH 1 LESS ATTEMPT
            attempts -= 1
            if attempts < 1:
                print('No attempts remaining. Exiting now.')
            else:
                print('\n', 'Incorrect key(s). Try again.', sep='')
                print('{} attempt remaining.'.format(attempts), '\n', sep='')
                return account(BASE_URL='https://paper-api.alpaca.markets',
                                attempts=attempts)
        # TO REPLICATE BUG ENTER INCORRECT KEYS


    except KeyboardInterrupt:
        # ABORT LOGIN
        print('\n', 'Canceled by user. Exiting now.', sep='')
        sys.exit(0)
    except ValueError:
        # RETRY LOGIN WITH SAME ATTEMPTS
        print('\n', 'Keys must be in correct form. Try again.', '\n', sep='')
        return account(BASE_URL='https://paper-api.alpaca.markets',
                        attempts=attempts)
