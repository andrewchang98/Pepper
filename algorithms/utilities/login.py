import sys
import datetime
from getpass import getpass
from requests.exceptions import HTTPError
import alpaca_trade_api as tradeapi
from alpaca_trade_api.stream import Stream

# PROMPT USER INFO IN TERMINAL
def prompt():
    print('Please enter account keys:')
    try:
        apikey = input('API Key: ')
        secretkey = getpass('Secret Key: ')
    except KeyboardInterrupt:
        print('\n', 'CANCELLED by user. Exiting now.', sep='')
        sys.exit(0)
    else:
        return apikey, secretkey

# LOG INTO ALPACA AND RETURN ALPACA API AND STREAM
def account(BASE_URL='https://paper-api.alpaca.markets'):
    # TRY TO LOAD PASSWORDS FILE
    print('Loading account info...')
    try:
        from accounts import passwords
    except ImportError:
        print('No account info found in ~/.local/lib/python3.9/site-packages/accounts/')
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
                print('\n', 'CANCELLED by user. Exiting now.', sep='')
                sys.exit(0)
        except KeyboardInterrupt:
            print('\n', 'CANCELLED by user. Exiting now.', sep='')
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
    except HTTPError:
        print('\n', 'Login failed. Please check keys.', sep='')
        print('Exiting now.')
        sys.exit(0)
    else:
        print('Successfully logged into ', BASE_URL, '\n', sep='')
        return alpaca, stream
