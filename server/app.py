from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from my_agent.utils.llm import generate_agent_response

app = Flask(__name__)


CALL_MEMORY = {}
COMPLETED_CALLS= {}


@app.route("/incoming-call", methods=["POST"])
def incoming_call():
    resp = VoiceResponse()

    call_sid = request.form.get("CallSid")
    # # Initialize memory if not present
    if call_sid not in CALL_MEMORY:
        CALL_MEMORY[call_sid] = [
            {
                "role" : "assistant",
                "content" :"Hello! How can I help you today?"
            }
        ]
        resp.say("Hello! How can I help you today?", voice="alice", language="en-IN")


    # if "messages" not in session:
    #     session["messages"] = [
    #         {
    #             "role": "system",
    #             "content": "You are a helpful AI assistant talking on a phone call."
    #         },
    #         {
    #             "role": "assistant",
    #             "content": "Hello! How can I help you today?"
    #         }
    #     ] not using the session cause we need the convo for the summary 

    gather = Gather(
        input="speech",
        speech_timeout=0.8,
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
    call_sid = request.form.get("CallSid")
    if not user_text:
        resp = VoiceResponse()
        resp.say("Sorry, I didn't catch that. Please repeat.", voice="alice")
        resp.redirect("/incoming-call", method="POST")
        return Response(str(resp), mimetype="text/xml")

    # Load memory
    messages = CALL_MEMORY.get(call_sid, [])

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
    CALL_MEMORY[call_sid] = messages

    resp = VoiceResponse()
    resp.say(ai_text, voice="alice", language="en-IN")

    # Loop back for next turn
    resp.redirect("/incoming-call", method="POST")

    return Response(str(resp), mimetype="text/xml")


@app.route("/call-ended", methods=["POST"])
def call_ended():
    call_sid = request.form.get("CallSid")
    call_status = request.form.get("CallStatus")

    if call_status != "completed":
        return "", 200

    messages = CALL_MEMORY.pop(call_sid, [])


    print("CALL ENDED:", call_sid)
    print("CONVERSATION:")
    for m in messages:
        print(f"{m['role'].upper()}: {m['content']}")

    # Optionally store it in another in-memory dict
    COMPLETED_CALLS[call_sid] = messages

    return "", 200


@app.route("/conversations/<call_sid>")
def get_conversation(call_sid):
    return {
        "call_sid": call_sid,
        "messages": COMPLETED_CALLS.get(call_sid, [])
    }


@app.route("/")
def home():
    return "Twilio Voice AI is running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
