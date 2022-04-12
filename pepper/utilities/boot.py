"""
Boot file contains begin() function to begin an Alpaca + Twilio session.
Provides abstraction barrier for logging in.
Looks for 'alpaca.key' and 'twilio.key' Pickle files.
Prompts manual user for service if respective .key file is not found.

!!! NEVER SHARE YOUR *.key FILES !!!

This file also contains helper functions to facilitate.
"""

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
from utilities.slowprinter import Printer

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
def get_timestr(tz='pst', date_format='%I:%M:%S %p %m/%d/%Y %Z') -> str:
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
    timestr = get_timestr('pst', date_format='%I:%M %p %m/%d/%Y')
    body = twilio.messages.create(to=receiver,
                                  from_=sender,
                                  body=alert+' '+timestr)

# Checks if response matches any args
def read_input(response: str, *args: str) -> bool:
    for char in args:
        if response == char:
            return True
    return False

# Asks user yes or no
def input_confirmation(message="Continue (y/n)?", printer=print) -> bool:
    printer(message, end=' ')
    response = input()
    if read_input(response, 'y', 'Y'):
        return True
    elif read_input(response, 'n', 'Y'):
        return False
    else:
        return input_confirmation(printer)

# The Alpaca + Twilio Login Function that does it all
def begin(APCA_API_BASE_URL="https://paper-api.alpaca.markets",
          data_feed='sip',
          disable_slowprinter=False,
          char_per_sec=50,
          max_attempts=3) -> tuple:
    # Main Try clause
    try:
        # Instantiate char by char printer
        slow = Printer(char_per_sec, disable_slowprinter)
        # Load Alpaca keys
        try:
            alpaca_key_dict = load_key_dict('alpaca.key')
            APCA_API_KEY_ID = alpaca_key_dict['acc_key']
            APCA_API_SECRET_KEY = alpaca_key_dict['auth_key']
            slow.printer(f"Loaded Alpaca account: {APCA_API_KEY_ID}")
            from_alpaca_save = True
            # Asks for new keys if User declines loaded keys
            if not input_confirmation("Continue with loaded account (y/n)?",
                                      slow.printer):
                from_alpaca_save = False
                APCA_API_KEY_ID, \
                APCA_API_SECRET_KEY = alpaca_prompter(slow.printer)
        # Asks for new Alpaca keys if Alpaca keys could not be loaded
        except (FileNotFoundError, AttributeError, ImportError,
                KeyError) as error:
            slow.printer("\nError loading Alpaca keys from " + \
                         "~/Peppaboot/peppaboot/utilities:")
            slow.printer(str(error))
            from_alpaca_save = False
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
            from_alpaca_save = False
            APCA_API_KEY_ID, \
            APCA_API_SECRET_KEY = alpaca_prompter(slow.printer)
            alpaca_key_dict = {
                               'acc_key' : APCA_API_KEY_ID,
                               'auth_key': APCA_API_SECRET_KEY
                              }
        # Connect to Alpaca and get status
        try:
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
            slow.printer("Connecting to Alpaca...")
            account = alpaca.get_account()
            slow.printer(f"Logged in as: {APCA_API_KEY_ID}")
            slow.printer(f"Your account status: {account.status}")
        # Exit if authentication fails
        except (HTTPError, ValueError) as error:
            slow.printer("Error occurred during Alpaca login:")
            slow.printer(str(error))
            # Recurse Login with one less Login attempt
            max_attempts -= 1
            # Check max_attempts
            if max_attempts < 1:
                raise RecursionError("No attempts remaining.")
            slow.printer(f"You have {str(max_attempts)} more attempts.")
            return begin(APCA_API_BASE_URL,
                         data_feed,
                         disable_slowprinter,
                         char_per_sec,
                         max_attempts)
        # Save Alpaca keys if successful
        try:
            if not from_alpaca_save:
                # Ask to save new Alpaca keys and replace old Alpaca keys
                if input_confirmation("Save Alpaca Login? This will " + \
                                      "replace any previously saved keys. " + \
                                      "(y/n)?",
                                      slow.printer):
                    # Try to pickle Alpaca Login dictionary
                    save_key_dict('alpaca.key', alpaca_key_dict)
                    slow.printer("Alpaca keys saved.")
                else:
                    slow.printer("Alpaca keys not saved.")
        # Print error but do not exit script if exception is raised
        except (AttributeError, ImportError, KeyError) as error:
                slow.printer("Alpaca keys not saved due to Error:")
                slow.printer(str(error))
        # Load Twilio keys
        try:
            twilio_key_dict = load_key_dict('twilio.key')
            TWLO_SID_KEY = twilio_key_dict['acc_key']
            TWLO_AUTH_TOKEN = twilio_key_dict['auth_key']
            TWLO_PHONE_NUM = twilio_key_dict['phone_num']
            TWLO_USER_NUM = twilio_key_dict['user_num']
            slow.printer(f"Found Twilio account: {TWLO_SID_KEY}")
            from_twilio_save = True
            if not input_confirmation("Continue with loaded account (y/n)?",
                                      slow.printer):
                from_twilio_save = False
                TWLO_SID_KEY, \
                TWLO_AUTH_TOKEN, \
                TWLO_PHONE_NUM, \
                TWLO_USER_NUM = twilio_prompter(slow.printer)
        # Asks for new keys if Twilio keys could not be loaded
        except (FileNotFoundError, AttributeError, ImportError,
                KeyError) as error:
            slow.printer("\nError loading Twilio keys from " + \
                         "~/Peppaboot/peppaboot/utilities:")
            slow.printer(str(error))
            from_twilio_save = False
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
            from_twilio_save = False
            TWLO_SID_KEY, \
            TWLO_AUTH_TOKEN, \
            TWLO_PHONE_NUM, \
            TWLO_USER_NUM = twilio_prompter(slow.printer)
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
                      alert=f"ALERT! Logged in on {socket.gethostname()}:")
            slow.printer(f"Alert sent to: {TWLO_USER_NUM}")
        # Exit and print error if Twilio fails
        except (TwilioRestException, ValueError) as error:
            slow.printer("Error occured while sending alert to " + \
                         f"{TWLO_USER_NUM}:")
            slow.printer(str(error))
            # Recurse Login with one less Login attempt
            max_attempts -= 1
            # Check max_attempts
            if max_attempts < 1:
                raise RecursionError("No attempts remaining.")
            slow.printer(f"You have {str(max_attempts)} more attempts.")
            return begin(APCA_API_BASE_URL,
                         data_feed,
                         disable_slowprinter,
                         char_per_sec,
                         max_attempts)
        # Save Twilio keys if successful
        try:
            if not from_twilio_save:
                # Ask to save new Twilio keys and replace old Twilio keys
                if input_confirmation("Save Twilio Login? This will replace" + \
                                      " any previously saved keys. (y/n)?",
                                      slow.printer):
                    save_key_dict('twilio.key', twilio_key_dict)
                    slow.printer("Twilio Login saved.")
                else:
                    slow.printer("Twilio Login not saved.")
        # Print error but do not exit script if exception is raised
        except (AttributeError, ImportError, KeyError) as error:
            slow.printer("Twilio keys not saved due to Error:")
            slow.printer(str(error))
    # Exit gracefully if KeyboardInterrupt is raised.
    except KeyboardInterrupt:
        slow.printer("\nLogin cancelled by user.\nExiting Now.")
        sys.exit(0)
    # Return tuple of necessary objects
    else:
        return alpaca, stream, twilio
