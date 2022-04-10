import sys
from prompter import prompter
from pydexcom import Dexcom
from slowprinter import Printer

# MAIN ROUTINE TO LOAD ACCOUNT INFO
def login():
    # TRY TO LOAD PASSWORDS FILE
    rp = Printer(delay=0.05)
    rp.printer('Loading account info...')
    try:
        import passwords
    except ImportError:
        rp.printer('No account info found in ~/Trading')
        DEXCOM_USERNAME, DEXCOM_PASSWORD = prompter(rp.printer)
    else:
        # ASK TO LOGIN AS USER
        rp.printer('Login as {} (Y/n)?'.format(passwords.account[0]), end=' ')
        try:
            keystroke = input()
            if keystroke == 'y' or keystroke == 'Y':
                DEXCOM_USERNAME = passwords.account[0]
                DEXCOM_PASSWORD = passwords.account[1]
            elif keystroke == 'n' or keystroke == 'N':
                DEXCOM_USERNAME, DEXCOM_PASSWORD = prompter(rp.printer)
            else:
                rp.printer('\nCancelled by user. Exiting now.')
                sys.exit(0)
        except KeyboardInterrupt:
            rp.printer('\nCancelled by user. Exiting now.')
            sys.exit(0)
    # CONNECT TO DEXCOM SHARE API
    try:
        rp.printer('\nConnecting to Dexcom servers...')
        dexcom = Dexcom(DEXCOM_USERNAME, DEXCOM_PASSWORD)
    except:
        rp.printer('\nLogin failed. Please check username and password.')
        rp.printer('Exiting now.')
        sys.exit(0)
    else:
        rp.printer('Logged in as {}\n'.format(DEXCOM_USERNAME))
        return dexcom
