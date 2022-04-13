"""
A char by char Printer class

ex:
$ cd ~/Pepper/pepper/utilities
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
    def __init__(self, char_per_sec=50, disabled=False):
        self.disabled = disabled
        if char_per_sec < 1:
            char_per_sec = 1
        self.delay = 1 / char_per_sec

    # Main printer function
    # NOTE: Can only take in one string for now. No separator argument.
    def printer(self, message: str, end='\n') -> None:
        try:
            if self.disabled:
                print(message, end=end)
            else:
                for char in message:
                    stdout.write(char)
                    stdout.flush()
                    sleep(self.delay)
                if type(end) is str:
                    stdout.write(end)
                    stdout.flush()
        except KeyboardInterrupt:
            printer("\nCancelled by user.\nExiting Now.")
            exit(0)

    # Enable slow printing
    def enable_printer(self) -> None:
        self.disabled = False

    # Use built-in print() function
    def disable_printer(self) -> None:
        self.disabled = True

    # Change print speed in character/second
    def change_char_per_sec(self, char_per_sec=50) -> None:
        self.delay = char_per_sec

    # Change delay between prints directly
    def change_delay(self, delay=0.02) -> None:
        self.delay = delay
