from utilities import boot
from utilities import slowprinter.Printer

slow = Printer()

# LOGIN AND ASSIGN ALPACA AND STREAM OBJECTS
try:
    bot = login.Connection()
except RecursionError as error:
    slow.printer(str(error))
