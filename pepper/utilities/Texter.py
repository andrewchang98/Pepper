from twilio.rest import Client
from twilio.base.exceptions import TwilioException, TwilioRestException

# Twilio SMS Texter class
class Texter:
    def __init__(
                 self,
                 acc_key: str,
                 auth_key: str,
                 phone_num: str,
                 target_num: str
                ):
        # Instantiate Twilio Client
        self.client = Client(acc_key, auth_key)
        self.phone_num = phone_num
        self.target_num = target_num

    # Send SMS text method
    def text(self, *args, sep=' ') -> str:
        sep = str(sep)
        message = sep.join(map(str, args))
        body = self.client.messages.create(
                                      to=self.target_num,
                                      from_=self.phone_num,
                                      body=message
                                     )
        return message
