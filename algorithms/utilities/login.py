import sys
from prompter import prompter
from slowprinter import Printer
import alpaca_trade_api as tradeapi

# MAIN ROUTINE TO LOAD ACCOUNT INFO
def login():

    APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'

    # TRY TO LOAD PASSWORDS FILE
    rp = Printer(delay=0.05)
    rp.printer('Loading account info...')
    try:
        import passwords
    except ImportError:
        rp.printer('No account info found in ~/Trading')
        APCA_API_KEY_ID, APCA_SECRET_KEY_ID = prompter(rp.printer)
    else:
        # ASK TO LOGIN AS USER
        rp.printer('Login as {} (Y/n)?'.format(passwords.account[0]), end=' ')
        try:
            keystroke = input()
            if keystroke == 'y' or keystroke == 'Y':
                APCA_API_KEY_ID = passwords.account[0]
                APCA_SECRET_KEY_ID = passwords.account[1]
            elif keystroke == 'n' or keystroke == 'N':
                APCA_API_KEY_ID, APCA_SECRET_KEY_ID = prompter(rp.printer)
            else:
                rp.printer('\nCancelled by user. Exiting now.')
                sys.exit(0)
        except KeyboardInterrupt:
            rp.printer('\nCancelled by user. Exiting now.')
            sys.exit(0)
    # CONNECT TO DEXCOM SHARE API
    try:
        rp.printer('\nConnecting to Alpaca servers...')
        alpaca = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                               APCA_API_BASE_URL)
        #stream = tradeapi.stream.Stream(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                               APCA_API_BASE_URL)
    except KeyboardInterrupt:
        rp.printer('\nLogin failed. Please check username and password.')
        rp.printer('Exiting now.')
        sys.exit(0)
    else:

        rp.printer('Logged in as {}\n'.format(APCA_API_KEY_ID))
        account = alpaca.get_account()
        rp.printer(account.status)
        return alpaca, stream
