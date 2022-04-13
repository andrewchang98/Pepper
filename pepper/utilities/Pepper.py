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
        self.twilio = begin(APCA_API_BASE_URL, data_feed, disable_slowprinter)
        self.locked = True
        self.timezone = tz
        self.timestamp = get_datetime(tz)
        self.slow = Printer(50, disable_slowprinter)

    def lock(self) -> None:
        self.locked = True
        self.slow.printer("Pepper cannot hunt.")

    def unlock(self) -> None:
        self.locked = False
        self.slow.printer("Pepper can hunt!")

    def step(self):
        pass

    def pounce(self):
        self.ohyep("Pepper is getting ready to pounce...")
        self.ohyep("Pepper decided to pounce!")
        self.ohyep("Pepper missed! Meow!")
        pass

    def drop(self):
        pass

    def hunt(self):
        pass

    def panic(self):
        pass

    def ohyep(self, message="Oh yep, pep!") -> None:
        self.slow.printer(message)

























class Connection:
    def __init__(
                 self,
                 APCA_API_KEY_ID="https://paper-api.alpaca.markets",
                 data_feed='sip',
                 locked=False
                ) -> None:
        self.slow = Printer()
        self.alpaca, \
        self.stream, \
        self.twilio = pep(APCA_API_KEY_ID,
                            data_feed,
                            disable_slowprinter=False,
                            char_per_sec=50,
                            max_attempts=3)
        self.locked = locked
        self.timestamp = get_timestr()
        self.slow.printer("Connection successful: " + self.timestamp)

    # Set lock attribute to True
    def lock(self) -> None:
        self.locked = True
        self.slow.printer("Connection locked.")

    # Set lock attribute to False
    def unlock(self) -> None:
        self.locked = False
        self.slow.printer("Connection unlocked.")

    # Return lock: bool attribute
    def is_locked(self) -> bool:
        return self.locked

    # Return timestamp string
    def get_start_time(self) -> str:
        return self.timestamp
