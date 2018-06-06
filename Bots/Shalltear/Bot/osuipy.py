import requests
import json

Base = "https://osu.ppy.sh/api/"
Key = None

class _Modes:
    def standard(self):
        return 0
    
    def taiko(self):
        return 1
    
    def ctb(self):
        return 2
    
    def mania(self):
        return 3

Modes = _Modes()
    
def Request(Req, Headers):
    response = requests.get(Base+Req, Headers)
    
    if response.status_code == 200:
        Data = json.loads(response.content.decode('utf-8'))
        
        return Data
    else:
        return None

def SetKey(key):
    Key = key

def get_user(Name, Mode = 0):
    Headers = {"k": Key,
               "u": Name,
               "m": Mode}
    
    Resp = Request("get_user", Headers)
    return Resp # None if got no data

def get_user_best(Name, Mode = 0, Limit = 5):
    Headers = {"k": Key,
               "u": Name,
               "m": Mode,
               "limit": 5}
    
    Resp = Request("get_user_best", Headers)
    return Resp # None if got no data
