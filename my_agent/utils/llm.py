import requests

OLLAMA_URL = "https://2b6ec36d8c58.ngrok-free.app/api/generate"
MODEL = "mistral"

SYSTEM_PROMPT = """
You are a phone agent from XYZ Company.
You speak to customers on live phone calls.
Be polite, professional, calm, and brief.
Do not repeat greetings unnecessarily.
"""


def build_prompt(messages: list[dict]) -> str:
    convo = ""

    for m in messages:
        if m["role"] == "user":
            convo += f"Customer: {m['content']}\n"
        elif m["role"] == "assistant":
            convo += f"Agent: {m['content']}\n"

    return f"""
{SYSTEM_PROMPT}

Conversation so far:
{convo}

Respond as XYZ Company phone agent.
Be concise. Do not repeat greetings.
"""


def generate_agent_response(messages: list[dict]) -> str:
    prompt = build_prompt(messages)

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        headers={
            "Content-Type": "application/json",
            "ngrok-skip-browser-warning": "true"
        },
        timeout=30
    )
    response.raise_for_status()

    return response.json()["response"].strip()
