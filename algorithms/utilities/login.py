import sys
from prompter import prompter
from pydexcom import Dexcom
from slowprinter import Printer

# MAIN ROUTINE TO LOAD ACCOUNT INFO
def login():
    # TRY TO LOAD PASSWORDS FILE
    ui = Printer(delay=0.05)
    ui.printer('Loading account info...')
    try:
        import passwords
    except ImportError:
        ui.printer('No account info found in ~/Dexlink/')
        DEXCOM_USERNAME, DEXCOM_PASSWORD = prompter(ui.printer)
    else:
        # ASK TO LOGIN AS USER
        ui.printer('Login as {} (Y/n)?'.format(passwords.account[0]), end=' ')
        try:
            keystroke = input()
            if keystroke == 'y' or keystroke == 'Y':
                DEXCOM_USERNAME = passwords.account[0]
                DEXCOM_PASSWORD = passwords.account[1]
            elif keystroke == 'n' or keystroke == 'N':
                DEXCOM_USERNAME, DEXCOM_PASSWORD = prompter(ui.printer)
            else:
                ui.printer('\nCancelled by user. Exiting now.')
                sys.exit(0)
        except KeyboardInterrupt:
            ui.printer('\nCancelled by user. Exiting now.')
            sys.exit(0)
    # CONNECT TO DEXCOM SHARE API
    try:
        ui.printer('\nConnecting to Dexcom servers...')
        dexcom = Dexcom(DEXCOM_USERNAME, DEXCOM_PASSWORD)
    except:
        ui.printer('\nLogin failed. Please check username and password.')
        ui.printer('Exiting now.')
        sys.exit(0)
    else:
        ui.printer('Logged in as {}\n'.format(DEXCOM_USERNAME))
        return dexcom
