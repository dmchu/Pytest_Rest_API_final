import requests

def test_cookie_from_homework():
    URL = "https://playground.learnqa.ru/api/homework_cookie"
    response = requests.get(URL)
    all_cookies = response.cookies
    assert all_cookies.get("HomeWork") == "hw_value", f"The value of 'Homework' cookie is not as expected." \
                                                      f" It's value is: {all_cookies.get('HomeWork')}"