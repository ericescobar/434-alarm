#!/usr/bin/python
def sms(phoneNumber, messageSMS):
        from twilio.rest import TwilioRestClient
        account = ""
        token = ""
        client = TwilioRestClient(account, token)
        message = client.messages.create(
                to=phoneNumber,
                from_="+1xxxxxxxxxx",
                body=messageSMS,
        )

