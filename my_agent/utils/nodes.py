def call_node(state):
    return {**state, "transcript": "User responded positively"}

def generate_report_node(state):
    return {**state, "report": f"Feedback: {state['transcript']}"}

def evaluate_node(state):
    text = state["transcript"].lower()
    if "bad" in text or "issue" in text:
        return {**state, "sentiment": "bad"}
    return {**state, "sentiment": "good"}

def greet_user_node(state):
    return state

def report_manager_node(state):
    return state
