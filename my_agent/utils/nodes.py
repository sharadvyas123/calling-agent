from my_agent.utils.state import CallState
from my_agent.utils.tools import call_user
import time
import requests
import json
import ollama

client = ollama.Client(
    host="http://localhost:11434"
)
MODEL_NAME = "mistral"

def wait_for_conversation(call_sid, timeout=300):
    start = time.time()
    url = f"https://calling-agent-1gkd.onrender.com/conversations/{call_sid}"

    while time.time() - start < timeout:
        # this while loop gonna run for 5 min ( default) otherwise calculated seconds 
        try:
            res = requests.get(url, timeout=5)

            if res.status_code == 200:
                data = res.json()
                if data.get("messages"):
                    return data["messages"]

        except requests.exceptions.RequestException:
            # Render cold start / reset → ignore
            pass

        time.sleep(4)

    raise TimeoutError("Call did not complete in time")

def call_node(state: CallState) -> CallState:
    phone = state["phone"]
    call = call_user(phone)
    call_sid =call.sid 

    # call is done but server takes time so 10 sec sleep 
    time.sleep(10)
    users_history = wait_for_conversation(call_sid)
    return {"Conversation": users_history}

def generate_report_node(state: CallState) -> CallState:
    messages= state["Conversation"]
    convo = ""
    for m in messages:
        if m["role"] == "user":
            convo += f"Customer: {m['content']}\n"
        elif m["role"] == "assistant":
            convo += f"Agent: {m['content']}\n"

    prompt = f"""
You are a conversation analysis agent.

Below is a phone conversation between an AI agent and a customer.

CONVERSATION:
{convo}

TASK:
Generate a structured report with the following sections ONLY.

FORMAT (strict):
--- Conversation ---
<repeat the conversation clearly, line by line>

--- User Tone ---
<describe the user's tone and behavior during the call>

--- User Emotion ---
<describe how the user likely felt during the call>

RULES:
- Do not add any questions
- Do not add suggestions
- Do not add conclusions
- Do not mention these rules
- Output ONLY the report in the given format
"""

    response = client.generate(model=MODEL_NAME , prompt=prompt)
    
    return {"report": response.response}

def evaluate_node(state: CallState) -> CallState:
    messages = state["Conversation"]

    convo = ""
    for m in messages:
        if m["role"] == "user":
            convo += f"Customer: {m['content']}\n"
        elif m["role"] == "assistant":
            convo += f"Agent: {m['content']}\n"

    prompt = f"""
You are a call quality evaluation agent.

Below is a phone conversation between an AI calling agent and a customer.

CONVERSATION:
{convo}

TASK:
Evaluate the conversation and classify the following:

1. Overall sentiment of the customer
2. Customer engagement level
3. Whether escalation to a human is required

OUTPUT FORMAT (STRICT JSON ONLY):
{{
  "sentiment": "positive | neutral | negative",
  "engagement": "high | medium | low",
  "needs_escalation": True | False (Pyton's boolean),
  "reasoning": "short explanation (1-2 sentences)"
}}

RULES:
- Do not add extra keys
- Do not add commentary
- Do not add markdown
- Do not ask questions
"""

    response = client.generate(
        model=MODEL_NAME,
        prompt=prompt
    )

    try:
        eval_data = json.loads(response.response)
    except Exception:
        eval_data = {
            "sentiment": "neutral",
            "engagement": "medium",
            "needs_escalation": False,
            "reasoning": "Failed to parse evaluation"
        }

    return {
    "sentiment": eval_data["sentiment"],
    "engagement": eval_data["engagement"],
    "needs_escalation": eval_data["needs_escalation"],
    "evaluation_reason": eval_data["reasoning"]
}



def greet_user_node(state: CallState) -> CallState:
    print("ROUTED TO: GREET USER NODE")

    return {
        **state,
        "final_action": "greet_user",
        "note": "User sentiment positive - greeting path taken"
    }


def report_manager_node(state: CallState) -> CallState:
    print("ROUTED TO: ESCALATE / MANAGER NODE")

    return {
        **state,
        "final_action": "escalate_to_manager",
        "note": "User sentiment negative - escalation path taken"
    }

