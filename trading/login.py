import sys
import socket
import pickle
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

# Pickle key_dict to file_name
def save_key_dict(file_name: str, key_dict: dict) -> None:
    with open(file_name, 'wb') as file:
        pickle.dump(key_dict, file, pickle.HIGHEST_PROTOCOL)

# Unpickle key_dict to file_name
def load_key_dict(file_name: str) -> dict:
    with open(file_name, 'rb') as file:
        key_dict = pickle.load(file)
    return key_dict

# Get UTC or PST string following date_format argument
def get_timestr(tz='pst', date_format='%I:%M:%S%p %m/%d/%Y %Z') -> str:
    utc = datetime.now(tz=pytz.utc)
    pst = utc.astimezone(timezone('US/Pacific'))
    if tz == 'pst':
        return pst.strftime(date_format)
    elif tz == 'utc':
        return utc.strftime(date_format)
    else:
        raise TypeError("Not a recognized timezone.")

# Sends SMS alert
def sms_alert(twilio: Client,
              sender: str,
              receiver: str,
              alert="!ALERT!",
              printer=print) -> bool:
    try:
        date_format = ' %I:%M%p %w %d %Y'
        timestr = get_timestr('pst')
        body = client.messages.create(
            to=receiver,
            from_=sender,
            body=alert+timestr)
        return True
    except TwilioRestException as error:
        printer("Error! SMS Alert could not be sent!")
        printer(str(error))
        return False


def read_input(response: str, *args: str) -> bool:
    for char in args:
        if response == char:
            return True
    return False


def input_confirmation(message="Continue (y/n)?", printer=print) -> bool:
    printer(message, end=' ')
    response = input()
    if read_input(response, 'y', 'Y'):
        return True
    elif read_input(response, 'n', 'Y'):
        return False
    else:
        return input_confirmation(printer)


def exit(printer=print, code=0) -> None:
    printer("Exiting now.")
    sys.exit(code)

# The Alpaca + Twilio Login Function that does it all
def login(APCA_API_BASE_URL="https://paper-api.alpaca.markets",
          data_feed='sip',
          disable_slow_print=False) -> tuple:
    try:
        slow = Printer(char_per_sec=50, disabled=disable_slow_print)
        try:
            alpaca_key_dict = load_key_dict('alpaca.key')
            APCA_API_KEY_ID = alpaca_key_dict['acc_key']
            APCA_API_SECRET_KEY = alpaca_key_dict['auth_key']
            slow.printer(f"Found Alpaca account: {APCA_API_KEY_ID}")
            if not input_confirmation(slow.printer):
                APCA_API_KEY_ID,
                APCA_API_SECRET_KEY = alpaca_prompter(slow.printer)
        except (AttributeError, ImportError, KeyError) as error:
            slow.printer(str(error))
            slow.printer("\nError loading <alpaca_key_dict> from \
                         ~/Trading/trading/passwords.py")
            APCA_API_KEY_ID,
            APCA_API_SECRET_KEY = alpaca_prompter(slow.printer)
        else:
            slow.printer("Connecting to Alpaca...")

        try:
            alpaca = REST(
                          APCA_API_KEY_ID,
                          APCA_API_SECRET_KEY,
                          APCA_API_BASE_URL
                         )
            stream = Stream(
                            APCA_API_KEY_ID,
                            APCA_API_SECRET_KEY,
                            APCA_API_BASE_URL,
                            data_feed=data_feed
                           )
        except TypeError:
            slow.printer("\nEnsure all key_dict values are <class 'str'>")
            exit(slow.printer)
        else:
            try:
                account = alpaca.get_account()
                slow.printer(f"Logged in as: {APCA_API_KEY_ID}")
                slow.printer(f"Your account status: {account.status}")
            except HTTPError as err:
                slow.printer("Error occurred during Alpaca login.")
                slow.printer(str(err))
            else:
                if input_confirmation("Save Alpaca Login? This will replace \
                                      any previously saved keys. (y/n)?",
                                      slow.printer):
                    alpaca_key_dict = {
                                       'acc_key':   TWLO_SID_KEY,
                                       'auth_key':  TWLO_AUTH_TOKEN
                                      }

                    try:
                        save_key_dict('alpaca.key', alpaca_key_dict)
                    except (AttributeError, ImportError, KeyError) as error:
                        slow.printer("Alpaca Login not saved due to Error")
                        slow.printer(str(error))

        try:
            load_key_dict('twilio.key')
            TWLO_SID_KEY = twilio_key_dict['acc_key']
            TWLO_AUTH_TOKEN = twilio_key_dict['auth_key']
            TWLO_PHONE_NUM = twilio_key_dict['phone_num']
            TWLO_USER_NUM = twilio_key_dict['user_num']
            slow.printer(f"Found Twilio account: {TWLO_SID_KEY}")
            if not input_confirmation(slow.printer):
                TWLO_SID_KEY,
                TWLO_AUTH_TOKEN,
                TWLO_PHONE_NUM,
                TWLO_USER_NUM = twilio_prompter(slow.printer)
        except (AttributeError, ImportError, KeyError) as error:
            slow.printer(str(error))
            slow.printer("\nError loading <twilio_key_dict> from \
                         ~/Trading/trading/passwords.py")
            TWLO_SID_KEY,
            TWLO_AUTH_TOKEN,
            TWLO_PHONE_NUM,
            TWLO_USER_NUM = twilio_prompter(slow.printer)

        try:
            twilio = Client(TWLO_SID_KEY, TWLO_AUTH_TOKEN)
        except TypeError:
            slow.printer("\nEnsure all entered values are <class 'str'>")
            exit(slow.printer)
        else:
            hostname = socket.gethostname()
            if sms_alert(twilio,
                         TWLO_PHONE_NUM,
                         TWLO_USER_NUM,
                         alert=f"ALERT! Logged in on: {hostname}"):
                slow.printer(f"Alert sent to: {TWLO_USER_NUM}")
            else:
                slow.printer(f"! Could not sent alert to {TWLO_USER_NUM} !")

        try:
            if input_confirmation("Save Twilio Login? This will replace any \
                                  previously saved keys. (y/n)?",
                                  slow.printer):
                twilio_key_dict = {
                                   'acc_key':   TWLO_SID_KEY,
                                   'auth_key':  TWLO_AUTH_TOKEN,
                                   'phone_num': TWLO_PHONE_NUM,
                                   'user_num':  TWLO_USER_NUM,
                                  }
                save_key_dict('twilio.key', twilio_key_dict)
                slow.printer("Twilio Login saved.")
            else:
                slow.printer("Twilio Login not saved.")
        except (AttributeError, ImportError, KeyError) as error:
            slow.printer("Twilio Login not saved due to Error")
            slow.printer(str(error))

    except KeyboardInterrupt:
        slow.printer("\nLogin cancelled by user.")
        exit(slow.printer)
    else:
        return alpaca, stream, twilio, slow

# Stores outputs of 'login'
class Connection:
    def __init__(
                 self,
                 APCA_API_BASE_URL="https://paper-api.alpaca.markets",
                 data_feed='sip',
                 locked=False
                ) -> None:
        alpaca, stream, twilio, slow = login()
        self.alpaca = alpaca
        self.stream = stream
        self.twilio = twilio
        self.locked = locked
        self.slow = slow
        self.timestamp = get_timestr()
        self.slow.printer("Connection successful: " + self.timestamp)


    def lock(self) -> bool:
        self.locked = True
        self.slow.printer("Connection locked.")
        return self.locked


    def unlock(self) -> bool:
        self.locked = False
        self.slow.printer("Connection unlocked.")
        return self.locked



    def get_start_time(self) -> str:
        return self.slow.printer(self.timestamp)
