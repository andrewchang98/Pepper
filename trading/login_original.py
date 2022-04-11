

def login(APCA_API_BASE_URL="https://paper-api.alpaca.markets"):
    try:
        slow = Printer(delay=0.05)
        slow.printer("Loading account info...")
        try:
            from passwords import alpaca_keys as keys
        except ImportError:
            slow.printer("Did not find Alpaca account in \
                         ~/Trading/trading/passwords.py")
            APCA_API_KEY_ID, APCA_API_SECRET_KEY = prompter(slow.printer,
                                                            " to Alpaca:")
        else:
            slow.printer("Log in as {} (y/n)?".format(keys['acc_key']), end=' ')
            response = input()
            read_input
            if response == 'y' or response == 'Y':
                APCA_API_KEY_ID = keys['acc_key']
                APCA_API_SECRET_KEY = keys['auth_key']
            elif response == 'n' or response == 'N':
                APCA_API_KEY_ID, APCA_API_SECRET_KEY = prompter(slow.printer,
                                                                " to Alpaca:")
            else:
                slow.printer("\nCancelled by user. Exiting now.")
                sys.exit(0)
        slow.printer("\nConnecting to Alpaca servers...\n")
        try:
            alpaca = REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                                   APCA_API_BASE_URL)
            stream = Stream(APCA_API_KEY_ID, APCA_API_SECRET_KEY,
                                   APCA_API_BASE_URL)
        except:
            slow.printer("Something went wrong. Inspect Alpaca keys and code.")
            slow.printer("Exiting now.")
            sys.exit(0)
        else:
            slow.printer("Logged in as {}".format(APCA_API_KEY_ID))
            account = alpaca.get_account()
            slow.printer("Your account is: {}".format(account.status))
            slow.printer("Would you like to enable Twilio SMS text alerts \
                         (y/n)?")
            response = input()
            if read_input(response, slow, 'y', 'Y'):
                try:
                    from passwords import twilio_keys as keys
                    slow.printer("Login as {} (y/n)?".format(keys['phone_num']),
                                 end=' ')
                    response = input()
                except ImportError:
                    slow.printer("Did not find Twilio account in )
            elif read_input(response, slow, 'n', 'N'):
                TWILIO_SID_KEY, TWILIO_AUTH_KEY = prompter(slow.printer,
                                                           " to Twilio:")
            else:
                return alpaca, stream
    except KeyboardInterrupt:
        slow.printer("\nLogin cancelled by user.")
        exit()
