from sys import stdout, exit
from time import sleep

# CHARACTER BY CHARACTER PRINT FUNCTION
class Printer:
    def __init__(self, char_per_sec:int=50, disabled:bool=False):
        self.disabled = disabled
        if char_per_sec < 1:
            char_per_sec = 1
        self.delay = 1 / char_per_sec


    # MAIN FUNCTION
    def printer(self, string, end='\n'):
        try:
            if self.disabled:
                print(string, end=end)
            else:
                for char in string:
                    stdout.write(char)
                    stdout.flush()
                    sleep(self.delay)
                if end is not None:
                    stdout.write(end)
                    stdout.flush()
        except KeyboardInterrupt:
            print("\nCancelled by user. Exiting now.")
            exit(0)


    # ENABLE SLOW PRINTS
    def enable_printer(self):
        self.disabled = False

    # USE REGULAR PRINTS
    def disable_printer(self):
        self.disabled = True

    # Change print speed in character/second
    def change_char_per_sec(self, char_per_sec:int=50):
        self.delay = char_per_sec

    # Change delay between prints directly
    def change_delay(self, delay:float=0.02):
        self.delay = delay
