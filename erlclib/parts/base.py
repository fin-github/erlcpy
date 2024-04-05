from requests import request
from icecream import ic
from time import sleep as wait
import erlclib.ratelimit as ratelimit



def send_request(method: str,
                 part: str,
                 key: str,
                 ratelimit_key: str,
                 headers: dict = {},
                 json: dict = {},
                 payload: dict = {},
                 body: str = None):
    # default: https://api.policeroleplay.community/v1/server/{part}
    json = payload
    if ratelimit.check_rate_limit() and not ratelimit.outdated():
        print("ERROR: CAN NOT CONTINUE | Ratelimited")
        return
    
    headers["Server-Key"] = key
    if not ratelimit_key is None: headers["Authorization"] = ratelimit_key
    
    req = request(
        method=method,
        url=f"https://api.policeroleplay.community/v1/server/{part}",
        headers=headers,
        json=json,
        data=body
    )
    if req.status_code == 429:
        print("FATAL ERROR: EXPLICIT RATELIMIT")
        return
    ratelimit.update(headers=req.headers)
    return req

def send_command_request(command: str,
                         key: str,
                         ratelimit_key: str):
    
    if ratelimit.check_rate_limit() and not ratelimit.outdated():
        print("ERROR: CAN NOT CONTINUE | Ratelimited")
        return
    
    headers = {
        "Content-Type": "application/json"
    }
    command = "{\"command\":\""+command+"\"}"
    
    
    headers["Server-Key"] = key
    if not ratelimit_key is None: headers["Authorization"] = ratelimit_key
    
    req = request(
        method="POST",
        url=f"https://api.policeroleplay.community/v1/server/command",
        headers=headers,
        data=command
    )
    
    if req.status_code == 429:
        print("FATAL ERROR: EXPLICIT RATELIMIT")
    
    ratelimit.update(headers=req.headers)
    return req
