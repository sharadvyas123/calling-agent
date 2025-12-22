from my_agent.utils.tools import call_user
import time
import requests

def wait_for_conversation(call_sid , timeout= 300):
    start = time.time()

    while time.time() - start < timeout:
        res = requests.get(
            f"https://calling-agent-1gkd.onrender.com/conversations/{call_sid}"
        ).json()

        if res["messages"] :
            return res["messages"]
        time.sleep(3)

    raise TimeoutError("call did not Completer in Time")

call =call_user(
    phone="+917359861771",
    url="https://calling-agent-1gkd.onrender.com"
)

print("call SID : ", call.sid)

print(wait_for_conversation(call.sid))