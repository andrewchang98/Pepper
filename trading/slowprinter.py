"""
A char by char print function that returns good vibes.

ex:
$ cd ~/Trading/trading
$ python3
>>> from slowprinter import Printer
>>> slow = Printer(100, False)
>>> slow.printer("Wow that printed fast!")
Wow that printed fast!
>>> slow = Printer(50, False)
>>> slow.printer("I like this one.", end=' ')
I like this one. >>> slow = Printer(10, False)
>>> slow.printer("S L O W   M O T I O N")
S L O W   M O T I O N
>>> slow = Printer(10, True)
>>> slow.printer("Just a regular print <3", end="\nEnd.\n")
Just a regular print <3
End.
"""

from sys import stdout, exit
from time import sleep

class Printer:
    def __init__(self, char_per_sec:int=50, disabled:bool=False) -> None:
        self.disabled = disabled
        if char_per_sec < 1:
            char_per_sec = 1
        self.delay = 1 / char_per_sec

    # Main printer function
    # Can only take in one string for now.
    def printer(self, message:str, end:str='\n') -> None:
        try:
            if self.disabled:
                print(message, end=end)
            else:
                for char in string:
                    stdout.write(char)
                    stdout.flush()
                    sleep(self.delay)
                if end is not None:
                    stdout.write(end)
                    stdout.flush()
        except KeyboardInterrupt:
            printer("\nCancelled by user.")
            printer("Exiting now.")
            exit(0)

    # Enable slow printing
    def enable_printer(self) -> None:
        self.disabled = False

    # Use built-in print() function
    def disable_printer(self) -> None:
        self.disabled = True

    # Change print speed in character/second
    def change_char_per_sec(self, char_per_sec:int=50) -> None:
        self.delay = char_per_sec

    # Change delay between prints directly
    def change_delay(self, delay:float=0.02) -> None:
        self.delay = delay
