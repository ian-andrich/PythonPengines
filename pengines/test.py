from urllib.request import Request
import json

# Make the URL
urlbase = "http://localhost:4243"
url_action = "/pengine/create"
url = urlbase + url_action

header = dict()
header["User-Agent"] = "PythonPengine"
header["Accept"] = "application/json"
header["Accept-Language"] = "en-us,en;q=0.5"
header["Content-type"] = "application/json"

# Encode the body as json in utf8
data_ = {}
data = json.JSONEncoder(data_)
data = data.encode("utf-8")

response = Request(url, data=data, headers=header)
