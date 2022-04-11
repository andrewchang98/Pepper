import sys
from getpass import getpass
from datetime import datetime
from requests import HTTPError
from twilio.rest import Client
from alpaca_trade_api import REST
from alpaca_trade_api.stream import Stream
from slowprinter import Printer


def prompter(printer=None, message=":"):
    if printer is None:
        printer = print
    else:
        printer = printer
    printer("Log in", end='')
    printer(message)
    printer("\nAccount Key:", end=' ')
    username = input()
    printer("Authorization Key:", end=' ')
    password = getpass(prompt='')
    return username, password

def sms_alert(message=None)
    if message is None:
        message =

def read_input(response, *args):
    for char in args:
        if response == char:
            return True
    return False

def exit(code=0):
    slow.printer("Exiting now.")
    sys.exit(code)


def auto_login(APCA_API_BASE_URL="https://paper-api.alpaca.markets", data_feed='sip'):
    try:
        try:
            from passwords import alpaca_key_dict
            APCA_API_KEY_ID = alpaca_key_dict['acc_key']
            APCA_API_SECRET_KEY = alpaca_key_dict['auth_key']
        except ImportError:
            slow.printer("\n\n~/Trading/trading/passwords.py is missing alpaca_key_dict")
        except KeyError:
            slow.printer("\n\nalpaca_key_dict not properly configured in ~/Trading/trading/passwords.py")

        alpaca = REST(APCA_API_KEY_ID,
                      APCA_API_SECRET_KEY,
                      APCA_API_BASE_URL)
        stream = Stream(APCA_API_KEY_ID,
                        APCA_API_SECRET_KEY,
                        APCA_API_BASE_URL,
                        data_feed=data_feed)

        try:
            from passwords import twilio_key_dict
            TWLO_SID_KEY = twilio_key_dict['acc_key']
            TWLO_AUTH_TOKEN = twilio_key_dict['auth_key']
            TWLO_PHONE_NUM = twilio_key_dict['phone_num']
        except ImportError:
            slow.printer("\n\n~/Trading/trading/passwords.py is missing twilio_key_dict")
        except KeyError:
            slow.printer("\n\ntwilio_key_dict not properly configured in ~/Trading/trading/passwords.py")

        twilio = Client(TWLO_SID_KEY, TWLO_AUTH_TOKEN)


    except KeyboardInterrupt:
        slow.printer("\n\nLogin cancelled by user.")
        sys.exit()
    except ImportError:
        slow.printer("\n\n~/Trading/trading/passwords.py not found.")
        exit()
    except HTTPError:
        slow.printer("\n\nFailed to connect. Check if keys are valid.")
        exit()
    except:
        slow.printer("\n\nSomething went wrong. Check code for errors.")


def login(APCA_API_BASE_URL="https://paper-api.alpaca.markets"):
    try:
        slow = Printer(delay=0.05)
        slow.printer("Loading account info...")
        try:
            from passwords import alpaca_keys as keys
        except ImportError:
            slow.printer("Did not find Alpaca account in ~/Trading/trading/passwords.py")
            APCA_API_KEY_ID, APCA_API_SECRET_KEY = prompter(slow.printer, " to Alpaca:")
        else:
            slow.printer("Log in as {} (y/n)?".format(keys['acc_key']), end=' ')
            response = input()
            read_input
            if response == 'y' or response == 'Y':
                APCA_API_KEY_ID = keys['acc_key']
                APCA_API_SECRET_KEY = keys['auth_key']
            elif response == 'n' or response == 'N':
                APCA_API_KEY_ID, APCA_API_SECRET_KEY = prompter(slow.printer, " to Alpaca:")
            else:
                slow.printer("\nCancelled by user. Exiting now.")
                sys.exit(0)
        slow.printer("\nConnecting to Alpaca servers...\n")
        try:
            alpaca = REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                                   APCA_API_BASE_URL)
            stream = Stream(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                                   APCA_API_BASE_URL)
        except:
            slow.printer("Something went wrong. Inspect Alpaca keys and code.")
            slow.printer("Exiting now.")
            sys.exit(0)
        else:
            slow.printer("Logged in as {}".format(APCA_API_KEY_ID))
            account = alpaca.get_account()
            slow.printer("Your account is: {}".format(account.status))
            slow.printer("Would you like to enable Twilio SMS text alerts (y/n)?")
            response = input()
            if read_input(response, slow, 'y', 'Y'):
                try:
                    from passwords import twilio_keys as keys
                    slow.printer("Login as {} (y/n)?".format(keys['phone_num']), end=' ')
                    response = input()
                except ImportError:
                    slow.printer("Did not find Twilio account in )
            elif read_input(response, slow, 'n', 'N'):
                TWILIO_SID_KEY, TWILIO_AUTH_KEY = prompter(slow.printer, " to Twilio:")
            else:
                return alpaca, stream
    except KeyboardInterrupt:
        slow.printer("\n\nLogin cancelled by user.")
        exit()
