import requests
import json


def Turning(message, userid):
    url = "http://www.tuling123.com/openapi/api"
    #print(message, " ", userid)
    payload = {"key": "c8500f7e1a344755b0eefcbddc21f770", "info": message, "userid": userid}
    r = requests.post(url, data=payload)
    re = json.loads(r.text)
    # print(re)
    furl = re.get("url")
    if furl is not None:
        pic = download(furl)
        return re['text'] + furl
    return re['text']


def download(furl):
    r = requests.get(furl)
    # print(r.text)
