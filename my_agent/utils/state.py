from typing import TypedDict, Literal

class CallState(TypedDict):
    phone: str
    Conversation: list[dict]
    report: str
    sentiment : Literal["positive" , "neutral" , "negative"]
    engagement : Literal["high" , "medium" , "low"]
    needs_escalation : bool
    reasoning : str

    final_action : str
    note : str