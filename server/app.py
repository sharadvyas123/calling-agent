from flask import Flask, Response
from twilio.twiml.voice_response import VoiceResponse
from my_agent.utils.llm import generate_agent_response

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    # For now, simulated user input
    user_text = "I really like your product"

    ai_text = generate_agent_response(user_text)

    resp = VoiceResponse()
    resp.say(ai_text, voice="alice", language="en-IN")

    return Response(str(resp), mimetype="text/xml")


@app.route("/")
def home():
    return "Twilio Voice Webhook Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
