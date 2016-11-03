from urllib.request import Request, urlopen
import json

# Make the URL
urlbase = "http://localhost:4243"
url_action = "/pengine/create"
url = urlbase + url_action

# Header is dict not JSON for urllib
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

# Request using urllib due to request libs broken implementation.
request_object = Request(url, data=data_utf8, headers=header)
response = urlopen(request_object)
response_string_utf8 = response.read()
response_string = response_string_utf8.decode("utf-8")

# Super fragile parsing!! Only handles one digit pengine slave counts.
print(len(response_string))
assert len(response_string) == 68
print(response_string[8:47], response_string[62])
pengine_id = response_string[8:47]
pengine_slave_count = response_string[62]

# Start the query cycle.
print("Starting query")
# Initial creation is done -- pengine id aquired and slave counts named.
url_ask = urlbase + "/pengine/send?format=json&id={}".format(pengine_id) # Error: Raises error
print("URL: ", url_ask)
# Header has a different Content-type
header["Content-type"] = "application/x-prolog; charset=UTF-8"
print("Header: ", header)

# Create the body.
body_ask = "ask({}, []).".format("member(X, [1,2,3])") # po.getrequestbodyask
print("Body: ", body_ask)
body_utf8 = body_ask.encode("utf-8")
query_request = Request(url_ask, data=body_utf8, headers = header)
query_response = urlopen(query_request)
query_response_utf8 = query_response.readall()
query_response_string = query_response_utf8.decode("utf-8")
print("Response received: ", query_response_string)
query_response_dict = json.JSONDecoder().decode(query_response_string)
print("Decoded JSON: ", query_response_dict)
