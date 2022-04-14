"""
A char by char Printer class

ex:
$ cd ~/Pepper/pepper/utilities
$ python3
>>> from Printer import Printer
>>> slow = Printer(100, False)
>>> slow.printer("Wow that printed fast!")
Wow that printed fast!
>>> slow = Printer(50, False)
>>> slow.printer("I like this one.", end=' ')
I like this one. >>> slow = Printer(10, False)
>>> slow.printer(' '.join('SLOW MOTION'))
S L O W   M O T I O N
>>> slow = Printer(10, True)
>>> slow.printer("Just a regular print <3", end="\nEnd.\n")
Just a regular print <3
End.
"""
from sys import stdout, exit
from time import sleep

# Slow printer class
class Printer:
    def __init__(self, char_per_sec=50, enabled=True):
        self.enabled = enabled
        if char_per_sec < 1:
            char_per_sec = 1
        self.delay = 1 / char_per_sec

    # Main printer method that imitates built-in print function
    def printer(self, *args: str, sep=' ', end='\n') -> None:
        sep = str(sep)
        end = str(end)
        if not self.enabled:
            print(*args, sep=sep, end=end)
        message = sep.join(map(str, args))
        for char in message:
            stdout.write(char)
            stdout.flush()
            sleep(self.delay)
        stdout.write(end)
        stdout.flush()

    # Enable slow printing
    def enable_printer(self) -> None:
        self.enabled = True

    # Use built-in print() function
    def disable_printer(self) -> None:
        self.enabled = False

    # Change print speed in character/second
    def change_char_per_sec(self, char_per_sec=50) -> None:
        self.delay = char_per_sec

    # Change delay between prints directly
    def change_delay(self, delay=0.02) -> None:
        self.delay = delay
