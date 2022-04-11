import sys
from getpass import getpass
from prompter import prompter
from slowprinter import Printer
import alpaca_trade_api as tradeapi
from twilio.rest import Client

# HELPER ROUTINE TO READ USER INPUTS
def read_input(response, printer, *args)
    if printer is None:
        printer = print()
    for char in args:
        if response == char:
            return True
    return False

# HELPER FUNCTION TO PROMPT USER INFO
def prompter(printer=None, message="Log into Alpaca:"):
    if printer is None:
        printer = print
    else:
        printer = printer
    printer(message)
    try:
        printer("\nAccount SID:", end=' ')
        username = input()
        printer("Auth Token:", end=' ')
        password = getpass(prompt='')
    except KeyboardInterrupt:
        print("\nCancelled by user. Exiting now.")
        sys.exit(0)
    else:
        return username, password


# MAIN ROUTINE TO START TRADING
def login(APCA_API_BASE_URL="https://paper-api.alpaca.markets"):
    try:
        rp = Printer(delay=0.05)
        rp.printer("Loading account info...")
        # IMPORT ALPACA KEYS FROM 'passwords.py'
        try:
            from passwords import alpaca_keys as keys
        except ImportError:
            rp.printer("No account info found in ~/Trading")
            APCA_API_KEY_ID, APCA_API_SECRET_KEY = prompter(rp.printer)
        else:
            # ASK TO LOG IN AS USER IF "alpaca" IS FOUND IN 'passwords.py'
            rp.printer("Log in as {} (y/n)?".format(keys['acc_key']), end=' ')
            response = input()
            read_input
            if response == 'y' or response == 'Y':
                APCA_API_KEY_ID = keys['acc_key']
                APCA_API_SECRET_KEY = keys['auth_key']
            elif response == 'n' or response == 'N':
                APCA_API_KEY_ID, APCA_API_SECRET_KEY = prompter(rp.printer)
            else:
                rp.printer("\nCancelled by user. Exiting now.")
                sys.exit(0)
        # CONNECT AND ASSIGN ALPACA REST API AND STREAM
        rp.printer("\nConnecting to Alpaca servers...\n")
        alpaca = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                               APCA_API_BASE_URL)
        stream = tradeapi.stream.Stream(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                               APCA_API_BASE_URL)



        else:
            rp.printer("Logged in as {}".format(APCA_API_KEY_ID))
            account = alpaca.get_account()
            rp.printer("Your account is: {}".format(account.status))
            # ASK TO ENABLE TWILIO TEXT ALERTS
            rp.printer("Would you like to enable Twilio SMS text alerts (y/n)?")
            response = input()
            if read_input(response, rp, 'y', 'Y'):
                # IMPORT TWILIO KEYS FROM 'passwords.py'
                try:
                    from passwords import twilio_keys as keys
                    rp.printer("Login as {} (y/n)?".format(keys['phone_num']), end=' ')
                    response = input()

            else:
                return alpaca, stream
    except KeyboardInterrupt:
        rp.printer("\n\nLogin cancelled by user.")
        rp.printer("Exiting now.")
        sys.exit(0)
