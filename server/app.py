from flask import Flask, Response
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/voice", methods=["POST", "GET"])
def voice():
    resp = VoiceResponse()
    resp.say(
        "Hello I am from XYZ company. This call is successful.",
        voice="alice"
    )
    return Response(str(resp), mimetype="text/xml")

@app.route("/")
def home():
    return "Twilio Voice Webhook Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
