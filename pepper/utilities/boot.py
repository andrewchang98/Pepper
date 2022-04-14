"""
Boot file contains boot() function to start an Alpaca + Twilio session.
Provides abstraction barrier for logging in.
Looks for 'alpaca.key' and 'twilio.key' Pickle files.
Prompts manual user for service if respective .key file is not found.

!!! NEVER SHARE YOUR *.key FILES !!!

This file also contains helper functions such as:

get_timestr(tz, date_format)
"""
import os
import sys
import socket
import pickle
from pathlib import Path, PosixPath
import pytz
from pytz import timezone
from getpass import getpass
from datetime import datetime
from requests.exceptions import HTTPError
from twilio.rest import Client
from twilio.base.exceptions import TwilioException, TwilioRestException
from alpaca_trade_api import REST
from alpaca_trade_api.stream import Stream
from utilities.Printer import Printer
from utilities.Texter import Texter

# Change this string if you plan on renaming the Key File Folder
path = 'keys'

# Pickle key_dict to file_name
def save_key_dict(file_name: str, key_dict: dict) -> None:
    current_directory = Path(__file__).parent
    file = open(os.path.join(current_directory, path, file_name), 'wb')
    pickle.dump(key_dict, file, pickle.HIGHEST_PROTOCOL)

# Unpickle key_dict to file_name
def load_key_dict(file_name: str) -> dict:
    current_directory = Path(__file__).parent
    file = open(os.path.join(current_directory, path, file_name), 'rb')
    key_dict = pickle.load(file)
    return key_dict

# Ask for Alpaca Credentials in the CLI
def alpaca_prompter(printer=print) -> tuple:
    printer("Log into Alpaca:")
    printer("API Key ID:", end=' ')
    acc_key = input()
    printer("Secret Key:", end=' ')
    auth_key = getpass(prompt='')
    return acc_key, auth_key

# Ask for Twilio Credentials in the CLI
def twilio_prompter(printer=print) -> tuple:
    printer("Log into Twilio:")
    printer("\nAccount SID:", end=' ')
    acc_key = input()
    printer("Auth Token:", end=' ')
    auth_key = getpass(prompt='')
    printer("Twilio Phone Number:", end=' ')
    phone_num = input()
    printer("Target Phone Number:", end=' ')
    target_num = input()
    return acc_key, auth_key, phone_num, target_num

# Returns True if all values in a dictionary are <class 'str'>, else False
def verify_key_dict(dict):
    for item in dict:
        if type(dict[item]) is not str:
            return False
    return True

# Get datetime in PST or UTC
def get_datetime(tz='pst') -> datetime:
    utc = datetime.now(tz=pytz.utc)
    pst = utc.astimezone(timezone('US/Pacific'))
    if tz == 'pst':
        return pst
    if tz == 'utc':
        return utc
    else:
        raise TypeError("Not a recognized timezone.")

# Get UTC or PST string
def get_timestr(tz='pst', date_format='%I:%M:%S %p %m/%d/%Y %Z') -> str:
    dt = get_datetime(tz)
    return dt.strftime(date_format)

# Checks if response matches any args
def read_input(response: str, *args: str) -> bool:
    for char in args:
        if response == char:
            return True
    return False

# Asks user yes or no
def input_confirmation() -> bool:
    response = input()
    if read_input(response, 'y', 'Y'):
        return True
    elif read_input(response, 'n', 'Y'):
        return False
    else:
        return input_confirmation()

# The Alpaca + Twilio boot Function that does it all
def boot(APCA_API_BASE_URL="https://paper-api.alpaca.markets",
          data_feed='sip',
          enable_printer=False,
          char_per_sec=50,
          max_attempts=3) -> tuple:
    # Main Try clause
    try:
        # Instantiate char by char printer
        slow = Printer(char_per_sec, enable_printer)
        # Load Alpaca keys
        try:
            alpaca_key_dict = load_key_dict('alpaca.key')
            APCA_API_KEY_ID = alpaca_key_dict['acc_key']
            APCA_API_SECRET_KEY = alpaca_key_dict['auth_key']
        # Asks for new Alpaca keys if Alpaca keys could not be loaded
        except (FileNotFoundError, AttributeError, ImportError,
                KeyError) as error:
            slow.printer("\nError loading Alpaca keys from",
                         "~/Peppaboot/peppaboot/utilities/keys:")
            slow.printer(str(error))
            from_alpaca_save = False
            APCA_API_KEY_ID, \
            APCA_API_SECRET_KEY = alpaca_prompter(slow.printer)
        else:
            slow.printer("Loaded Alpaca account:", APCA_API_KEY_ID)
            from_alpaca_save = True
            # Asks for new keys if User declines loaded keys
            slow.printer("Continue with loaded account (y/n)?", end=' ')
            if not input_confirmation():
                from_alpaca_save = False
                APCA_API_KEY_ID, \
                APCA_API_SECRET_KEY = alpaca_prompter(slow.printer)
                # Compile/recompile Alpaca key dictionary
                alpaca_key_dict = {
                                   'acc_key' : APCA_API_KEY_ID,
                                   'auth_key': APCA_API_SECRET_KEY
                                  }
        # Ask for new Alpaca keys while verify_key_dict returns False
        while verify_key_dict(alpaca_key_dict) is False:
            slow.printer("\nAlpaca keys corrupted!. Re-enter keys.")
            slow.printer("Keep access to key files restricted!")
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
            slow.printer("Connecting to Alpaca...")
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
            account = alpaca.get_account()
            slow.printer(f"Logged in as: {APCA_API_KEY_ID}")
            slow.printer(f"Your account status: {account.status}")
        # Recurse boot if authentication fails
        except (HTTPError, ValueError) as error:
            slow.printer("Error occurred during Alpaca login:")
            slow.printer(str(error))
            # Recurse boot with one less attempt
            max_attempts -= 1
            # Check max_attempts
            if max_attempts < 1:
                raise RecursionError("No attempts remaining.")
            slow.printer(f"You have {str(max_attempts)} more attempts.")
            return boot(APCA_API_BASE_URL,
                         data_feed,
                         enable_printer,
                         char_per_sec,
                         max_attempts)
        # Save Alpaca keys if successful
        try:
            if not from_alpaca_save:
                # Ask to save new Alpaca keys and replace old Alpaca keys
                slow.printer("Remember Alpaca login? (y/n)?", end=' ')
                if input_confirmation():
                    # Pickle Alpaca key dictionary
                    save_key_dict('alpaca.key', alpaca_key_dict)
                    slow.printer("Alpaca keys saved.")
                else:
                    slow.printer("Alpaca keys not saved.")
        # Print error but do not exit script if exception is raised
        except (FileNotFoundError, AttributeError, ImportError,
                KeyError) as error:
                slow.printer("Alpaca keys not saved due to Error:")
                slow.printer(str(error))
        # Load Twilio keys
        try:
            twilio_key_dict = load_key_dict('twilio.key')
            TWLO_SID_KEY = twilio_key_dict['acc_key']
            TWLO_AUTH_TOKEN = twilio_key_dict['auth_key']
            TWLO_PHONE_NUM = twilio_key_dict['phone_num']
            TWLO_TARGET_NUM = twilio_key_dict['target_num']
            slow.printer(f"Found Twilio account: {TWLO_SID_KEY}")
            from_twilio_save = True
            slow.printer("Continue with loaded account (y/n)?", end=' ')
            if not input_confirmation():
                from_twilio_save = False
                TWLO_SID_KEY, \
                TWLO_AUTH_TOKEN, \
                TWLO_PHONE_NUM, \
                TWLO_TARGET_NUM = twilio_prompter(slow.printer)
        # Asks for new keys if Twilio keys could not be loaded
        except (FileNotFoundError, AttributeError, ImportError,
                KeyError) as error:
            slow.printer("\nError loading Twilio keys from",
                         "~/Peppaboot/peppaboot/utilities/keys:")
            slow.printer(str(error))
            from_twilio_save = False
            TWLO_SID_KEY, \
            TWLO_AUTH_TOKEN, \
            TWLO_PHONE_NUM, \
            TWLO_TARGET_NUM = twilio_prompter(slow.printer)
        # Create/recompile Twilio key dictionary
        twilio_key_dict = {
                           'acc_key'  : TWLO_SID_KEY,
                           'auth_key' : TWLO_AUTH_TOKEN,
                           'phone_num': TWLO_PHONE_NUM,
                           'target_num' : TWLO_TARGET_NUM
                          }
        # Ask for new Twilio keys while verify_key_dict returns False
        while verify_key_dict(twilio_key_dict) is False:
            slow.printer("\nTwilio key file is corrupted!. Re-enter keys.")
            slow.printer("Keep access to key files restricted!")
            from_twilio_save = False
            TWLO_SID_KEY, \
            TWLO_AUTH_TOKEN, \
            TWLO_PHONE_NUM, \
            TWLO_TARGET_NUM = twilio_prompter(slow.printer)
            twilio_key_dict = {
                               'acc_key'  : TWLO_SID_KEY,
                               'auth_key' : TWLO_AUTH_TOKEN,
                               'phone_num': TWLO_PHONE_NUM,
                               'target_num' : TWLO_TARGET_NUM
                              }
        # Instantiate Twilio Client and Send SMS alert
        try:
            twilio = Texter(
                            TWLO_SID_KEY,
                            TWLO_AUTH_TOKEN,
                            TWLO_PHONE_NUM,
                            TWLO_TARGET_NUM
                           )
            twilio.text(
                        f"Pepper booted on: {socket.gethostname()}",
                        f"Account status: {account.status}",
                        f"Timestamp: {get_timestr()}",
                        sep = '\n'
                       )
            slow.printer(f"Logged in as: {TWLO_SID_KEY}")
            slow.printer(f"Alert sent to: {TWLO_TARGET_NUM}")
        # Recurse boot if authentication or texter fails
        except (TwilioException, TwilioRestException, ValueError) as error:
            slow.printer("Error occurred during Twilio login:")
            slow.printer(str(error))
            # Recurse boot with one less attempt
            max_attempts -= 1
            # Check max_attempts
            if max_attempts < 1:
                raise RecursionError("No attempts remaining.")
            slow.printer(f"You have {str(max_attempts)} more attempts.")
            return boot(APCA_API_BASE_URL,
                         data_feed,
                         enable_printer,
                         char_per_sec,
                         max_attempts)
        # Save Twilio keys if successful
        try:
            if not from_twilio_save:
                # Ask to save new Twilio keys and replace old Twilio keys
                slow.printer("Remember Twilio login (y/n)?", end=' ')
                if input_confirmation():
                    # Pickle Twilio key dictionary
                    save_key_dict('twilio.key', twilio_key_dict)
                    slow.printer("Twilio login saved.")
                else:
                    slow.printer("Twilio login not saved.")
        # Print error but do not exit script if exception is raised
        except (FileNotFoundError, AttributeError, ImportError,
                KeyError) as error:
                slow.printer("Twilio keys not saved due to Error:")
                slow.printer(str(error))
    # Exit gracefully if KeyboardInterrupt is raised.
    except KeyboardInterrupt:
        slow.printer("\nBoot cancelled by user.\nExiting Now.")
        sys.exit(0)
    # Return tuple of necessary objects
    else:
        slow.printer(f"\nBoot completed successfully @ {get_timestr()}\n")
        return alpaca, stream, twilio
