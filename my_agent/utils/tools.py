from twilio.rest import Client
import os

client = Client(
    os.environ["TWILIO_ACCOUNT_SID"],
    os.environ["TWILIO_AUTH_TOKEN"]
)

def call_user(phone, url):
    return client.calls.create(
        to=phone,
        from_=os.environ["TWILIO_NUMBER"],
        url=url,
        send_digits="1"
    )
