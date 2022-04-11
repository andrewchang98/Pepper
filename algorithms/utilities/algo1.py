import sys
import datetime
import alpaca_trade_api as tradeapi
from login import login

# LOGIN AND ASSIGN ALPACA AND STREAM OBJECTS
alpaca, stream = login(BASE_URL='https://paper-api.alpaca.markets')
