from my_agent.utils.tools import call_user
import time
import requests

import time
import requests

def wait_for_conversation(call_sid, timeout=300):
    start = time.time()
    url = f"https://calling-agent-1gkd.onrender.com/conversations/{call_sid}"

    while time.time() - start < timeout:
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


call =call_user(
    phone="+917874262883",
    url="https://calling-agent-1gkd.onrender.com"
)

print("call SID : ", call.sid)

time.sleep(10)
print(wait_for_conversation(call.sid))