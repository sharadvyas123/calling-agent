from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()
client = Client()

def call_user(phone, url):
    return client.calls.create(
        to=phone,
        from_="+18155766809",
        url=f"{url}/incoming-call",
        status_callback=f"{url}/call-ended",
        status_callback_event=["completed"],
        send_digits="1"
    )
