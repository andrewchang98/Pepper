"""
Pepper class stores outputs of Boot
Provides an abstraction layer above the Alpaca API

"""

from utilities.boot import begin
from utilities.boot import sms_alert
from utilities.pepper import Pepper
from utilities.slowprinter import Printer

class Pepper:
    
























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
