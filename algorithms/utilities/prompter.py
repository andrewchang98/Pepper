import sys
from getpass import getpass
from slowprinter import Printer

# ACCOUNT SUBROUTINE TO PROMPT USER INFO
def prompter(printer=None):
    if printer is None:
        printer = print
    else:
        printer = printer
    printer('Log into Dexcom:')
    try:
        printer('Username:', end=' ')
        username = input()
        password = getpass()
    except KeyboardInterrupt:
        print('\nCancelled by user. Exiting now.')
        sys.exit(0)
    else:
        return username, password
