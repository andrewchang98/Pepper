"""
 ___________________________________________________________
|   !!! DANGER !!!                                          |
|   NEVER SHARE OR STORE THIS FILE PUBLICLY AFTER EDITING   |
|___________________________________________________________|

Optional example password file imported by 'login.py'
If file cannot be imported or key dictionaries are improperly formatted,
'login.py' will ask the user to input proper credentials.

(1) COPY THIS FILE TO 'passwords.py':
$ cd ~/Trading/trading
$ sudo cp passwords_example.py passwords.py

(2) OPEN 'passwords.py':
$ cd ~/Trading/trading
$ sudo nano passwords.py

(3) EDIT VALUES IN 'alpha_key_dict' and 'twilio_key_dict':
NOTE: All user info MUST be <class 'str'>!
"""

# Password Dictionary File
# DO NOT STORE THIS FILE PUBLICLY!
# NEVER SHARE YOUR ACCOUNT INFORMATION!
alpaca_key_dict = {
                   'acc_key'  : '<APCA_API_KEY_ID>',
                   'auth_key' : '<APCA_API_SECRET_KEY>'
                  }

twilio_key_dict = {
                   'acc_key'  : '<TWILIO_ACCOUNT_SID>',
                   'auth_key' : '<TWILIO_AUTH_TOKEN>',
                   'phone_num': '<TWILIO_PHONE_NUM>',
                   'user_num' : '<USER_PHONE_NUM>'
                  }
