# Vaani – AI Caller Agent ☎️🤖

Vaani is an AI-powered calling agent built to help businesses and teams **collect customer feedback automatically**.

It doesn’t just make calls — it listens, analyzes the conversation, generates a report, and then decides what to do next based on the sentiment (positive / negative / neutral).

This project is still evolving and very much **builder-first**, so expect honesty over perfection.

---

## What Vaani Does (in short)

- Makes AI-powered phone calls using Twilio  
- Talks to users and collects feedback  
- Analyzes the full conversation using an LLM  
- Generates a friendly report  
- Decides the next action (greet, end, or escalate)

---

## How the Automation Works (Flow)

1. Twilio makes the call and handles voice input/output  
2. Voice instructions are served from a hosted backend (`app.py`)  
3. User speech is sent to an exposed Ollama LLM (via ngrok)  
4. The conversation is analyzed and routed using LangGraph  
5. Final decision is taken based on sentiment

Because this setup uses **Render + Ngrok + Local Ollama**, there can be some delay — this is a known tradeoff to avoid high cloud costs.

---

## Setup Instructions (Step-by-Step)

### 1️⃣ Register on Twilio
- Create a Twilio account  
- Buy a **US phone number**
- Keep your Twilio credentials ready (SID, Auth Token)

---

### 2️⃣ Configure the Twilio Calling Number

Go to this file:
my-agent/utils/tools.py

Inside it, find the `call_user` function and update the `from_` argument with your **Twilio phone number**.

Example (conceptual):
```python
from_="+1XXXXXXXXXX"
```

### 3️⃣ Host the Backend

Go to the `server/` folder\
Host `app.py` on **any hosting service** (Render, Railway, VPS, etc.)
This server is responsible for returning TwiML (XML responses) to Twilio

### 4️⃣ Set Up Ollama (Local LLM)

If you want to use Ollama like I did:

1. Install Ollama

2. Pull any model you like
```
ollama pull mistral
```

3. Expose Ollama using ngrok:
```
ngrok http 11434
```

4. Copy the public ngrok URL

Now go to:
```
llm.py
```

Update this variable:
```python
OLLAMA_URI = "<NGROK_URL>/api/generate"
```

Once this is done, your local LLM is ready to receive requests.

---
### 5️⃣ Add the Phone Number to Call

Go to:
```
scripts/calling-user.py
```

Plug in the target phone number you want Vaani to call.

### 6️⃣ Run the Agent

From the project root, run:
```
python -m scripts.call_user
```

📞 The call will be initiated.

---
Known Issues (Current Limitations)

- Some awkward pauses between conversation
- No real-time interruption support yet
- Longer calls can feel a bit robotic
- Twilio trial warning plays at the start of the call
- Latency due to multi-hop flow (Twilio → Server → Ollama → Server → Twilio)

These are known and expected at this stage.

---
### Future Improvements

- Reduce latency
- Improve voice naturalness
- Add interrupt handling
- Better conversation pacing
- Move towards a more real-time architecture
---
### Final Notes

This project is **built while optimizing for learning and cost**, not perfection.
If you’re experimenting with Voice AI, LangGraph workflows, or local LLMs — this should give you a solid starting point.

Feel free to fork, break, improve, or build on top of it.

Happy hacking 🚀

---