"""
Pepper class stores outputs of Boot
Provides an abstraction layer above the Alpaca API
"""
from utilities.Printer import Printer
from utilities.boot import boot, get_datetime

class Pepper:
    def __init__(
                 self,
                 symbols: set,
                 base_url="https://paper-api.alpaca.markets",
                 data_feed='sip',
                 enable_printer=True,
                 timezone='pst'
                ):
        self.symbols = symbols
        self.broker, \
        self.stream, \
        self.sms = boot(base_url, data_feed, enable_printer)
        self.timestamp = get_datetime(timezone)
        self.timezone = timezone
        self.locked = True
        self.slow = Printer(50, enable_printer)
        self.ohyep("Pep is looking for:", end='')
        for symbol in symbols:
            self.ohyep(' ', end='')
            self.ohyep(symbol, sep=' ', end='')
        self.ohyep()

    # Very special ohyeppep Printer
    def ohyep(self, message='', sep=' ', end='\n') -> None:
        self.slow.printer(message, sep=sep, end=end)

    # Lock Pepper inside so she cannot hunt
    def lock(self) -> None:
        self.locked = True
        self.ohyep("Pep cannot hunt.")

    # Unlock the door so Pepper can hunt outside
    def unlock(self) -> None:
        self.locked = False
        self.ohyep("Pep can hunt!")

    # Pepper pounces on prey (buy position)
    def pounce(self):
        self.ohyep("Pep is getting ready to pounce...")
        self.ohyep("Pep decided to pounce!")
        self.ohyep("Pep missed! Meow!")
        pass

    # Pepper drops prey off at the door (sell position)
    def drop(self):
        pass

    # Pepper steps without pouncing or dropping (hold position)
    def step(self):
        pass

    # Pepper hunts for prey in symbol_set
    def hunt(self):
        for symbol in self.symbols:
            pass

    # Pepper drops everything and prepares for the impending economic crisis
    def panic(self):
        self.ohyep('Pep says: "Holy Jesus!"')
        pass

    def hailmary(self):
        self.ohyep("Hail, Mary, full of grace,")
        self.ohyep("the Lord is with thee.")
        self.ohyep("Blessed art thou amongst women")
        self.ohyep("and blessed is the fruit of thy womb, Jesus.")
        self.ohyep("Holy Mary, Mother of God,")
        self.ohyep("pray for us sinners,")
        self.ohyep("now and at the hour of our death.")
        self.ohyep("Amen.")
