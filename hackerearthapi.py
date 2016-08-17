import requests

RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
CLIENT_SECRET = '0a7f0101e5cc06e4417a3addeb76164680ac83a4'


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





'''
Name: nikhil-123
Hostname: http://whatsup.pythonanywhere.com/
Client Id: bcad7a43c0d562aeef8f85d688fec2718edf0622b90a.api.hackerearth.com
Client Secret Key: 0fe5b082e17d60fca14d55dc1f4a1922778c3d3c
'''
