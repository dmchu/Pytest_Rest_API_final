import requests

URL = "https://playground.learnqa.ru/api/long_redirect"

response = requests.get(URL)

all_urls = [response.history[i].url for i in range(len(response.history))]
last_redirected_url = all_urls[-1]
number_of_redirections = len(response.history)

print(all_urls)
print(last_redirected_url)
print(number_of_redirections)