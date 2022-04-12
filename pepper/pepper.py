from utilities import boot
from utilities.slowprinter import Printer

slow = Printer()

# LOGIN AND ASSIGN ALPACA AND STREAM OBJECTS
try:
    bot = boot.Connection()
except RecursionError as error:
    slow.printer(str(error))
