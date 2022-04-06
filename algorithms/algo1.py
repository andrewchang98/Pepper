import sys
import datetime
import alpaca_trade_api as tradeapi
from utilities import login

# LOGIN AND ASSIGN ALPACA AND STREAM OBJECTS
alpaca, stream = login.account(BASE_URL='https://paper-api.alpaca.markets',
                        attempts=3)
