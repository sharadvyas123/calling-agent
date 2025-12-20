from typing import TypedDict, Literal

class CallState(TypedDict):
    phone: str
    transcript: str
    sentiment: Literal["good", "bad", "normal"]
    report: str
