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

# Returns True if all values in a dictionary are <class 'str'>, else False
def is_str_dictionary(dict):
    for item in dict:
        if type(dict[item]) is not str:
            return False
    return True

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
              printer=print) -> None:
    date_format = ' %I:%M%p %w %d %Y'
    timestr = get_timestr('pst')
    body = client.messages.create(to=receiver,
                                  from_=sender,
                                  body=alert+timestr)

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
          disable_slowprint=False) -> tuple:

    try:
        # Instantiate char by char printer
        slow = Printer(char_per_sec=50, disabled=disable_slowprint)
        # Load Alpaca keys
        try:
            alpaca_key_dict = load_key_dict('alpaca.key')
            APCA_API_KEY_ID = alpaca_key_dict['acc_key']
            APCA_API_SECRET_KEY = alpaca_key_dict['auth_key']
            slow.printer(f"Found Alpaca account: {APCA_API_KEY_ID}")
            # Asks for new keys if User declines loaded keys
            if not input_confirmation("Continue with loaded account (y/n)?",
                                      slow.printer):
                APCA_API_KEY_ID, \
                APCA_API_SECRET_KEY = alpaca_prompter(slow.printer)
        # Asks for new Alpaca keys if Alpaca keys could not be loaded
        except (FileNotFoundError, AttributeError, ImportError,
                KeyError) as error:
            slow.printer(str(error))
            slow.printer("\nError loading Alpaca keys from ~/Trading/trading")
            APCA_API_KEY_ID, \
            APCA_API_SECRET_KEY = alpaca_prompter(slow.printer)
        # Compile/recompile Alpaca key dictionary
        alpaca_key_dict = {
                           'acc_key' : APCA_API_KEY_ID,
                           'auth_key': APCA_API_SECRET_KEY
                          }
        # Ask for new Alpaca keys while is_str_dictionary returns False
        while is_str_dictionary(alpaca_key_dict) is False:
            slow.printer("\nEnsure all Alpaca key values are Strings")
            APCA_API_KEY_ID, \
            APCA_API_SECRET_KEY = alpaca_prompter(slow.printer)
            alpaca_key_dict = {
                               'acc_key' : APCA_API_KEY_ID,
                               'auth_key': APCA_API_SECRET_KEY
                              }
        # Instantiate Alpaca REST and Stream
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
        # Connect to Alpaca and get status
        try:
            slow.printer("Connecting to Alpaca...")
            account = alpaca.get_account()
            slow.printer(f"Logged in as: {APCA_API_KEY_ID}")
            slow.printer(f"Your account status: {account.status}")
        # Exit if authentication fails
        except HTTPError as error:
            slow.printer("Error occurred during Alpaca login. Retry")
            slow.printer(str(error))
            exit(slow.printer)
        # Save Alpaca keys if successful
        try:
            # Ask to save new Alpaca keys and replace old Alpaca keys
            if input_confirmation("Save Alpaca Login? This will replace \
                                  any previously saved keys. (y/n)?",
                                  slow.printer):
                # Try to pickle Alpaca Login dictionary
                save_key_dict('alpaca.key', alpaca_key_dict)
                slow.printer("Alpaca keys saved.")
            else:
                slow.printer("Alpaca keys not saved.")
        # Print error but do not exit script if exception is raised
        except (AttributeError, ImportError, KeyError) as error:
                slow.printer("Alpaca keys not saved due to Error!")
                slow.printer(str(error))
        # Load Twilio keys
        try:
            load_key_dict('twilio.key')
            TWLO_SID_KEY = twilio_key_dict['acc_key']
            TWLO_AUTH_TOKEN = twilio_key_dict['auth_key']
            TWLO_PHONE_NUM = twilio_key_dict['phone_num']
            TWLO_USER_NUM = twilio_key_dict['user_num']
            slow.printer(f"Found Twilio account: {TWLO_SID_KEY}")
            if not input_confirmation(slow.printer):
                TWLO_SID_KEY, \
                TWLO_AUTH_TOKEN, \
                TWLO_PHONE_NUM, \
                TWLO_USER_NUM = twilio_prompter(slow.printer)
        # Asks for new keys if Twilio keys could not be loaded
        except (FileNotFoundError, AttributeError, ImportError,
                KeyError) as error:
            slow.printer(str(error))
            slow.printer("\nError loading Twilio keys from ~/Trading/trading")
            TWLO_SID_KEY, \
            TWLO_AUTH_TOKEN, \
            TWLO_PHONE_NUM, \
            TWLO_USER_NUM = twilio_prompter(slow.printer)
        # Create/recompile Twilio key dictionary
        twilio_key_dict = {
                           'acc_key'  : TWLO_SID_KEY,
                           'auth_key' : TWLO_AUTH_TOKEN,
                           'phone_num': TWLO_PHONE_NUM,
                           'user_num' : TWLO_USER_NUM
                          }
        # Ask for new Twilio keys while is_str_dictionary returns False
        while is_str_dictionary(twilio_key_dict) is False:
            slow.printer("\nEnsure all Twilio key values are Strings")
            TWLO_SID_KEY, \
            TWLO_AUTH_TOKEN, \
            TWLO_PHONE_NUM, \
            TWLO_USER_NUM = alpaca_prompter(slow.printer)
            twilio_key_dict = {
                               'acc_key'  : TWLO_SID_KEY,
                               'auth_key' : TWLO_AUTH_TOKEN,
                               'phone_num': TWLO_PHONE_NUM,
                               'user_num' : TWLO_USER_NUM
                              }
        # Instantiate Twilio Client and send SMS Alert
        try:
            twilio = Client(TWLO_SID_KEY, TWLO_AUTH_TOKEN)
            sms_alert(twilio, TWLO_PHONE_NUM, TWLO_USER_NUM,
                      alert=f"ALERT! Logged in on: {socket.gethostname()}")
            slow.printer(f"Alert sent to: {TWLO_USER_NUM}")
        # Exit and print error if Twilio fails
        except TwilioRestException as error:
            slow.printer(str(error))
            slow.printer(f"! Could not sent alert to {TWLO_USER_NUM} !")
            exit(slow.printer)
        # Save Twilio keys if successful
        try:
            # Ask to save new Twilio keys and replace old Twilio keys
            if input_confirmation("Save Twilio Login? This will replace any \
                                  previously saved keys. (y/n)?",
                                  slow.printer):
                save_key_dict('twilio.key', twilio_key_dict)
                slow.printer("Twilio Login saved.")
            else:
                slow.printer("Twilio Login not saved.")
        # Print error but do not exit script if exception is raised
        except (AttributeError, ImportError, KeyError) as error:
            slow.printer("Twilio keys not saved due to Error!")
            slow.printer(str(error))
    # Exit gracefully if KeyboardInterrupt is raised.
    except KeyboardInterrupt:
        slow.printer("\nLogin cancelled by user.")
        exit(slow.printer)
    # Return tuple of necessary objects
    else:
        return alpaca, stream, twilio, slow

# Connection class stores outputs of 'login'
class Connection:
    def __init__(
                 self,
                 APCA_API_BASE_URL="https://paper-api.alpaca.markets",
                 data_feed='sip',
                 locked=False
                ) -> None:
        alpaca, stream, twilio, slow = login(APCA_API_BASE_URL,
                                             data_feed,
                                             disable_slowprint=False)
        self.alpaca,
        self.stream,
        self.twilio,
        self.slow =
        self.locked = locked
        self.timestamp = get_timestr()
        self.slow.printer("Connection successful: " + self.timestamp)

    # Set lock attribute to True
    def lock(self) -> None:
        self.locked = True
        self.slow.printer("Connection locked.")

    # Set lock attribute to False
    def unlock(self) -> None:
        self.locked = False
        self.slow.printer("Connection unlocked.")

    # Return lock: bool attribute
    def is_locked(self) -> bool:
        return self.locked

    # Return timestamp string
    def get_start_time(self) -> str:
        return self.timestamp
