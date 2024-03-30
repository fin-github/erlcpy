from requests import post, get, request

def send_request(method: str,
                 part: str,
                 key: str,
                 headers: dict = {},
                 payload: dict = {}):
    # default: https://api.policeroleplay.community/v1/server/{part}
    headers["Server-Key"] = key
    return request(
        method=method,
        url=f"https://api.policeroleplay.community/v1/server/{part}",
        headers=headers,
        json=payload
    )
