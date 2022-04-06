import sys
import requests
import datetime
from getpass import getpass
import alpaca_trade_api as tradeapi
from alpaca_trade_api.stream import Stream

# PROMPT USER INFO
def prompt():
    print('Please enter account keys:')
    try:
        apikey = input('API Key: ')
        secretkey = getpass('Secret Key: ')
    except KeyboardInterrupt:
        print('\n', 'Canceled by user. Exiting now.', sep='')
        sys.exit(0)
    else:
        return apikey, secretkey

# LOAD ACCOUNT INFO
def account(BASE_URL='https://paper-api.alpaca.markets', attempts=3):
    # TRY TO LOAD PASSWORDS FILE
    print('Loading account info...')
    try:
        from accounts import passwords
    except ImportError:
        print('No account info found.')
        ALPACA_API_KEY, ALPACA_SECRET_KEY = prompt()
    else:
        # ASK TO LOGIN AS USER
        print('Login as {} (y/n)?'.format(passwords.account[0]), end = ' ')
        try:
            keystroke = input()
            if keystroke == 'y' or keystroke == 'Y':
                ALPACA_API_KEY = passwords.account[0]
                ALPACA_SECRET_KEY = passwords.account[1]
            elif keystroke == 'n' or keystroke == 'N':
                ALPACA_API_KEY, ALPACA_SECRET_KEY = prompt()
            else:
                print('\n', 'Canceled by user. Exiting now.', sep='')
                sys.exit(0)
        except KeyboardInterrupt:
            print('\n', 'Canceled by user. Exiting now.', sep='')
            sys.exit(0)

    # CONNECT TO DEXCOM SHARE API
    print('\n', 'Connecting to Alpaca servers...', sep='')
    try:
        alpaca = tradeapi.REST(key_id=ALPACA_API_KEY,
                               secret_key=ALPACA_SECRET_KEY,
                               base_url=BASE_URL,
                               api_version='v2')
        stream = Stream(key_id=ALPACA_API_KEY,
                        secret_key=ALPACA_SECRET_KEY,
                        base_url='https://paper-api.alpaca.markets',
                        data_feed='sip')
    except:
        print('\n', 'Login failed. Please check keys.', sep='')
        print('Exiting now.')
        sys.exit(0)
    else:
        print('\n', 'Successfully logged into Alpaca.', '\n', sep='')
        return dexcom


# USER LOGIN METHOD
def account(BASE_URL='https://paper-api.alpaca.markets', attempts=3):
    print('Please enter account keys.')
    try:
        # ASK FOR API ACCOUNT KEYS
        ALPACA_API_KEY = input('API Key: ')
        ALPACA_SECRET_KEY = getpass('Secret Key: ')
        # TRY TO INSTANTIATE REST API CONNECTION AND STREAM
        print('\n', 'Logging in...', sep='')
        try:
            alpaca = tradeapi.REST(key_id=ALPACA_API_KEY,
                                   secret_key=ALPACA_SECRET_KEY,
                                   base_url=BASE_URL,
                                   api_version='v2')
            stream = Stream(key_id=ALPACA_API_KEY,
                            secret_key=ALPACA_SECRET_KEY,
                            base_url='https://paper-api.alpaca.markets',
                            data_feed='sip')
        # !!!THIS EXCEPTION IS BROKEN!!!
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
        except ValueError:
            # RETRY LOGIN WITH SAME ATTEMPTS
            print('\n', 'Keys must be in correct form. Try again.', '\n', sep='')
            return account(BASE_URL='https://paper-api.alpaca.markets',
                            attempts=attempts)
    except KeyboardInterrupt:
        # ABORT LOGIN
        print('\n', 'Canceled by user. Exiting now.', sep='')
        sys.exit(0)
    else:
        # PRINT ACCOUNT DETAILS
        print('\n', alpaca.get_account(), '\n', sep='')
        print('Successfully logged in. ',
              'Your account details are displayed above.',
              '\n', sep='')
        # RETURN API AND STREAM OBJECTS
        return alpaca, stream
