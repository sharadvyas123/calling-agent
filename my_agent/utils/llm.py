import requests

OLLAMA_URL = "https://f8d73fea56bf.ngrok-free.app/api/generate"
MODEL = "mistral"

SYSTEM_PROMPT = """
You are a phone agent from XYZ Company.
Be polite, professional, and brief.
"""


def generate_agent_response(user_text : str)->str:
    prompt = f"""
{SYSTEM_PROMPT}

Customer said :
{user_text}

Respond as the XYZ componey's Agent .
"""
    
    response = requests.post(
        OLLAMA_URL,
        json={
            "model":MODEL,
            "prompt" : prompt,
            "stream" : False
        },
        headers={
            "Content-Type": "application/json",
            "ngrok-skip-browser-warning" : "true"
        },
        timeout=30
    )
    response.raise_for_status()

    return response.json()["response"].strip()


print(generate_agent_response("Hello my name is sam !!"))