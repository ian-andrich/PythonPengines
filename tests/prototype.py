from urllib.request import Request, urlopen
import json

# Make the URL
urlbase = "http://localhost:4242"
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
response_string_utf8 = response.readall()
response_string = response_string_utf8.decode("utf-8")


def parse_create(response_string):
    pengine_id_char_list = []
    pengine_slave_limit_char_list = []
    state = 0
    print(response_string)
    for char in response_string:
        if state == 0 and char.isnumeric():
            print("Found first number")
            state = 1

        if state == 1 and char.isnumeric():
            pengine_id_char_list.append(char)
        elif state == 1:
            state = 2

        if state == 2 and char.isnumeric():
            pengine_slave_limit_char_list.append(char)

    pengine_id = "".join(pengine_id_char_list)
    pengine_slave_limit = "".join(pengine_slave_limit_char_list)
    print("Parse Results: Id: {}, Limit: {}".format(pengine_id, pengine_slave_limit))
    return pengine_id, pengine_slave_limit


# ToDo: Super fragile parsing!! Only handles one digit pengine slave counts.
# print(len(response_string))
# assert len(response_string) == 68
# print(response_string[8:47], response_string[62])
# pengine_id = response_string[8:47]
# pengine_slave_count = response_string[62]
pengine_id, pengine_slave_count = parse_create(response_string)


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
query_request = Request(url_ask, data=body_utf8, headers=header)
query_response = urlopen(query_request)
query_response_utf8 = query_response.readall()
query_response_string = query_response_utf8.decode("utf-8")
print("Response received: ", query_response_string)
query_response_dict = json.JSONDecoder().decode(query_response_string)
print("Decoded JSON: ", query_response_dict)
print("Data from JSON: ", query_response_dict['data'])

# More calls.
def get_more(urlbase, pengine_id, header):
    ''' This function gets more responses, if they exist.'''
    # Make URL
    print("Getting more...")
    url_next = urlbase + "/pengine/send?format=json&id={}".format(pengine_id)
    print("Next URL: ", url_next)
    # Pass headers as normal.
    # Make body.
    body = "next."
    print("Next body: ", body)
    body_utf8 = body.encode("utf-8")
    print("Headers: ", header)
    next_request = Request(url_next, data=body_utf8, headers=header)
    next_response = urlopen(next_request)
    next_response_utf8 = next_response.readall()
    next_response_string = next_response_utf8.decode("utf-8")
    next_response_dict = json.JSONDecoder().decode(next_response_string)
    return next_response_dict

print(get_more(urlbase, pengine_id, header))
print(get_more(urlbase, pengine_id, header))
