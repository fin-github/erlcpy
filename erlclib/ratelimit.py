from json import load, dumps
from time import time
from icecream import ic
def get_json():
    return load(open("erlclib/ratelimits.json"))
def set_json(new: dict):
    open("ratelimits.json", 'w').write(dumps(new))

def check_rate_limit(): # returns True if ratelimited
    if int(get_json()["reset"]) <= int(time()):
        new = get_json()
        new["possibly_outdated"] = True
        set_json(new)
        del new
        return False
    
    ic(get_json())
    
    return get_json()["remaining"] == 0

def update(headers: dict):
    new = get_json()
    try:
        new["remaining"] = headers["X-RateLimit-Remaining"]
        new["reset"] = headers["X-RateLimit-Reset"]
        new["limit"] = headers["X-RateLimit-Limit"]
        new["remaining"], new["reset"], new["limit"] = int(new["remaining"]), int(new["reset"]), int(new["limit"])
        new["possibly_outdated"] = False
    except KeyError:
        new["possibly_outdated"] = True
    
    set_json(new=new)

def outdated():
    return get_json()["possibly_outdated"]