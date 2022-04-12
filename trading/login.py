import sys
import socket
import pytz
from pytz import timezone
from getpass import getpass
from datetime import datetime
from requests.exceptions import HTTPError
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from alpaca_trade_api import REST
from alpaca_trade_api.stream import Stream
from slowprinter import Printer

# Ask for Alpaca Credentials in the CLI
def alpaca_prompter(printer=print) -> tuple:
    printer("Log into Alpaca:")
    printer("\nAccount Key:", end=' ')
    acc_key = input()
    printer("Authorization Key:", end=' ')
    auth_key = getpass(prompt='')
    return acc_key, auth_key

# Ask for Twilio Credentials in the CLI
def twilio_prompter(printer=print) -> tuple:
    printer("Log into Twilio:")
    printer("\nAccount Key:", end=' ')
    acc_key = input()
    printer("Authorization Key:", end=' ')
    auth_key = getpass(prompt='')
    printer("Twilio Phone Number:", end=' ')
    phone_num = input()
    printer("Target Phone Number:", end=' ')
    user_num = input()
    return acc_key, auth_key, phone_num, user_num


def get_timestr(tz='pst') -> str:
    date_format='%I:%M:%S%p %m/%d/%Y %Z'
    utc = datetime.now(tz=pytz.utc)
    pst = utc.astimezone(timezone('US/Pacific'))
    if tz == 'pst':
        return pst.strftime(date_format)
    elif tz == 'utc':
        return utc.strftime(date_format)
    else:
        raise TypeError("Not a recognized timezone.")


def sms_alert(client, sender, receiver, alert="!ALERT!", printer=print) -> None:
    try:
        date_format = ' %I:%M%p %w %d %Y'
        timestr = get_timestr('pst')
        body = client.messages.create(
            to=receiver,
            from_=sender,
            body=alert+timestr)
    except TwilioRestException as error:
        printer("Error! SMS Alert could not be sent!")
        printer(str(error))
        exit()




def read_input(response, *args):
    for char in args:
        if response == char:
            return True
    return False


def input_confirmation(printer=print):
    printer("Continue (y/n)?", end=' ')
    response = input()
    if read_input(response, 'y', 'Y'):
        return True
    elif read_input(response, 'n', 'Y'):
        return False
    else:
        return input_confirmation(printer)


def exit(printer=print, code=0):
    printer("Exiting now.")
    sys.exit(code)


def auto_login(APCA_API_BASE_URL='https://paper-api.alpaca.markets',
               data_feed='sip', disable_slow_print=False):
    try:
        slow = Printer(char_per_sec=50, disabled=disable_slow_print)
        try:
            from passwords import alpaca_key_dict
            APCA_API_KEY_ID = alpaca_key_dict['acc_key']
            APCA_API_SECRET_KEY = alpaca_key_dict['auth_key']
        except ImportError:
            slow.printer("\n~/Trading/trading/passwords.py is missing \
                         alpaca_key_dict")
            exit(slow.printer)
        except KeyError:
            slow.printer("\nalpaca_key_dict not properly configured in \
                         ~/Trading/trading/passwords.py")
            exit(slow.printer)
        slow.printer("Connecting to Alpaca...")
        try:
            alpaca = REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                          APCA_API_BASE_URL)
            stream = Stream(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                            APCA_API_BASE_URL, data_feed=data_feed)
        except TypeError:
            slow.printer("\nEnsure all twilio_key_dict values in \
                         ~/Trading/trading/passwords.py are <class 'str'>")
            exit(slow.printer)
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
            exit(slow.printer)
        except KeyError:
            slow.printer("\ntwilio_key_dict not properly configured in \
                         ~/Trading/trading/passwords.py")
            exit(slow.printer)
        try:
            twilio = Client(TWLO_SID_KEY, TWLO_AUTH_TOKEN)
        except TypeError:
            slow.printer("\nEnsure all twilio_key_dict values in \
                         ~/Trading/trading/passwords.py are <class 'str'>")
            exit(slow.printer)
        sms_alert(twilio, TWLO_PHONE_NUM, TWLO_USER_NUM,
                  alert="TradingBot has started!")
        slow.printer("Message sent to: {}".format(TWLO_USER_NUM))
    except KeyboardInterrupt:
        slow.printer("\nLogin cancelled by user.")
        exit(slow.printer)
    except ImportError:
        slow.printer("\n~/Trading/trading/passwords.py not found.")
        exit(slow.printer)
    except HTTPError:
        slow.printer("\nHTTPError: Failed to connect. Check if keys are valid.")
        raise
        exit(slow.printer)
    else:
        return alpaca, stream, twilio


def manual_login_alpaca(APCA_API_BASE_URL="https://paper-api.alpaca.markets",
               data_feed='sip', disable_slow_print=False):
    try:
        slow = Printer(char_per_sec=50, disabled=disable_slow_print)
        APCA_API_KEY_ID, APCA_API_SECRET_KEY = \
            alpaca_prompter(slow.printer)
        slow.printer("Connecting to Alpaca...")
        try:
            alpaca = REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                          APCA_API_BASE_URL)
            stream = Stream(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                            APCA_API_BASE_URL, data_feed=data_feed)
        except TypeError:
            slow.printer("\nEnsure all entered values are <class 'str'>")
            exit(slow.printer)
        slow.printer("Logged in as: {}".format(APCA_API_KEY_ID))
        account = alpaca.get_account()
        slow.printer("Your account status: {}".format(account.status))
        TWLO_SID_KEY, TWLO_AUTH_TOKEN, TWLO_PHONE_NUM, TWLO_USER_NUM = \
            twilio_prompter(slow.printer)
        try:
            twilio = Client(TWLO_SID_KEY, TWLO_AUTH_TOKEN)
        except TypeError:
            slow.printer("\nEnsure all entered values are <class 'str'>")
            exit(slow.printer)
        sms_alert(twilio, TWLO_PHONE_NUM, TWLO_USER_NUM,
                  alert="TradingBot has started!")
        slow.printer("Alert sent to: {}".format(TWLO_USER_NUM))
    except KeyboardInterrupt:
        slow.printer("\nLogin cancelled by user.")
        exit(slow.printer)
    except HTTPError:
        slow.printer("\nHTTPError: Failed to connect. Check if keys are valid.")
        raise
        exit(slow.printer)
    else:
        return alpaca, stream, twilio


def login(APCA_API_BASE_URL="https://paper-api.alpaca.markets",
               data_feed='sip', disable_slow_print=False):
    try:
        slow = Printer(char_per_sec=50, disabled=disable_slow_print)
        try:
            from passwords import alpaca_key_dict
            APCA_API_KEY_ID = alpaca_key_dict['acc_key']
            APCA_API_SECRET_KEY = alpaca_key_dict['auth_key']
            slow.printer("Found Alpaca account: {}".format(APCA_API_KEY_ID))
            if not input_confirmation(slow.printer):
                APCA_API_KEY_ID, APCA_API_SECRET_KEY = \
                    alpaca_prompter(slow.printer)
        except (ImportError, KeyError):
            slow.printer("\nError loading <alpaca_key_dict> from \
                         ~/Trading/trading/passwords.py")
            APCA_API_KEY_ID, APCA_API_SECRET_KEY = \
                alpaca_prompter(slow.printer)
        slow.printer("Connecting to Alpaca...")
        try:
            alpaca = REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                          APCA_API_BASE_URL)
            stream = Stream(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                            APCA_API_BASE_URL, data_feed=data_feed)
        except TypeError:
            slow.printer("\nEnsure all entered values are <class 'str'>")
            exit(slow.printer)
        try:
            account = alpaca.get_account()
            slow.printer("Logged in as: {}".format(APCA_API_KEY_ID))
            slow.printer("Your account status: {}".format(account.status))
        except HTTPError as err:
            slow.printer("Error occurred during Alpaca login.")
            slow.printer(str(err))
        try:
            from passwords import twilio_key_dict
            TWLO_SID_KEY = twilio_key_dict['acc_key']
            TWLO_AUTH_TOKEN = twilio_key_dict['auth_key']
            TWLO_PHONE_NUM = twilio_key_dict['phone_num']
            TWLO_USER_NUM = twilio_key_dict['user_num']
            slow.printer("Found Twilio account: {}".format(TWLO_SID_KEY))
            if not input_confirmation(slow.printer):
                TWLO_SID_KEY, TWLO_AUTH_TOKEN, TWLO_PHONE_NUM, TWLO_USER_NUM = \
                    twilio_prompter(slow.printer)
        except (ImportError, KeyError):
            slow.printer("\nError loading <twilio_key_dict> from \
                         ~/Trading/trading/passwords.py")
            TWLO_SID_KEY, TWLO_AUTH_TOKEN, TWLO_PHONE_NUM, TWLO_USER_NUM = \
                twilio_prompter(slow.printer)
        try:
            twilio = Client(TWLO_SID_KEY, TWLO_AUTH_TOKEN)
        except TypeError:
            slow.printer("\nEnsure all entered values are <class 'str'>")
            exit(slow.printer)
        hostname = socket.gethostname()
        sms_alert(twilio, TWLO_PHONE_NUM, TWLO_USER_NUM,
                  alert="ALERT! Logged in on: {}".format(hostname))
        slow.printer("Alert sent to: {}".format(TWLO_USER_NUM))
    except KeyboardInterrupt:
        slow.printer("\nLogin cancelled by user.")
        exit(slow.printer)
    except HTTPError:
        slow.printer("\nHTTPError: Failed to connect. Check if keys are valid.")
        raise
        exit(slow.printer)
    else:
        return alpaca, stream, twilio, slow


class Connection:
    def __init__(
                self,
                 APCA_API_BASE_URL="https://paper-api.alpaca.markets",
                 locked=False
                 ):
        alpaca, stream, twilio, slow = login()
        self.alpaca = alpaca
        self.stream = stream
        self.twilio = twilio
        self.locked = locked
        self.slow = slow
        self.timestamp = get_timestr()
        self.slow.printer("Connection successful: " + self.timestamp)


    def lock(self):
        self.locked = True
        self.slow.printer("Connection locked.")
        return self.locked


    def unlock(self):
        self.locked = False
        self.slow.printer("Connection unlocked.")
        return self.locked



    def get_start_time(self):
        return self.slow.printer(self.timestamp)
