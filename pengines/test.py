from urllib.request import Request, urlopen
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
print("Header information.")
print(header, type(header))

# Encode the body as json in utf8
data_ = {}
data = json.JSONEncoder().encode(data_)
data_utf8 = data.encode("utf-8")
print("Printing data information...")
print(data, type(data))

request_object = Request(url, data=data_utf8, headers=header)
response = urlopen(request_object)
response_string_utf8 = response.read()
print(response_string_utf8, type(response_string_utf8))
response_string = response_string_utf8.decode("utf-8")
print(response_string)
