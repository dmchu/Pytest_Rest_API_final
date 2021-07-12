import requests

def test_header_from_homework():
    URL = "https://playground.learnqa.ru/api/homework_header"
    response = requests.get(URL)
    all_headers = response.headers
    assert all_headers.get("x-secret-homework-header") == "Some secret value", f"The value of 'x-secret-homework-header' header value is not as expected." \
                                                      f" It's value is: {all_headers.get('HomeWork')}"