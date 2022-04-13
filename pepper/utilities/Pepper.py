"""
Pepper class stores outputs of Boot
Provides an abstraction layer above the Alpaca API
"""
from utilities.Printer import Printer
from utilities.boot import boot, sms_alert, get_datetime

class Pepper:
    def __init__(self,
                 APCA_API_BASE_URL="https://paper-api.alpaca.markets",
                 data_feed='sip',
                 tz='pst',
                 disable_slowprinter=False):
        self.alpaca, \
        self.stream, \
        self.twilio = boot(APCA_API_BASE_URL, data_feed, disable_slowprinter)
        self.locked = True
        self.timezone = tz
        self.timestamp = get_datetime(tz)
        self.slow = Printer(50, disable_slowprinter)

    # Very special ohyeppep Printer
    def ohyep(self, message="Oh yep, Pep!") -> None:
        self.slow.printer(message)

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

    # Pepper hunts for prey in symbol_list
    def hunt(self, symbol_list: list):
        pass

    # Pepper drops everything and prepares for the impending economic crisis
    def panic(self):
        self.ohyep('Pep says: "Holy Jesus!"')
        pass

    def pray(self):
        self.ohyep("Hail, Mary, full of grace,")
        self.ohyep("the Lord is with thee.")
        self.ohyep("Blessed art thou amongst women")
        self.ohyep("and blessed is the fruit of thy womb, Jesus.")
        self.ohyep("Holy Mary, Mother of God,")
        self.ohyep("pray for us sinners,")
        self.ohyep("now and at the hour of our death.")
        self.ohyep("Amen.")
