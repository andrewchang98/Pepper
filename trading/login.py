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
        printer = print()
    else:
        printer = printer
    printer("Log in", end='')
    printer(message)
    printer("\nAccount Key:", end=' ')
    username = input()
    printer("Authorization Key:", end=' ')
    password = getpass(prompt='')
    return username, password


def sms_alert(sender, receiver, alert='!ALERT! '):
    time = datetime.now(timezone.utc)
    timestr = time.strftime('%I:%M%p %w %d %Y')
    body = client.messages.create(
        to=receiver,
        from_=sender,
        body=alert+timestr)


def read_input(response, *args):
    for char in args:
        if response == char:
            return True
    return False


def exit(code=0):
    slow.printer("Exiting now.")
    sys.exit(code)


def auto_login(APCA_API_BASE_URL="https://paper-api.alpaca.markets",
               data_feed='sip'):
    try:
        slow = Printer()
        try:
            from passwords import alpaca_key_dict
            APCA_API_KEY_ID = alpaca_key_dict['acc_key']
            APCA_API_SECRET_KEY = alpaca_key_dict['auth_key']
        except ImportError:
            slow.printer("\n~/Trading/trading/passwords.py is missing \
                         alpaca_key_dict")
        except KeyError:
            slow.printer("\nalpaca_key_dict not properly configured in \
                         ~/Trading/trading/passwords.py")
        slow.printer("Connecting to Alpaca...")
        alpaca = REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                      APCA_API_BASE_URL)
        stream = Stream(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                        APCA_API_BASE_URL, data_feed=data_feed)
        slow.printer("Logged in as: {}".format(APCA_API_KEY_ID))
        account = alpaca.get_account()
        slow.printer("Your account status: {}".format(account.status))
        try:
            from passwords import twilio_key_dict
            TWLO_SID_KEY = twilio_key_dict['acc_key']
            TWLO_AUTH_TOKEN = twilio_key_dict['auth_key']
            TWLO_PHONE_NUM = twilio_key_dict['phone_num']
            TWLO_USER_NUM = twilio_key_dict['user_num']
        except ImportError:
            slow.printer("\n~/Trading/trading/passwords.py is missing \
                         twilio_key_dict")
        except KeyError:
            slow.printer("\ntwilio_key_dict not properly configured in \
                         ~/Trading/trading/passwords.py")

        twilio = Client(TWLO_SID_KEY, TWLO_AUTH_TOKEN)

        if not sms_alert(TWLO_PHONE_NUM, TWLO_USER_NUM,
                         alert="You have logged into Twilio "):
            slow.printer("!!! SMS ALERTS FAILED. !!! \
                         CHECK CODE IMMEDIATELY !!!")
    except KeyboardInterrupt:
        slow.printer("\nLogin cancelled by user.")
        exit()
    except ImportError:
        slow.printer("\n~/Trading/trading/passwords.py not found.")
        exit()
    except HTTPError:
        slow.printer("\nHTTPError: Failed to connect. Check if keys are valid.")
        exit()
    else:
        return alpaca, stream, twilio
