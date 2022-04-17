import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def send_sms(number):
    account_sid = 'ACe773103d0aa90393b53f2b9e0766b424'
    auth_token = 'eecf77c6301e444d96cb878905bbbf04'
    client = Client(account_sid, auth_token)
 
    message = client.messages \
        .create(
            body='Someone has signed up for volunteering your organization',
            from_='+19034156505',
            to=number
        )

    print(message.sid)

