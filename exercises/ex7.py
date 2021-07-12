import requests

URL = "https://playground.learnqa.ru/ajax/api/compare_query_type"

payload_get = {"method": "GET"}
payload_post = {"method": "POST"}
payload_put = {"method": "PUT"}
payload_delete = {"method": "DELETE"}
payload_head = {"method": "HEAD"}

response1 = requests.get(URL, params=payload_get)
response2 = requests.post(URL, data=payload_post)
response3 = requests.put(URL, data=payload_put)
response4 = requests.delete(URL, data=payload_delete)
response5 = requests.delete(URL, data=payload_head)

print(response1.status_code)
print(response1.text)
print(response2.status_code)
print(response2.text)
print(response3.status_code)
print(response3.text)
print(response4.status_code)
print(response4.text)
print(response5.status_code)
print(response5.text)
#4

all_methods_params = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
all_methods = ['requests.get(URL, params = payload)', 'requests.post(URL, data=payload)',
               'requests.put(URL, data=payload)', 'requests.delete(URL, data=payload)',
               'requests.head(URL, data=payload)', 'requests.options(URL, data=payload)',
               'requests.patch(URL, data=payload)']

for method in all_methods:
    for method_param in all_methods_params:
        payload = {"method": f"{method_param}"}
        if method == "get":
            response = eval(method)
        else:
            response = eval(method)
        print(f"method:{method}, method_param: {method_param}, {response.text}")
