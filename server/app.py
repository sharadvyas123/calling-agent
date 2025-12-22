from flask import Flask, request, Response, session
from twilio.twiml.voice_response import VoiceResponse, Gather
from my_agent.utils.llm import generate_agent_response

app = Flask(__name__)
app.secret_key = "super-secret-key"  # required for session


@app.route("/incoming-call", methods=["POST"])
def incoming_call():
    resp = VoiceResponse()

    # Initialize memory if not present
    if "messages" not in session:
        session["messages"] = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant talking on a phone call."
            },
            {
                "role": "assistant",
                "content": "Hello! How can I help you today?"
            }
        ]
        resp.say("Hello! How can I help you today?", voice="alice", language="en-IN")

    gather = Gather(
        input="speech",
        speech_timeout="auto",
        enhanced=True,
        action="/respond",
        method="POST"
    )

    gather.say("I am listening.", voice="alice", language="en-IN")
    resp.append(gather)

    return Response(str(resp), mimetype="text/xml")


@app.route("/respond", methods=["POST"])
def respond():
    user_text = request.form.get("SpeechResult")

    if not user_text:
        resp = VoiceResponse()
        resp.say("Sorry, I didn't catch that. Please repeat.", voice="alice")
        resp.redirect("/incoming-call", method="POST")
        return Response(str(resp), mimetype="text/xml")

    # Load memory
    messages = session.get("messages", [])

    # Append user message
    messages.append({
        "role": "user",
        "content": user_text
    })

    # Call Ollama / local LLM
    ai_text = generate_agent_response(messages)

    # Append assistant response
    messages.append({
        "role": "assistant",
        "content": ai_text
    })

    # Save back to session
    session["messages"] = messages

    resp = VoiceResponse()
    resp.say(ai_text, voice="alice", language="en-IN")

    # Loop back for next turn
    resp.redirect("/incoming-call", method="POST")

    return Response(str(resp), mimetype="text/xml")


@app.route("/")
def home():
    return "Twilio Voice AI is running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
