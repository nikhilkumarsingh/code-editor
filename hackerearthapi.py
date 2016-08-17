import requests

RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
CLIENT_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'


def run_code(lang,code,inputs):
    source = code
    data = {
        'input':inputs,
        'client_secret': CLIENT_SECRET,
        'async': 0,
        'source': source,
        'lang': lang,
        'time_limit': 5,
        'memory_limit': 262144,
        }
    r = requests.post(RUN_URL, data=data)
    return r.json()






