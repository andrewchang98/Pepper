import sys
import datetime
import alpaca_trade_api as tradeapi
from utilities import login

# LOGIN AND ASSIGN ALPACA OBJECT
alpaca = login.account(BASE_URL='https://paper-api.alpaca.markets',
                        attempts=3)

# PRINT ACCOUNT DETAILS
print(alpaca.get_account())
