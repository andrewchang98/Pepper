import login
from slowprinter import Printer

slow = Printer()

# LOGIN AND ASSIGN ALPACA AND STREAM OBJECTS
try:
    bot = login.Connection()
except RecursionError as error:
    slow.printer(str(error))
