import json.decoder
from requests import Response
from datetime import datetime as dt

class BaseCase:
    def get_cookie(self, response:Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies.get(cookie_name)

    def get_header(self, response:Response, headers_name):
        assert headers_name in response.headers, f"Cannon find header with the name {headers_name} in the last response"
        return response.headers.get(headers_name)

    def get_json_value(self, response:Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format, Response test is '{response.text}'"
        assert name in response_as_dict, f"Response JSON doesn't have key '{name}"
        return response_as_dict.get(name)

    def prepare_registration_data(self, email=None, missing_param=None, empty_param=None) -> dict:
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = dt.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"

        params = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        if missing_param is not None:
            if params.get(missing_param):
                params.pop(missing_param)
            else:
                raise Exception(f"Bad 'missing parameter' '{missing_param} was received'")

        elif empty_param is not None:
            if params.get(empty_param):
                params[empty_param] = ''
            else:
                raise Exception(f"Bad 'empty parameter' '{empty_param} was received'")
        return params
