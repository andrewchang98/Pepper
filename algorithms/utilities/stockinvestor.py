from alpaca_trade_api.stream import Stream

class Bot:
    def __init__(self, name, symbol, initial_buying_power, account, stream):
        self.name = name
        self.symbol = symbol
        self.totalvalue = initial_buying_power
        self.account = account
        self.stream = stream
