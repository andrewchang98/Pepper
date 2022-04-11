import sys
from prompter import prompter
from slowprinter import Printer
import alpaca_trade_api as tradeapi
from twilio.rest import Client


# MAIN ROUTINE TO LOAD ACCOUNT INFO
def login(APCA_API_BASE_URL='https://paper-api.alpaca.markets'):
    # TRY TO IMPORT ALPACA KEY FROM 'passwords.py' FILE
    rp = Printer(delay=0.05)
    rp.printer('Loading account info...')
    try:
        from passwords import alpaca as alpaca_keys
    except ImportError:
        rp.printer('No account info found in ~/Trading')
        APCA_API_KEY_ID, APCA_API_SECRET_KEY = prompter(rp.printer)
    else:
        # ASK TO LOGIN AS USER IF 'alpaca' IS FOUND IN 'passwords.py' FILE
        rp.printer('Login as {} (Y/n)?'.format(alpaca_keys['acc_key']), end=' ')
        try:
            keystroke = input()
            if keystroke == 'y' or keystroke == 'Y':
                APCA_API_KEY_ID = alpaca_keys['acc_key']
                APCA_API_SECRET_KEY = alpaca_keys['auth_key']
            elif keystroke == 'n' or keystroke == 'N':
                APCA_API_KEY_ID, APCA_API_SECRET_KEY = prompter(rp.printer)
            else:
                rp.printer('\nCancelled by user. Exiting now.')
                sys.exit(0)
        except KeyboardInterrupt:
            rp.printer('\nCancelled by user. Exiting now.')
            sys.exit(0)
    # CONNECT AND ASSIGN ALPACA REST API AND STREAM
    try:
        rp.printer('\nConnecting to Alpaca servers...\n')
        alpaca = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                               APCA_API_BASE_URL)
        stream = tradeapi.stream.Stream(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                               APCA_API_BASE_URL)
    except KeyboardInterrupt:
        rp.printer('Login failed. Please check username and password.')
        rp.printer('Exiting now.')
        sys.exit(0)
    else:
        rp.printer('Logged in as {}'.format(APCA_API_KEY_ID))
        account = alpaca.get_account()
        rp.printer('Your account is: {}\n'.format(account.status))
        return alpaca, stream
